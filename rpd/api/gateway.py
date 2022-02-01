# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
"""Implementation of the Discord Gateway."""

from __future__ import annotations

import asyncio
import json
import logging
import platform
import zlib
from random import random
from time import time
from typing import List

import aiohttp

from rpd.events import OnMessage, OnMessageDelete, OnMessageEdit
from rpd.internal.dispatcher import Dispatcher

from ..state import ConnectionState
from .rest_factory import RESTFactory

ZLIB_SUFFIX = b"\x00\x00\xff\xff"
_log = logging.getLogger(__name__)
url = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"


class Shard:
    """Represents a Discord Shard.

    Attributes
    ----------
    buffer
        An array of bytes which buffers the connection.
    dis
        The dispatcher
    """

    def __init__(
        self,
        state: ConnectionState,
        dispatcher: Dispatcher,
        shard_id: int,
        mobile: bool = False,
    ):
        self.remaining = 110
        self.per = 60.0
        self.window = 0.0
        self.max = 110
        self.state = state
        self.mobile = mobile
        self.dis = dispatcher
        self.inflator = zlib.decompressobj()
        self.shard_id = shard_id
        self.buffer = bytearray()
        self._session_id = None
        self._ratelimit_lock: asyncio.Lock = asyncio.Lock()

    async def connect(self, token):
        self._session = aiohttp.ClientSession()
        self.ws = await self._session.ws_connect(url)
        self.token = token
        if self._session_id is None:
            await self.identify()
            self.state.loop.create_task(self.recv())
        else:
            await self.resume()
            _log.debug("Reconnected to the Gateway")

    @property
    def is_ratelimited(self):
        now = time()
        if now > self.window + self.per:
            return False
        return self.remaining == 0

    def delay(self):
        now = time()

        if now > self.window + self.per:
            self.remaining = self.max

        if self.remaining == self.max:
            self.window = now

        if self.remaining == 0:
            return self.per - (now - self.window)

        self.remaining -= 1
        if self.remaining == 0:
            self.window = now

        return 0.0

    async def block(self):
        async with self._ratelimit_lock:
            delay = self.delay()
            if delay:
                _log.warning(
                    "Shard %s was ratelimited, waiting %.2f seconds.",
                    self.shard_id,
                    delay,
                )
                await asyncio.sleep(delay)

    async def send(self, data: dict):
        _log.debug("< %s", data)
        payload = json.dumps(data)

        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        await self.ws.send_bytes(payload)

    async def recv(self):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                self.buffer.extend(msg.data)
                raw = self.inflator.decompress(self.buffer).decode("utf-8")
                if len(msg.data) < 4 or msg.data[-4:] != ZLIB_SUFFIX:
                    raise
                self.buffer = bytearray()  # clean buffer
                data = json.loads(raw)
                _log.debug("> %s", data)

                self._seq = data["s"]
                self.dis.dispatch("RAW_SOCKET_RECEIVE")

                if data["op"] == 0:
                    if (
                        data["t"] == "READY"
                    ):  # only fire up getting the session_id on a ready event.
                        await self._ready(data)
                        self.dis.dispatch("READY")
                    elif data["t"] == "GUILD_CREATE":
                        self.state._guilds_cache[data["d"]["id"]] = data["d"]
                        self.dis.dispatch("RAW_GUILD_CREATE", data["d"])
                    elif data["t"] == "MESSAGE_CREATE":
                        self.dis.dispatch("RAW_MESSAGE", data["d"])
                        OnMessage(data["d"], self.dis, self.state)
                    elif data["t"] == "MESSAGE_DELETE":
                        self.dis.dispatch("RAW_MESSAGE_DELETE", data["d"])
                        OnMessageDelete(data["d"], self.dis, self.state)
                    elif data["t"] == "MESSAGE_UPDATE":
                        self.dis.dispatch("RAW_MESSAGE_EDIT", data["d"])
                        OnMessageEdit(data["d"], self.dis, self.state)
                    else:
                        self.dis.dispatch("RAW_{}".format(data["t"]), data["d"])
                elif data["op"] == 9:
                    await self.ws.close(code=1008)
                    await self.resume()
                elif data["op"] == 10:
                    await self.hello(data)
                elif data["op"] == 11:
                    _log.debug("> %s", data)
                else:
                    self.dis.dispatch(data["op"], data)

            else:
                raise RuntimeError

        code = self.ws.close_code
        if code is None:
            return
        else:
            await self.closed(code)

    async def closed(self, code):
        if code == 4000:
            pass

        elif code == 4001:
            pass

        elif code == 4002:
            # just ignore it.
            pass

        elif code == 4003:
            # something weird happened, just ignore it.
            pass

        elif code == 4004:
            raise

        elif code == 4005:
            # pass!
            pass

        elif code == 4007:
            # pass and make a new session
            pass

        elif code == 4008:
            # retry!
            pass

        elif code == 4009:
            # try to resume.
            await self.resume()

        elif code == 4010:
            raise  # this doesn't really happen, unless you are dumb

        elif code == 4011:
            # just tell the owner to shard!
            raise

        elif code == 4012:
            # most likely a old lib version.
            raise

        elif code == 4013:
            raise

        elif code == 4014:
            raise

        await self.connect(token=self.token)

    async def heartbeat(self, interval: float):
        if self.is_ratelimited:
            await self.block()
        await self.send({"op": 1, "d": self._seq})
        await asyncio.sleep(interval)
        self.state.loop.create_task(self.heartbeat(interval))

    async def close(self, code: int = 1000):
        if self.ws:
            await self.ws.close(code=code)
        self.buffer.clear()

    async def hello(self, data):
        interval = data["d"]["heartbeat_interval"] / 1000
        init = interval * random()
        await asyncio.sleep(init)
        self.state.loop.create_task(self.heartbeat(interval))

    async def _ready(self, data):
        self._session_id = data["d"]["session_id"]
        self.state._ready.set()

    async def identify(self) -> None:
        await self.send(
            {
                "op": 2,
                "d": {
                    "token": self.token,
                    "intents": self.state._bot_intents,
                    "properties": {
                        "$os": platform.system(),
                        "$browser": "RPD" if self.mobile is False else "Discord iOS",
                        "$device": "RPD",
                    },
                    "shard": (self.shard_id, self.state.shard_count),
                },
            }
        )

    async def resume(self) -> None:
        await self.send(
            {
                "op": 6,
                "d": {
                    "token": self.token,
                    "session_id": self._session_id,
                    "seq": self._seq,
                },
            }
        )


class Gateway:
    def __init__(
        self,
        state: ConnectionState,
        dispatcher,
        factory: RESTFactory,
        mobile: bool = False,
    ):
        self._s = state
        self.mobile = mobile
        self.count = self._s.shard_count
        self._d = dispatcher
        self._f = factory
        self.shards: List[Shard] = []

    async def connect(self, token):
        r = await self._f.get_gateway_bot()
        if self.count is None:
            shds = int(r["shards"])
            self._s.shard_count = shds
        else:
            shds = self.count

        for shard in range(shds):
            self.s = Shard(self._s, self._d, shard, mobile=self.mobile)
            self._s.loop.create_task(self.s.connect(token))
            self.shards.append(self.s)

    def send(self, payload):
        return self.s.send(payload)

    def gain_voice_access(self, guild, channel, mute: bool, deaf: bool):
        json = {
            "op": 4,
            "d": {
                "guild_id": guild,
                "channel_id": channel,
                "self_mute": mute,
                "self_deaf": deaf,
            },
        }
        return self.s.send(json)

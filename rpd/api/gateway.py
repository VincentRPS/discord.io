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

import aiohttp

from rpd.internal.dispatcher import Dispatcher

from ..state import ConnectionState

ZLIB_SUFFIX = b"\x00\x00\xff\xff"
inflator = zlib.decompressobj()
_log = logging.getLogger(__name__)
url = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"


class Gateway:
    """Represents a Gateway connection with Discord."""

    def __init__(self, state: ConnectionState):
        self.state = state
        self.dis = Dispatcher(self.state)
        self.buffer = bytearray()

    async def connect(self):
        self._session = aiohttp.ClientSession()
        self.ws = await self._session.ws_connect(url)
        if self.state._session_id is None:
            await self.identify()
            self.state.loop.create_task(self.recv())
            self.state._ready.set()
        else:
            await self.resume()
            _log.debug("Reconnected to the Gateway")

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
                raw = inflator.decompress(self.buffer).decode("utf-8")
                if len(msg.data) < 4 or msg.data[-4:] != ZLIB_SUFFIX:
                    raise
                self.buffer = bytearray()  # clean buffer
                data = json.loads(raw)
                _log.debug("> %s", data)

                if data["s"] is not None:
                    self._seq = data["s"]

                if data["op"] == 0:
                    self.dis.dispatch(data["t"], data["d"])
                    if (
                        data["t"] == "READY"
                    ):  # only fire up getting the session_id on a ready event.
                        await self._ready(data)
                    elif data["t"] == "GUILD_CREATE":
                        self.state._guilds_cache[data["d"]["id"]] = data["d"]
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
                raise

        code = self.ws.close_code
        if code is None:
            return
        else:
            await self.closed(code)

    async def closed(self, code):
        if code == 4000:
            pass

        elif code == 4001:
            raise

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

        await self.connect()

    async def heartbeat(self, interval: float):
        if self._seq is None:
            await self.close(1008)
            await self.connect()
            return
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
        self.state._session_id = data["d"]["session_id"]

    async def identify(self) -> None:
        await self.send(
            {
                "op": 2,
                "d": {
                    "token": self.state._bot_token,
                    "intents": self.state._bot_intents,
                    "properties": {
                        "$os": platform.system(),
                        "$browser": "RPD",
                        "$device": "RPD",
                    },
                },
            }
        )

    async def resume(self) -> None:
        await self.send(
            {
                "op": 6,
                "d": {
                    "token": self.state._bot_token,
                    "session_id": self.state._session_id,
                    "seq": self._seq,
                },
            }
        )

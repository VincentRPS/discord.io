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

# Implementation of the everyday Discord Shard.

import asyncio
import json
import platform
import random
import typing
import zlib

import aiohttp

from rpd.api import rest_factory as RF
from rpd.api.rest import _log
from rpd.intents import Intents

__all__: typing.List[str] = [
    "ShardGateway",
]

ZLIB_SUFFIX = b"\x00\x00\xff\xff"


class ShardGateway:
    """The Gateway connection with Discord.

    .. versionadded:: 0.3.0
    """

    def __init__(
        self,
        shards: int,
        shard_id: int,
        token: str,
        intents: typing.Optional[Intents] = None,
    ):
        self.token = token
        self.intents = intents
        self.shards = shards
        self.shard_id = shard_id
        self._zlib = zlib.decompressobj()
        self._buffer = bytearray()
        self.socket = aiohttp.ClientSession()
        self.rest = RF.RESTFactory()
        self.url = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"  # the gateway url
        self.sesh: int = None
        self.seq: int = None
        self.loop: asyncio.AbstractEventLoop = asyncio.get_running_loop()
        self.helloed = False

    async def connect(self):
        if self.sesh is None:
            await self.identify()
            self.loop.create_task(self.recieve())

    async def send(self, data: typing.Dict):
        if self.sesh is None:
            ...
        else:
            self.r = await self.socket.ws_connect(self.url)
            await self.r.send_str(json.dumps(data))
            _log.debug("< %s", data)

    async def recieve(self):
        async for msg in self.r:
            if msg.type == aiohttp.WSMsgType.BINARY:
                raw_data = self._decom(msg.data)
                data = json.loads(raw_data.decode("utf-8"))
                if self.helloed is False:
                    await self.hello(data)
                    self.helloed = True
                _log.debug("> %", data)

                if data["op"] == 0:
                    t = data["t"]
                    d = data["d"]
                    return t, d
            else:
                _log.error("Invalid data type was recieved: %s", msg.type)
            cc = self.r.close_code
            if cc is None:
                return

    async def heartbeat(self, interval: float):
        await self.send({"op": 1, "d": self.seq})
        _log.debug("Sent out heartbeat")
        await asyncio.sleep(interval)

    def _decom(self, data) -> bytes:
        self._buffer.extend(data)

        if len(data) < 4 or data[-4:] != ZLIB_SUFFIX:
            _log.error("Partial data was given.")
            pass
        try:
            decompressed = self._zlib.decompress(self._buffer)
        except:
            self._buffer = bytearray()
            _log.error("Data exception occured")
        self._buffer = bytearray()
        return decompressed

    async def hello(self, d: dict):
        """Handles Opcode 10, "Hello" """
        interval = d["d"]["heartbeat_interval"] / 1000
        intitial = interval * random.random()
        await asyncio.sleep(intitial)
        self.loop.create_task(self.heartbeat(interval))

    async def change_seq(self, _: int, d: dict):
        if (seq := d["s"]) is not None:
            _log.debug("Sequence number was updated to %s", seq)
            self.seq = seq

    async def ready(self, d: dict):
        self.sesh = d["session_id"]
        _log.debug("Session ID set to %s", self.sesh)

    async def identify(self):
        """Identifys to the Discord WebSocket"""
        payload = {
            "op": 2,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": platform.system(),
                    "$browser": "RPD",
                    "$device": "RPD",
                },
                "shard": (self.shard_id, self.shards),
            },
        }
        return self.send(payload)

    async def resume(self):
        """Handling of Opcode 6"""
        payload = {
            "op": 6,
            "d": {
                "token": self.token,
                "session_id": self.sesh,
                "seq": self.seq,
            },
        }
        return self.send(payload)

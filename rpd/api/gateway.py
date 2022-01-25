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
buffer = bytearray()
inflator = zlib.decompressobj()
_log = logging.getLogger(__name__)
url = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"


class Gateway:
    """Represents a Gateway connection with Discord."""

    def __init__(self, state: ConnectionState):
        self.state = state
        self.dis = Dispatcher()

    async def connect(self):
        self._session = aiohttp.ClientSession()
        self.ws = await self._session.ws_connect(url)
        await self.identify()
        self.state.loop.create_task(self.recv())
        self.state._ready.set()

    async def send(self, data: dict):
        _log.debug("< %s", data)
        payload = json.dumps(data)

        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        await self.ws.send_bytes(payload)

    async def recv(self):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                buffer.extend(msg.data)
                raw = inflator.decompress(buffer).decode("utf-8")
                data = json.loads(raw)
                if self.state._said_hello is False:
                    self.state._said_hello = True
                    await self.hello(data)
                    await self._ready(data)
                if self.state._seq != data["s"]:
                    self.state._seq = data["s"]
                _log.debug("> %s", data)
                self.dis.dispatch(data["op"], data)

                if data["op"] == 0:
                    self.dis.dispatch(data["op"], data["d"])
            else:
                raise

    async def heartbeat(self, interval: float):
        await self.send({"op": 1, "d": self.seq})
        await asyncio.sleep(interval)

    async def hello(self, data):
        interval = data["d"]["heartbeat_interval"] / 1000
        init = interval * random()
        await asyncio.sleep(init)
        self.state.loop.create_task(self.heartbeat(interval))

    async def _ready(self, data):
        self.state._session_id = data["session_id"]

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
                    "seq": self.state._seq,
                },
            }
        )

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
"""The V4 Voice Gateway Impl"""

import asyncio
import json
import logging
import zlib
from random import random

import aiohttp

from rpd.api.gateway import ZLIB_SUFFIX, Gateway
from rpd.internal.dispatcher import Dispatcher
from rpd.state import ConnectionState

_log = logging.getLogger(__name__)
url = "wss://gateway.discord.gg/?v=4&encoding=json&compress=zlib-stream"


class VoiceGateway:
    def __init__(
        self,
        state: ConnectionState,
        dispatcher: Dispatcher,
        session_id: int,
        gateway: Gateway,
        self_mute: bool = False,
        self_deaf: bool = False,
    ):
        self.dispatcher = dispatcher
        self.gateway = gateway
        self.state = state
        self.mute = self_mute
        self.deaf = self_deaf
        self.session_id = session_id
        self.buffer = bytearray()
        self.inflator = zlib.decompressobj()

    async def connect(self, guild, channel):
        self._session = aiohttp.ClientSession()
        r = await self.gateway.gain_voice_access(guild, channel, self.mute, self.deaf)
        self.ws = await self._session.ws_connect(url)
        if self.session_id is None:
            await self.identify()
            self.state.loop.create_task(self.recv())
        else:
            await self.resume()
            _log.debug("Reconnected to the Gateway")

    async def heartbeat(self, interval: float):
        await self.send({"op": 1, "d": self._seq})
        await asyncio.sleep(interval)
        self.state.loop.create_task(self.heartbeat(interval))

    async def hello(self, data):
        interval = data["d"]["heartbeat_interval"] / 1000
        init = interval * random()
        await asyncio.sleep(init)
        self.state.loop.create_task(self.heartbeat(interval))

    async def recv(self):
        for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                self.buffer.extend(msg.data)
                raw = self.inflator.decompress(self.buffer).decode("utf-8")
                if len(msg.data) < 4 or msg.data[-4:] != ZLIB_SUFFIX:
                    raise RuntimeError("Partial data given.")
                self.buffer = bytearray()  # clean buffer
                data = json.loads(raw)
                _log.debug("> %s", data)

                if data["op"] == 2:
                    self.dispatcher.dispatch("VOICE_READY", data["d"])
                elif data["op"] == 4:
                    self.dispatcher.dispatch("SESSION_DESCRIPTION_UPDATE", data["d"])
                elif data["op"] == 5:
                    self.dispatcher.dispatch("USER_SPEAKING_UPDATE", data["d"])
                elif data["op"] == 8:
                    await self.hello(data)
                elif data["op"] == 9:
                    _log.info("Voice Gateway Resume Successful")
                elif data["op"] == 13:
                    self.dispatcher.dispatch("USER_VOICE_CHANNEL_LEAVE")
            else:
                _log.error("Inproper WebSocket message type given.")

    def speaking(self):
        json = {
            "op": 5,
            "d": {
                "speaking": 1,
                "delay": 0,
            },
        }
        return self.send(json)

    async def send(self, data: dict):
        _log.debug("< %s", data)
        payload = json.dumps(data)

        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        await self.ws.send_bytes(payload)

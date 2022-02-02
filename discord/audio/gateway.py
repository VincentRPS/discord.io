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
from random import randint, random

import aiohttp

from discord.api.gateway import ZLIB_SUFFIX, Gateway
from discord.internal.dispatcher import Dispatcher
from discord.state import ConnectionState

_log = logging.getLogger(__name__)
aurl = "wss://gateway.discord.gg/?v=4&encoding=json&compress=zlib-stream"


class VoiceGateway:
    def __init__(
        self,
        state: ConnectionState,
        dispatcher: Dispatcher,
        gateway: Gateway,
        self_mute: bool = False,
        self_deaf: bool = False,
    ):
        self.dispatcher = dispatcher
        self.gateway = gateway
        self.state = state
        self.mute = self_mute
        self.deaf = self_deaf
        self.session_id: str = None
        self.buffer = bytearray()
        self.inflator = zlib.decompressobj()
        self.started: asyncio.Event = asyncio.Event()
        self.dispatcher.add_listener(
            self.on_voice_state_update, "on_raw_voice_state_update"
        )
        self.dispatcher.add_listener(
            self.on_voice_server_update, "on_raw_voice_server_update"
        )

    async def connect(self, guild=None, channel=None, url: str = None):
        self._session = aiohttp.ClientSession()
        if url is not None:
            self.ws = await self._session.ws_connect(url[:-4])
        self.session = aiohttp.ClientSession()
        self.v4ws = await self.session.ws_connect(aurl)
        await self.gateway.gain_voice_access(guild, channel, self.mute, self.deaf)
        if self.session_id is None:
            self.state.loop.create_task(self.recv())
            if self.ws is not None:
                self.state.loop.create_task(self.recv())
                await self.identify()
        else:
            await self.resume()
            _log.debug("Reconnected to the Gateway")

    async def on_voice_state_update(self, data):
        self.session_id = data["session_id"]
        self.started.set()

    async def heartbeat(self, interval: float):
        await self.send({"op": 1, "d": randint(100000, 999999)}, v4=False)
        await asyncio.sleep(interval)
        self.state.loop.create_task(self.heartbeat(interval))

    async def hello(self, data):
        interval = data["d"]["heartbeat_interval"] / 1000
        init = interval * random()
        await asyncio.sleep(init)
        self.state.loop.create_task(self.heartbeat(interval))

    async def on_voice_server_update(self, data):
        if not self.started.is_set():
            await self.started.wait()
        else:
            self.token = data["token"]
            self.endpoint = data["endpoint"]
            self.guild = data["guild_id"]
            await self.connect(url="wss://" + self.endpoint)

    def identify(self):
        json = {
            "op": 0,
            "d": {
                "server_id": self.guild,
                "user_id": self.state._bot_id,
                "session_id": self.session_id,
                "token": self.token,
            },
        }
        return self.send(json)

    async def recv(self):
        for msg in self.v4ws and self.ws:
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

    def speaking(
        self,
    ):
        json = {
            "op": 5,
            "d": {
                "speaking": 1,
                "delay": 0,
            },
        }
        return self.send(json, False)

    def resume(self):
        ret = {
            "op": 7,
            "d": {
                "server_id": self.guild,
                "session_id": self.session_id,
                "token": self.token,
            },
        }
        return self.send(ret, False)

    async def send(self, data: dict, v4: bool = True):
        _log.debug("< %s", data)
        payload = json.dumps(data)

        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        if v4:
            await self.v4ws.send_bytes(payload)
        else:
            await self.ws.send_bytes(payload)

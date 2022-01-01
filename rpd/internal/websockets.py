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

# Implementation of the everyday Discord WebSocket.

from __future__ import annotations

import typing

import aiohttp
from aiohttp.http_websocket import WSMsgType
import attrs
from .aioclient import CreateClientSession
from zlib import decompressobj
from rpd import helpers

__all__: typing.List[str] = [
    "DiscordClientWebSocketResponse",
    "WebSocketClient",
]

ZLIB_SUFFIX = b'\x00\x00\xff\xff'
inflator = decompressobj()

@attrs.define(init=False)
class DiscordClientWebSocketResponse(aiohttp.ClientWebSocketResponse):
    """The Discord Client WebSocket Response.

    .. versionadded:: 0.3.0
    """

    async def close(self, *, code: int = 4000, message: bytes = b"") -> bool:
        return await super().close(code=code, message=message)

@attrs.define(init=False)
class WebSocketClient:
    """The WebSocket connection with Discord.
    
    .. versionadded:: 0.3.0
    """
    def __init__(self):
        self.socket = CreateClientSession()
        self.temp = aiohttp.ClientSession()
        self.ws = DiscordClientWebSocketResponse
        self.url = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream" # the gateway url
    
    async def send(self, data):
        r = await self.socket.ws_connect(url=self.url)
        
        r.send_json(data=data, dumps=helpers._from_json)

    def wsr_decompressor(self, msg: bytes) -> typing.Optional[str]:
            self.__buffer = bytearray()
            self.__buffer.extend(msg)

            if len(self.__buffer) < 4 or self.__buffer[-4:] != ZLIB_SUFFIX:
                return None

            msg = inflator.decompress(msg)
            return msg # type: ignore

    async def decompress(self):
        async for wsr in self.ws:
            if wsr.type == WSMsgType.TEXT:
                pass
            elif wsr.type == WSMsgType.BINARY:
                data = self.wsr_decompressor(wsr.data)
                if data:
                    await self.handle_data(data)
    
    async def send_data(self, data: typing.Dict[typing.Any]):
        """Sends data to discord."""


    async def identify(self):
        """Identifys to Discord WebSocket"""
        self.send
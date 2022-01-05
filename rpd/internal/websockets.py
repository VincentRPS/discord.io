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
from zlib import decompressobj

import aiohttp
import attrs
from aiohttp.http_websocket import WSMsgType

from rpd import helpers

from .aioclient import CreateClientSession

__all__: typing.List[str] = [
    "WebSocketClient",
]

ZLIB_SUFFIX = b"\x00\x00\xff\xff"
inflator = decompressobj()


@attrs.define(init=True)
class WebSocketClient:
    """The WebSocket connection with Discord.

    .. versionadded:: 0.3.0
    """
    socket = CreateClientSession()
    ws = DiscordClientWebSocketResponse
    url = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"  # the gateway url

    async def send(self, data):
        r = await self.socket.ws_connect(url=self.url)

        r.send_json(data=data, dumps=helpers._from_json)

    async def identify(self):
        """Identifys to Discord WebSocket"""
        ...

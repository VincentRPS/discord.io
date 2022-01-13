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

import platform
import typing

from aiohttp import ClientSession

from rpd import ext
from rpd.factories import rest_factory as RF
from rpd.intents import Intents
from rpd.internal.rest import _log

__all__: typing.List[str] = [
    "WebSocketClient",
]


class WebSocketClient:
    """The WebSocket connection with Discord.

    .. versionadded:: 0.3.0
    """

    def __init__(self, token: str, intents: Intents):
        self.token = token
        self.intents = intents
        self.socket = ClientSession()
        self.rest = RF.RESTFactory()
        self.url = "wss://gateway.discord.gg/?v=9&encoding=json&compress=zlib-stream"  # the gateway url
        self.identifed: bool = False

    async def send(self, data: typing.Dict):
        r = await self.socket.ws_connect(self.url)

        _log.debug("Sending {data}")

        await r.send_json(data=data, dumps=ext._to_json)  # type: ignore

        return await r.receive_json(loads=ext._from_json)  # type: ignore

    async def identify(self):
        """Identifys to the Discord WebSocket"""
        if not self.identifed:
            await self.rest.get_gateway_bot()  # Make sure we have access.
        else:
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
                },
            }
            return await self.send(payload)

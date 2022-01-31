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
"""The Voice Client."""
import asyncio
import logging

from rpd.internal.dispatcher import Dispatcher

from .gateway import VoiceGateway

has_nacl: bool

try:
    import nacl.secret
except (ImportError, ModuleNotFoundError):
    has_nacl = False
else:
    has_nacl = True

_log = logging.getLogger(__name__)


class VoiceClient:
    def __init__(self, state, dispatcher: Dispatcher, gateway):
        self.ssrc: int = None
        self.dispatcher = dispatcher
        self.gateway = VoiceGateway(state, self.dispatcher, gateway)
        self._supported = [
            "xsalsa20_poly1305_lite",
            "xsalsa20_poly1305_suffix",
            "xsalsa20_poly1305",
        ]
        self.dispatcher.add_listener(
            self.on_voice_server_update, "on_voice_server_update"
        )
        self.endpoints = {}
        self.session_id = None

    async def on_voice_server_update(self, data):
        self.token = data["token"]
        self.endpoints[data["guild_id"]] = data["endpoint"]
        _log.info("Updated Server Info!")

    async def connect(self, guild, channel):
        self.guild = guild
        self.channel = channel
        await self.gateway.connect(guild, channel)
        await asyncio.sleep(0.300)
        await self.identify()

    def speak_without_audio(self):
        return self.gateway.speaking

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
import logging

from discord.internal.dispatcher import Dispatcher

from .gateway import VoiceGateway

has_nacl: bool

try:
    import nacl.secret  # noqa: ignore
except (ImportError, ModuleNotFoundError):
    has_nacl = False
else:
    has_nacl = True

_log = logging.getLogger(__name__)


class VoiceClient:
    """Used to interact with the discord voice api
    
    Parameters
    ----------
    state
        The :class:`ConnectionState`
    dispatcher
        The :class:`Dispatcher`
    gateway
        The :class:`Gateway`
    """
    def __init__(self, state, dispatcher: Dispatcher, gateway):
        self.ssrc: int = None
        self.dispatcher = dispatcher
        self.gateway = VoiceGateway(state, self.dispatcher, gateway)
        self._supported = [
            "xsalsa20_poly1305_lite",
            "xsalsa20_poly1305_suffix",
            "xsalsa20_poly1305",
        ]
        self.endpoint: str = None

    async def connect(self, guild, channel):
        """Connects to a voice channel
        
        Parameters
        ----------
        guild
            The guild the channel is in
        channel
            The channel id
        """
        self.guild = guild
        self.channel = channel
        await self.gateway.connect(guild=guild, channel=channel)
        _log.info("Connected to the Voice Server.")

    def speak_without_audio(self):
        return self.gateway.speaking

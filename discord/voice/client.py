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
import socket
import struct
import threading
from typing import List, Optional, Tuple

from discord import utils

from ..channels import VoiceChannel
from ..state import ConnectionState
from .gateway import VoiceGateway
from .opus import Encoder
from .players import AudioPlayer

has_nacl: bool

try:
    from nacl import secret as nacl  # noqa: ignore
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

    endpoint_ip: str
    voice_port: int
    secret_key: List[int]
    ssrc: int

    def __init__(self, state: ConnectionState, channel: VoiceChannel):
        if not has_nacl:
            raise RuntimeError('PyNaCl is needed in order to use voice')

        self.token: str = None
        self.socket = None
        self.loop: asyncio.AbstractEventLoop = state.loop
        self._state: ConnectionState = state
        self._connected: threading.Event = threading.Event()

        self._handshaking: bool = False
        self._potentially_reconnecting: bool = False
        self._voice_state_complete: asyncio.Event = asyncio.Event()
        self._voice_server_complete: asyncio.Event = asyncio.Event()

        self.mode: str = None
        self._connections: int = 0
        self.sequence: int = 0
        self.timestamp: int = 0
        self.channel = channel
        self.timeout: float = 0
        self._runner: asyncio.Task = None
        self._player: Optional[AudioPlayer] = None
        self.encoder: Encoder = None
        self._lite_nonce: int = 0
        self.ws: VoiceGateway = None
        self._state.app.dispatcher.add_listener(
            self.on_voice_state_update, 'on_raw_voice_state_update'
        )
        self._state.app.dispatcher.add_listener(
            self.on_voice_server_update, 'on_raw_voice_server_update'
        )

    warn_nacl = not has_nacl
    supported_modes: Tuple[str] = (
        'xsalsa20_poly1305_lite',
        'xsalsa20_poly1305_suffix',
        'xsalsa20_poly1305',
    )

    async def on_voice_state_update(self, data):
        self.session_id = data['session_id']
        channel_id = data['channel_id']

        if not self._handshaking or self._potentially_reconnecting:
            if channel_id is None:
                await self.disconnect()
            else:
                guild = self.guild_id
                self.channel = (
                    channel_id and guild and guild._factory.channels.get_channel(int(channel_id))
                )
        else:
            self._voice_state_complete.set()

    async def on_voice_server_update(self, data: dict):
        if self._voice_server_complete.is_set():
            return

        self.token = data.get('token')
        self.guild_id = int(data['guild_id'])
        endpoint: str = data.get('endpoint')

        if endpoint is None or self.token is None:
            return

        self.endpoint, _, _ = endpoint.rpartition(':')
        if self.endpoint.startswith('wss://'):
            self.endpoint = self.endpoint[6:]

        self.endpoint_ip = None

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)

        if not self._handshaking:
            await self.ws.close(4000)
            return

        self._voice_server_complete.set()

    async def voice_connect(self):
        await self.channel.guild.change_voice_state(channel=self.channel.id)

    async def voice_disconnect(self):
        await self.channel.guild.change_voice_state(channel=None)

    def prepare_handshake(self):
        self._voice_server_complete.clear()
        self._voice_state_complete.clear()
        self._handshaking = True
        self._connections += 1

    def finish_handshake(self):
        _log.info('Hand shaking done, using endpoint: %s', self.endpoint)
        self._handshaking = False
        self._voice_server_complete.clear()
        self._voice_state_complete.clear()

    async def ws_connect(self) -> VoiceGateway:
        ws = await VoiceGateway.voice_client_entry(self)
        self._connected.clear()
        await ws.connect()
        self._connected.set()
        return ws

    async def connect(self, *, reconnect: bool, timeout: float):
        self.timeout = timeout

        for i in range(5):
            self.prepare_handshake()

            futures = [
                self._voice_server_complete.wait(),
                self._voice_state_complete.wait(),
            ]

            await self.voice_connect()

            try:
                await utils.wait_for(futures, timeout=timeout)
            except asyncio.TimeoutError:
                await self.disconnect(force=True)
                raise

            self.finish_handshake()

            try:
                self.ws = await self.ws_connect()
                break
            except asyncio.TimeoutError:
                if reconnect:
                    _log.error('Failed to connect to the voice gateway, retrying...')
                    await asyncio.sleep(1 + i * 2)
                    await self.voice_disconnect()
                    continue
                else:
                    raise

    async def disconnect(self, *, force: bool = False):
        if not force and not self.is_connected():
            return

        self._connected.clear()

        try:
            if self.ws:
                await self.ws.close(1000)

            await self.voice_disconnect()
        finally:
            if self.socket:
                self.socket.close()

    async def move_to(self, channel: int):
        await self.channel.guild.change_voice_state(channel=channel)

    def is_connected(self) -> bool:
        return self._connected.is_set()

    # encryption things

    def checked_add(self, attr, value, limit):
        val = getattr(self, attr)
        if val + value > limit:
            setattr(self, attr, 0)
        else:
            setattr(self, attr, val + value)

    def _get_voice_packet(self, data):
        byteheader = bytearray(12)

        byteheader[0] = 0x80
        byteheader[1] = 0x78
        struct.pack_into('>H', byteheader, 2, self.sequence)
        struct.pack_into('>I', byteheader, 4, self.timestamp)
        struct.pack_into('>I', byteheader, 8, self.ssrc)

        encrypt_packet = getattr(self, '__encrypt__' + self.mode)
        return encrypt_packet(byteheader, data)

    def send_audio_packet(self, data: bytes, *, encode: bool = True):
        self.checked_add('sequence', 1, 65535)
        if encode:
            encoded_data = self.encoder.encode(data, 960)
        else:
            encoded_data = data

        packet = self._get_voice_packet(data)
        try:
            self.socket.sendto(packet, (self.endpoint_ip, self.voice_port))
        except BlockingIOError:
            _log.error('A packet was dropped')

        self.checked_add('timestamp', 65535, 4294967295)

# Apache-2.0
#
# Copyright 2021 VincentRPS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the LICENSE file for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import asyncio
import logging
import threading
import time
import zlib

import aiohttp

_log = logging.getLogger(__name__)

__all__ = [
    "DiscordClientWebSocketResponse",
    "ResumeWebSocket",
    "WebSocketConnectionClosed",
    "KeepSocketAlive",
]


class ResumeWebSocket(Exception):
    def __init__(self, resume: bool = True):
        self.resume = resume
        self.op = "RESUME" if resume else "IDENTIFY"


class WebSocketConnectionClosed(Exception):
    """Signals WebSocket closure since aiohttp doesn't."""

    pass


class DiscordClientWebSocketResponse(aiohttp.ClientWebSocketResponse):
    async def close(self, *, code: int = 4000, message: bytes = b"") -> bool:
        return await super().close(code=code, message=message)


# TODO; Make this work.
class KeepSocketAlive(threading.Thread):
    def __init__(self, *args, **kwargs):
        ws = kwargs.pop("ws", None)
        self.ws = ws

    pass


class GatewayRatelimiter:
    def __init__(self, count=110, per=60.0):
        self.max = count
        self.remaining = count
        self.window = 0.0
        self.per = per
        self.lock = asyncio.Lock()

    def is_ratelimited(self):
        current = time.time()
        if current > self.window + self.per:
            return False
        return self.remaining == 0

    def get_delay(self):
        current = time.time()

        if current > self.window + self.per:
            self.remaining = self.max

        if self.remaining == self.max:
            self.window = current

        if self.remaining == 0:
            return self.per - (current - self.window)

        self.remaining -= 1
        if self.remaining == 0:
            self.window = current
        return 0.0

    async def block(self):
        async with self.lock:
            delta = self.get_delay()
            if delta:
                _log.warning(
                    f"The WebSocket connection has been ratelimited, waiting {delta}"
                )


class DiscordWebSocket:
    """
    The WebSocket connection handler between discord and the library.

    Attributes
    ----------
    Socket
        The WebSocket
    Loop
        The Loop to pick

    .. versionadded:: 0.3.0
    """

    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    PRESENCE = 3
    VOICE_STATE = 4
    VOICE_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_MEMBERS = 8
    INVALIDATE_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11
    GUILD_SYNC = 12

    def __init__(self, socket, *, loop):
        self.socket = socket
        self.loop = loop

        self._dispatch = lambda *args: None  # Empty for preventation of crashes
        self._dispatch_listeners = []
        self._keep_alive = None  # Keep alive.
        self.thread_id = threading.get_ident()

        self.session_id = None
        self.sequence = None
        self._zlib = zlib.decompressobj()
        self._buffer = bytearray()
        self._close_code = None
        self._rate_limiter = GatewayRatelimiter()

    @property
    def open(self):
        return not self.socket.closed

    def is_ratelimited(self):
        return self._rate_limiter.is_ratelimited()

    def debug_log_receive(self, data, /):
        self._dispatch("socket_raw_receive", data)

    def log_receive(self, _, /):
        pass

    @classmethod
    async def from_client(
        cls,
        client,
        *,
        initial=False,
        gateway=None,
        session=None,
        sequence=None,
        resume=False,
    ):
        """Creates a WebSocket for :class:`Client` using :meth:`Client.ws_start`

        .. versionadded:: 0.3.0
        """
        gateway = gateway or await client.http.get_gateway()
        socket = await client.http.ws_connect(gateway)
        ws = cls(socket, loop=client.loop)

        # Some attr's needed, taken from Client
        ws.token = client.http.token

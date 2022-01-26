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
"""
The ConnectionState Caches most things during connection.
"""
import asyncio
from typing import Any


class ConnectionState:
    # if you are intereasted, the ConnectionState caches everything during connections.
    # in the future i want this to support redis and other dbs.
    def __init__(self, **options):
        self._guilds_cache = {}
        self._sent_messages_cache = {}
        self._deleted_messages_cache = {}
        self._ready: asyncio.Event = asyncio.Event()

        self._bot_token: str = options.get("token", None)
        """The cached bot token, used for Gateway."""

        self._bot_intents: int = options.get("intents", 0)
        """The cached bot intents, used for Gateway"""

        self._session_id: int = None
        """The Gateway, session id"""

        self._seq: int = None
        """The seq number"""

        self._said_hello: bool = False
        """If the Gateway got a hello or not."""

        self.loop: asyncio.AbstractEventLoop = options.get("loop", None)

        self._bot_presences: list[str, Any] = []
        """The precenses"""

        self._bot_status: str = "online"
        """The status"""

        self._bot_presence_type: int = 0
        """Precense type"""

        self.listeners = {}
        """The listeners"""

        self._gle_l = []
        """Global listeners"""

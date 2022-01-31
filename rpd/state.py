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
from typing import Any, Callable, Dict, List, Tuple


class ConnectionState:
    """The Connection State

    .. note::

        The connection state is responsible for caching
        everything, meaning most classes will depend on it.

    .. note::

        .. data:: ConnectionState._speaking

        is planned to be deprecated soon.

    Attributes
    ----------
    _bot_intents :class:`int`
        The cached bot intents, used for Gateway

    _session_id :class:`int`
        The Gateway, session id

    _voice_session_id :class:`int`
        The Voice Gateway Session ID

    _seq :class:`int`
        The Gateway seq number, can be None.

    app :class:`BotApp` or :class:`WebhookApp`
        The bot app

        .. versionadded:: 0.5.0

    _voice_seq :class:`int`
        The Voice Gateway seq

        .. versionadded:: 0.5.0

    _voice_user_data :class:`dict`
        The Voice User Data given by the Voice Gateway.

        .. versionadded:: 0.5.0

    _speaking :class:`bool`
        If the bot is currently speaking, defaults False

        .. versionadded:: 0.5.0

    _said_hello :class:`bool`
        If the Gateway got a hello or not.

    loop :class:`asyncio.AbstractEventLoop`
        The current loop

    _bot_presences :class:`list`
        A list of the bots presences

    _bot_status :class:`str`
        The bot status, e.g. online

    _bot_presence_type :class:`int`
        The bot presence type, defaults to 0

    listeners :class:`dict`
        The bot listeners

    all :class:`dict`
        The appendix of all cache.

    shard_count :class:`int`
        the number of shards.

        .. versionadded:: 0.6.0

    .. versionadded:: 0.4.0

    """

    def __init__(self, **options):
        self._guilds_cache = {}
        self._sent_messages_cache = {}
        self._deleted_messages_cache = {}
        self._ready: asyncio.Event = asyncio.Event()

        self._bot_intents: int = options.get("intents", 0)
        """The cached bot intents, used for Gateway"""

        self._bot_id: int = None

        self._voice_session_id: int = None

        self._seq: int = None
        """The seq number"""

        self.app = options.get("bot", None)
        """The bot app
        
        .. versionadded:: 0.5.0
        """

        self._voice_seq: int = None
        """The Voice Gateway seq
        
        .. versionadded:: 0.5.0
        """

        self._voice_user_data: Dict = {}
        """The Voice User Data given by the Voice Gateway.
        
        .. versionadded:: 0.5.0
        """

        self._speaking: bool = False
        """If the bot is currently speaking
        
        .. versionadded:: 0.5.0
        """

        self._said_hello: bool = False
        """If the Gateway got a hello or not."""

        self.loop: asyncio.AbstractEventLoop = options.get("loop", None)
        """The current loop"""

        self._bot_presences: list[str, Any] = []
        """The precenses"""

        self._bot_status: str = "online"
        """The status"""

        self._bot_presence_type: int = 0
        """Precense type"""

        self.listeners: Dict[str, List[Tuple[asyncio.Future, Callable[..., bool]]]] = {}
        """The listeners"""

        self.all = {}
        """The appendix of all cache."""

        self.shard_count: int = options.get("shard_count", 1)
        """The shard count"""

        self.commands = {}
        """Stores commands
        
        The basic idea of: ::

            self.commands = {
                "command_name": {
                    "id": "interaction.id",
                    "options": {
                        ...
                    }
                }
            }
        """

    async def update(self):
        """Updates the cache appendix."""
        self.all["status"] = self._bot_status
        self.all["presences"] = self._bot_presences
        self.all["gateway_seq"] = self._seq
        self.all["listeners"] = self.listeners
        self.all["intents"] = self._bot_intents
        self.all["token"] = self._bot_token
        self.all["presence_type"] = self._bot_presence_type
        self.all["guilds"] = self._guilds_cache
        self.all["ready"] = self._ready.is_set()
        self.all["sent_messages"] = self._sent_messages_cache
        self.all["deleted_messages"] = self._deleted_messages_cache
        self.loop.create_task(self.update())

    def create(self):
        """Creates a cache appendix."""
        # yes this is very very slow, nothing i can do about it.
        self.all["status"] = self._bot_status
        self.all["presences"] = self._bot_presences
        self.all["gateway_seq"] = self._seq
        self.all["listeners"] = self.listeners
        self.all["intents"] = self._bot_intents
        self.all["token"] = self._bot_token
        self.all["presence_type"] = self._bot_presence_type
        self.all["guilds"] = self._guilds_cache
        self.all["ready"] = self._ready.is_set()
        self.all["sent_messages"] = self._sent_messages_cache
        self.all["deleted_messages"] = self._deleted_messages_cache
        self.all["voice"] = {
            "session_id": self._voice_session_id,
            "seq": self._voice_seq,
            "user_data": self._voice_user_data,
        }
        self.loop.create_task(self.update(), name="RPD Full Connection Cache")

    def list(self) -> Dict:
        return self.all

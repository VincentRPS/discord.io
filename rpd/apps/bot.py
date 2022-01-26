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
"""The bot app"""

import asyncio
import logging
from typing import Any, Awaitable, Callable, List

from rpd.api import RESTFactory
from rpd.api.gateway import Gateway
from rpd.internal import dispatcher
from rpd.presence import Presence
from rpd.state import ConnectionState
from rpd.ui import print_banner

_log = logging.getLogger(__name__)
__all__: List[str] = [
    "BotApp"
]


class BotApp:
    """Represents a Discord bot.

    .. versionadded:: 0.4.0

    Attributes
    ----------
    factory
        The instance of RESTFactory
    state
        The client's connection state
    """

    def __init__(self, **options):
        self.token = options.get("token")
        self.state = ConnectionState(
            loop=options.get("loop", asyncio.new_event_loop()),
            intents=options.get("intents"),
            token=self.token,
        )
        self.dispatcher = dispatcher.Dispatcher(state=self.state)
        self.factory = RESTFactory(state=self.state)
        self.gateway = Gateway(state=self.state)
        self._got_gateway_bot: bool = False
        self.p = Presence(options.get("status", "online"), options.get("afk", False))
        print_banner(options.get("module", "rpd"))

    async def login(self, token):
        """Starts the bot connection

        .. versionadded:: 0.4.0

        """
        self.token = token
        await self.factory.login(token)

    async def connect(self):
        """Starts the WebSocket(Gateway) connection with Discord.

        .. versionadded:: 0.4.0
        """
        if self._got_gateway_bot is False:
            await self.factory.get_gateway_bot()

        await self.gateway.connect()

    def run(self):
        """A blocking function to start your bot"""

        async def runner():
            await self.login(token=self.token)
            await self.factory.get_gateway_bot()
            await self.connect()

        self.state.loop.create_task(runner())
        self.state.loop.run_forever()

    @property
    async def is_ready(self):
        """Returns if the bot is ready or not."""
        return self.state._ready.is_set()

    async def change_presence(self, name: str, type: int):
        await self.p.edit(name, type)

    @property
    def presence(self) -> list[str]:
        return self.state._bot_presences

    def listen(
        self, event: Any = None
    ) -> Callable[[Any], Callable[..., Awaitable[Any]]]:
        """Listens to a certain event."""

        def inside(
            coro: Callable[..., Awaitable[Any]]
        ) -> Callable[..., Awaitable[Any]]:
            if event is None:
                self.state._gle_l.append(coro)
            else:
                self.state.listeners[event].append(coro)
            return coro

        return inside

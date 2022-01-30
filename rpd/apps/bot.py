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
import importlib
import logging
import os
from threading import Event
from typing import List, Optional

from rpd.api import RESTFactory
from rpd.api.gateway import Gateway
from rpd.internal import dispatcher
from rpd.presence import Presence
from rpd.state import ConnectionState
from rpd.ui import print_banner
from rpd.audio import has_nacl

_log = logging.getLogger(__name__)
__all__: List[str] = ["BotApp"]


class BotApp:
    """Represents a Discord bot.

    .. versionadded:: 0.4.0

    Attributes
    ----------
    factory
        The instance of RESTFactory
    state
        The client's connection state
    dispatcher
        The dispatcher
    gateway
        The Gateway
    p
        The presence
    cogs
        A :class:`dict` of all Cogs.

    Parameters
    ----------
    token
        The bot token
    intents
        The bot intents, defaults `32509`
    status
        The bot status, defaults to online
    afk
        If the bot is afk, default to False
    loop
        The loop you want to use, defaults to :class:`asyncio.new_event_loop`
    module
        The module with a `banner.txt` to print
    """

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = asyncio.new_event_loop(),
        intents: Optional[int] = 32509,
        status: Optional[str] = "online",
        afk: Optional[bool] = False,
        module: Optional[str] = "rpd",
    ):
        self.state = ConnectionState(
            loop=loop,
            intents=intents,
            bot=self,
        )
        self.dispatcher = dispatcher.Dispatcher(state=self.state)
        self.factory = RESTFactory(state=self.state)
        self.gateway = Gateway(state=self.state, dispatcher=self.dispatcher)
        self._got_gateway_bot: Event = Event()
        self.cogs = {}
        self.p = Presence(
            gateway=self.gateway,
            state=self.state,
            status=status,
            afk=afk,
        )
        print_banner(module)
        if not has_nacl:
            _log.warning(
                "You don't have PyNaCl, meaning you won't be able to use Voice features."
            )

    async def login(self, token: str):
        """Starts the bot connection

        .. versionadded:: 0.4.0

        """
        self.token = token
        await self.factory.login(token)

    async def connect(self, token: str):
        """Starts the WebSocket(Gateway) connection with Discord.

        .. versionadded:: 0.4.0
        """
        if self._got_gateway_bot.is_set() is False:
            await self.factory.get_gateway_bot()
            self._got_gateway_bot.set()

        await self.gateway.connect(token=token)

    def run(self, token: str):
        """A blocking function to start your bot"""

        async def runner():
            await self.login(token=token)
            await self.factory.get_gateway_bot()
            await self.connect(token=token)

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

    def listen(self, coro: dispatcher.Coro) -> dispatcher.Coro:
        return self.dispatcher.listen(coro)

    def load_module(self, location, package):
        importlib.import_module(location, package)

    def load_modules(self, folder):
        for file in os.listdir(folder):
            self.load_module(file)

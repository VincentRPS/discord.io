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
from typing import Callable, List, Optional, TypeVar

from rpd.api import RESTFactory
from rpd.api.gateway import Gateway
from rpd.audio import has_nacl
from rpd.implements.core import implements
from rpd.interactions.command import Command
from rpd.internal import dispatcher
from rpd.state import ConnectionState
from rpd.ui import print_banner

_log = logging.getLogger(__name__)
__all__: List[str] = ["BotApp"]
CFT = TypeVar("CFT", bound="dispatcher.CoroFunc")


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
        module: Optional[str] = "rpd",
        shards: Optional[int] = None,
        mobile: Optional[bool] = False,
        command_prefix: Optional[str] = None,
    ):
        self.command_prefix = command_prefix
        self.state = ConnectionState(
            loop=loop,
            intents=intents,
            bot=self,
            shard_count=shards,
        )
        self.dispatcher = dispatcher.Dispatcher(state=self.state)
        self.factory = RESTFactory(state=self.state)
        self.gateway = Gateway(
            state=self.state,
            dispatcher=self.dispatcher,
            factory=self.factory,
            mobile=mobile,
        )
        self._got_gateway_bot: Event = Event()
        self.cogs = {}
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
        r = await self.factory.login(token)
        self.state._bot_id = r["id"]
        return r

    async def connect(self, token: str):
        """Starts the WebSocket(Gateway) connection with Discord.

        .. versionadded:: 0.4.0
        """

        await self.gateway.connect(token=token)

    def implements(self, command_name: str, prefixed_command: bool = False):
        return implements(
            self, self.command_prefix, self.dispatcher, command_name, prefixed_command
        )

    def run(self, token: str):
        """A blocking function to start your bot"""

        async def runner():
            await self.login(token=token)
            await asyncio.sleep(0.111)  # sleep for a bit
            await self.connect(token=token)

        self.state.loop.create_task(runner())
        self.state.loop.run_forever()

    @property
    async def is_ready(self):
        """Returns if the bot is ready or not."""
        return self.state._ready.is_set()

    @property
    def presence(self) -> list[str]:
        return self.state._bot_presences

    def event(self, coro: dispatcher.Coro) -> dispatcher.Coro:
        return self.dispatcher.listen(coro)

    def load_module(self, location, package):
        importlib.import_module(location, package)

    def load_modules(self, folder):
        for file in os.listdir(folder):
            self.load_module(file)

    def listen(self, name: str = None) -> Callable[[CFT], CFT]:
        def decorator(func: CFT) -> CFT:
            self.dispatcher.add_listener(func, name)
            return func

        return decorator

    def command(
        self,
        slash_command: bool = False,
        user_command: bool = False,
        message_command: bool = False,
    ):
        return Command(self.state, self.factory)

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
"""The Client powering discord.io's bots."""

import asyncio
import importlib
import logging
import os
from threading import Event
from time import time
from typing import Callable, List, Literal, Optional, TypeVar, Union

from discord.api.gateway import Gateway
from discord.api.rest_factory import RESTFactory
from discord.audio import VoiceClient, has_nacl
from discord.internal import command_dispatcher, dispatcher
from discord.state import ConnectionState
from discord.types.dict import Dict
from discord.ui import print_banner, start_logging
from discord.user import User

from .components import Button, Coro

_log = logging.getLogger(__name__)
__all__: List[str] = ["Client"]
CFT = TypeVar("CFT", bound="dispatcher.CoroFunc")


class Client:
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
    voice
        If to enable the voice gateway or not, defaults False.
    logs
        A :class:`int`, :class:`str` or :class:`dict`.
    debug
        To show debug logs or not.
    state :class:`ConnectionState`
        Allow's for custom ConnectionStates,
        and soforth custom db caches.
    command_prefix :class:`str`
        The prefix for prefixed commands,
        defaults to "".
    """

    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = asyncio.new_event_loop(),
        intents: Optional[int] = 32509,
        module: Optional[str] = "discord",
        shards: Optional[int] = None,
        mobile: Optional[bool] = False,
        proxy: Optional[str] = None,
        proxy_auth: Optional[str] = None,
        voice: Optional[bool] = False,
        logs: Optional[Union[None, int, str, Dict]] = None,
        debug: Optional[bool] = False,
        state: Optional[ConnectionState] = None,
        command_prefix: Optional[str] = "",
    ):
        print_banner(module)
        start_logging(logs, debug)
        self.state = state or ConnectionState(
            loop=loop,
            intents=intents,
            bot=self,
            shard_count=shards,
            prefix=command_prefix,
        )
        self.command_prefix = command_prefix
        self.cmd_dispatch = command_dispatcher.CommandDispatcher(self.state)
        self.dispatcher = dispatcher.Dispatcher(state=self.state)
        self.factory = RESTFactory(state=self.state, proxy=proxy, proxy_auth=proxy_auth)
        self.gateway = Gateway(
            state=self.state,
            dispatcher=self.dispatcher,
            factory=self.factory,
            mobile=mobile,
        )
        if voice is True:
            self.voice = VoiceClient(self.state, self.dispatcher, self.gateway)
        self._got_gateway_bot: Event = Event()
        self.cogs = {}

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

    def run(self, token: str):
        """A blocking function to start your bot"""

        async def runner():
            await self.login(token=token)
            await asyncio.sleep(0.111)  # sleep for a bit
            await self.connect(token=token)

        self.state.loop.create_task(runner())
        self.state.loop.run_forever()

    def create_button(
        self,
        label: str,
        callback: Coro,
        style: Literal[1, 2, 3, 4, 5] = 1,
        custom_id: str = None,
        url: str = None,
    ):
        return Button(self.state).create(label, callback, style, custom_id, url)

    @property
    async def is_ready(self):
        """Returns if the bot is ready or not."""
        return self.state._ready.is_set()

    @property
    def presence(self) -> list[str]:
        return self.state._bot_presences

    def change_presence(
        self,
        name: str,
        type: int,
        status: Literal["online", "dnd", "idle", "invisible", "offline"] = "online",
        stream_url: Optional[str] = None,
        afk: Optional[bool] = False,
    ):
        if type == 1 and stream_url is None:
            raise NotImplementedError("Streams need to be provided a url!")
        elif type == 1 and stream_url is not None:
            ret = {
                "name": name,
                "type": 1,
                "url": stream_url,
            }
        else:
            # another type
            ret = {
                "name": name,
                "type": type,
            }
        json = {"op": 3, "d": {"activities": [ret]}}

        if afk is True:
            json["d"]["afk"] = True
            json["d"]["since"] = time()
        else:
            json["d"]["afk"] = False
            json["d"]["since"] = None

        json["d"]["status"] = status

        return self.gateway.send(json)

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

    def command(self, name: str = None) -> Callable[[CFT], CFT]:
        """Registers a prefixed command"""

        def decorator(func: CFT) -> CFT:
            self.cmd_dispatch.add_command(func, name)
            return func

        return decorator

    @property
    def user(self):
        return User(self.state.bot_info[self])

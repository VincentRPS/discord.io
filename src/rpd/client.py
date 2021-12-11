"""
Apache-2.0

Copyright 2021 RPS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the LICENSE file for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

import logging
from typing import Any, Callable, Coroutine, TypeVar

import aiohttp
from asyncio import get_event_loop

from .._rpd import Command, Response, Route, Send, OpcodeDispatch, EventDispatch
from .exceptions import HTTPException, LoginFailure

_log = logging.getLogger(__name__)

__all__ = ("Client",)

from typing import List, Union

Snowflake = Union[str, int]
SnowflakeList = List[Snowflake]

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]
CFT = TypeVar("CFT", bound="CoroFunc")


class Client:
    """Client For Bots"""

    def __init__(self):
        self.loop = get_event_loop()
        self.opcode_dispatcher = OpcodeDispatch(self.loop)
        self.event_dispatcher = EventDispatch(self.loop)

    async def command(self) -> Callable[[CFT], CFT]:
        """Command Stuff"""
        return Command

    def send(self) -> Send:
        """Sends Messages For Client"""
        return Send

    def run(self):
        """
        Starts the client.
        """
        try:
            self.loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.close())
        if self.fatal_exception is not None:
            raise self.fatal_exception from None

    async def fatal(self, exception):
        """
        Raises a fatal exception to the bot.
        Please do not use this for non-fatal exceptions.
        """
        self.fatal_exception = exception
        await self.close()

    def logout(self) -> Response[None]:
        return self.request(Route("POST", "/auth/logout"))

    def listen(self, event):
        """
        Listen to an event or opcode.
        Parameters
        ----------
        event: Union[int, str]
            An opcode or event name to listen to.
        Raises
        ------
        TypeError
            Invalid event type was passed.
        """

        def get_func(func):
            if isinstance(event, int):
                self.opcode_dispatcher.register(event, func)
            elif isinstance(event, str):
                self.event_dispatcher.register(event, func)
            else:
                raise TypeError("Invalid event type!")

        return get_func
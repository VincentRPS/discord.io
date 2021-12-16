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
from asyncio import get_event_loop
from typing import Any, Callable, Coroutine, TypeVar

import aiohttp

from . import EventDispatch, OpcodeDispatch
from .exceptions import TokenNotFound

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

    def __init__(self, token=None):
        self.loop = get_event_loop()
        self.opcode_dispatcher = OpcodeDispatch(self.loop)
        self.event_dispatcher = EventDispatch(self.loop)
        self.token = token

    async def command(self) -> Callable[[CFT], CFT]:
        """Command Stuff"""
        pass

    async def send(self):
        """Sends Messages For Client"""
        pass

    async def login(self, token: str) -> None:
        """|coro|
        Logs in the client with the specified credentials.
        Parameters
        -----------
        token: :class:`str`
            The authentication token. Do not prefix this token with
            anything as the library will do it for you.
        Raises
        ------
        :exc:`.LoginFailure`
            The wrong credentials are passed.
        :exc:`.HTTPException`
            An unknown HTTP related error occurred,
            usually when it isn't 200 or the known incorrect credentials
            passing status code.
        """

        _log.info("logging in using static token")

        data = await self.http.static_login(token.strip())

    def listen(self, event):
        def get_func(func):
            if isinstance(event, int):
                self.opcode_dispatcher.register(event, func)
            elif isinstance(event, str):
                self.event_dispatcher.register(event, func)
            else:
                raise TypeError("Invalid event type!")

        return get_func

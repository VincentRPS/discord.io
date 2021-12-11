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

from .exceptions import HTTPException, LoginFailure
from .._rpd.client.core import Command, Send
from .._rpd.connections.gate import DiscordClientWebSocketResponse
from .._rpd.connections.web import Response, Route

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
        pass

    async def command(self) -> Callable[[CFT], CFT]:
        """Command Stuff"""
        return Command

    def send(self) -> Send:
        """Sends Messages For Client"""
        return Send

    async def login(self, token: str):
        # Necessary to get aiohttp to stop complaining about session creation
        self.session = aiohttp.ClientSession(
            connector=self.connector, ws_response_class=DiscordClientWebSocketResponse
        )
        old_token = self.token
        self.token = token

        try:
            data = await self.request(Route("GET", "/users/@me"))
        except HTTPException as exc:
            self.token = old_token
            if exc.status == 401:
                raise LoginFailure("Improper token has been passed.") from exc
            raise

        return data

    async def fatal(self, exception):
        """
        Raises a fatal exception to the bot.
        Please do not use this for non-fatal exceptions.
        """
        self.fatal_exception = exception
        await self.close()

    def logout(self) -> Response[None]:
        return self.request(Route("POST", "/auth/logout"))

    async def listen(self):
        pass

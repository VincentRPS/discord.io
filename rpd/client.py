"""
Apache-2.0

Copyright 2021 VincentRPS

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

import asyncio
import logging
from typing import Any, Callable, Coroutine, List, Optional, TypeVar, Union

from rpd.internal import HTTPClient

_log = logging.getLogger(__name__)

__all__ = "Client"

Snowflake = Union[str, int]
SnowflakeList = List[Snowflake]

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]
CFT = TypeVar("CFT", bound="CoroFunc")


class Client:
    """The base Client for RPD interactions

    .. versionadded:: 2.0
    """

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop
        self.http = HTTPClient()

    async def command(self) -> Callable[[CFT], CFT]:
        """A callable function for commands

        .. versionadded:: 0.1.0
        """
        pass

    async def login(self, token: str):
        """|coro|
        Logs in the client with the specified credentials.

        .. versionadded:: 0.3.0

        Parameters
        -----------
        token: :class:`str`
            Your bot token.
        Raises
        ------
        :exc:`.LoginFailure`
            The token passed was invalid.
        :exc:`.HTTPException`
            An unknown HTTP related error occurred,
            usually when it isn't 200 or the known incorrect credentials
            passing status code.
        """
        self.token = token

        _log.info("Trying to login with the specified credentials")

        data = await self.http.login(token.strip())

    def start(self):
        """Starts the :class:`Client` instance."""

    def listen(self, event):
        """Listens to a certain OPCode event

        .. versionadded:: 0.1.0
        """

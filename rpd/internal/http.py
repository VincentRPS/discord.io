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
import sys
from typing import Any, Dict, Optional, TYPE_CHECKING

import aiohttp
from .gateway import DiscordClientWebSocketResponse

from rpd import __version__
from rpd.exceptions import (
    Forbidden,
    HTTPException,
    NotFound,
    RateLimitError,
    Unauthorized,
)
from ..helpers.missing import MISSING
from ..helpers.orjson import _from_json

if TYPE_CHECKING:
    from ..data.types.user import User
    from ..data.types.snowflake import Snowflake, SnowflakeList

__all__ = ("Route", "HTTPClient")

POST = "https://discord.com/api/v9"


class Route:
    def __init__(self, method, route, **parameters):
        self.method = method
        self.path = route.format(**parameters)

        # Used for bucket cooldowns
        self.channel_id = parameters.get("channel_id")
        self.guild_id = parameters.get("guild_id")

    @property
    def bucket(self):
        """
        The Route's bucket identifier.
        """
        return f"{self.channel_id}:{self.guild_id}:{self.path}"


class HTTPClient:
    def __init__(
        self,
        loop=asyncio.get_event_loop(),
        connector: Optional[aiohttp.BaseConnector] = None,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
    ):
        self.__session: aiohttp.ClientSession = MISSING
        self.loop = loop
        self.connector = connector
        self.token: Optional[str] = None
        self.proxy: Optional[str] = proxy
        self.proxy_auth: Optional[aiohttp.BasicAuth] = proxy_auth
        user_agent = "DiscordBot (https://github.com/RPD-py/RPD {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )
        self.headers = {
            "X-RateLimit-Precision": "millisecond",
            "Authorization": f"Bot {self.token}",
        }

    async def ws_connect(self, url: str, *, compress: int = 0) -> Any:
        kwargs = {
            "proxy_auth": self.proxy_auth,
            "proxy": self.proxy,
            "max_msg_size": 0,
            "timeout": 30.0,
            "autoclose": False,
            "headers": {
                "User-Agent": self.user_agent,
            },
            "compress": compress,
        }

        return await self.__session.ws_connect(url, **kwargs)

    async def request(self, **kwargs: Any):

        headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
        }

        if self.token is not None: # Makes sure the token is None
            headers["Authorization"] = "Bot " + self.token
        # Making sure it's json
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = _from_json(kwargs.pop("json"))

        kwargs["headers"] = headers
        r = await self.__session.request(**kwargs)
        headers = r.headers

        if r.status == 429:
            raise RateLimitError(r)

        elif r.status == 401:
            raise Unauthorized(r)

        elif r.status == 403:
            raise Forbidden(r, await r.text())

        elif r.status == 404:
            raise NotFound(r)

        elif r.status >= 300:
            raise HTTPException(r, await r.text())

        return r

    # Closes The Session
    async def close(self):
        await self.__session.close()

    async def login(self, token: str) -> User:
        # Statically logs-into discord
        self.__session = aiohttp.ClientSession(connector=self.connector, ws_response_class=DiscordClientWebSocketResponse)
        self.previous_token = self.token
        self.token = token
        
        try:
            data = await self.request(Route("GET", "users/@me"))
        except HTTPException as HTTPe:
            self.token = self.previous_token
            if HTTPe.status == 401:
                raise LoginFailure(f"Invalid or no Token was passed. {HTTPe}")
        return data

    def logout(self):
        # Tells discord to log out
        return self.request(Route("POST", "/auth/logout"))

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

import asyncio
import json
import logging
import sys
from typing import Any, ClassVar, Dict, Optional, Union
from urllib.parse import quote

import aiohttp
from aiohttp import ClientSession, ClientWebSocketResponse
from aiohttp import __version__ as aiohttp_version

from ...__init__ import __discord__ as version
from ...__init__ import __version__
from ...client import Client, Snowflake, SnowflakeList
from ...exceptions import (
    Forbidden,
    HTTPException,
    NotFound,
    RateLimitError,
    Unauthorized,
)
from ..enums import *

_LOG = logging.getLogger(__name__)


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding="utf-8")
    try:
        if response.headers["content-type"] == "application/json":
            return json.dumps(text)
    except KeyError:
        pass

    return text


class Route:
    BASE: ClassVar[str] = "https://discord.com/api/v9"

    def __init__(self, method: str, path: str, **parameters: Any) -> None:
        self.path: str = path
        self.method: str = method
        url = self.BASE + self.path
        if parameters:
            url = url.format_map(
                {
                    k: quote(v) if isinstance(v, str) else v
                    for k, v in parameters.items()
                }
            )
        self.url: str = url

        # major parameters:
        self.channel_id: Optional[Snowflake] = parameters.get("channel_id")
        self.guild_id: Optional[Snowflake] = parameters.get("guild_id")

    @property
    def bucket(self) -> str:
        # the bucket is just method + path w/ major parameters
        return f"{self.channel_id}:{self.guild_id}:{self.path}"


class HTTPClient:
    def __init__(self, loop=asyncio.get_event_loop()):
        self.session = ClientSession()
        self.loop = loop
        user_agent = "DiscordBot (https://github.com/RPD-py/RPD {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )
        self.headers = {
            "X-RateLimit-Precision": "millisecond",
            "Authorization": f"Bot {Client.start.token}",
        }

    async def connect_to_ws(self, *, compression) -> ClientWebSocketResponse:
        if self.session.closed:
            self.session = ClientSession()
        ws_info = {
            "max_msg_size": 0,
            "timeout": 40,
            "autoclose": False,
            "headers": {"User-Agent": self.headers["User-Agent"]},
            "compress": compression,
        }
        return await self.session.ws_connect(Route, **ws_info)

    async def request(self, **kwargs: Any):
        if self.session.closed:
            self.session = ClientSession()

        headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
        }

        if self.token is not None:
            headers["Authorization"] = "Bot " + self.token
        # Making sure it's json
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.dumps(kwargs.pop("json"))

        kwargs["headers"] = headers
        r = await self.session.request(Route, **kwargs)
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

    async def close_ws(self) -> Any:
        await self.session.close()

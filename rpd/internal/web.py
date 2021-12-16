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
import asyncio
import json
import sys
from typing import Any, Dict

import aiohttp
from aiohttp import ClientSession, ClientWebSocketResponse

from .. import __version__
from ..exceptions import (
    Forbidden,
    HTTPException,
    NotFound,
    RateLimitError,
    Unauthorized,
)
from .gate import DiscordClientWebSocketResponse

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


class LockManager:
    def __init__(self, lock: asyncio.Lock):
        self.lock = lock
        self.unlock = True

    def __enter__(self):
        return self

    def defer(self):
        """
        Stops the lock from being automatically being unlocked when it ends
        """
        self.unlock = False

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.unlock:
            self.lock.release()


class HTTPClient:
    def __init__(self, loop=asyncio.get_event_loop(), token=None):
        self.session = ClientSession()
        self.loop = loop
        self.token = token
        user_agent = "DiscordBot (https://github.com/RPD-py/RPD {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )
        self.headers = {
            "X-RateLimit-Precision": "millisecond",
            "Authorization": f"Bot {self.token}",
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
        return await self.session.ws_connect(POST, **ws_info)

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
        r = await self.session.request(**kwargs)
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

    async def close(self):
        await self.session.close()

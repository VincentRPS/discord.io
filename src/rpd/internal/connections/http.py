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
import asyncio
from json import dump

from aiohttp import ClientSession, __version__ as aiohttp_version, ClientWebSocketResponse
from sys import version_info as python_version
from typing import Any, Dict

from ...__init__ import __discord__ as version, __version__
from ..enums import *
from ...exceptions import Forbidden, NotFound, HTTPException, Unauthorized, RateLimitError

_LOG = logging.getLogger(__name__)

POST = f"https://discord.com/api/v{version}"


class HTTPClient:
    def __init__(self, loop=asyncio.get_event_loop()):
        self.session = ClientSession()
        self.loop = loop

        self.headers = {
            "X-RateLimit-Precision": "millisecond",
            "Authorization": f"Bot {self.token}",
            "User-Agent": f"DiscordBot (https://github.com/RPD-py/RPD {__version__}) "
                          f"Python/{python_version[0]}.{python_version[1]} "
                          f"aiohttp/{aiohttp_version}"
        }

    async def connect_to_ws(self, *, compression) -> ClientWebSocketResponse:
        if self.session.closed:
            self.session = ClientSession()
        ws_info = {
            "max_msg_size": 0,
            "timeout": 40,
            "autoclose": False,
            "headers": {
                "User-Agent": self.headers["User-Agent"]
            },
            "compress": compression
        }
        return await self.session.ws_connect(POST, **ws_info)

    async def request(self, url: POST, **kwargs: Any):
        if self.session.closed:
            self.session = ClientSession()
    
        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
        }
        
        if self.token is not None:
            headers['Authorization'] = 'Bot ' + self.token
        # Making sure it's json
        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['data'] = dump(kwargs.pop('json'))
        
        r = await self.session.request(self.url, **kwargs)
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

    async def close_ws(self):
        await self.session.close()
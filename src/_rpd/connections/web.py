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
import weakref
from types import TracebackType
from typing import (
    Any,
    ClassVar,
    Coroutine,
    Dict,
    Iterable,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
)
from urllib.parse import quote

import aiohttp
from aiohttp import ClientSession, ClientWebSocketResponse
from aiohttp import __version__ as aiohttp_version

from ...rpd.__init__ import __discord__ as version
from ...rpd.__init__ import __version__
from ...rpd.client import Snowflake
from ...rpd.exceptions import (
    Base,
    Forbidden,
    HTTPException,
    LoginFailure,
    NotFound,
    RateLimitError,
    Unauthorized,
)
from ..file import File
from .gate import DiscordClientWebSocketResponse

_log = logging.getLogger(__name__)
T = TypeVar("T")
MU = TypeVar("MU", bound="MaybeUnlock")
BE = TypeVar("BE", bound=Base)
Response = Coroutine[Any, Any, T]


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding="utf-8")
    try:
        if response.headers["content-type"] == "application/json":
            return json.dumps(text)
    except KeyError:
        pass

    return text


class MaybeUnlock:
    def __init__(self, lock: asyncio.Lock) -> None:
        self.lock: asyncio.Lock = lock
        self._unlock: bool = True

    def __enter__(self: MU) -> MU:
        return self

    def defer(self) -> None:
        self._unlock = False

    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None:
        if self._unlock:
            self.lock.release()


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
    def __init__(
        self,
        token,
        connector: Optional[aiohttp.BaseConnector] = None,
        loop=asyncio.get_event_loop(),
    ):
        self.session = ClientSession()
        self.loop = loop
        self.token = token
        self.connector = connector
        user_agent = "DiscordBot (https://github.com/RPD-py/RPD {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )
        self.headers = {
            "X-RateLimit-Precision": "millisecond",
            "Authorization": f"Bot {self.token}",
        }
        self._locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self._global_over: asyncio.Event = asyncio.Event()
        self._global_over.set()

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

    # Based Off Of discord.py's request
    async def request(
        self,
        route: Route,
        *,
        files: Optional[Sequence[File]] = None,
        form: Optional[Iterable[Dict[str, Any]]] = None,
        **kwargs: Any,
    ) -> Any:
        bucket = route.bucket
        method = route.method
        url = route.url

        lock = self._locks.get(bucket)
        if lock is None:
            lock = asyncio.Lock()
            if bucket is not None:
                self._locks[bucket] = lock

        # header creation
        headers: Dict[str, str] = {
            "User-Agent": self.user_agent,
        }

        if self.token is not None:
            headers["Authorization"] = "Bot " + self.token
        # some checking if it's a JSON request
        if "json" in kwargs:
            headers["Content-Type"] = "application/json"
            kwargs["data"] = json.loads(kwargs.pop("json"))

        try:
            reason = kwargs.pop("reason")
        except KeyError:
            pass
        else:
            if reason:
                headers["X-Audit-Log-Reason"] = quote(reason, safe="/ ")

        if not self._global_over.is_set():
            # wait until the global lock is complete
            await self._global_over.wait()

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None
        await lock.acquire()
        with MaybeUnlock(lock) as maybe_lock:
            for tries in range(5):
                if files:
                    for f in files:
                        f.reset(seek=tries)

                if form:
                    form_data = aiohttp.FormData()
                    for params in form:
                        form_data.add_field(**params)
                    kwargs["data"] = form_data

                try:
                    async with self.session.request(method, url, **kwargs) as response:
                        _log.debug(
                            "%s %s with %s has returned %s",
                            method,
                            url,
                            kwargs.get("data"),
                            response.status,
                        )

                        data = await json_or_text(response)

                        if 300 > response.status >= 200:
                            _log.debug("%s %s has received %s", method, url, data)
                            return data

                        if response.status in {500, 502, 504}:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        if response.status == 403:
                            raise Forbidden(response, data)
                        elif response.status == 404:
                            raise NotFound(response, data)
                        elif response.status >= 500:
                            raise HTTPException(response, data)
                        else:
                            raise HTTPException(response, data)

                except OSError as e:
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise

            if response is not None:
                if response.status >= 500:
                    raise HTTPException(response, data)

                raise HTTPException(response, data)

            raise RuntimeError("Unreachable code in HTTP handling")

    async def close_ws(self) -> Any:
        await self.session.close()

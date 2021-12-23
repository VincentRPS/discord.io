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
import sys
import weakref
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    ClassVar,
    Coroutine,
    Dict,
    Optional,
    Type,
    TypeVar,
    Union,
)
from urllib.parse import quote as _uriquote

import aiohttp

import rpd

from ..exceptions import *
from .gateway import DiscordClientWebSocketResponse

_log = logging.getLogger(__name__)

from ..helpers.missing import MISSING
from ..helpers.whichjson import _from_json, _to_json

if TYPE_CHECKING:
    from ..data.types.snowflake import Snowflake, SnowflakeList
    from ..data.types.user import User

    T = TypeVar("T")
    BE = TypeVar("BE", bound=BaseException)
    MU = TypeVar("MU", bound="MaybeUnlock")
    Response = Coroutine[Any, Any, T]

__all__ = ("Route", "HTTPClient")


class Route:
    BASE: ClassVar[str] = "https://discord.com/api/v9"

    def __init__(self, method, path: str, **parameters: Any):

        self.method = method
        self.path: str = path
        url = self.BASE + self.path

        if parameters:
            url = url.format_map(
                {
                    k: _uriquote(v) if isinstance(v, str) else v
                    for k, v in parameters.items()
                }
            )
        self.url: str = url

        # Used for bucket cooldowns
        self.channel_id = parameters.get("channel_id")
        self.guild_id = parameters.get("guild_id")

    @property
    def bucket(self) -> str:
        return f"{self.channel_id}:{self.guild_id}:{self.path}"


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding="utf-8")
    try:
        if response.headers["content-type"] == "application/json":
            return _from_json(text)
    except KeyError:
        # Thanks Cloudflare
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


class HTTPClient:
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        connector: Optional[aiohttp.BaseConnector] = None,
    ):
        self._locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self.__session: aiohttp.ClientSession = MISSING
        self._global_over: asyncio.Event = asyncio.Event()
        self._global_over.set()
        self.loop: asyncio.AbstractEventLoop = (
            asyncio.get_event_loop() if loop is None else loop
        )
        self.connector = connector
        self.token: Optional[str] = None
        user_agent = "DiscordBot (https://github.com/RPD-py/RPD {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            rpd.__version__, sys.version_info, aiohttp.__version__
        )

    def handle_close(self) -> None:
        if self.__session.closed:
            self.__session = aiohttp.ClientSession(
                connector=self.connector,
                ws_response_class=DiscordClientWebSocketResponse,
            )

    async def ws_connect(self, url: str, *, compress: int = 0) -> Any:
        kwargs = {
            "max_msg_size": 0,
            "timeout": 30.0,
            "autoclose": False,
            "headers": {
                "User-Agent": self.user_agent,
            },
            "compress": compress,
        }

        return await self.__session.ws_connect(url, **kwargs)

    async def request(
        self,
        route: Route,
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
            kwargs["data"] = _to_json(kwargs.pop("json"))

        try:
            reason = kwargs.pop("reason")
        except KeyError:
            pass
        else:
            if reason:
                headers["X-Audit-Log-Reason"] = _uriquote(reason, safe="/ ")

        kwargs["headers"] = headers

        if not self._global_over.is_set():
            # wait until the global lock is complete
            await self._global_over.wait()

        response: Optional[aiohttp.ClientResponse] = None
        data: Optional[Union[Dict[str, Any], str]] = None
        await lock.acquire()
        with MaybeUnlock(lock) as maybe_lock:
            for tries in range(5):

                try:
                    async with self.__session.request(
                        method, url, **kwargs
                    ) as response:
                        _log.debug(
                            "%s %s with %s has returned %s",
                            method,
                            url,
                            kwargs.get("data"),
                            response.status,
                        )

                        # even errors have text involved in them so this is safe to call
                        data = await json_or_text(response)

                        # check if we have rate limit header information
                        remaining = response.headers.get("X-Ratelimit-Remaining")

                        # the request was successful so just return the text/json
                        if 300 > response.status >= 200:
                            _log.debug("%s %s has received %s", method, url, data)
                            return data

                        # we are being rate limited
                        if response.status == 429:
                            if not response.headers.get("Via") or isinstance(data, str):
                                # Banned by Cloudflare more than likely.
                                raise HTTPException(response, data)

                            fmt = 'Currently being ratelimited. Retrying in %.2f seconds. Handled with the bucket "%s"'

                            # sleep a bit
                            retry_after: float = data["retry_after"]
                            _log.warning(fmt, retry_after, bucket)

                            # check if it's a global rate limit
                            is_global = data.get("global", False)
                            if is_global:
                                _log.warning(
                                    "Global rate limit has been hit. Retrying in %.2f seconds.",
                                    retry_after,
                                )
                                self._global_over.clear()

                            await asyncio.sleep(retry_after)
                            _log.debug(
                                "Done sleeping for the rate limit. Retrying now..."
                            )

                            # release the global lock now that the
                            # global rate limit has passed
                            if is_global:
                                self._global_over.set()
                                _log.debug("Global rate limit is now over.")

                            continue

                        # we've received a 500, 502, or 504, unconditional retry
                        if response.status in {500, 502, 504}:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        # the usual error cases
                        if response.status == 403:
                            raise Forbidden(response, data)
                        elif response.status == 404:
                            raise NotFound(response, data)
                        elif response.status >= 500:
                            raise ServerError(response, data)
                        else:
                            raise HTTPException(response, data)

                # This is handling exceptions from the request
                except OSError as e:
                    # Connection reset by peer
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise

            if response is not None:
                # We've run out of retries, raise.
                if response.status >= 500:
                    raise ServerError(response, data)

                raise HTTPException(response, data)

            raise RuntimeError("Unreachable code in HTTP handling")

    async def close(self) -> None:
        if self.__session:
            await self.__session.close()

    async def _client_login(self, token: str) -> User:
        self.__session = aiohttp.ClientSession(
            connector=self.connector, ws_response_class=DiscordClientWebSocketResponse
        )
        old_token = self.token
        self.token = token

        try:
            data = await self.request(Route("GET", "/users/@me"))
        except HTTPException as exc:
            self.token = old_token
            if exc.status == 401:
                raise LoginFailure("Invalid credentials were given.") from exc
            raise

        return data

    def _client_logout(self) -> Response[None]:
        return self.request(Route("POST", "/auth/logout"))

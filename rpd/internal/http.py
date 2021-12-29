# Apache-2.0
#
# Copyright 2021 VincentRPS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the LICENSE file for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import asyncio
import logging
import sys
import types
import typing
import weakref
from urllib.parse import quote as _uriquote

import aiohttp

import rpd
from rpd.exceptions import Forbidden, HTTPException, LoginFailure, NotFound, ServerError
from rpd.helpers.missing import MISSING
from rpd.helpers.whichjson import _from_json, _to_json
from rpd.internal.gateway import DiscordClientWebSocketResponse

_log = logging.getLogger(__name__)

if typing.TYPE_CHECKING:
    # from ..data.types.snowflake import Snowflake, SnowflakeList
    from ..data.types.user import User

    T = typing.TypeVar("T")
    BE = typing.TypeVar("BE", bound=BaseException)
    MU = typing.TypeVar("MU", bound="PossiblyUnlock")
    Response = typing.Coroutine[typing.Any, typing.Any, T]

__all__ = ("Route", "HTTPClient")


class Route:
    BASE: typing.ClassVar[str] = f"https://discord.com/api/v9"

    def __init__(self, method, path: str, **parameters: typing.Any):

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

        # bucketing cooldowns
        self.channel_id = parameters.get("channel_id")
        self.guild_id = parameters.get("guild_id")

    # the ratelimit bucket with the parameters.
    @property
    def bucket(self) -> str:
        return f"{self.channel_id}:{self.guild_id}:{self.path}"


async def json_or_text(
    response: aiohttp.ClientResponse,
) -> typing.Union[typing.Dict[str, typing.Any], str]:
    text = await response.text(encoding="utf-8")
    try:
        if response.headers["content-type"] == "application/json":
            return _from_json(text)
    except KeyError:
        # Thanks, Cloudflare
        pass

    return text


class PossiblyUnlock:
    def __init__(self, lock: asyncio.Lock) -> None:
        self.lock: asyncio.Lock = lock
        self._unlock: bool = True

    def __enter__(self: MU) -> MU:
        return self

    def defer(self) -> None:
        self._unlock = False

    def __exit__(
        self,
        exc_type: typing.Optional[typing.Type[BE]],
        exc: typing.Optional[BE],
        traceback: typing.Optional[types.TracebackType],
    ) -> None:
        if self._unlock:
            self.lock.release()


class HTTPClient:
    def __init__(
        self,
        loop: typing.Optional[asyncio.AbstractEventLoop] = None,
        connector: typing.Optional[aiohttp.BaseConnector] = None,
    ):
        self._locks: weakref.WeakValueDictionary = weakref.WeakValueDictionary()
        self.__session: aiohttp.ClientSession = (
            MISSING  # Gets filled in by HTTPClient._client_login()
        )
        self._global_over: asyncio.Event = asyncio.Event()
        self._global_over.set()
        self.loop: asyncio.AbstractEventLoop = (
            asyncio.get_event_loop() if loop is None else loop
        )
        self.connector = connector
        self.token: typing.Optional[str] = None
        user_agent: str = "DiscordBot (https://github.com/RPD-py/RPD {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"
        self.user_agent: str = user_agent.format(
            rpd.__version__, sys.version_info, aiohttp.__version__
        )

    def handle_close(self) -> None:
        if self.__session.closed:
            self.__session = aiohttp.ClientSession(
                connector=self.connector,
                ws_response_class=DiscordClientWebSocketResponse,
            )

    async def ws_connect(self, url: str, *, compress: int = 0) -> typing.Any:
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
        **kwargs: typing.Any,
    ) -> typing.Any:
        bucket = route.bucket
        method = route.method
        url = route.url

        lock = self._locks.get(bucket)
        if lock is None:
            lock = asyncio.Lock()
            if bucket is not None:
                self._locks[bucket] = lock

        # create a basic header.
        headers: typing.Dict[str, str] = {
            "User-Agent": self.user_agent,
        }
        # if the token isn't none add it to the auth header.
        if self.token is not None:
            headers["Authorization"] = "Bot " + self.token
        # checking if it's json
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
            # if global_over lock isn't set wait for it to be.
            await self._global_over.wait()

        response: typing.Optional[aiohttp.ClientResponse] = None # here for more of a conveniance.
        data: typing.Optional[typing.Union[typing.Dict[str, typing.Any], str]] = None
        await lock.acquire()
        with PossiblyUnlock(lock):
            for tries in range(5):

                try:
                    async with self.__session.request(
                        method, url, **kwargs
                    ) as response:
                        _log.debug(
                            "%s %s with %s has returned %s", # weirdly can't get this to be F-stringed? maybe someone else can try.
                            method,
                            url,
                            kwargs.get("data"),
                            response.status,
                        )

                        # even errors have text involved in them so this is safe to call
                        data = await json_or_text(response)

                        # the request was successful, now return the text/json
                        if 300 > response.status >= 200:
                            _log.debug("%s %s has received %s", method, url, data)
                            return data

                        # http ratelimited by discord.
                        if response.status == 429:
                            if not response.headers.get("Via") or isinstance(data, str):
                                # Probably banned by Cloudflare
                                raise HTTPException(response, data)

                            fmt = 'Ratelimit has seemingly been reached, Retrying in %.2f seconds. Handled with the bucket "%s"'  # type: ignore

                            # sleep a bit
                            retry_after: float = data["retry_after"]
                            _log.warning(fmt, retry_after, bucket)

                            # checks if it's a global rate limit
                            is_global = data.get("global", False)
                            if is_global:
                                _log.warning(
                                    f"The Global ratelimit bucket was just tipped. Retrying in {retry_after} seconds."
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

                        # Try if we've gotten any of these
                        if response.status in {500, 502, 504}:
                            await asyncio.sleep(1 + tries * 2)
                            continue

                        # "Normal" Exceptions
                        if response.status == 403:
                            raise Forbidden(response, data)
                        elif response.status == 404:
                            raise NotFound(response, data)
                        elif response.status >= 500:
                            raise ServerError(response, data)
                        else:
                            raise HTTPException(response, data)

                # Hanling exceptions for the request
                except OSError as e:
                    # Connection was reset by peer
                    if tries < 4 and e.errno in (54, 10054):
                        await asyncio.sleep(1 + tries * 2)
                        continue
                    raise

            if response is not None:
                # Raise when retries have run out
                if response.status >= 500:
                    raise ServerError(response, data)

                raise HTTPException(response, data)

            raise RuntimeError("Unreachable code in HTTP handling")

    async def close(self) -> None:
        if self.__session:
            await self.__session.close()

    # Gets the current bot from the gateway
    def get_gateway_bot(self):
        return self.request(Route("GET", "/gateway/bot"))

    # Statically logs-in to discord.
    async def _client_login(self, token: str) -> User:
        self.__session = aiohttp.ClientSession(
            connector=self.connector, ws_response_class=DiscordClientWebSocketResponse
        )
        old_token = self.token
        self.token = token
        if len(self.token) != 59: # Checks if the token given is exactly 59 characters.
            raise LoginFailure("Credentials given are too short to be a bot token.")

        try:
            data = await self.request(Route("GET", "/users/@me"))
        except HTTPException as exc:
            self.token = old_token
            if exc.status == 401:
                raise LoginFailure("Invalid credentials were given.") from exc
            raise

        return data

    # Handles logging out.
    def _client_logout(self):
        return self.request(Route("POST", "/auth/logout"))

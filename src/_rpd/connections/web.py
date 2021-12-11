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
-----------------
This file contains code from speedcord (https://github.com/TAG-Epic/Speedcord)
"""
import asyncio
import logging
from sys import version_info as python_version
from urllib.parse import quote as uriquote

from aiohttp import ClientSession, ClientWebSocketResponse
from aiohttp import __version__ as aiohttp_version

from ...rpd.__init__ import __version__ as version
from ...rpd.exceptions import Forbidden, HTTPException, NotFound, Unauthorized

__all__ = ("Route", "HTTPClient")


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
    def __init__(
        self,
        token,
        *,
        baseuri="https://discord.com/api/v9",
        loop=asyncio.get_event_loop(),
    ):
        self.baseuri = baseuri
        self.token = token
        self.loop = loop
        self.session = ClientSession()

        self.ratelimit_locks = {}
        self.global_lock = asyncio.Event(loop=self.loop)

        # Clear the global lock on start
        self.global_lock.set()

        self.default_headers = {
            "X-RateLimit-Precision": "millisecond",
            "Authorization": f"Bot {self.token}",
            "User-Agent": f"DiscordBot (https://github.com/RPD-py/RPD {version}) "
            f"Python/{python_version[0]}.{python_version[1]} "
            f"aiohttp/{aiohttp_version}",
        }

        self.retry_attempts = 3

    async def create_ws(self, url, *, compression) -> ClientWebSocketResponse:
        if self.session.closed:
            self.session = ClientSession()
        options = {
            "max_msg_size": 0,
            "timeout": 60,
            "autoclose": False,
            "headers": {"User-Agent": self.default_headers["User-Agent"]},
            "compress": compression,
        }
        return await self.session.ws_connect(url, **options)

    async def request(self, route: Route, **kwargs):
        if self.session.closed:
            self.session = ClientSession()
        bucket = route.bucket

        for retry_count in range(self.retry_attempts):
            if not self.global_lock.is_set():
                self.logger.debug("Sleeping for global rate-limit")
                await self.global_lock.wait()

            ratelimit_lock: asyncio.Lock = self.ratelimit_locks.get(bucket, None)
            if ratelimit_lock is None:
                self.ratelimit_locks[bucket] = asyncio.Lock()
                continue

            await ratelimit_lock.acquire()
            with LockManager(ratelimit_lock) as lockmanager:
                # Merge default headers with the users headers, could probably use a if to check if is headers set?
                # Not sure which is optimal for speed
                kwargs["headers"] = {
                    **self.default_headers,
                    **kwargs.get("headers", {}),
                }

                # Format the reason
                try:
                    reason = kwargs.pop("reason")
                except KeyError:
                    pass
                else:
                    if reason:
                        kwargs["headers"]["X-Audit-Log-Reason"] = uriquote(
                            reason, safe="/ "
                        )
                r = await self.session.request(
                    route.method, self.baseuri + route.path, **kwargs
                )
                headers = r.headers

                if r.status == 429:
                    data = await r.json()
                    retry_after = data["retry_after"]
                    if "X-RateLimit-Global" in headers.keys():
                        # Global rate-limited
                        self.global_lock.set()
                        self.logger.warning(
                            "Global rate-limit reached! Please contact discord support to get this increased. "
                            "Trying again in %s Request attempt %s"
                            % (retry_after, retry_count)
                        )
                        await asyncio.sleep(retry_after)
                        self.global_lock.clear()
                        self.logger.debug(
                            f"Trying request again. Request attempt: {retry_count}"
                        )
                        continue
                    else:
                        self.logger.info(
                            "Ratelimit bucket hit! Bucket: %s. Retrying in %s. Request count %s"
                            % (bucket, retry_after, retry_count)
                        )
                        await asyncio.sleep(retry_after)
                        self.logger.debug(
                            f"Trying request again. Request attempt: {retry_count}"
                        )
                        continue
                elif r.status == 401:
                    raise Unauthorized(r)
                elif r.status == 403:
                    raise Forbidden(r, await r.text())
                elif r.status == 404:
                    raise NotFound(r)
                elif r.status >= 300:
                    raise HTTPException(r, await r.text())

                # Check if we are just on the limit but not passed it
                remaining = r.headers.get("X-Ratelimit-Remaining")
                if remaining == "0":
                    retry_after = float(headers.get("X-RateLimit-Reset-After", "0"))
                    self.logger.info(
                        "Rate-limit exceeded! Bucket: %s Retry after: %s"
                        % (bucket, retry_after)
                    )
                    lockmanager.defer()
                    self.loop.call_later(retry_after, ratelimit_lock.release)

                return r

    async def close(self):
        await self.session.close()

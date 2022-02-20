# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
from __future__ import annotations

import asyncio
import json
import logging
import typing
import weakref
from typing import Any, Iterable, Optional, Sequence, TypeVar, Union
from urllib.parse import quote

import aiohttp

from discord import utils
from discord.file import File
from discord.state import ConnectionState
from discord.types.dict import Dict

from ..internal.exceptions import Forbidden, NotFound, RESTError, ServerError

_log = logging.getLogger(__name__)

__all__: typing.List[str] = [
    'RESTClient',
]

PAD = typing.TypeVar('PAD', bound='PadLock')

aiohttp.hdrs.WEBSOCKET = 'websocket'


async def parse_tj(
    response: aiohttp.ClientResponse,
) -> typing.Union[Dict, str]:
    text = await response.text(encoding='utf-8')
    try:
        if response.headers['content-type'] == 'application/json':
            return json.loads(text)  # type: ignore
    except KeyError:
        # could be errored out
        # cause of cloudflare
        pass

    return text


class Route:
    def __init__(self, method: str, endpoint: str, **params: typing.Any):
        self.method = method
        self.endpoint = endpoint

        self.guild_id: typing.Optional[int] = params.get('guild_id')
        self.channel_id: typing.Optional[int] = params.get('channel_id')

        # Webhooks
        self.webhook_id: typing.Optional[int] = params.get('webhook_id')
        self.webhook_token: typing.Optional[str] = params.get('webhook_token')

    @property
    def bucket(self) -> str:
        return f'{self.method}:{self.endpoint}:{self.guild_id}:{self.channel_id}:{self.webhook_id}:{self.webhook_token}'  # type: ignore # noqa: ignore


class PadLock:
    # based off the PadLock of interactions.py & MaybeUnlock of discord.py.
    def __init__(self, lock: asyncio.Lock):
        self.lock: asyncio.Lock = lock
        self.MaybeUnlock: bool = True

    def __enter__(self: PAD) -> PAD:
        return self

    # defers the UnLock.
    def defer(self) -> None:
        self.MaybeUnlock = False

    def __exit__(self, exc_type, exc, traceback) -> None:
        if self.MaybeUnlock:
            self.lock.release()


class RESTClient:
    """Represents a Rest connection with Discord.

    .. versionadded:: 0.3.0

    Attributes
    ----------
    url
        The Discord API URL
    loop
        The current event loop or your own.
    connector
        The base aiohttp connector
    header
        The header sent to discord.
    """

    def __init__(self, *, state=None, proxy=None, proxy_auth=None, version=10):
        self.user_agent = 'DiscordBot (https://github.com/VincentRPS/discord.io)'
        self.header: typing.Dict[str, str] = {'User-Agent': self.user_agent}
        self._locks: weakref.WeakValueDictionary[
            str, asyncio.Lock
        ] = weakref.WeakValueDictionary()
        self._has_global: asyncio.Event = asyncio.Event()
        self._has_global.set()
        self.state = state or ConnectionState()
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self._session: aiohttp.ClientSession = None
        self.url = f'https://discord.com/api/v{version}'

        if version not in (8, 9, 10):
            raise DeprecationWarning(
                'The API Version you are running has been decommissioned, please bump the version.'
            )

    async def send(  # noqa: ignore
        self,
        route: Route,
        files: typing.Optional[typing.Sequence[File]] = None,
        form: typing.Optional[typing.Iterable[Dict]] = None,
        **params: typing.Any,
    ):
        """Sends a request to discord

        .. versionadded:: 0.3.0
        """
        method = route.method
        url = self.url + route.endpoint
        bucket = route.bucket

        self._session = aiohttp.ClientSession()

        lock = self._locks.get(bucket)

        if lock is None:
            lock = asyncio.Lock()
            if bucket is not None:
                self._locks[bucket] = lock

        if self.proxy is not None:
            params['proxy'] = self.proxy

        if self.proxy_auth is not None:
            params['proxy_auth'] = self.proxy_auth

        if 'json' in params:
            self.header['Content-Type'] = 'application/json'  # Only json.
            params['data'] = json.dumps(params.pop('json'))

        if 'token' in params:
            self.header['Authorization'] = 'Bot ' + params.pop('token')

        try:
            reason: str = params.pop('reason')
        except KeyError:
            pass
        else:
            self.header['X-Audit-Log-Reason'] = quote(str(reason), safe='/ ')

        params['headers'] = self.header

        if not self._has_global.is_set():
            await self._has_global.wait()

        await lock.acquire()
        with PadLock(lock) as padl:
            for tries in range(5):

                if files:
                    for f in files:
                        f.reset(seek=tries)

                if form:
                    form_data = aiohttp.FormData()
                    for kwargs in form:
                        form_data.add_field(**kwargs)

                    params['data'] = form_data

                try:
                    async with self._session.request(method, url, **params) as r:

                        d = await parse_tj(r)
                        _log.debug(
                            '< %s %s %s %s', method, url, params.get('data'), bucket
                        )

                        try:
                            remains = r.headers.get('X-RateLimit-Remaining')
                            reset_after = r.headers.get('X-RateLimit-Reset-After')
                        except KeyError:
                            # Some endpoints don't give you these ratelimit headers
                            # and so they will error out.
                            pass

                        if remains == '0' and r.status != 429:
                            # the bucket was depleted
                            padl.defer()
                            _log.debug(
                                'A ratelimit Bucket was depleted. (bucket: %s, retry: %s)',
                                bucket,
                                float(reset_after),
                            )
                            self.state.loop.call_later(float(reset_after), lock.release)

                        if r.status == 429:
                            if not r.headers.get('via') or isinstance(d, str):
                                # handles couldflare bans
                                raise RESTError(d)

                            retry_in: float = d['retry_after']
                            _log.warning(
                                'The Rest Client seems to be ratelimited,'
                                ' Retrying in: %.2f seconds. Handled with the bucket: %s',
                                retry_in,
                                bucket,
                            )

                            is_global = d.get('global', False)

                            if is_global:
                                _log.debug(
                                    'Global ratelimit was hit, retrying in %s', retry_in
                                )
                                self._has_global.clear()

                            await asyncio.sleep(retry_in)
                            _log.debug(
                                'Finished waiting for the ratelimit, now retrying...'
                            )

                            if not is_global:
                                self._has_global.set()
                                _log.debug('Global ratelimit has been depleted.')

                            continue

                        elif r.status == 403:
                            raise Forbidden(d)
                        elif r.status == 404:
                            raise NotFound(d)
                        elif r.status == 500:
                            raise ServerError(d)
                        elif 300 > r.status >= 200:
                            _log.debug('> %s', d)
                            await self._session.close()
                            return d
                        elif r.status == 204:
                            pass
                        else:
                            _log.error(r)

                except Exception as exc:
                    raise RESTError(f'{exc}')

    async def cdn(self, url) -> bytes:
        async with self._session.get(url) as r:
            if r.status == 200:
                return await r.read()
            elif r.status == 404:
                raise NotFound(f'{url} is not found!')
            elif r.status == 403:
                raise Forbidden('You are not allowed to see this image!')
            else:
                raise RESTError(r, 'asset recovery failed.')

    async def close(self) -> None:
        if self._session:
            await self._session.close()  # Closes the session

    async def create_if_not_exists(self):
        if self._session is None or utils.MISSING:
            self._session = aiohttp.ClientSession()
        else:
            pass

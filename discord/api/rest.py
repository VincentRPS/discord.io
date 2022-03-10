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
import time
from urllib.parse import quote

import aiohttp

from discord import utils
from discord.file import File
from discord.state import ConnectionState, HTTPStream
from discord.types.dict import Dict

from ..internal.exceptions import Forbidden, NotFound, RESTError, ServerError

_log = logging.getLogger(__name__)

__all__: typing.List[str] = [
    'RESTClient',
]

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
        self.params = params

        self.guild_id: typing.Optional[int] = params.get('guild_id')
        self.channel_id: typing.Optional[int] = params.get('channel_id')

        # Webhooks
        self.webhook_id: typing.Optional[int] = params.get('webhook_id')
        self.webhook_token: typing.Optional[str] = params.get('webhook_token')

    @property
    def bucket(self) -> str:
        return f'{self.method}:{self.endpoint}:{self.guild_id}:{self.channel_id}:{self.webhook_id}:{self.webhook_token}'  # type: ignore # noqa: ignore

class Lock:
    def __init__(self, bucket: str):
        self.bucket = bucket
        self.pending_release: typing.List[asyncio.Future[None]] = []
        self.reserved = 0
        self.left = None
        self.left_after = None
        self.left_pending = None
        self.limit = 0
        self.reset_at: float = None
        self.loop = asyncio.get_event_loop()

    def request(self, left: int):
        self.left = left
        self._left = left
        self.left_after = self.left - 1
        self.left_pending = self.left - self.reserved

    @property
    def _left(self):
        return self.left
    
    @_left.setter
    def _left(self, i: int):
        self.limit = i
        if i == 0:
            sleep = self.reset_at - time.time()
            self.loop.call_later(sleep, self.release)

    def release(self):
        self.left = self.limit
        for _ in range(self.left_pending):
            try:
                future = self.pending_release.pop(0)
            except IndexError:
                break
            future.set_result(None)

    async def __aenter__(self) -> Lock:
        if self.left == None:
            return self
        if self.left == 0 or self.left_pending <= 0:
            fut = asyncio.Future()
            self.pending_release.append(fut)
            await fut
        self.reserved += 1
        return self

    async def __aexit__(self, *_):
        try:
            if self.left_after - len(self.pending_release) != 0:
                self.release()
        except TypeError:
            pass

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
        self.locks = {}
        self.specific_limits: typing.Dict[str, int] = {'/channels': 500}

        if version < 8:
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
        url = self.url + route.endpoint.format_map(
            {k: quote(v) if isinstance(v, str) else v for k, v in route.params.items()}
        )
        bucket = route.bucket

        self._session = aiohttp.ClientSession()

        _bucket: Lock = self.locks.get(route.endpoint)

        if _bucket == None:
            _bucket = Lock(route.endpoint)
            self.locks[route.endpoint] = _bucket

        for key, limit in self.specific_limits.items():
            if route.endpoint.endswith(key):
                _bucket.limit = limit

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

        for tries in range(5):
            async with _bucket as buck:
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

                        limit = r.headers.get('X-RateLimit-Limit')
                        
                        if limit == None:
                            buck.limit = None
                        else:
                            buck.limit = int(limit)

                        if remains:
                            buck.request(int(remains))

                        reset = r.headers.get('X-RateLimit-Reset')

                        if reset:
                            buck.reset_at = float(reset)
                        else:
                            buck.reset_at = None

                        stream = HTTPStream(
                            {
                                'route': url,
                                'bucket': route.bucket,
                                'ratelimit_bucket': r.headers.get(
                                    'X-RateLimit-Bucket', 
                                    None
                                ),
                                'data': d,
                                'global': d.get('global', False) if isinstance(d, dict) else False,
                                'limit': r.headers.get('X-RateLimit-Limit', None)
                            }
                        )
    
                        self.state.http_streams.append(stream)

                        _log.debug(f'Created stream for {route.endpoint}: {stream}')

                        if r.status == 429:
                            if not r.headers.get('via') or isinstance(d, str):
                                # handles couldflare bans
                                raise RESTError(d)

                            continue

                        elif r.status == 403:
                            raise Forbidden(d)
                        elif r.status == 404:
                            raise NotFound(d)
                        elif r.status == 500:
                            raise ServerError(d)
                        elif 300 > r.status >= 200:
                            _log.debug('> %s (bucket: %s)', d, r.headers.get('X-RateLimit-Bucket', None))
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

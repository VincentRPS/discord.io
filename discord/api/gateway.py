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
"""Implementation of the Discord Gateway."""

from __future__ import annotations

import asyncio
import json
import logging
import platform
import zlib
from random import random
from time import perf_counter, time
from typing import Any, Coroutine, List

import aiohttp

from discord import utils
from discord.events import catalog
from discord.snowflake import Snowflakeish
from discord.types.dict import Dict

from ..http import RESTFactory
from ..internal.dispatcher import Dispatcher
from ..state import ConnectionState

ZLIB_SUFFIX = b'\x00\x00\xff\xff'
_log = logging.getLogger(__name__)
url_extension = '?v=10&encoding=json&compress=zlib-stream'


class Shard:
    """Represents a Discord Shard.

    Parameters
    ----------
    state
        The :class:`ConnectionState` cache to use.
    dispatcher
        The :class:`Dispatcher` to use.
    shard_id: :class:`int`
        The shard number.
    url: :class:`str`
        The URL to use.
    mobile :class:`bool`
        If to have a mobile presence or not.

    Attributes
    ----------
    buffer
        An array of bytes which buffers the connection.
    remaining
        The amount remaining
    per
        The times per
    window
        The window
    max
        The max
    inflator
        The inflator for this shard.
    """

    def __init__(
        self,
        state: ConnectionState,
        dispatcher: Dispatcher,
        shard_id: int,
        url: str,
        mobile: bool = False,
    ):
        self.remaining = 110
        self.per = 60.0
        self.window = 0.0
        self.max = 110
        self.state = state
        self.url = url
        self.mobile = mobile
        self.dis = dispatcher
        self.inflator = zlib.decompressobj()
        self.shard_id = shard_id
        self.buffer = bytearray()
        self.last_recv = perf_counter()
        self.last_send = perf_counter()
        self.last_ack = perf_counter()
        self._session_id: int = None
        self._ratelimit_lock: asyncio.Lock = asyncio.Lock()
        self.ws: aiohttp.ClientWebSocketResponse = None
        self.latency: float = float('nan')
        self.ready: asyncio.Event =  asyncio.Event()
        self.state.loop.create_task(self.enter())

    async def enter(self):
        self._session = aiohttp.ClientSession()

    async def connect(self, token: str) -> None:
        """Connects to the url specified, with the token

        Parameters
        ----------
        token
            Your bot token.

        Attributes
        ----------
        _session
            The aiohttp ClientSession
        ws
            The WebSocket connection.
        """
        self.ws = await self._session.ws_connect(self.url)

        self.token = token
        if self._session_id is None:
            await self.identify()
            self.state.loop.create_task(self.recv())
            self.state.loop.create_task(self.check_connection())
        else:
            await self.resume()
            _log.debug('Reconnected to the Gateway')

    @property
    def is_ratelimited(self) -> bool:
        """Returns a True if this shard is ratelimited
        and False if it isn't
        """
        now = time()
        if now > self.window + self.per:
            return False
        return self.remaining == 0

    def delay(self) -> float:
        """A float showing how long we should delay until retrying."""
        now = time()

        if now > self.window + self.per:
            self.remaining = self.max

        if self.remaining == self.max:
            self.window = now

        if self.remaining == 0:
            return self.per - (now - self.window)

        self.remaining -= 1
        if self.remaining == 0:
            self.window = now

        return 0.0

    async def block(self) -> None:
        """A function to block the connection tempoarily"""
        async with self._ratelimit_lock:
            delay = self.delay()
            if delay:
                _log.warning(
                    'Shard %s was ratelimited, waiting %.2f seconds.',
                    self.shard_id,
                    delay,
                )
                await asyncio.sleep(delay)

    async def check_connection(self):
        await asyncio.sleep(20)
        if self.last_recv + 60.0 < perf_counter():
            _log.warning(
                f'Shard {self.shard_id} has stopped receiving from the gateway, reconnecting'
            )
            await self.ws.close(code=4000)
            await self.closed(4000)
        elif self.latency > 10:
            _log.warning(f'Shard {self.shard_id} is behind by {self.latency}')
        self.state.loop.create_task(self.check_connection())

    async def send(self, data: Dict) -> None:
        """Send a request to the Gateway via the shard

        Parameters
        ----------
        data :class:`Dict`
            The data to send
        """
        self.last_send = perf_counter()
        _log.debug('< %s', data)
        raw_payload = json.dumps(data)

        if isinstance(raw_payload, str):
            payload = raw_payload.encode('utf-8')

        await self.ws.send_bytes(payload)

    async def recv(self) -> None:
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.BINARY:
                self.latency = self.last_ack - self.last_send
                self.buffer.extend(msg.data)
                try:
                    raw = self.inflator.decompress(self.buffer).decode('utf-8')
                except:
                    # probably corrupted data
                    self.buffer = bytearray()
                    return
                if len(msg.data) < 4 or msg.data[-4:] != ZLIB_SUFFIX:
                    raise RuntimeError
                self.buffer = bytearray()  # clean buffer
                data = json.loads(raw)
                _log.debug('> %s', data)

                self._seq = data['s']
                self.dis.dispatch('RAW_SOCKET_RECEIVE')

                self.last_recv = perf_counter()

                if data['op'] == 0:
                    if (
                        data['t'] == 'READY'
                    ):  # only fire up getting the session_id on a ready event.
                        await self._ready(data)
                        self.dis.dispatch('READY')
                    else:
                        catalog.Cataloger(data, self.dis, self.state)
                elif data['op'] == 9:
                    await self.ws.close(code=4000)
                    await self.closed(4000)
                elif data['op'] == 10:
                    await self.hello(data)
                elif data['op'] == 11:
                    self.last_ack = perf_counter()
                    _log.debug('> %s', data)
                else:
                    self.dis.dispatch(data['op'], data)

            else:
                raise RuntimeError

        code = self.ws.close_code
        if code is None:
            return
        else:
            await self.closed(code)

    async def closed(self, code: int) -> None:
        _log.error(f'Shard {self.shard_id} closed with code {code}')
        if code == 4000:
            pass

        elif code == 4001:
            pass

        elif code == 4002:
            # just ignore it.
            pass

        elif code == 4003:
            # something weird happened, just ignore it.
            pass

        elif code == 4004:
            raise

        elif code == 4005:
            # pass!
            pass

        elif code == 4007:
            # pass and make a new session
            pass

        elif code == 4008:
            # retry!
            pass

        elif code == 4009:
            # try to resume.
            await self.resume()
            return

        elif code == 4010:
            raise  # this doesn't really happen, unless you are dumb

        elif code == 4011:
            # just tell the owner to shard!
            raise

        elif code == 4012:
            # most likely a old lib version.
            raise

        elif code == 4013:
            raise

        elif code == 4014:
            raise

        await self.connect(token=self.token)

    async def heartbeat(self, interval: float) -> None:
        if self.is_ratelimited:
            await self.block()
        if not self.ws.closed:
            await self.send({'op': 1, 'd': self._seq})
            await asyncio.sleep(interval)
            self.state.loop.create_task(self.heartbeat(interval))

    async def close(self, code: int = 4000) -> None:
        if self.ws:
            await self.ws.close(code=code)
        self.buffer.clear()

    async def hello(self, data: Dict) -> None:
        interval = data['d']['heartbeat_interval'] / 1000
        init = interval * random()
        await asyncio.sleep(init)
        self.state.loop.create_task(self.heartbeat(interval))

    async def _ready(self, data: Dict) -> None:
        self._session_id = data['d']['session_id']
        self.state._ready.set()
        self.ready.set()

    async def identify(self) -> None:
        await self.send(
            {
                'op': 2,
                'd': {
                    'token': self.token,
                    'intents': self.state._bot_intents,
                    'properties': {
                        '$os': platform.system(),
                        '$browser': 'discord.io'
                        if self.mobile is False
                        else 'Discord iOS',
                        '$device': 'discord.io',
                    },
                    'shard': (self.shard_id, self.state.shard_count),
                    'v': 9,
                    'compress': True,
                },
            }
        )

    async def resume(self) -> None:
        await self.send(
            {
                'op': 6,
                'd': {
                    'token': self.token,
                    'session_id': self._session_id,
                    'seq': self._seq,
                },
            }
        )


class Gateway:
    """Represents a Gateway connection with Discord.

    Parameters
    ----------
    state
        The :class:`ConnectionState` to use.
    dispatcher
        The :class:`Dispatcher` to use.
    factory
        The :class:`RESTFactory` to use.
    mobile
        If your bot should have a mobile presence or not.
    """

    def __init__(
        self,
        state: ConnectionState,
        dispatcher: Dispatcher,
        factory: RESTFactory,
        mobile: bool = False,
    ):
        self._s = state
        self.mobile = mobile
        self.count = self._s.shard_count
        self._d = dispatcher
        self._f = factory
        self.shards: List[Shard] = []

    @utils.copy_doc(Shard.connect)
    async def connect(self, token: str) -> None:
        r = await self._f.get_gateway_bot()
        if self.count is None:
            shds = r['shards']
            self._s.shard_count = shds
        else:
            shds = self.count

        for shard in range(shds):
            s = Shard(
                self._s,
                self._d,
                shard,
                mobile=self.mobile,
                url=r['url'] + url_extension,
            )
            self._s.loop.create_task(s.connect(token))
            while not s.ready.is_set():
                await s.ready.wait()
            self.shards.append(s)
            _log.info('Shard %s has connected to Discord', shard)

    @utils.copy_doc(Shard.send)
    async def send(self, payload: Dict, shard=None) -> Coroutine[Any, Any, None]:
        if shard == None:
            for s in self.shards:
                await s.send(payload)
        else:
            await self.shards[shard].send(payload)

    async def _chunk_members(self):
        await asyncio.sleep(20)
        for guild in self._s.guilds._cache.values():
            shard_id = (int(guild['id']) >> 22) % self._s.shard_count
            await self.shards[shard_id].send(
                {'op': 8, 'd': {'guild_id': guild['id'], 'query': '', 'limit': 0}}
            )

    async def voice_state(
        self, guild: int, channel: Snowflakeish, mute: bool, deaf: bool
    ) -> Coroutine[Any, Any, None]:
        json = {
            'op': 4,
            'd': {
                'guild_id': guild,
                'channel_id': channel,
                'self_mute': mute,
                'self_deaf': deaf,
            },
        }
        shard_id = (int(guild) >> 22) % self._s.shard_count
        await self.shards[shard_id].send(json)

    @property
    def latency(self) -> float:
        lat: float = float(0)
        for shard in self.shards:
            lat += shard.latency

        return lat

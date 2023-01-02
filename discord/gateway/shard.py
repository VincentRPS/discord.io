# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

import asyncio
import json
import logging
import zlib
from platform import system
from random import random
from typing import Any

import aiohttp
from aiohttp import ClientSession, WSMsgType

from .concurrer import Concurrer
from .state import GatewayState

ZLIB_SUFFIX = b'\x00\x00\xff\xff'
url = '{base}/?v=10&encoding=json&compress=zlib-stream'
_log = logging.getLogger(__name__)
RESUMABLE: list[int] = [
    4000,
    4001,
    4002,
    4003,
    4005,
    4007,
    4008,
    4009,
]
__all__ = ['Shard']


class Shard:
    def __init__(
        self,
        token: str,
        shard_id: int,
        active_shards: int,
        session: ClientSession,
        state: GatewayState,
        proxy: str | None = None,
        proxy_auth: aiohttp.BasicAuth | None = None,
    ) -> None:
        self.token = token
        self.id = shard_id
        self._active_shards = active_shards
        self._session = session
        self._state = state
        self._proxy = proxy
        self._proxy_auth = proxy_auth

        # non-user made attributes
        self._send_concurrer = Concurrer(110, 60)
        self._inflator: zlib._Decompress | None = None
        self._sequence: int | None = None
        self._ws: aiohttp.ClientWebSocketResponse | None = None
        self._resume_gateway_url: str | None = None
        self._heartbeat_interval: float | None = None
        self._hb_received: asyncio.Future[None] | None = None
        self._receive_task: asyncio.Task[None] | None = None
        self._connection_alive: asyncio.Future[None] = asyncio.Future()
        self._hello_received: asyncio.Future[None] | None = None
        self._hb_task: asyncio.Task[None] | None = None
        self._session_id: str | None = None

    async def start(self, resume: bool = False) -> None:
        self._hello_received = asyncio.Future()
        self._inflator = zlib.decompressobj()

        try:
            _log.debug(f'shard:{self.id}: attempting to establish a connection to the Gateway')
            async with self._state.concurrency:
                self._ws = await self._session.ws_connect(
                    url=url.format(base=(self._resume_gateway_url if resume else 'wss://gateway.discord.gg')),
                    proxy=self._proxy,
                    proxy_auth=self._proxy_auth,
                )
            _log.debug(f'shard:{self.id}: successfully established a connection to the Gateway')
        except (aiohttp.ClientConnectionError, aiohttp.ClientConnectorError):
            _log.error(f'shard:{self.id}: failed to establish a connection, retrying in 30 seconds')

            await asyncio.sleep(30)
            asyncio.create_task(self.start(resume=resume))
            return

        self._receive_task = asyncio.create_task(self._receive())

        if not resume:
            await self.identify()

    async def send(self, data: dict[str, Any]) -> None:
        if self._ws is None:
            raise RuntimeError('WebSocket connection must be established first')

        async with self._send_concurrer:
            d = json.dumps(data)
            _log.debug(f'shard:{self.id}: sending a message to socket: {d}')
            await self._ws.send_str(d)

    async def _receive(self) -> None:
        if self._ws is None or self._inflator is None:
            return

        async for message in self._ws:
            if message.type == WSMsgType.CLOSED:
                break
            elif message.type == WSMsgType.BINARY:
                if len(message.data) < 4 or message.data[-4:] != ZLIB_SUFFIX:
                    continue

                try:
                    text = self._inflator.decompress(message.data).decode()
                except (UnicodeDecodeError, zlib.error):
                    _log.error(f'shard:{self.id}: failed to decode gateway message')
                    continue

                _log.debug(f'shard:{self.id}: received message {text}')

                data = json.loads(text)

                sequence = data.get('s', str)
                op = data.get('op')
                t = data.get('t')
                d = data.get('d')

                if sequence != str:
                    self._sequence = sequence

                if op == 0:
                    asyncio.create_task(self._process_event(t, d))
                elif op == 1:
                    await self._ws.send_str(json.dumps({'op': 1, 'd': self._sequence}))
                elif op == 10:
                    self._heartbeat_interval = d['heartbeat_interval'] / 1000

                    asyncio.create_task(self._start_heartbeat(jitter=True))
                    if self._hello_received:
                        self._hello_received.set_result(None)
                elif op == 11:
                    if self._hb_received and not self._hb_received.done():
                        self._hb_received.set_result(None)

                        self._hb_task = asyncio.create_task(self._start_heartbeat())
                elif op == 7:
                    await self._ws.close(code=1002)
                    await self.start(resume=True)
                    return
                elif op == 9:
                    await self._ws.close()
                    await self.start()
                    return

        if self._ws.closed and self._ws.close_code:
            await self._closed(self._ws.close_code)

    async def _start_heartbeat(self, jitter: bool = False) -> None:
        if self._heartbeat_interval is None or self._ws is None or self._receive_task is None:
            return

        if jitter:
            await asyncio.sleep(self._heartbeat_interval * random())
        else:
            await asyncio.sleep(self._heartbeat_interval)

        self._hb_received = asyncio.Future()

        _log.debug(f'shard:{self.id}: sending heartbeat')

        try:
            await self._ws.send_str(json.dumps({'op': 1, 'd': self._sequence}))
        except ConnectionResetError:
            _log.debug(f'shard:{self.id}: failed to send heartbeat due a connection reset, reconnecting...')
            self._receive_task.cancel()
            if not self._ws.closed:
                await self._ws.close(code=1008)
            await self.start(bool(self._resume_gateway_url))
            return

        try:
            await asyncio.wait_for(self._hb_received, 5)
        except asyncio.TimeoutError:
            _log.debug(f'shard:{self.id}: heartbeat waiting timed out, reconnecting...')
            self._receive_task.cancel()
            if not self._ws.closed:
                await self._ws.close(code=1008)
            await self.start(bool(self._resume_gateway_url))

    async def _process_event(self, type: str, data: dict[str, Any]) -> None:
        if type == 'READY':
            self._session_id = data['session_id']
            self._resume_gateway_url = data['resume_gateway_url']
            self._state.user_ready = data['user']

        asyncio.create_task(self._state.subscriptor.dispatch(type, data))

    async def identify(self) -> None:
        await self.send(
            {
                'op': 2,
                'd': {
                    'token': self.token,
                    'properties': {
                        'os': system(),
                        'browser': 'discord.io',
                        'device': 'discord.io',
                    },
                    'compress': True,
                    'large_threshold': 250,
                    'shard': (self.id, self._active_shards),
                    'intents': self._state.intents,
                },
            }
        )

    async def send_resume(self) -> None:
        await self.send(
            {
                'op': 6,
                'd': {
                    'token': self.token,
                    'session_id': self._session_id,
                    'seq': self._sequence,
                },
            }
        )

    async def _closed(self, code: int) -> None:
        _log.debug(f'shard:{self.id}: closed with code {code}')
        if self._hb_task and not self._hb_task.done():
            self._hb_task.cancel()
        if code in RESUMABLE:
            await self.start(True)
        else:
            if code == 4004:
                raise RuntimeError('Authentication used in gateway is invalid')
            elif code == 4011:
                raise RuntimeError('Discord is requiring you shard your bot')
            elif code == 4014:
                raise RuntimeError("You aren't allowed to carry a privileged intent wanted")

            if code > 4000 or code == 4000:
                await self._handle_death()
            else:
                # the connection most likely died
                await self.start(resume=True)

    async def _handle_death(self) -> None:
        await self.start(False)

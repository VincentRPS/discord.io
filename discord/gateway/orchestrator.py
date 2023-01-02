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
import logging

import aiohttp

from .shard import Shard
from .state import GatewayState

__all__ = ['Orchestrator']

_log = logging.getLogger(__name__)


class Orchestrator:
    def __init__(
        self,
        token: str,
        state: GatewayState,
        shards: int | list[int],
        active_shards: int | None = None,
        proxy: str | None = None,
        proxy_auth: aiohttp.BasicAuth | None = None,
    ) -> None:
        self.token = token
        self.shards: list[Shard] = []

        if isinstance(shards, int):
            shards = list(range(shards))

        self._shards: list[int] = shards
        self._state = state
        self._session = aiohttp.ClientSession()

        if active_shards is None:
            self.active_shards = max(self._shards)
        else:
            self.active_shards = active_shards

        self.proxy = proxy
        self.proxy_auth = proxy_auth

    async def orchestrate(self) -> None:
        t = []
        for shard_id in self._shards:
            shard = Shard(self.token, shard_id, self.active_shards, self._session, self._state, self.proxy, self.proxy_auth)

            t.append(shard.start())

            self.shards.append(shard)

        await asyncio.gather(*t)

    async def shutdown(self) -> None:
        for shard in self.shards:
            if not shard._receive_task or not shard._hb_task or not shard._ws:
                return

            _log.info(f'shutting down shard {shard.id}')

            shard._receive_task.cancel()
            shard._hb_task.cancel()
            await shard._ws.close()
            self.shards.remove(shard)

            _log.info(f'successfully shutdown shard {shard.id}')

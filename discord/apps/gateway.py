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
import inspect
import logging
from datetime import datetime, timedelta
from typing import Callable, Coroutine, Type, TypeVar

from aiohttp import BasicAuth

from ..api import HTTPClient
from ..api.route import Route
from ..events.base import BaseEvent, GatewayEvent
from ..gateway import GatewayState, Orchestrator, concurrer
from ..interface import print_banner, start_logging
from ..internal.subscriptor import AsyncFunc, Subscription
from ..traits import BaseApp
from .api import APIApp

_log = logging.getLogger(__name__)

__all__ = ['GatewayApp']


T = TypeVar('T')


class GatewayApp(BaseApp, APIApp):
    def __init__(
        self,
        intents: int,
        log_config: dict | int | str | None = logging.INFO,
        shards: int | list[int] = 1,
        active_shards: int = 1,
        proxy: str | None = None,
        proxy_auth: BasicAuth | None = None,
    ) -> None:
        self._log_config = log_config
        self._intents = intents
        self._state = GatewayState(self, (0, 0), self._intents)

        if isinstance(shards, int):
            shards = list(range(shards))

        self.shards = shards
        self._active_shards = active_shards
        self._proxy = proxy
        self._proxy_auth = proxy_auth
        self._left: datetime | None = None
        self._num: int | None = None

    async def _fill_concurrer(self) -> None:
        concurrency = await self._http.request('GET', Route('/gateway/bot'))

        if concurrency is None:
            return

        ssl = concurrency['session_start_limit']
        self._state.concurrency = concurrer.Concurrer(ssl['max_concurrency'], 5)
        self._num = ssl['remaining']
        self._left = datetime.now() + timedelta(milliseconds=ssl['reset_after'])

    async def start(self, token: str) -> None:
        self._http = HTTPClient(token)
        self._state.loop_activated()
        await self._fill_concurrer()

        print_banner()
        start_logging(self._log_config)
        if self._num is not None and self._left is not None:
            _log.info(
                f'sessions left remains at {self._num}, minus what will be used by the orchestrator you will have {self._num - len(self.shards)} remaining.'
            )
            _log.info(f'session count will reset in {self._left.hour} hour(s) and {self._left.minute} minute(s)')

        _log.info('attempting initiation of orchestrator')
        self.orchestrator = Orchestrator(
            token,
            self._state,
            self.shards,
            active_shards=self._active_shards,
            proxy=self._proxy,
            proxy_auth=self._proxy_auth,
        )
        await self.orchestrator.orchestrate()
        _log.info('asynchronous orchestration phase completed')
        await self._block_until_complete()

    async def _block_until_complete(self) -> None:
        try:
            await asyncio.Future()
        except (asyncio.CancelledError, KeyboardInterrupt):
            while True:
                _log.info('got interrupted, shutting down')
                await self._http.close_session()
                _log.info('closed http session')
                await self.orchestrator.shutdown()
                await self.orchestrator._session.close()
                _log.info('successfully shutdown orchestrator')
                return

    def run(self, token: str, asyncio_debug: bool = False) -> None:
        asyncio.run(self.start(token), debug=asyncio_debug)

    def subscribe(self, event: Type[BaseEvent] | None = None) -> Callable[..., AsyncFunc]:
        def wrapper(func: AsyncFunc) -> AsyncFunc:
            if event is None:
                sig = inspect.signature(func)
                try:
                    event_param = sig.parameters['event']
                except KeyError:
                    raise RuntimeError('event field is required for unspecified subscribings')

                if event_param.annotation == inspect.Parameter.empty:
                    raise RuntimeError('annotation must be provided to subscribe to an event')

                if event_param.annotation.__base__ != BaseEvent and event_param.annotation.__base__ != GatewayEvent:
                    raise RuntimeError('annotation must be a BaseEvent')

                sub_event: Type[BaseEvent] = event_param.annotation
            else:
                sub_event = event

            if sub_event._type is None:
                raise RuntimeError('Event must have a type')

            self._state.subscriptor.add_subscription(Subscription(sub_event, type=sub_event._type, callback=func))

            return func

        return wrapper

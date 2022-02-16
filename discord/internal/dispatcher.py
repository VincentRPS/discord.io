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
"""
Dispatches raw Opcode events to Event classes.
"""

import asyncio
import logging
from typing import Any, Callable, Coroutine, List, Optional, TypeVar

from discord.state import ConnectionState

__all__ = (
    'Dispatcher',
)
_log = logging.getLogger(__name__)
CoroT = TypeVar('CoroT', bound=Callable[..., Coroutine[Any, Any, Any]])
T = TypeVar('T')
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]

class Dispatcher:
    """Dispatches raw and non-raw events

    Parameters
    ----------
    state
        The :class:`ConnectionState`
    """

    def __init__(self, state: ConnectionState):
        self.state = state

    async def run(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        cog,
        one_shot: bool,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        if one_shot:
            delattr(self, name)
        try:
            if cog:
                await coro(cog, *args, **kwargs)
            else:
                await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

    def scheduler(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        cog: Any,
        one_shot: bool,
        *args: Any,
        **kwargs: Any,
    ) -> asyncio.Task:
        wrap = self.run(coro, name, cog, one_shot, *args, **kwargs)
        return self.state.loop.create_task(wrap, name=f'discord.io: {name}')

    def dispatch(self, name: str, *args, **kwargs) -> None:
        fake_name = str(name.lower())
        real_name = 'on_' + str(fake_name)
        _log.debug('Dispatching event: %s', real_name)

        listeners = self.state.listeners.get(real_name)
        if listeners:
            removed = []
            for i, (future, condition) in enumerate(listeners):
                if future.cancelled():
                    removed.append(i)
                    continue

                try:
                    result = condition(*args)
                except Exception as exc:
                    future.set_exception(exc)
                    removed.append(i)
                else:
                    if result:
                        if len(args) == 0:
                            future.set_result(None)
                        elif len(args) == 1:
                            future.set_result(args[0])
                        else:
                            future.set_result(args)
                        removed.append(i)

            if len(removed) == len(listeners):
                self.state.listeners.pop(real_name)
            else:
                for res in reversed(listeners):
                    removed.append(res)

        try:
            coro = getattr(self, real_name)
        except AttributeError:
            ...
        else:
            try:
                one_cycle = coro['one_cycle']
            except KeyError:
                one_cycle = False
            self.scheduler(
                coro['main'], real_name, coro['cog'], one_cycle, *args, **kwargs
            )

    def listen(self, coro: Coro) -> Coro:
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError('Function is not a coroutine.')

        setattr(self, coro.__name__, {'main': coro, 'cog': None, 'one_cycle': False})
        _log.info(f'{coro.__name__} has been registered!')

    def wait_for(self, event: str):
        def decorator(func: CoroFunc):
            self.add_listener(func, name=event, one_cycle=True)
            return func

        return decorator

    def add_listener(
        self, func: CoroFunc, name: Optional[str] = None, cog=None, one_cycle=False
    ):
        name = func.__name__ if name is None else name

        if not asyncio.iscoroutinefunction(func):
            raise TypeError('Function is not a coroutine.')

        setattr(self, name, {'main': func, 'cog': cog, 'one_cycle': one_cycle})

        if name.startswith('on_raw'):
            _log.debug(f'{name} added as a listener!')
        else:
            _log.info(f'{name} added as a listener!')

    def remove_listener(self, func: CoroFunc, name: Optional[str] = None):
        name = func.__name__ if name is None else name

        if name in self.state.listeners:
            try:
                self.state.listeners[name].remove(func)
            except ValueError:
                pass

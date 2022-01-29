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
Dispatches raw OpCode events to Event classes.
"""

import asyncio
import logging
from typing import Any, Callable, Coroutine, TypeVar

from rpd.state import ConnectionState

_log = logging.getLogger(__name__)
Coro = TypeVar("Coro", bound=Callable[..., Coroutine[Any, Any, Any]])


class Dispatcher:
    def __init__(self, state: ConnectionState):
        self.state = state

    async def run(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

    def scheduler(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        *args: Any,
        **kwargs: Any,
    ) -> asyncio.Task:
        wrap = self.run(coro, name, *args, **kwargs)
        return asyncio.create_task(wrap, name=f"RPD: {name}")

    def dispatch(self, name: str, *args, **kwargs) -> None:
        fake_name = str(name.lower())
        real_name = "on_" + str(fake_name)
        _log.debug("Dispatching event: %s", name)

        listeners = self.state.listeners.get(name)
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
                self.state.listeners.pop(name)
            else:
                for res in reversed(listeners):
                    removed.append(res)

        try:
            coro = getattr(self, real_name)
        except AttributeError:
            ...
        else:
            self.scheduler(coro, name, *args, **kwargs)

    def listen(self, coro: Coro) -> Coro:
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("Function is not a coroutine.")

        setattr(self, coro.__name__, coro)
        _log.debug(f"{coro.__name__} has been registered!")

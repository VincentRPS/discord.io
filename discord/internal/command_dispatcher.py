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
Dispatches Commands.
"""

import asyncio
import logging
from typing import Any, Callable, Coroutine, Optional, TypeVar

from discord.state import ConnectionState

_log = logging.getLogger(__name__)
CoroT = TypeVar("CoroT", bound=Callable[..., Coroutine[Any, Any, Any]])
T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]


class CommandDispatcher:
    def __init__(self, state: ConnectionState):
        self.state = state
        self.commands = []
        self.application_commands = []

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
        return self.state.loop.create_task(wrap, name=f"discord.io: {name}")

    def dispatch(self, name: str, application: bool = False, *args, **kwargs) -> None:
        _log.debug("Dispatching Command: %s", name)

        if not application:
            listeners = self.state.prefixed_commands.get(name)
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
                self.state.prefixed_commands.pop(name)
            else:
                for res in reversed(listeners):
                    removed.append(res)
        else:
            listeners = self.state.application_commands.get(name)
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
                self.state.application_commands.pop(name)
            else:
                for res in reversed(listeners):
                    removed.append(res)

        try:
            coro = getattr(self, name)
        except AttributeError:
            _log.warning(f"Failed to get command {name}")
        else:
            self.scheduler(coro, name, *args, **kwargs)

    def command(self, coro: Coro) -> Coro:
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError("Function is not a coroutine.")

        setattr(self, coro.__name__, coro)
        _log.info(f"{coro.__name__} has been registered!")

    def add_command(
        self, func: CoroFunc, application: bool = False, name: Optional[str] = None
    ):
        name = func.__name__ if name is None else name

        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Function is not a coroutine.")

        if not application:
            self.commands.append(name)
        else:
            self.application_commands.append(name)

        _log.info(f"command {name} has been registered.")

    def remove_command(
        self, func: CoroFunc, name: Optional[str] = None, application: bool = False
    ):
        name = func.__name__ if name is None else name

        if name in self.commands:
            self.commands.remove(name)

        if application:
            if name in self.state.application_commands.items():
                try:
                    self.state.application_commands[name].remove(func)
                except ValueError:
                    pass
        else:
            if name in self.state.prefixed_commands.items():
                try:
                    self.state.prefixed_commands[name].remove(func)
                except ValueError:
                    pass
            elif name in self.commands:
                self.commands.remove(name)

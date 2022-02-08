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
import asyncio
import functools
import inspect
from typing import Any, Callable, Generic, ParamSpec, Type, TypeVar

from ...state import ConnectionState
from ..cogs import Cog
from .context import Context

T = TypeVar("T")
CogT = TypeVar("CogT", bound="Cog")
P = ParamSpec("P")
CommandT = TypeVar("CommandT", bound="Command")


def func_unwrap(func: Callable):
    while True:
        if hasattr(func, "__wrapped__"):
            func = func.__wrapped__
        elif isinstance(func, functools.partial):
            func = func.func
        else:
            return func


def get_sig_params(func, globals) -> dict:
    signature = inspect.signature(func)
    params = {}

    for name, param in signature.parameters.items():
        annotation = param.annotation
        if annotation is param.empty:
            params[name] = param
        elif annotation is None:
            params[name] = param.replace(annotation=type(None))

    return params


class Command(Generic[CogT, P, T]):
    def __new__(cls: Type[CommandT], *args: Any, **kwargs: Any) -> CommandT:
        self = super().__new__(cls)
        self.__original_kwargs__ = kwargs.copy()
        return self

    def __init__(self, func: Callable, state: ConnectionState, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Command is not a coroutine.")

        self.callback = func
        self.state = state
        self.enabled = kwargs.get("enabled", True)

        self.help = func.__doc__

        self.aliases = kwargs.get("aliases", None)
        self.bot = kwargs.get("bot")

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, func: Callable):
        self._callback = func
        unwrapped = func_unwrap(func)
        self.module = unwrapped.__module__

        try:
            globals = unwrapped.__globals__
        except AttributeError:
            globals = {}

        self.params = get_sig_params(func, globals)

    async def __call__(self, context: Context, *args, **kwargs) -> T:
        if self.cog is None:
            return await self.callback(self.cog, context, *args, **kwargs)
        else:
            return await self.callback(context, *args, **kwargs)
    
    async def run(
        self,
        context: Context,
        coro,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        coro = self.callback
        try:
            await coro(context, *args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

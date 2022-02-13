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
from typing import Callable, Optional

from ...internal import run_storage
from ...state import ConnectionState
from ..cogs import Cog


class Command:
    """Represents a prefixed Discord command

    .. versionadded:: 0.9.0
    """

    def __init__(
        self, 
        func: Callable, 
        prefix: str, 
        state: ConnectionState, 
        *, 
        cog: Cog = None,
        description: Optional[str] = None
    ):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Command must be a coroutine")
        self.coro = func
        self.prefix = prefix
        self.state = state
        self.cog = cog
        self._desc = description or func.__doc__ or "No description provided"
        self._storage = run_storage.InternalRunner(self.state.loop)

    def __call__(self, context, *args, **kwargs):
        if self.cog:
            self._storage._run_process(self.coro, self.cog, context, *args, **kwargs)
        else:
            self._storage._run_process(self.coro, context, *args, **kwargs)

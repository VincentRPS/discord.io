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
Handles so-called 'dependency injection' for commands.
"""

from typing import Any, Callable


class Injector:
    def __init__(self, **inject):

        # only take stuff which the user wanted to ingest.

        if 'bot' in inject:
            self.bot = inject.pop('bot')
        if 'gateway' in inject:
            self.gateway = inject.pop('gateway')
        if 'cache' in inject:
            self.cache = inject.pop('cache')
        if 'data' in inject:
            self.data = inject.pop('data')  # if the user wants the raw data (aka, discord.Message).
        if 'other' in inject:
            self.other_injections = inject

    async def inject_callback(self, coro: Callable, *args, **kwargs):
        injections = []

        if 'bot' in kwargs:
            injections.append(self.bot)
            kwargs.pop('bot')
        
        if 'gateway' in kwargs:
            injections.append(self.gateway)
            kwargs.pop('gateway')
        
        if 'cache' in kwargs:
            injections.append(self.cache)
            kwargs.pop('cache')

        if 'data' in kwargs:
            injections.append(self.data)

        if 'other' in kwargs:
            injections.append(self.other_injections)

        result = await coro(*args, *injections, **kwargs)
        return result

    def add_injections(self, **kwargs):
        if 'bot' in kwargs:
            self.bot = kwargs.pop('bot')

        if 'gateway' in kwargs:
            self.gateway = kwargs.pop('gateway')

        if 'cache' in kwargs:
            self.cache = kwargs.pop('cache')

        if 'data' in kwargs:
            self.data = kwargs.pop('data')

        if 'other' in kwargs:
            self.other_injections = kwargs.pop('other')

    def __getitem__(self, i: str):
        return getattr(self, i, None)

class inject:

    def __class_getitem__(cls, obj):
        if isinstance(obj, tuple):
            raise TypeError('object must not be a tuple')

        return _Inject(obj)

class _Inject:
    def __init__(self, injection: Any):
        self.inj = injection

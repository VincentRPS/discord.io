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
discord.ext.tasks
~~~~~~~~~~~~~~~~~
asyncio task helpers.
"""

import asyncio
import datetime
from typing import Any, Callable


class Sleeper:
    def __init__(self, interval: float, callback: Callable, **kwargs):
        self._interval = interval
        self._callback = callback
        self.loop = asyncio.get_running_loop()
        self.fut = self.loop.create_future()
        self.loop.create_task(self._looper(**kwargs), name='Task Handler')
        self.handler = self.loop.call_later(interval, self.fut.set_result, True)

    def wait(self) -> asyncio.Future[Any]:
        return self.fut

    def done(self) -> bool:
        return self.fut.done()

    async def _looper(self, **_) -> None:
        if self.done():
            await self._callback(**_)
            return
        self.loop.create_task(self._looper(**_))

    def cancel(self):
        self.handler.cancel()
        self.fut.cancel()


class Task:
    def __init__(self, interval: float, callback: Callable, loop=None):
        self.interval = interval
        self.callback = callback
        self.loop = loop or asyncio.get_running_loop()
        self.canceled: bool = False

    async def start(self, **kwargs):
        self.sleeper = Sleeper(self.interval, self.callback, **kwargs)
        if self.canceled:
            self.sleeper.cancel()
            return
        await self.sleeper.wait()
        if self.canceled:
            return

        self.loop.create_task(self.start())

    async def stop(self):
        self.canceled = True


def loop(
    seconds: int = None,
    minutes: int = None,
    hours: int = None,
    weeks: int = None,
    loop: asyncio.AbstractEventLoop = None,
):
    kwds = {}

    if seconds:
        kwds['seconds'] = seconds
    if minutes:
        kwds['minutes'] = minutes
    if hours:
        kwds['hours'] = hours
    if weeks:
        kwds['weeks'] = weeks

    if kwds == {}:
        raise TypeError('Time to loop for was not provided.')

    interval: float = datetime.timedelta(**kwds).total_seconds()

    def decorator(func: Callable) -> Task:
        task = Task(interval=interval, callback=func, loop=loop)
        return task

    return decorator

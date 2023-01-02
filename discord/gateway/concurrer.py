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

import time
from asyncio import AbstractEventLoop, Future, get_running_loop

import typing_extensions

__all__ = ['Concurrer']

class Concurrer:
    def __init__(self, concurrency: int, per: float | int) -> None:
        self.concurrency: int = concurrency
        self.per: float | int = per

        self.current: int = self.concurrency
        self._reserved: list[Future] = []
        self.loop: AbstractEventLoop = get_running_loop()
        self.pending_reset: bool = False

    async def __aenter__(self) -> typing_extensions.Self:
        while self.current == 0:
            future = self.loop.create_future()
            self._reserved.append(future)
            await future

        self.current -= 1

        if not self.pending_reset:
            self.pending_reset = True
            self.loop.call_later(self.per, self.reset)

        return self

    async def __aexit__(self, *_) -> None:
        ...

    def reset(self) -> None:
        current_time = time.time()
        self.reset_at = current_time + self.per
        self.current = self.concurrency

        for _ in range(self.concurrency):
            try:
                self._reserved.pop().set_result(None)
            except IndexError:
                break

        if len(self._reserved):
            self.pending_reset = True
            self.loop.call_later(self.per, self.reset)
        else:
            self.pending_reset = False

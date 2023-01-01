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
from typing import Optional

from .route import BaseRoute


class Executer:
    def __init__(self, route: BaseRoute) -> None:
        self.route = route
        self.is_global: Optional[bool] = None
        self.holding_queue: Optional[asyncio.Queue[asyncio.Event]] = None
        self.rate_limited: bool = False

    async def executed(self, reset_after: int | float, limit: int, is_global: bool) -> None:
        self.rate_limited = True
        self.is_global = is_global
        self._reset_after = reset_after
        self.holding_queue = asyncio.Queue()

        await asyncio.sleep(reset_after)

        self.is_global = False

        # NOTE: This could break if someone did a second global rate limit somehow
        requests_passed: int = 0
        for _ in range(self.holding_queue.qsize() - 1):
            if requests_passed == limit:
                if not is_global:
                    await asyncio.sleep(reset_after)
                else:
                    await asyncio.sleep(5)

            requests_passed + 1
            e = await self.holding_queue.get()
            e.set()

    async def wait(self) -> None:
        if not self.rate_limited:
            return

        event = asyncio.Event()

        self.holding_queue.put(event)
        await event.wait()

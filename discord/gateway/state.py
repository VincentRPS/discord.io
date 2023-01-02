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


from typing import Any

from discord import traits

from ..cache.core import Cache
from ..internal import Subscriptor
from ..user import User
from .concurrer import Concurrer

__all__ = ['GatewayState']


class GatewayState:
    user: User

    def __init__(
        self, app: traits.BaseApp, shard_concurrency: tuple[int, int], intents: int, cache: Cache, impls: dict[str, Any]
    ) -> None:
        self.intents = intents
        self.user_ready = None
        self.subscriptor = Subscriptor(app)
        self.shard_concurrency = shard_concurrency
        self.cache = cache
        self.impls = impls

    def loop_activated(self) -> None:
        self.concurrency = Concurrer(self.shard_concurrency[0], self.shard_concurrency[1])

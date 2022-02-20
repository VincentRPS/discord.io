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

from typing import Callable, Optional

from ..interactions import Interaction
from ..internal import run_storage
from ..partial import PartialEmoji
from ..state import ConnectionState


def SelectOption(
    label: str,
    value: str,
    description: Optional[str] = None,
    emoji: Optional[PartialEmoji] = None,
    default: Optional[bool] = False,
):
    ...


class Select:
    """Represents a Discord Select Menu

    .. versionadded:: 1.0

    Parameters
    ----------
    state: :class:`ConnectionState`
    """

    def __init__(self, state: ConnectionState):
        self.state = state
        self.storage = run_storage.InternalRunner(self.state.loop)
        self.func: Callable = None

    def _run(self, interaction: Interaction):
        self.state.loop.create_task(self.storage._run_process(self.func(interaction)))

    def create(self, callback: Callable):
        self.func = callback
        data = {}
        self.state.components[self] = {}

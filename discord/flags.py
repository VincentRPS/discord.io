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

from typing import List

__all__: List[str] = ['MessageFlags']


class MessageFlags:
    """Represents a discord message flag object

    .. versionadded:: 0.7.0
    """

    @classmethod
    def CROSSPOSTED(self):
        return 1 << 0

    @classmethod
    def IS_CROSSPOSTED(self):
        return 1 << 1

    @classmethod
    def SUPPRESS_EMBEDS(self):
        return 1 << 2

    @classmethod
    def SOURCE_MESSAGE_DELETED(self):
        return 1 << 3

    @classmethod
    def URGENT(self):
        return 1 << 4

    @classmethod
    def HAS_THREAD(self):
        return 1 << 5

    @classmethod
    def EPHEMERAL(self):
        return 1 << 6

    @classmethod
    def LOADING(self):
        return 1 << 7

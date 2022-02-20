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
"""Implementation of Colors."""

from typing import List

__all__: List[str] = ['Color']


class Color:
    """Represents the default discord colors

    Defines factory methods which return a certain color code to be used.

    .. versionadded:: 0.7.0
    """

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError('Expected a integer.')

        self.value: int = value

    @classmethod
    def default(self) -> int:
        """A factory color method which returns `0`"""
        return int(0)

    @classmethod
    def teal(self) -> int:
        """A factory color method which returns `0x1ABC9C`"""
        return int(0x1ABC9C)

    @classmethod
    def dark_teal(self) -> int:
        """A factory color method which returns `0x11806A`"""
        return int(0x11806A)

    @classmethod
    def brand_green(self) -> int:
        """A factory color method which returns `0x57F287`"""
        return int(0x57F287)

    @classmethod
    def green(self) -> int:
        """A factory color method which returns `0x2ECC71`"""
        return int(0x2ECC71)

    @classmethod
    def dark_green(self) -> int:
        """A factory color method which returns `0x1F8B4C`"""
        return int(0x1F8B4C)

    @classmethod
    def blue(self) -> int:
        """A factory color method which returns `0x3498DB`"""
        return int(0x3498DB)

    @classmethod
    def dark_blue(self) -> int:
        """A factory color method which returns `0x206694`"""
        return int(0x206694)

    @classmethod
    def purple(self) -> int:
        """A factory color method which returns `0x9b59b6`"""
        return int(0x9B59B6)

    @classmethod
    def dark_purple(self) -> int:
        """A factory color method which returns `0x71368A`"""
        return int(0x71368A)

    @classmethod
    def magenta(self) -> int:
        """A factory color method which returns `0xE91E63`"""
        return int(0xE91E63)

    @classmethod
    def dark_magenta(self) -> int:
        """A factory color method which returns `0xAD1457`"""
        return int(0xAD1457)

    @classmethod
    def gold(self) -> int:
        """A factory color method which returns `0xF1C40F`"""
        return int(0xF1C40F)

    @classmethod
    def dark_gold(self) -> int:
        """A factory color method which returns `0xC27C0E`"""
        return int(0xC27C0E)

    @classmethod
    def orange(self) -> int:
        """A factory color method which returns `0xE67E22`"""
        return int(0xE67E22)

    @classmethod
    def dark_orange(self) -> int:
        """A factory color method which returns `0xA84300`"""
        return int(0xA84300)

    @classmethod
    def brand_red(self) -> int:
        """A factory color method which returns `0xED4245`"""
        return int(0xED4245)

    @classmethod
    def red(self) -> int:
        """A factory color method which returns `0xE74C3C`"""
        return int(0xE74C3C)

    @classmethod
    def dark_red(self) -> int:
        """A factory color method which returns `0x992D22`"""
        return int(0x992D22)

    @classmethod
    def dark_gray(self) -> int:
        """A factory color method which returns `0x607D8B`"""
        return int(0x607D8B)

    @classmethod
    def light_gray(self) -> int:
        """A factory color method which returns `0x979C9F`"""
        return int(0x979C9F)

    @classmethod
    def blurple(self) -> int:
        """A factory color method which returns `0x5865F2`"""
        return int(0x5865F2)

    @classmethod
    def dark_theme(self) -> int:
        """A factory color method which returns `0x2F3136`"""
        return int(0x2F3136)

    @classmethod
    def fushia(self) -> int:
        """A factory color method which returns `0xEB459E`"""
        return int(0xEB459E)

    @classmethod
    def yellow(self) -> int:
        """A factory color method which returns `0xFEE75C`"""
        return int(0xFEE75C)

    @classmethod
    def from_rgb(self, red: int, green: int, blue: int) -> int:
        """A factory color method which gets its color from rgb values"""
        return (red << 16) + (green << 8) + blue

    @classmethod
    def from_hex(self, hex_code: str):
        """A factory color method which gets its color from a hex code string"""
        if '#' in hex_code:
            hex_code = hex_code.lstrip('#')
        x = len(hex_code)
        return self.from_rgb(
            *tuple(int(hex_code[i : i + x // 3], 16) for i in range(0, x, x // 3))
        )

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

class Color:
    """Represents the default discord colors

    Defines factory methods which return a certain color code to be used.

    .. versionadded:: 0.7.0
    """
    
    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Expected a integer.")
        
        self.value: int = value
    
    @classmethod
    def default(self) -> int:
        return int(0)
    
    @classmethod
    def teal(self) -> int:
        return int(0x1abc9c)
    
    @classmethod
    def dark_teal(self) -> int:
        return int(0x11806a)
    
    @classmethod
    def brand_green(self) -> int:
        return int(0x57F287)
    
    @classmethod
    def green(self) -> int:
        return int(0x2ecc71)

    @classmethod
    def dark_green(self) -> int:
        return int(0x1f8b4c)
    
    @classmethod
    def blue(self) -> int:
        return int(0x3498db)
    
    @classmethod
    def dark_blue(self) -> int:
        return int(0x206694)
    
    @classmethod
    def purple(self) -> int:
        return int(0x206694)
    
    @classmethod
    def dark_purple(self) -> int:
        return int(0x71368a)

    @classmethod
    def magenta(self) -> int:
        return int(0xe91e63)
    
    @classmethod
    def dark_magenta(self) -> int:
        return int(0xad1457)
    
    @classmethod
    def gold(self) -> int:
        return int(0xf1c40f)
    
    @classmethod
    def dark_gold(self) -> int:
        return int(0xc27c0e)

    @classmethod
    def orange(self) -> int:
        return int(0xe67e22)

    @classmethod
    def dark_orange(self) -> int:
        return int(0xa84300)

    @classmethod
    def brand_red(self) -> int:
        return int(0xED4245)

    @classmethod
    def red(self) -> int:
        return int(0xe74c3c)

    @classmethod
    def dark_red(self) -> int:
        return int(0x992d22)

    @classmethod
    def dark_gray(self) -> int:
        return int(0x607d8b)

    @classmethod
    def light_gray(self) -> int:
        return int(0x979c9f)
    
    @classmethod
    def blurple(self) -> int:
        return int(0x5865F2)

    @classmethod
    def dark_theme(self) -> int:
        return int(0x2F3136)
    
    @classmethod
    def fushia(self) -> int:
        return int(0xEB459E)
    
    @classmethod
    def yellow(self) -> int:
        return int(0xFEE75C)

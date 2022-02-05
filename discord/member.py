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
"""Represents a Discord Member

ref: https://discord.dev/resources/guild#guild-member-object
"""
from typing import Any, List

from .user import User

__all__: List[str] = ["Member"]


class Member:
    """Represents a Discord Guild Member

    .. versionadded:: 0.7.0
    """

    def __init__(self, data: dict, factory):
        self.from_dict = data
        self._factory = factory

    def user(self):
        return User(self.from_dict["user"])

    def nick(self) -> str:
        return self.from_dict["nick"]

    def avatar(self) -> str:
        raise NotImplementedError

    def roles(self):
        raise NotImplementedError

    def joined_at(self) -> str:
        return self.from_dict["joined_at"]

    def premium_since(self) -> str:
        return self.from_dict["premium_since"]

    def deaf(self) -> bool:
        return self.from_dict["deaf"]

    def mute(self) -> bool:
        return self.from_dict["mute"]

    def pending(self) -> bool:
        return self.from_dict["pending"]

    def permissions(self) -> dict[str, Any]:
        return self.from_dict["permissions"]

    def communication_disabled_until(self):
        return self.from_dict["communication_disabled_until"]

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
"""Represents a partial Discord Emoji.

ref: https://discord.dev/resources/emoji
"""
from .enums import StickerFormatType, StickerType
from .state import ConnectionState
from .types import Dict
from .user import User


class Emoji:
    """Represents a Discord Emoji.

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data
        The raw emoji data

    Attributes
    ----------
    from_dict
        The raw emoji data
    """

    def __init__(self, data: Dict):
        self.from_dict = data
        """The data in dict format."""

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    @property
    def name(self) -> str:
        return self.from_dict["name"]

    # def roles(self) -> Role:

    @property
    def creator(self) -> User:
        return User(self.from_dict["user"])

    def require_colons(self) -> bool:
        return self.from_dict["require_colons"]

    def managed(self) -> bool:
        return self.from_dict["managed"]

    def animated(self) -> bool:
        return self.from_dict["animated"]

    def available(self) -> bool:
        return self.from_dict["available"]


class Sticker:
    """Represents a Discord Sticker.

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw Sticker data
    state: :class:`ConnectionState`
        The connection state

    Attributes
    ----------
    from_dict
        The raw Sticker data
    """

    def __init__(self, data: dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    @property
    def pack(self) -> int:
        return self.from_dict["pack_id"]

    @property
    def name(self) -> str:
        return self.from_dict["name"]

    def description(self) -> str:
        return self.from_dict["description"]

    def tags(self) -> str:
        return self.from_dict["tags"]

    def type(self) -> StickerType:
        if self.from_dict["type"] == 1:
            return StickerType.STANDARD
        else:
            return StickerType.GUILD

    def format(self) -> StickerFormatType:
        if self.from_dict["format_type"] == 1:
            return StickerFormatType.PNG
        elif self.from_dict["format_type"] == 2:
            return StickerFormatType.APNG
        else:
            return StickerFormatType.LOTTIE

    def available(self) -> bool:
        return self.from_dict["available"]

    def guild_id(self) -> int:
        return int(self.from_dict["guild_id"])

    def creator(self) -> User:
        return User(self.from_dict["user"])

    def sort_value(self) -> int:
        return int(self.from_dict["sort_value"])

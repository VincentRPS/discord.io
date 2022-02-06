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
from collections import namedtuple
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List


def _new_value_cls(name):
    cls = namedtuple("_EnumValue_" + name, "name value")
    cls.__repr__ = lambda self: f"<{name}.{self.name}: {self.value!r}>"
    cls.__str__ = lambda self: f"{name}.{self.name}"
    return cls


def _descriptor(obj):
    return (
        hasattr(obj, "__get__") or hasattr(obj, "__set__") or hasattr(obj, "__delete__")
    )


class EnumMeta(type):
    if TYPE_CHECKING:
        __name__: ClassVar[str]
        _enum_member_names_: ClassVar[List[str]]
        _enum_member_map_: ClassVar[Dict[str, Any]]
        _enum_value_map_: ClassVar[Dict[Any, Any]]

    def __new__(cls, name, bases, attrs):
        value_mapping = {}
        member_mapping = {}
        member_names = []

        val = _new_value_cls(name)
        for item, value in list(attrs.items()):
            desc = _descriptor(value)
            if item[0] == "_" and not desc:
                continue

            if isinstance(value, classmethod):
                continue

            if desc:
                setattr(value, item, value)
                del attrs[item]
                continue

            try:
                new_value = value_mapping[value]
            except KeyError:
                new_value = val(name=item, value=value)
                value_mapping[value] = new_value
                member_names.append(item)

            member_mapping[item] = new_value
            attrs[item] = new_value

        attrs["_enum_value_map_"] = value_mapping
        attrs["_enum_member_map_"] = member_mapping
        attrs["_enum_member_names_"] = member_names
        attrs["_enum_value_cls"] = value
        real_cls = super().__new__(cls, name, bases, attrs)
        val._real_cls_ = real_cls
        return real_cls

    def __getitem__(cls, item):
        return cls._enum_member_map_[item]

    def __repr__(cls) -> str:
        return f"<emum {cls.__name__}>"


class Enum(metaclass=EnumMeta):
    @classmethod
    def try_value(cls, value):
        try:
            return cls._enum_value_map_[value]
        except (KeyError, TypeError):
            return value


class ButtonStyle(Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5
    BLURPLE = 1
    GRAY = 2
    GREEN = 3
    RED = 4


class ChannelType(Enum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GROUP_DM = 3
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_STORE = 6  # probably gonna be deprecated soon
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13


class VideoQuality(Enum):
    AUTO = 1
    FULL = 2


class ApplicationCommandType(Enum):
    CHAT_INPUT = 1
    USER = 2
    MESSAGE = 3

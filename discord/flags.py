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

from typing import Callable, Type, TypeVar

F = TypeVar('F', bound='Flags')


class flag:
    def __init__(self, func: Callable):
        self.value: int = func(None)
        self.__doc__ = func.__doc__

    def __get__(self, instance: F | None, _: Type[F]) -> int | bool:
        return instance._has_flag(self.value) if instance else self.value

    def __set__(self, instance: F, value: bool) -> None:
        instance._overwrite_flag(flag=self.value, value=value)


class Flags:
    def __init__(self, **flags_named: bool) -> None:
        self._flag_overwrites: list[tuple[int, bool]] = []

        for name, value in flags_named.items():
            if name.startswith('_'):
                raise AttributeError('Flags cannot be private')

            if not hasattr(self, name):
                raise AttributeError(f'Flag {repr(name)} does not exist')

            flag_value = getattr(self.__class__, name)
            self._overwrite_flag(flag_value, value)

    def _has_flag(self, flag: int) -> bool:
        return next(
            (overwrite[1] for overwrite in self._flag_overwrites if overwrite[0] == flag), False
        )

    def _overwrite_flag(self, flag: int, value: bool) -> None:
        self._flag_overwrites.append((flag, value))


class Intents(Flags):
    @flag
    def guilds(self) -> bool | int:
        return 1 << 0

    @flag
    def guild_members(self) -> bool | int:
        return 1 << 1

    @flag
    def guild_bans(self) -> bool | int:
        return 1 << 2

    @flag
    def guild_emojis_and_stickers(self) -> bool | int:
        return 1 << 3

    @flag
    def guild_integrations(self) -> bool | int:
        return 1 << 4

    @flag
    def guild_webhooks(self) -> bool | int:
        return 1 << 5

    @flag
    def guild_invites(self) -> bool | int:
        return 1 << 6

    @flag
    def guild_voice_states(self) -> bool | int:
        return 1 << 7

    @flag
    def guild_presences(self) -> bool | int:
        return 1 << 8

    @flag
    def guild_messages(self) -> bool | int:
        return 1 << 9

    @flag
    def guild_message_reactions(self) -> bool | int:
        return 1 << 10

    @flag
    def guild_message_typing(self) -> bool | int:
        return 1 << 11

    @flag
    def direct_messages(self) -> bool | int:
        return 1 << 12

    @flag
    def direct_message_reactions(self) -> bool | int:
        return 1 << 13

    @flag
    def direct_message_typing(self) -> bool | int:
        return 1 << 14

    @flag
    def message_content(self) -> bool | int:
        return 1 << 15

    @flag
    def guild_scheduled_events(self) -> bool | int:
        return 1 << 16

    @flag
    def auto_moderation_configuration(self) -> bool | int:
        return 1 << 20

    @flag
    def auto_moderation_execution(self) -> bool | int:
        return 1 << 21

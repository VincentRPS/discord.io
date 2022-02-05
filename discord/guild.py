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
"""Represents a Discord Guild.

ref: https://discord.dev/resources/guild
"""
from typing import Any, Dict, List

from discord.member import Member

__all__: List[str] = ["Guild"]


class Guild:
    """Represents a Discord Guild.

    .. versionadded:: 0.6.0
    """

    # cache helpers for guilds.
    def __init__(self, guild: dict, rest_factory):
        self.from_dict = guild
        self._factory = rest_factory

    def joined_at(self) -> str:
        return self.from_dict["joined_at"]

    def vanity(self) -> str:
        """The vanity url, if None returns None"""
        return self.from_dict["vanity_url_code"]

    def splash(self) -> str:
        """The splash screen, if None returns None"""
        return self.from_dict["splash"]

    def discovery_splash(self) -> str:
        """The discovery splash, if None returns None"""
        return self.from_dict["discovery_splash"]

    def sub_count(self) -> int:
        """The subscription count, returns a int"""
        return self.from_dict["premium_subscription_count"]

    def emojis(self) -> List[Dict[str, Any]]:
        """A list of emojis

        .. note::

            we are currently working on making a emoji class
            to return a list of them, but while that is being made
            this will just return a dict of all emojis.
        """
        return self.from_dict["emojis"]

    def id(self) -> int:
        return self.from_dict["id"]

    async def get_member(self, id: int):
        unparsed = await self._factory.get_guild_member(self.id(), id)
        return Member(unparsed, self._factory)

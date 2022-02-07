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
from typing import Any, Dict, List, Optional

from .enums import FormatType
from .member import Member

__all__: List[str] = ["Guild"]


class Guild:
    """Represents a Discord Guild.

    .. versionadded:: 0.6.0

    Parameters
    ----------
    guild
        The raw guild object
    rest_factory
        The current :class:`RESTFactory`
    """

    # cache helpers for guilds.
    def __init__(self, guild: dict, rest_factory):
        self.from_dict = guild
        self._factory = rest_factory

    def joined_at(self) -> str:
        return self.from_dict["joined_at"]

    def vanity(self) -> str:
        """The vanity url, if None returns None

        Returns
        -------
        :class:`str`
        """
        return self.from_dict["vanity_url_code"]

    def splash(self) -> str:
        """The splash screen, if None returns None

        Returns
        -------
        :class:`str`
        """
        return self.from_dict["splash"]

    def discovery_splash(self) -> str:
        """The discovery splash, if None returns None

        Returns
        -------
        :class:`str`
        """
        return self.from_dict["discovery_splash"]

    def sub_count(self) -> int:
        """The subscription count, returns a int

        Returns
        -------
        :class:`int`
        """
        return self.from_dict["premium_subscription_count"]

    def emojis(self) -> List[Dict[str, Any]]:
        """A list of emojis

        .. note::

            we are currently working on making a emoji class
            to return a list of them, but while that is being made
            this will just return a dict of all emojis.
        """
        return self.from_dict["emojis"]

    @property
    def id(self) -> int:
        """The guild id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict["id"]

    async def get_member(self, id: int):
        """Gets a member and returns a :class:`Member` object

        Parameters
        ----------
        id
            The members id

        Returns
        -------
        :class:`Member`
        """
        unparsed = await self._factory.get_guild_member(self.id(), id)
        return Member(unparsed, self.id, self._factory)


def parse_role_icon(format: FormatType, role_id: int, role_icon: str) -> str:
    return f"https://cdn.discordapp.com/role-icons/{role_id}/{role_icon}.{format}"


def _parse_tags(data: dict):
    return data.get("bot_id") or data.get("integration_id") or ""


class Role:
    def __init__(self, data: dict):
        self.from_dict = data

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    @property
    def name(self) -> str:
        return self.from_dict["name"]

    @property
    def color(self) -> int:
        return self.from_dict["color"]

    def hoist(self) -> bool:
        return self.from_dict["hoist"]

    def icon(self, format: Optional[FormatType] = FormatType.PNG) -> str:
        return parse_role_icon(
            format=format, role_id=self.id, role_icon=self.from_dict["icon"]
        )

    def unicode_emoji(self) -> str:
        return self.from_dict["unicode_emoji"]

    @property
    def position(self) -> int:
        return self.from_dict["position"]

    def permissions(self) -> str:
        # TODO: Replace with a Permission class?
        return self.from_dict["permissions"]

    def managed(self) -> bool:
        return self.from_dict["managed"]

    def mentionable(self) -> bool:
        return self.from_dict["mentionable"]

    def tags(self):
        _parse_tags(self.from_dict)

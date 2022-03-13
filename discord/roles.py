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

from typing import Dict, TYPE_CHECKING, Optional
from .enums import FormatType

if TYPE_CHECKING:
    from .http import RESTFactory

__all__ = (
    'Role'
)

def parse_role_icon(format: FormatType, role_id: int, role_icon: str) -> str:
    return f'https://cdn.discordapp.com/role-icons/{role_id}/{role_icon}.{format}'


def _parse_tags(data: Dict) -> str:
    return data.get('bot_id') or data.get('integration_id') or ''


class Role:
    """Represents a Discord Role

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw role data
    """

    def __init__(self, data: Dict, factory):
        self.from_dict = data
        self.factory: RESTFactory = factory

    @property
    def id(self) -> int:
        """Gives the snowflake id of the role

        Returns
        -------
        :class:`int`
        """
        return int(int(self.from_dict['id']))

    @property
    def name(self) -> str:
        """Gives the name of the role

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    @property
    def color(self) -> int:
        """Returns the roles color

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['color']

    def hoist(self) -> bool:
        """If the role is hoisted or not

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['hoist']

    def icon(self, format: Optional[FormatType] = FormatType.PNG) -> str:
        """Gives the role icon's link, if any.

        Returns
        -------
        :class:`str`
        """
        return parse_role_icon(format=format, role_id=self.id, role_icon=self.from_dict['icon'])

    def unicode_emoji(self) -> str:
        """Gives the roles unicode emoji

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['unicode_emoji']

    @property
    def position(self) -> int:
        """Gives the current role position

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['position']

    def permissions(self) -> str:
        """Gives the role permissions

        Returns
        -------
        :class:`str`
        """
        # TODO: Replace with a Permission class?
        return self.from_dict['permissions']

    def managed(self) -> bool:
        """If the role is managed or not

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['managed']

    def mentionable(self) -> bool:
        """If the role is publicly mentionable

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['mentionable']

    def tags(self) -> str:
        """The current role' tags

        Returns
        -------
        :class:`str`
        """
        return _parse_tags(self.from_dict)

    def give_to(self, user_id: int, reason: Optional[str] = None):
        """Gives a user the role"""
        return self.factory.guilds.give_user_role(user_id, self.id, reason=reason)

    def remove_from(
        self,
        user_id: int,
        reason: Optional[str] = None,
    ):
        """Removes a user from the role"""
        return self.factory.guilds.remove_user_role(user_id, self.id, reason=reason)


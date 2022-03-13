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

from typing import Dict, List, Union
from .user import User


class Presence:
    """Represents a Discord Presence

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw presence data
    """

    def __init__(self, data: Dict):
        self.from_dict = data

    @property
    def user(self) -> User:
        """Gives the :class:`User` which has this presence

        Returns
        -------
        :class:`User`
        """
        return User(self.from_dict['user'])

    @property
    def guild_id(self) -> int:
        """Gives the id of the guild

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['guild_id']

    @property
    def status(self) -> str:
        """The users current status, i.e 'online', 'offline', etc

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['status']

    @property
    def activites(self) -> List['Activity']:
        """Gives the users activites

        Returns
        -------
        List[:class:`Activity`]
        """
        return [Activity(raw) for raw in self.from_dict['activites']]

    @property
    def client_status(self) -> str:
        """The users current client status, i.e desktop, mobile, etc

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['client_status']


# still needs finishing i just don't feel like doing it now.
class Activity:
    """Represents a Discord Activity

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw activity data
    """

    def __init__(self, data: Dict):
        self.from_dict = data

    @property
    def name(self) -> str:
        return self.from_dict['name']

    @property
    def type(self) -> int:
        return self.from_dict['type']

    @property
    def url(self) -> Union[str, None]:
        return self.from_dict['url']

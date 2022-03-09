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
"""Represents a Discord User

ref: https://discord.dev/resources/users
"""
from typing import List

__all__: List[str] = ['User']


class User:
    """Represents a Discord User

    .. versionadded:: 0.6.0

    Parameters
    ----------
    usr
        The user in dict format
    """

    def __init__(self, usr: dict):
        self.from_dict = usr

    def __repr__(self):
        return f"<User id={self.id!r}>"

    def username(self) -> str:
        """The users username

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['username']

    def discriminator(self) -> int:
        """The users discriminator id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['discriminator']

    @property
    def id(self) -> int:
        """The users snowflake id

        Returns
        -------
        :class:`int`
        """
        return int(self.from_dict['id'])

    def public_flags(self):
        """The users public flags."""
        return self.from_dict['public_flags']

    @property
    def bot(self) -> bool:
        """If the User is a bot or not

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['bot']

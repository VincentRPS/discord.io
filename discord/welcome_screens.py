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

from typing import Dict, TYPE_CHECKING, List, Union

if TYPE_CHECKING:
    from .http import RESTFactory

__all__ = (
    'WelcomeScreen',
    'WelcomeChannel'
)

class WelcomeScreen:
    """Represents a Discord Guild WelcomeScreen

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
    """

    def __init__(self, data: Dict, factory):
        self.from_dict = data
        self.factory: RESTFactory = factory

    @property
    def description(self) -> str:
        """Gives the WelcomeScreen' description

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['description']

    def channels(self) -> List['WelcomeChannel']:
        """Gives a list of :class:`WelcomeChannel`

        Returns
        -------
        list[:class:`WelcomeChannel`]
        """
        return [WelcomeChannel(channel) for channel in self.from_dict['welcome_channels']]


class WelcomeChannel:
    """Represents a Discord WelcomeScreen Channel

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw WelcomeChannel data
    """

    def __init__(self, data: Dict):
        self.from_dict = data

    @property
    def channel_id(self) -> int:
        """Gives the Channel' id


        Returns
        -------
        :class:`int`
        """
        return self.from_dict['channel_id']

    @property
    def description(self) -> str:
        """Gives the description of the channel

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['description']

    def emoji_id(self) -> Union[int, None]:
        """Gives the Emoji id, if any

        Returns
        -------
        :class:`int`
        :class:`None`
        """
        return self.from_dict.get('emoji_id')

    def emoji_name(self) -> Union[str, None]:
        """Gives the Emoji name, if any

        Returns
        -------
        :class:`str`
        :class:`None`
        """
        return self.from_dict.get('emoji_name')
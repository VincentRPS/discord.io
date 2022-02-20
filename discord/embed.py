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
"""Represents a Discord Embed.

ref: https://discord.dev/resources/channel#embed-limits
"""
import datetime
from typing import Any, List, Optional, Union

from discord.color import Color
from discord.colour import Colour

__all__: List[str] = ['Embed']


class Embed:
    """Represents a Discord Embed.

    Parameters
    ----------
    title
        The embed title
    description
        The embed description
    url
        The embed url
    date
        The embed date
    color
        The embed color
    colour
        The embed colour
    timestamp
        The embed timestamp
    """

    def __init__(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None,
        url: Optional[str] = None,
        date: Optional[str] = None,
        color: Optional[Union[int, Color]] = None,
        colour: Optional[Union[int, Colour]] = None,
        timestamp: datetime.datetime = None,
    ):
        self.obj: dict[str, Any] = {
            'type': 'rich',
        }

        if title:
            self.obj['title'] = title
        if description:
            self.obj['description'] = description
        if url:
            self.obj['url'] = url
        if date:
            self.obj['date'] = date
        if color:
            self.obj['color'] = color
        if colour:
            self.obj['color'] = colour
        if timestamp:
            self.obj['timestamp'] = timestamp

    def to_dict(self):
        """Gives the dictionary which the embed is within

        Returns
        -------
        obj :class:`dict`
            The dict
        """
        return self.obj

    def set_footer(self, text: str = None, icon_url: str = None):
        """Sets the footer

        Parameters
        ----------
        text
            A text footer
        icon_url
            The icon url of the footer
        """
        if text:
            self.obj['footer']['text'] = text
        if icon_url:
            self.obj['footer']['icon_url'] = icon_url

    def remove_footer(self):
        """Removes the footer"""
        del self.obj['footer']

    def set_thumbnail(self, url: str = None):
        """Sets a thumbnail on the embed

        Parameters
        ----------
        url
            The thumbnail url
        """
        if url is None:
            del self.obj['thumbnail']
        else:
            self.obj['thumbnail'] = {'url': url}

    def set_author(self, name: str, url: str = None, icon_url: str = None):
        """Sets the embed author

        Parameters
        ----------
        name
            The author name
        url
            The author's url
        icon_url
            The author's icon_url
        """
        self.obj['author'] = name

        if url:
            self.obj['author']['url'] = url
        if icon_url:
            self.obj['author']['icon_url'] = icon_url

    def remove_author(self):
        """Removes the author from the embed"""
        del self.obj['author']

    def add_field(self, name: str, value: str, inline: bool = True):
        """Adds a field to the embed

        Parameters
        ----------
        name
            The field name
        value
            The field value
        inline
            If the field should be inline
        """
        field = {'name': name, 'value': value, 'inline': inline}

        try:
            self.obj['fields'].append(field)
        except KeyError:
            self.obj['fields'] = [field]

    def remove_field(self, name: str):
        """Removes the field

        Parameters
        ----------
        name
            The field to remove
        """
        del self.obj['fields'][name]

    def set_image(self, url: str):
        if url is None:
            del self.obj['image']
        else:
            self.obj['image'] = {'url': str(url)}

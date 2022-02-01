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

from typing import List, Optional, Union

from rpd.color import Color

__all__: List[str] = ["Embed"]


def Embed(
    title: Optional[str] = None,
    description: Optional[str] = None,
    url: Optional[str] = None,
    date: Optional[str] = None,
    color: Optional[Union[int, Color]] = None,
):
    """Generates a rich embed"""
    ret = {
        "type": "rich",
    }

    if title:
        ret["title"] = title
    if description:
        ret["description"] = description
    if url:
        ret["url"] = url
    if date:
        ret["date"] = date
    if color:
        ret["color"] = color

    return [ret]

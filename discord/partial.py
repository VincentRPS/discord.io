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
"""In some cases Discord will want to give or take a partial object.
this means we don't want to hand them the complete object, this simply covers that.
"""

from typing import Optional


class PartialEmoji:
    """Represents a Partial Discord Emoji

    .. versionadded:: 1.0

    Parameters
    ----------
    data: Optional[:class:`dict`]
        The raw emoji data
    id: :class:`int`
        The emoji id
    name: :class:`str`
        The emoji name
    animated: :class:`bool`
        If the emoji is animated
    """

    def __init__(
        self,
        data: Optional[dict] = None,
        id: Optional[int] = None,
        name: Optional[str] = None,
        animated: Optional[bool] = False,
    ):
        self.from_dict = data
        self.id = id
        self.name = name
        self.animated = self.animated

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

from typing import List, Optional, Union

from ..assets import Attachment
from ..channels import Category, TextChannel, Thread, VoiceChannel
from ..guild import Role
from ..member import Member
from ..user import User


def Choice(
    name: str,
    value: str,
):
    return {"name": name, "value": value}


def Option(
    name: str,
    description: str,
    type: Union[
        str,
        int,
        bool,
        User,
        TextChannel,
        VoiceChannel,
        Thread,
        Category,
        Role,
        Member,
        Attachment,
    ],
    required: Optional[bool] = False,
    choices: List[Choice] = None,
    channel_types: List[int] = None,
    min_value: int = None,
    max_value: int = None,
    autocomplete: bool = False,
):
    ret = {
        "name": name,
        "description": description,
    }

    # probably the most jank thing i wrote but it works, and does it good.
    if type == str:
        ret["type"] = 3
    elif type == int:
        ret["type"] = 4
    elif type == bool:
        ret["type"] = 5
    elif type == User:
        ret["type"] = 6
    elif type == TextChannel or VoiceChannel or Thread or Category:
        ret["type"] = 7
    elif type == Role:
        ret["type"] = 8
    elif type == Member:
        ret["type"] = 9
    elif type == Attachment:
        ret["type"] = 11

    if required is True:
        ret["required"] = True

    if choices is not None:
        ret["choices"] = choices

    if channel_types:
        ret["channel_types"] = channel_types

    if min_value:
        ret["min_value"] = min_value
    if max_value:
        ret["max_value"] = max_value

    if autocomplete:
        ret["autocomplete"] = True

    return ret

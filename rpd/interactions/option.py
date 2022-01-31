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

from typing import List, Optional


def SlashOptionType(
    string: bool = False, 
    integer: bool = False, 
    boolean: bool = False, 
    user: bool = False, 
    channel: bool = False, 
    role: bool = False, 
    mentionable: bool = False, 
    number: bool = False
) -> int:
    if string:
        return 3
    if integer:
        return 4
    if boolean:
        return 5
    if user:
        return 6
    if channel:
        return 7
    if role:
        return 8
    if mentionable:
        return 9
    if number:
        return 10

def SlashChoice(
    name: str,
    value: str
):
    return name, value

def SlashOption(
    type: SlashOptionType, 
    name: str, 
    description: Optional[str] = None, 
    required: bool = False,
    choices: List[SlashChoice] = None,
    channel_types: int = None,
    min_value: int = None,
    max_value: int = None,
    autocomplete: bool = False
):
    ret = {
        "type": type,
        "name": name
    }
    if description:
        ret["description"] = description
    if required is not False:
        ret["required"] = required
    if choices:
        ret["choices"] = choices
    if channel_types:
        ret["channel_types"] = channel_types
    if min_value:
        ret["min_value"] = min_value
    if max_value:
        ret["max_value"] = max_value
    if autocomplete:
        raise NotImplementedError

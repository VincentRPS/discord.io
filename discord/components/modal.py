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
from typing import Optional
from .. import utils
from ..enums import ModalStyle

def ModalComponent(
    label: str,
    placeholder: Optional[str] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    style: ModalStyle = ModalStyle.SHORT,
    required: Optional[bool] = False,
    value: Optional[str] = None,
):
    ret = {
        "type": 1,
        "components": [{
            "type": 4,
            "custom_id": utils.create_snowflake(),
            "label": label,
            "style": style,
        }]
    }
    if placeholder:
        ret["components"][0]["placeholder"] = placeholder
    if min_length:
        ret["components"][0]["min_length"] = min_length
    if max_length:
        ret["components"][0]["max_length"] = max_length
    if required:
        ret["components"][0]["required"] = True
    if value:
        ret["components"][0]["value"] = value

def Modal(
    title: str,
    components: ModalComponent,
    custom_id: int = utils.create_snowflake(),
    ):
    ret = {
        "title": title,
        "custom_id": custom_id,
        "components": [components]
    }
    return ret
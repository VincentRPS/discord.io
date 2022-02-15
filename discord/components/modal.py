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

import asyncio
from typing import Any, Callable, Coroutine, Optional, Dict, List

from .. import utils
from ..enums import ModalStyle
from ..interactions import Interaction
from ..state import ConnectionState


def ModalComponent(
    label: str,
    placeholder: Optional[str] = None,
    min_length: Optional[int] = 1,
    max_length: Optional[int] = 4000,
    style: ModalStyle = ModalStyle.SHORT,
    required: Optional[bool] = False,
    value: Optional[str] = None,
):
    ret = {
        'type': 1,
        'components': [
            {
                'type': 4,
                'custom_id': utils.create_snowflake(),
                'label': label,
                'style': style,
            }
        ],
    }
    if placeholder:
        ret['components'][0]['placeholder'] = placeholder
    if min_length:
        ret['components'][0]['min_length'] = min_length
    if max_length:
        ret['components'][0]['max_length'] = max_length
    if required:
        ret['components'][0]['required'] = True
    if value:
        ret['components'][0]['value'] = value

    return ret


class Modal:
    """Represents a Discord button interaction.

    Parameters
    ----------
    state
        The connection state
    """

    def __init__(self, state: ConnectionState):
        self.state = state

    async def _run_callback(
        self, coro: Callable[..., Coroutine[Any, Any, Any]], data, state
    ) -> None:
        try:
            await coro(Interaction(data, state))
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

    def create(
        self,
        title: str,
        callback: Any,
        components: List[ModalComponent],
        custom_id: int = utils.create_snowflake(),
    ):
        self.id = custom_id
        ret = {'title': title, 'custom_id': self.id, 'components': components}
        self.state.components[self] = {
            'self': self,
            'callback': callback,
            'data': ret,
            'id': self.id,
        }
        return ret

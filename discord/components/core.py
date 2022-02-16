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
import random
import string
import typing
from typing import Any, Callable, Coroutine

from ..interactions.interaction import Interaction
from ..internal.dispatcher import Coro
from ..state import ConnectionState

__all__: typing.List[str] = ['Button']


class Button:
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

    async def create(
        self,
        label: str,
        callback: Coro,
        style: typing.Literal[1, 2, 3, 4, 5] = 1,
        custom_id: str = None,
        url: str = None,
    ):
        """Creates a button

        Parameters
        ----------
        label
            The button label
        callback
            The button callback
        style
            The button style to use
        custom_id
            A custom_id
        url
            A url

            .. note::

                can only be used in buttons,
                with style type 5
        """
        self.id = (
            custom_id
            if custom_id is not None
            else ''.join(
                random.choice(string.ascii_letters)
                for _ in range(random.randint(10, 100))
            )
        )

        ret = {
            'type': 1,
            'components': [
                {
                    'type': 2,
                    'label': label,
                    'style': style,
                    'url': url,
                    'custom_id': self.id,
                }
            ],
        }

        self.callback = callback

        self.state.components[self] = {
            'self': self,
            'callback': self.callback,
            'data': ret,
            'id': self.id,
        }

        return ret

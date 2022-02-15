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

import inspect
from collections import OrderedDict
from typing import Any, Callable, Dict, List, Optional
from uuid import uuid4

from .option_converter import Choice, Option
from .registry import ApplicationCommandRegistry


class ApplicationCommand:
    def __init__(
        self,
        func: Callable,
        name: Optional[str] = None,
        description: Optional[str] = None,
        registry: ApplicationCommandRegistry = None,
    ):
        self.registry = registry
        self.coro = func
        self.name = func.__name__ if name is None else name
        self.desc = description or func.__doc__ or 'No description provided'
        self.obj: Dict[str, Any] = {
            'self': self,
            'options': [option for option in self._options],
        }

    @property
    def options(self):
        dict = OrderedDict(inspect.signature(self._callback).parameters)
        dict.popitem(last=False)
        return dict

    def _parse_options(self):
        self._options = []
        for name, param in self.options.items():
            if param == Option:
                self._options.append(param)
            else:
                raise RuntimeError("%s is not using the Option class!", name)

    @property
    def _callback(self):
        return self.coro

    @_callback.setter
    def _callback(self, func: Callable[..., Any]):
        self.coro = func

    def sub_command(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        options: List[Option] = None,
        choices: List[Choice] = None,
    ):
        def decorator(func: Callable) -> ApplicationCommand:
            _name = name or func.__name__
            _description = description or func.__doc__ or 'No description provided'
            sub_command = {
                "name": _name,
                "description": _description,
                "choices": choices,
                "type": 1,
                'options': options,
            }
            self.obj['options'].append(sub_command)

            return self  # type: ignore

        return decorator

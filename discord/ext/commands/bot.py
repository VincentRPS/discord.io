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

from ...client import Callable, Client
from .core import Command, Flag


class Bot(Client):
    def __init__(self, command_prefix: str, **kwargs):
        super().__init__(**kwargs)
        self.command_prefix = command_prefix
        self._cmd_cls = Command

    def command(self, name: Optional[str] = None, flags: list[Flag] = []):
        def decorator(func: Callable) -> Command:
            _name = name or func.__name__
            _description = func.__doc__
            cmd = self._cmd_cls(
                func=func,
                prefix=self.command_prefix,
                state=self.state,
                description=_description,
                name=_name,
                flags=flags,
            )
            self.state.prefixed_commands.append(cmd)
            return cmd

        return decorator

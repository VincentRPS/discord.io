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

from typing import Optional, Any

from ...client import Callable, Client
from .core import Command, Flag
from ..cogs import Cog


class Bot(Client):
    def __init__(self, command_prefix: str, **kwargs):
        super().__init__(**kwargs)
        self.command_prefix = command_prefix

    def __add_cog_commands__(self, cog: Cog):
        for command in cog.prefixed_commands.values():
            self.state.prefixed_commands.append(
                Command(
                    func=command.func,
                    name=command.name,
                    prefix=self.command_prefix,
                    state=self.state,
                    description=command.description,
                    cog=cog
                )
            )

    def command(self, name: Optional[str] = None, flags: list[Flag] = []):
        def decorator(func: Callable) -> Command:
            _name = name or func.__name__
            _description = func.__doc__
            cmd = Command(
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


    def add_cog(self, cog: Cog, *, override: bool = False):
        if not isinstance(cog, Cog):
            raise TypeError('ALL cogs must subclass Cog.')

        name = cog.__cog_name__
        current = self.cogs.get(name)

        if current is not None:
            if not override:
                raise TypeError('There is already another Cog with this name!')
            self.remove_cog(current)

        cog = cog._inject(self)
        self.__add_cog_commands__(cog)


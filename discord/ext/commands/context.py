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

import shlex
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence

from ...embed import Embed
from ...file import File
from ...message import Message, Guild, TextChannel, User
from ...types import allowed_mentions

if TYPE_CHECKING:
    from .core import Command


class Context:
    """Represents a :class:`Command`' context"""

    def __init__(self, msg: Message, command_invoked_under):
        self.message = msg
        self.command: Command = command_invoked_under
        self.pargs = []

        if self.command._parser:
            try:
                pargs = self.command._parser.parse(shlex.split(msg.content))
            except Exception as err:
                print(err)
            else:
                for i in self.command._parser._parser._actions:
                    setattr(self, i.dest, getattr(pargs, i.dest, None))
                    self.pargs.append(i.dest)

    @property
    def guild_id(self) -> int:
        return int(self.from_dict['guild_id'])

    @property
    def guild(self) -> "Guild":
        if not self._guild:
            self._guild = self.message.fetch_guild()
        return self._guild

    @property
    def channel(self) -> "TextChannel":
        return self.message.channel

    @property
    def author(self) -> "User":
        return self.message.author

    def __getattribute__(self, __name: str) -> Any:
        if __name not in self.__dict__.keys():
            return None
        else:
            super.__getattribute__(self, __name)

    def send(
        self,
        content: Optional[str] = None,
        files: Optional[Sequence[File]] = None,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: List[Dict[str, Any]] = None,
        component=None,
    ):
        return self.message.send(content, files, embed, embeds, tts, allowed_mentions, components, component)

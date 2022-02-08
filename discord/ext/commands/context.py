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

from typing import TYPE_CHECKING, List, Optional, ParamSpec, TypeVar

from discord import utils

from ...message import Message
from ..cogs import Cog

if TYPE_CHECKING:
    from ...state import ConnectionState
    from .bot import Bot
    from .core import P

__all__: List[str] = ["Context"]

BotT = TypeVar("BotT", bound="Bot")
T = TypeVar("T")
CogT = TypeVar("CogT", bound="Cog")
P = ParamSpec("P")


class Context:
    def __init__(
        self,
        message: Message,
        bot: BotT,
        prefix: str,
        command = None,
        command_failed: bool = False,
    ):
        self.message = message
        self._state: ConnectionState = message.app.state
        self.bot = bot
        self.prefix = prefix
        self.command = command
        self.command_failed = command_failed

    async def invoke(
        self, command, /, *args: P.args, **kwargs: P.kwargs
    ):
        return await command(self, *args, **kwargs)

    @utils.copy_doc(Message.author)
    def author(self):
        return self.message.author

    @utils.copy_doc(Message.channel)
    def channel(self):
        return self.message.channel

    @utils.copy_doc(Message.send)
    def send(self, content: Optional[str] = None, **kwargs):
        return self.message.send(content=content, **kwargs)

    @utils.copy_doc(Message.reply)
    def reply(self, content: Optional[str] = None, **kwargs):
        return self.message.reply(content=content, **kwargs)

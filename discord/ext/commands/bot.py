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
from typing import Any, List

from ...client import CFT, Client
from ...message import Message
from .context import Context
from ...internal import dispatcher

__all__: List[str] = ["Bot"]


def when_mentioned(bot: "Bot"):
    return [f"<@bot.user.id> ", f"<@!{bot.user.id}> "]


def when_mentioned_or(bot: "Bot", *prefixes: List[str]) -> list[str]:
    r = list(prefixes)
    r = when_mentioned(bot) + r
    return r


class Bot(Client):
    def __init__(self, command_prefix: str, **kwargs):
        self.command_prefix = command_prefix
        self.commands: dict[str, Any] = {}
        self.dispatcher = dispatcher.Dispatcher(state=self.state)
        self.dispatcher.add_listener(self.processor, "on_raw_message")
        super().__init__(**kwargs)

    def get_context(self, message: Message):
        ctx = Context(
            message=message,
            bot=self,
            prefix=self.command_prefix,
        )

        if message.author.id == self.user.id:
            return
        
        return ctx
    
    async def invoke(self, context: Context, func):
        await context.command.run(context, func)
    
    async def processor(self, raw_message):
        # just made to make normal users not see the event starting.
        # has no difference otherwise
        message = Message(raw_message, self)
        
        if message.author.bot:
            return
        
        if message.content.startswith(tuple(self.command_prefix)):
            for command, func in self.commands:
                if message.content[:-len(self.command_prefix)].startswith(command):
                    ctx = self.get_context(message)
                    await self.invoke(ctx, func)
        else:
            return

    def command(self, name: str = None):
        """Register a command.

        Parameters
        ----------
        name
            The command name
        """

        def decorator(func: CFT) -> CFT:
            self.commands[name or func.__name__] = func
            return func

        return decorator
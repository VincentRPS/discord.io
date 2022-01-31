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

from typing import List, Optional

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
from rpd.cache import Embed, Guild, User
from rpd.internal.dispatcher import Dispatcher
from rpd.snowflake import Snowflakeish


class Context:
    def __init__(self, msg: dict, app):
        self._message = msg
        self.app = app
        self.channel: Snowflakeish = msg["channel_id"]

    @property
    def id(self):
        return self._message["id"]

    def guild(self):
        return Guild(id=self._message["guild_id"])

    def author(self):
        return User(usr=self._message["author"])

    async def send(
        self,
        content: str,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[bool] = False,
    ):
        await self.app.factory.create_message(
            channel=self.channel,
            content=content,
            embeds=embeds,
            tts=tts,
            allowed_mentions=allowed_mentions,
        )

    async def reply(
        self,
        content: str,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[bool] = False,
    ):
        await self.app.factory.create_message(
            channel=self.channel,
            content=content,
            embeds=embeds,
            tts=tts,
            allowed_mentions=allowed_mentions,
            message_reference={
                "message_id": self.id,
            },
        )


class Command:
    def __init__(self, app, dispatcher: Dispatcher, prefix: str, name: str):
        self.app = app
        self.dispatch = dispatcher
        self.prefix = prefix
        self.name = name

    async def callback(self, data):
        if str(data["content"]).startswith(f"{self.prefix}{self.name}"):
            return Context(self.app, data)

    def __call__(self, context: Context):
        return self.dispatch.add_listener(self.callback, "on_message")

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
"""Represents a Discord Message

ref: https://discord.dev/resources/channel
"""

from typing import List, Optional, Sequence

from discord.components.core import Button
from discord.file import File
from discord.snowflake import Snowflakeish
from discord.types import allowed_mentions

from .embed import Embed
from .guild import Guild
from .user import User

__all__: List[str] = ["Message"]

# makes message data readable.
class Message:  # noqa: ignore
    """Represents a Discord Message

    .. versionadded:: 0.6.0
    """

    def __init__(self, msg: dict, app):
        self.from_dict = msg
        self.app = app
        try:
            self.content: str = self.from_dict["content"]
        except KeyError:
            # can error out for embed only/link only messages.
            self.content: str = ""
        self.channel: Snowflakeish = msg["channel_id"]

    @property
    def id(self):
        """Returns the message id"""
        return self.from_dict["id"]

    def guild(self):
        """Returns the :class:`Guild` of the message"""
        return Guild(id=self.from_dict["guild_id"])

    def author(self) -> User:
        """Returns the :class:`User` of the message"""
        return User(usr=self.from_dict["author"])

    async def send(
        self,
        content: Optional[str] = None,
        files: Optional[Sequence[File]] = None,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: List[Button] = None,
    ):
        """Sends a message."""
        await self.app.factory.create_message(
            channel=self.channel,
            content=content,
            files=files,
            embeds=embeds,
            tts=tts,
            allowed_mentions=allowed_mentions,
            components=components,
        )

    async def reply(
        self,
        content: Optional[str] = None,
        files: Optional[Sequence[File]] = None,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: List[Button] = None,
    ):
        """Replys to the certain message."""
        await self.app.factory.create_message(
            channel=self.channel,
            content=content,
            files=files,
            embeds=embeds,
            tts=tts,
            allowed_mentions=allowed_mentions,
            message_reference={
                "message_id": self.id,
            },
            components=components,
        )

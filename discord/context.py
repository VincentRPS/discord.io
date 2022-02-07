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

from typing import Any, List, Optional, Sequence

from discord.embed import Embed
from discord.file import File
from discord.message import Message
from discord.types import allowed_mentions

from .embed import Embed

__all__: List[str] = ["Context"]


class Context:
    """Represents a command context

    .. versionadded:: 0.7.0

    Parameters
    ----------
    data
        A :class:`Message`
    """

    def __init__(self, data: Message):
        self.message = data

    async def send(
        self,
        content: Optional[str] = None,
        files: Optional[Sequence[File]] = None,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: List[dict[str, Any]] = None,
        component: List[dict[str, Any]] = None,
    ):
        """Sends a message to the channel which the command was invoked

        Parameters
        ----------
        content
            The message content
        files
            A :class:`Sequence` of :class:`File`
        embed
            A :class:`Embed`
        embeds
            A :class:`list` of :class:`Embed`
        tts
            Text-To-Speach
        allowed_mentions
            A allowed mentions object
        components
            A list of component :class:`dict`s
            or :class:`Button`
        """
        emb = None
        if embed and not embeds:
            if isinstance(embed, Embed):
                emb = [embed.obj]
            else:
                emb = [embed]
        elif embed and embed:
            raise TypeError("Used both `embed` and `embed` only 1 is allowed.")
        elif embeds and not embed:
            try:
                emb = [embed.obj for embed in embeds]
            except:
                emb = embeds
        if component:
            cm = [component]
        elif components:
            cm = components
        else:
            cm = None
        await self.message.app.factory.create_message(
            channel=self.message.channel,
            content=content,
            files=files,
            embeds=emb,
            tts=tts,
            allowed_mentions=allowed_mentions,
            components=cm,
        )

    async def reply(
        self,
        content: Optional[str] = None,
        files: Optional[Sequence[File]] = None,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: List[dict[str, Any]] = None,
        component: List[dict[str, Any]] = None,
    ):
        """Replys to the message which invoked the command

        Parameters
        ----------
        content
            The message content
        files
            A :class:`Sequence` of :class:`File`
        embed
            A :class:`Embed`
        embeds
            A :class:`list` of :class:`Embed`
        tts
            Text-To-Speach
        allowed_mentions
            A allowed mentions object
        components
            A list of component :class:`dict`s
            or :class:`Button`
        """
        emb = None
        if embed and not embeds:
            if isinstance(embed, Embed):
                emb = [embed.obj]
            else:
                emb = [embed]
        elif embed and embed:
            raise TypeError("Used both `embed` and `embed` only 1 is allowed.")
        elif embeds and not embed:
            try:
                emb = [embed.obj for embed in embeds]
            except:
                emb = embeds
        if component:
            cm = [component]
        elif components:
            cm = components
        else:
            cm = None
        await self.message.app.factory.create_message(
            channel=self.message.channel,
            content=content,
            files=files,
            embeds=emb,
            tts=tts,
            allowed_mentions=allowed_mentions,
            message_reference={
                "message_id": self.message.id,
            },
            components=cm,
        )

    @property
    def author(self):
        return self.message.author

    @property
    def guild(self):
        return self.message.guild

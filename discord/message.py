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

import asyncio
from typing import Any, List, Optional, Sequence

from discord.file import File
from discord.types import allowed_mentions

from .channels import TextChannel
from .embed import Embed
from .guild import Guild
from .user import User

__all__: List[str] = ['Message']

# makes message data readable.
class Message:  # noqa: ignore
    """Represents a Discord Message

    .. versionadded:: 0.6.0

    Parameters
    ----------
    msg
        The message in dict format
    app
        The current :class:`Client`

    Attributes
    ----------
    from_dict
        A dict object of the message
    content
        The message content in string format
    channel
        The channel where the message happened
    """

    def __init__(self, msg: dict, app):
        self.from_dict = msg
        self.app = app
        try:
            self.content: str = self.from_dict['content']
        except KeyError:
            # can error out for embed only/link only messages.
            self.content: str = ''

    def __repr__(self):
        return f'<Message id={self.id!r}, Channel id={self.channel.id!r}>'

    @property
    def channel(self):
        """Returns the channel which this message took place in.

        Returns
        -------
        :class:`TextChannel`
        """
        raw = self.app.state.channels.get(self.from_dict['channel_id'])
        return TextChannel(raw, self.app.state)

    @property
    def id(self) -> int:
        """Returns the message id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def guild(self):
        """Returns the :class:`Guild` of the message

        Returns
        -------
        :class:`Guild`
        """
        return Guild(id=self.from_dict['guild_id'], rest_factory=self.app.factory)

    @property
    def author(self) -> User:
        """Returns the :class:`User` of the message

        Returns
        -------
        :class:`User`
        """
        return User(self.from_dict['author'])

    async def send(
        self,
        content: Optional[str] = None,
        files: Optional[Sequence[File]] = None,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: List[dict[str, Any]] = None,
        component=None,
    ):
        """Sends a message to the channel currently active in

        Parameters
        ----------
        content
            The message content
        files
            The message files
        embed
            A :class:`Embed`
        embeds
            A :class:`list` of :class:`Embed`
        tts
            A :class:`bool` of if tts should be on in this message
        allowed_mentions
            A allowed mentions object
        components
            A :class:`list` of components
        """
        emb = None
        com = None
        if embed and not embeds:
            if isinstance(embed, Embed):
                emb = [embed.obj]
            else:
                emb = [embed]
        elif embed and embed:
            raise TypeError('Used both `embed` and `embed` only 1 is allowed.')
        elif embeds and not embed:
            if isinstance(embeds, Embed):
                emb = [embed.obj for embed in embeds]
            else:
                emb = embeds
        if component:
            com = [component]
        if components:
            com = components
        await self.app.factory.create_message(
            channel=self.channel.id,
            content=content,
            files=files,
            embeds=emb,
            tts=tts,
            allowed_mentions=allowed_mentions,
            components=com,
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
        component: dict[str, Any] = None,
    ):
        """Replys to the current message

        Parameters
        ----------
        content
            The message content
        files
            The message files
        embed
            A :class:`Embed`
        embeds
            A :class:`list` of :class:`Embed`
        tts
            A :class:`bool` of if tts should be on in this message
        allowed_mentions
            A allowed mentions object
        components
            A :class:`list` of components
        """
        emb = None
        com = None
        if embed and not embeds:
            if isinstance(embed, Embed):
                emb = [embed.obj]
            else:
                emb = [embed]
        elif embed and embed:
            raise TypeError('Used both `embed` and `embed` only 1 is allowed.')
        elif embeds and not embed:
            if isinstance(embeds, Embed):
                emb = [embed.obj for embed in embeds]
            else:
                emb = embeds
        if component:
            com = [component]
        if components:
            com = components
        await self.app.factory.create_message(
            channel=self.channel.id,
            content=content,
            files=files,
            embeds=emb,
            tts=tts,
            allowed_mentions=allowed_mentions,
            message_reference={
                'message_id': self.id,
            },
            components=com,
        )

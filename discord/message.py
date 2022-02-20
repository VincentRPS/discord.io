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

from typing import Any, Dict, List, Optional, Sequence

from discord.file import File
from discord.types import allowed_mentions, embed_parse

from .assets import Attachment
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
        self.content: str = self.from_dict.get('content', '')

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

    def fetch_guild(self) -> Guild:
        """Returns the :class:`Guild` of the message

        Returns
        -------
        :class:`Guild`
        """
        raw = self.app.state.guilds.get(self.from_dict['guild_id'])
        return Guild(raw, rest_factory=self.app.factory)

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
        components: List[Dict[str, Any]] = None,
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
            emb = [embed.obj for embed in embeds]
        if component:
            com = [component]
        if components:
            com = components
        r = await self.app.factory.channels.create_message(
            channel=self.channel.id,
            content=content,
            files=files,
            embeds=emb,
            tts=tts,
            allowed_mentions=allowed_mentions,
            components=com,
        )

        return Message(r, self.app)

    async def reply(
        self,
        content: Optional[str] = None,
        files: Optional[Sequence[File]] = None,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        tts: Optional[bool] = False,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: List[Dict[str, Any]] = None,
        component: Dict[str, Any] = None,
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
            emb = [embed.obj for embed in embeds]
        if component:
            com = [component]
        if components:
            com = components
        r = await self.app.factory.channels.create_message(
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
        return Message(r, self.app)

    def edit(
        self,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        embed: Optional[Embed] = None,
        flags: Optional[int] = None,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: Optional[List[dict]] = None,
        files: Optional[Sequence[File]] = None,
        attachments: Optional[List[Attachment]] = None,
    ):
        """Edits the current message"""
        emd = {}
        if embeds:
            emd = embed_parse.parse_embeds(embeds)
        elif embed:
            emd = embed_parse.parse_embed(embed)
        return self.app.factory.channels.edit_message(
            channel=self.channel.id,
            message=self.id,
            content=content,
            embeds=emd,
            flags=flags,
            allowed_mentions=allowed_mentions,
            components=components,
            files=files,
            attachments=attachments,
        )

    async def delete(self, reason: Optional[str] = None):
        return self.app.factory.channels.delete_message(
            channel=self.channel.id, message=self.id, reason=reason
        )

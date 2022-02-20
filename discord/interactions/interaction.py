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
from typing import TYPE_CHECKING, Any, List, Optional

from discord.types import allowed_mentions
from discord.user import User

from ..api.rest import Route
from ..embed import Embed
from ..member import Member
from ..message import Message
from ..types import Dict, embed_parse
from ..webhooks import WebhookAdapter

if TYPE_CHECKING:
    from ..state import ConnectionState

__all__: List[str] = ['Interaction']


class Interaction:
    """Represents a Discord Interaction & Interaction Response

    Parameters
    ----------
    data
        The interaction data
    state
        The connection state

    Attributes
    ----------
    webhook
        A :class:`Webhook`
    token
        The interaction token
    type
        The interaction type
    guild_id
        The interaction guild id
    channel_id
        The interaction channel id
    data
        The interaction data
    id
        The interaction id
    message
        The interaction message

        .. note::

            This only appears on Component interactions.
    """

    def __init__(self, data: Dict, state):
        self.data = data
        self.state: ConnectionState = state
        self._responded: bool = False
        self.collect_children(data)

    def collect_children(self, data):
        # collects the data
        self.token: str = data['token']
        self.type: int = data['type']
        self.guild_id: int = data['guild_id']
        self.channel_id: int = data['channel_id']
        self.data: Dict = data['data']
        self.id: int = data['id']

        try:
            self.options = data['data']['options']
        except KeyError:
            self.options = None

        try:
            self.modals = data['data']['components']
        except KeyError:
            self.modals = None

        try:
            # buttons will give this data
            self.message = Message(data['message'], self.state.app)
        except KeyError:
            self.message = None

    def followup(
        self,
        content: Optional[str] = None,
        tts: bool = False,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
    ):
        """Followup a defered interaction.

        Parameters
        ----------
        content
            The message content
        tts
            Text-To-Speach
        embed
            A :class:`Embed` object or :class:`dict`
        embeds
            A :class:`list` of :class:`Embed` or :class:`dict`
        allowed_mentions
            A allowed mentions object

        Returns
        -------
        :meth:`Webhook.execute`
        """
        adapter = WebhookAdapter(self.state)
        return adapter.execute(
            id=self.state._bot_id,
            token=self.token,
            content=content,
            tts=tts,
            embed=embed,
            embeds=embeds,
            flags=self.invisable,
        )

    def respond(
        self,
        content: Optional[str] = None,
        modal: Optional[Dict[str, Any]] = None,
        tts: bool = False,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        type: Optional[int] = 4,
        invisable: Optional[bool] = False,
    ):
        """Send a response to a interaction

        Parameters
        ----------
        content
            The message content
        tts
            Text-To-Speach
        embed
            A :class:`Embed` object or :class:`dict`
        embeds
            A :class:`list` of :class:`Embed` or :class:`dict`
        allowed_mentions
            A allowed mentions object
        type
            The interaction type
        invisable
            If the interaction should only be seeable by the invoker.
        """
        if self._responded:
            return self.followup(
                content=content,
                tts=tts,
                embed=embed,
                embeds=embeds,
            )

        ret = {'type': type, 'data': {}}
        if content:
            ret['data']['content'] = content
        ret['data']['tts'] = tts
        if embed:
            emb = embed_parse.parse_embed(embed)
        if embeds:
            emb = embed_parse.parse_embeds(embeds)

        if not embeds and not embed:
            emb = []

        if allowed_mentions:
            ret['data']['allowed_mentions'] = allowed_mentions
        else:
            ret['data']['allowed_mentions'] = {'parse': []}

        if invisable:
            ret['data']['flags'] = 1 << 6
            self.invisable = 1 << 6
        else:
            self.invisable = None

        ret['data']['embeds'] = emb

        if modal:
            ret = {'type': 9, 'data': modal}

        adapter = WebhookAdapter(self.state)
        self._responded = True
        return adapter.rest.send(
            Route('POST', f'/interactions/{self.id}/{self.token}/callback'), json=ret
        )

    def defer(self, invisable: bool = False):
        """defers an interaction response

        Returns
        -------
        An empty :meth:`Interaction.respond`
        """

        return self.respond(type=5, invisable=invisable)

    @property
    def member(self):
        """Returns the member object of the invoker.

        Returns
        -------
        :class:`Member`
        """
        return Member(self.data['member'], self.state.app.factory)

    def send(self, content: Optional[str] = None, **kwargs):
        """Shorthand for :meth:`Interaction.respond`

        .. versionadded:: 1.0
        """
        return self.respond(content, **kwargs)

    @property
    def author(self) -> User:
        return User(self.data.get('message')['author'])

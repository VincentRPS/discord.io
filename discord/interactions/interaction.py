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
from typing import TYPE_CHECKING, List, Optional

from discord.types import allowed_mentions

from ..api.rest import Route
from ..embed import Embed
from ..member import Member
from ..types import Dict, embed_parse
from ..webhooks import Webhook

if TYPE_CHECKING:
    from ..state import ConnectionState


class Interaction:
    def __init__(self, data: Dict, state):
        self.data = data
        self.state: ConnectionState = state
        self.webhook = Webhook(data["id"], data["token"])
        self.collect_children(data)

    def collect_children(self, data):
        # collects the data
        self.token: str = data["token"]
        self.type: int = data["type"]
        self.guild_id: int = data["guild_id"]
        self.channel_id: int = data["channel_id"]
        self.data: Dict = data["data"]
        self.id: int = data["id"]

        try:
            # buttons will give this data
            self.message = data["message"]
        except KeyError:
            pass

    def followup(
        self,
        content: Optional[str] = None,
        tts: bool = False,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
    ):
        """Followup and interaction.
        
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
        """
        return self.webhook.execute(
            content=content, tts=tts, embed=embed, embeds=embeds
        )

    def respond(
        self,
        content: Optional[str] = None,
        tts: bool = False,
        embed: Optional[Embed] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
    ):
        """Send a initial response to a interaction

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
        """
        ret = {"type": 4, "data": {}}
        if content:
            ret["data"]["content"] = content
        ret["data"]["tts"] = tts
        if embed:
            emb = embed_parse.parse_embed(embed)
        if embeds:
            emb = embed_parse.parse_embeds(embeds)

        if not embeds and not embed:
            emb = []

        if allowed_mentions:
            ret["data"]["allowed_mentions"] = allowed_mentions
        else:
            ret["data"]["allowed_mentions"] = {"parse": []}

        ret["data"]["embeds"] = emb

        return self.webhook.rest.send(
            Route("POST", f"/interactions/{self.id}/{self.token}/callback"), json=ret
        )

    @property
    def member(self):
        """Returns the member object of the invoker."""
        return Member(self.data["member"], self.state.app.factory)

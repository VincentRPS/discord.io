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
"""Implementation of Discord Webhooks."""

import typing

from discord import utils

from .api.rest import RESTClient, Route
from .embed import Embed
from .file import File
from .snowflake import Snowflakeish

__all__: typing.List[str] = ['Webhook', 'WebhookAdapter']


class WebhookAdapter:
    """The base class for interperting Webhooks

    .. versionadded:: 0.3.0

    Parameters
    ----------
    id
        The webhook id
    token
        The webhook token

    Attributes
    ----------
    rest
        An instance of RESTClient.
    """

    def __init__(self, state):
        self.rest = RESTClient(state=state)

    def fetch_webhook(self, id, token):
        """Fetch the current Webhook from the API."""
        return self.rest.send('GET', f'/webhooks/{id}/{token}')

    def modify_webhook(
        self,
        id,
        token,
        name: typing.Optional[str] = None,
        avatar: typing.Optional[str] = None,
    ):
        """Modify the Webhook

        Parameters
        ----------
        name
            Change the name
        avatar
            Change the avatar
        """
        json = {}
        if name:
            json['name'] = name
        if avatar:
            json['avatar'] = avatar
        return self.rest.send(
            Route(
                'PATCH',
                f'/webhooks/{id}/{token}',
                webhook_id=id,
                webhook_token=token,
            ),
            json=json,
        )

    def delete_webhook(self, id, token):
        """Deletes the Webhook"""
        return self.rest.send(
            Route(
                'DELETE',
                f'/webhooks/{id}/{self.token}',
                webhook_id=id,
                webhook_token=token,
            )
        )

    def fetch_message(self, id, token, message: Snowflakeish):
        """Fetches a Webhook message."""
        return self.rest.send(
            Route(
                'GET',
                f'/webhooks/{id}/{token}/messages/{message}',
                webhook_id=id,
                webhook_token=token,
            )
        )

    def edit_message(
        self,
        id,
        token,
        message: Snowflakeish,
        content: typing.Optional[str] = None,
        allowed_mentions: typing.Optional[bool] = None,
    ):
        """Edits a Webhook message

        Parameters
        ----------
        message
            The Message ID
        content
            Change the content
        allowed_mentions
            A allowed mentions object
        """
        json = {}
        if content:
            json['content'] = content
        elif allowed_mentions:
            json['allowed_mentions'] = allowed_mentions
        return self.rest.send(
            Route(
                'POST',
                f'/webhooks/{id}/{token}/messages/{message}',
                webhook_id=id,
                webhook_token=token,
            ),
            json=json,
        )

    def delete_message(
        self,
        id,
        token,
        message: Snowflakeish,
    ):
        """Deletes a message

        Parameters
        ----------
        message
            The message to delete
        """
        return self.rest.send(
            Route(
                'DELETE',
                f'/webhooks/{id}/{token}/messages/{message}',
                webhook_id=id,
                webhook_token=token,
            )
        )

    def execute(
        self,
        id,
        token,
        content: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
        avatar_url: typing.Optional[str] = None,
        tts: typing.Optional[bool] = None,
        allowed_mentions: typing.Optional[bool] = None,
        embed: typing.Optional[Embed] = None,
        embeds: typing.Optional[typing.List[Embed]] = None,
        flags: typing.Optional[typing.Any] = None,
        files: typing.Optional[typing.Sequence[File]] = None,
    ):
        """Execute the Webhook

        Parameters
        ----------
        content: :class:`str`
            The content to send.
        username: :class:`str`
            The username the Webhook should have
        avatar_url: :class:`str`
            The avatar the Webhook should have
        tts: :class:`bool`
            If the message should have tts enabled
        allowed_mentions
            A allowed mentions object
        """
        json = {}
        if content:
            json['content'] = content
        if username:
            json['username'] = username
        if avatar_url:
            json['avatar_url'] = avatar_url
        if tts:
            json['tts'] = tts
        if allowed_mentions:
            json['allowed_mentions'] = allowed_mentions
        if embed:
            if isinstance(embed, Embed):
                emb = [embed.obj]
            else:
                emb = [embed]
        if embeds:
            if isinstance(embeds, Embed):
                emb = [embed.obj for embed in embeds]
            else:
                emb = embeds
        if embed or embeds:
            json['embeds'] = emb

        if flags:
            json['flags'] = flags

        return self.rest.send(
            Route(
                'POST',
                f'/webhooks/{id}/{token}',
                webhook_id=id,
                webhook_token=token,
            ),
            json=json,
            files=files,
        )


@utils.copy_doc(WebhookAdapter)
class Webhook:
    def __init__(self, id, token, state):
        self.id = id
        self.token = token
        self.adapter = WebhookAdapter(state)

    @utils.copy_doc(WebhookAdapter.execute)
    def execute(
        self,
        content: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
        avatar_url: typing.Optional[str] = None,
        tts: typing.Optional[bool] = None,
        allowed_mentions: typing.Optional[bool] = None,
        embed: typing.Optional[Embed] = None,
        embeds: typing.Optional[typing.List[Embed]] = None,
        flags: typing.Optional[typing.Any] = None,
        files: typing.Optional[typing.Sequence[File]] = None,
    ):
        return self.adapter.execute(
            id=self.id,
            token=self.token,
            content=content,
            username=username,
            avatar_url=avatar_url,
            tts=tts,
            allowed_mentions=allowed_mentions,
            embed=embed,
            embeds=embeds,
            flags=flags,
            files=files,
        )

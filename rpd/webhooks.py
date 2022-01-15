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

import typing
from logging import getLogger

from rpd import api
from rpd.snowflake import Snowflake

log = getLogger(__name__)


class Webhook:
    """The base class for interperting Webhooks

    .. versionadded:: 0.3.0

    Parameters
    ----------
    id
        The webhook id
    token
        The webhook token
    """

    def __init__(self, webhook_id, webhook_token):
        self.id = webhook_id
        self.token = webhook_token
        self.rest = api.RESTClient()

    def fetch_webhook(self):
        return self.request("GET", f"/{self.id}/{self.token}")

    def modify_webhook(
        self, name: typing.Optional[str] = None, avatar: typing.Optional[str] = None
    ):
        json = {}
        if name:
            json["name"] = name
        if avatar:
            json["avatar"] = avatar
        return self.rest.send("PATCH", f"/{self.id}/{self.token}", json=json)

    def delete_webhook(self):
        return self.rest.send("DELETE", f"/{self.id}/{self.token}")

    def fetch_message(self, message: Snowflake):
        return self.rest.send("GET", f"/{self.id}/{self.token}/messages/{message}")

    def edit_message(
        self,
        message: Snowflake,
        content: typing.Optional[str] = None,
        allowed_mentions: typing.Optional[bool] = None,
    ):
        json = {}
        if content:
            json["content"] = content
        elif allowed_mentions:
            json["allowed_mentions"] = allowed_mentions
        return self.rest.send(
            "POST", f"/{self.id}/{self.token}/messages/{message}", json=json
        )

    def delete_message(
        self,
        message: Snowflake,
    ):
        return self.rest.send("DELETE", f"/{self.id}/{self.token}/messages/{message}")

    def send_message(
        self,
        content: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
        avatar_url: typing.Optional[str] = None,
        tts: typing.Optional[bool] = None,
        allowed_mentions: typing.Optional[bool] = None,
    ):
        json = {}
        if content:
            json["content"] = content
        elif username:
            json["username"] = username
        elif avatar_url:
            json["avatar_url"] = avatar_url
        elif tts:
            json["tts"] = tts
        elif allowed_mentions:
            json["allowed_mentions"] = allowed_mentions
        return self.rest.send("POST", f"/{self.id}/{self.token}", json=json)

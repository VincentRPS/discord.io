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
from urllib.parse import quote

import gevent  # type: ignore
import requests

from rpd.internal.exceptions import Forbidden, NotFound, ServerError
from rpd.snowflake import Snowflake
# mypy, it does have _to_json, _from_json.
from rpd.util import _to_json  # type: ignore

log = getLogger(__name__)


# If your wondering why this is basically a remade RESTClient, This was initally made before fully rewriting to sync.
# mostly to see if speed would differ a bunch, to test gevent and to have fun.
# and now i don't wanna have to rewrite to just use RESTClient so unless you wanna make a PR it will stay like this.
class Webhook:
    # https://discord.com/developers/docs/resources/webhook
    def __init__(self, webhook_id, webhook_token):
        self.id = webhook_id
        self.token = webhook_token
        self.__session = requests.Session()
        self.header: typing.Dict[str, str] = {
            "User-Agent": "DiscordBot https://github.com/RPD-py/RPD"
        }

    # Since Webhook.send is already a function, this is request.
    def request(self, method, endpoint, **kwargs: typing.Any):
        url = "https://discord.com/api/v9/webhooks" + endpoint

        # yes this kwargs system is probably garbage and not needed, but i am too lazy to not use them this way.
        if "json" in kwargs:
            self.header["Content-Type"] = "application/json"
            kwargs["data"] = _to_json(kwargs.pop("json"))

        if "reason" in kwargs:
            self.header["X-Audit-Log-Reason"] = quote(kwargs.pop("reason"), "/ ")

        kwargs["headers"] = self.header
        with self.__session.request(method, url, **kwargs) as r:
            if r.status_code == 429:
                gevent.sleep(10)
                self.request(method, endpoint)
            elif r.status_code == 403:
                raise Forbidden(r)  # Forbidden, raise
            elif r.status_code == 404:
                raise NotFound(r)  # not found, raise
            elif r.status_code == 500:
                raise ServerError(r)  # Server Exception, raise
            else:
                log.debug("< %s", r)
                return r

    def get_webhook(self):
        return self.request("GET", f"/{self.id}/{self.token}")

    def modify_webhook(self):
        return self.request("PATCH", f"/{self.id}/{self.token}")

    def delete_webhook(self):
        return self.request("DELETE", f"/{self.id}/{self.token}")

    def get_webhook_message(self, message: Snowflake):
        return self.request("GET", f"/{self.id}/{self.token}/messages/{message}")

    def edit_webhook_message(
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
        return self.request(
            "POST", f"/{self.id}/{self.token}/messages/{message}", json=json
        )

    def delete_webhook_message(
        self,
        message: Snowflake,
    ):
        return self.request("DELETE", f"/{self.id}/{self.token}/messages/{message}")

    def send(
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
        return self.request("POST", f"/{self.id}/{self.token}", json=json)

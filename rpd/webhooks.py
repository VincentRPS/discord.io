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

import asyncio
import typing
from logging import getLogger
from urllib.parse import quote

import aiohttp

from rpd.internal.exceptions import Forbidden, NotFound, ServerError
from rpd.snowflake import Snowflake

# mypy, it does have _to_json, _from_json.
from rpd.util import _to_json  # type: ignore

log = getLogger(__name__)


# I plan on moving a lot of this logic to RESTFactory & RESTApp.
class Webhook:
    # https://discord.com/developers/docs/resources/webhook
    def __init__(self, webhook_id, webhook_token):
        self.id = webhook_id
        self.token = webhook_token
        self.__session = aiohttp.ClientSession()
        self.header: typing.Dict[str, str] = {
            "User-Agent": "DiscordBot https://github.com/RPD-py/RPD"
        }

    # Since Webhook.send is already a function, this is request.
    async def request(self, method, endpoint, **kwargs: typing.Any):
        url = "https://discord.com/api/v9/webhooks" + endpoint

        # yes this kwargs system is probably garbage and not needed, but i am too lazy to not use them this way.
        if "json" in kwargs:
            self.header["Content-Type"] = "application/json"
            kwargs["data"] = _to_json(kwargs.pop("json"))

        if "reason" in kwargs:
            self.header["X-Audit-Log-Reason"] = quote(kwargs.pop("reason"), "/ ")

        kwargs["headers"] = self.header
        async with self.__session.request(method, url, **kwargs) as r:
            if r.status_code == 429:
                await asyncio.sleep(10)
                await self.request(method, endpoint)
            elif r.status == 403:
                raise Forbidden(r)  # Forbidden, raise
            elif r.status == 404:
                raise NotFound(r)  # Not found, raise
            elif r.status == 500:
                raise ServerError(r)  # Server Exception, raise
            else:
                log.debug("< %s", r)
                return r

    async def fetch_webhook(self):
        return await self.request("GET", f"/{self.id}/{self.token}")

    async def modify_webhook(
        self, name: typing.Optional[str] = None, avatar: typing.Optional[str] = None
    ):
        json = {}
        if name:
            json["name"] = name
        if avatar:
            json["avatar"] = avatar
        return await self.request("PATCH", f"/{self.id}/{self.token}", json=json)

    async def delete_webhook(self):
        return await self.request("DELETE", f"/{self.id}/{self.token}")

    async def fetch_message(self, message: Snowflake):
        return await self.request("GET", f"/{self.id}/{self.token}/messages/{message}")

    async def edit_message(
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

    async def delete_message(
        self,
        message: Snowflake,
    ):
        return await self.request(
            "DELETE", f"/{self.id}/{self.token}/messages/{message}"
        )

    async def send_message(
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
        return await self.request("POST", f"/{self.id}/{self.token}", json=json)

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
from __future__ import annotations

import asyncio
import logging
import typing

import aiohttp

from ..helpers.whichjson import _to_json
from .aioclient import CreateClientSession

_log = logging.getLogger(__name__)

__all__: typing.List[str] = [
    "RESTClient",
]


class RESTClient:
    """REST Implementation for RPD.

    .. versionadded:: 0.3.0

    Attributes
    ----------
    url
        The Discord API URL
    loop
        The current event loop or your own.
    connector
        The base aiohttp connector
    _session
        The aiohttp ClientSession
    header
        The header sent to discord.
    """

    def __init__(self, loop=None):
        self.url = "https://discord.com/api/v9"  # The Discord API Version.
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.connector = aiohttp.BaseConnector(
            loop=self.loop
        )  # defining our own connector would allow for more flexability.
        self._session = CreateClientSession()
        self.header: typing.Dict[str, str] = {
            "User-Agent": "DiscordBot https://github.com/RPD-py/RPD"
        }

    async def send(self, method, endpoint, **kwargs: typing.Any):
        """Sends a request to discord

        .. versionadded:: 0.3.0
        """
        self.method = method  # The method you are trying to use. e.g. GET.
        self.endpoint = endpoint  # The endpoint the method is in.
        url = self.url + self.endpoint  # The URL. + Endpoint.

        if "json" in kwargs:
            self.header["Content-Type"] = "application/json"  # Only json.
            kwargs["data"] = _to_json(kwargs.pop("json"))

        kwargs["headers"] = self.header

        try:
            await self._session.request(self.method, url, **kwargs)

        except Exception as exc:
            raise Exception(f"Exception Occured when trying to send a request. {exc}")

    async def close(self) -> None:
        if self._session:
            await self._session.close()  # Closes the session

    async def _client_login(self, token: str) -> None:
        self.token = token

        if len(self.token) != 59:
            raise Exception("Invalid Bot Token Was Passed")
        else:
            self.header["Authorization"] = "Bot " + self.token

        try:
            await self.send("GET", "/users/@me")  # Log's in
        except Exception as exc:
            raise Exception(f"Failed to login {exc}")  # If exception raise.

    async def _client_logout(self) -> None:
        await self.send("POST", "/auth/logout")  # Log's you out of the bot.

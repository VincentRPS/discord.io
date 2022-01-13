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
import random
import typing

import aiohttp

from rpd.ext import _to_json  # type: ignore

from .aioclient import CreateClientSession, ClientResponseErrors
from urllib.parse import quote

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
        self.loop = asyncio.get_running_loop() if loop is None else loop
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

        elif "token" in kwargs:
            self.header["Authorization"] = "Bot " + kwargs.pop("token")

        elif "reason" in kwargs:
            self.header["X-Audit-Log-Reason"] = quote(kwargs.pop("reason"), "/ ")

        kwargs["headers"] = self.header

        try:
            _log.debug("Sending a request...")
            async with self._session.request(self.method, url, **kwargs) as r:
                if r.status == 429:  # "Handles" Ratelimit's or 429s.
                    retries: int = random.randint(1, 90)
                    _log.critical(
                        "Detected a possible ratelimit, RPD will try to reconnect every 30 seconds."
                    )

                    for tries in retries:
                        await asyncio.sleep(
                            random.randint(1, 20)
                        )  # Need some better alternative to this, Then reconnect every 30s
                        self.send(method, endpoint, **kwargs)
                else:
                    await ClientResponseErrors(r)

        except Exception as exc:
            raise Exception(f"Exception Occured when trying to send a request. {exc}")

    async def close(self) -> None:
        if self._session:
            await self._session.close()  # Closes the session

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
from urllib.parse import quote

import aiohttp

from rpd.internal.exceptions import Forbidden, NotFound, ServerError
from rpd.util import _to_json  # type: ignore

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
    header
        The header sent to discord.
    """

    def __init__(self):
        self.url = "https://discord.com/api/v9"  # The Discord API Version.
        self.header: typing.Dict[str, str] = {
            "User-Agent": "DiscordBot https://github.com/RPD-py/RPD"
        }

    async def send(self, method, endpoint, **kwargs: typing.Any):
        """Sends a request to discord

        .. versionadded:: 0.3.0
        """
        self._session = aiohttp.ClientSession()
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
            _log.debug("< %s, %s", method, endpoint)
            async with self._session.request(self.method, url, **kwargs) as r:
                if r.status == 429:  # "Handles" Ratelimit's or 429s.
                    _log.critical("Detected a possible ratelimit, Handling...")

                    await asyncio.sleep(random.randint(1, 20))
                    await self.send(method, endpoint, **kwargs)
                elif r.status == 403:
                    raise Forbidden(r)
                elif r.status == 404:
                    raise NotFound(r)
                elif r.status == 500:
                    raise ServerError(r)
                else:
                    _log.debug("< %s", r)

        except Exception as exc:
            raise Exception(f"Exception Occured when trying to send a request. {exc}")

    async def close(self) -> None:
        if self._session:
            await self._session.close()  # Closes the session

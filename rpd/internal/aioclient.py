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
import logging

import aiohttp

from ..exceptions import Forbidden, NotFound, RESTError, ServerError
from .websockets import DiscordClientWebSocketResponse

_log = logging.getLogger(__name__)


class RESTClientResponse(aiohttp.ClientResponse):
    """A subclass of :class:`aiohttp.ClientResponse` built for RPD"""
    # Handles HTTPExceptions while doing REST Requests.
    async def ClientResponseErrors(self) -> RESTError:
        if 300 > self.status >= 200:
            _log.debug(f"Request was sucessfully sent, {self}")

        elif self.status == 429:  # "Handles" Ratelimit's or 429s.
            _log.critical(
                'Detected a possible ratelimit, RPD will try to reconnect every 30 seconds.'
            )


            await asyncio.sleep(
                30
            )  # Need some better alternative to this, Then reconnect every 30s

        elif self.status in {500, 502, 504}:
            await asyncio.sleep(7)

        elif self.status == 403:
            raise Forbidden(self)  # type: ignore
        elif self.status == 404:
            raise NotFound(self)  # type: ignore
        elif self.status >= 500:
            raise ServerError(self)  # type: ignore
        else:  # Handles any exception not covered here.
            raise RESTError(self)  # type: ignore
        # mypy doesn't like us returning nothing for some reason, maybe return self?
        return # type: ignore


def CreateClientSession(  # makes creating ClientSessions way easier.
    connector: aiohttp.BaseConnector,
    connector_owner: bool = False,
    trust_env: bool = True,
    loop=None,
) -> aiohttp.ClientSession:
    rloop = asyncio.get_event_loop() or loop
    return aiohttp.ClientSession(
        connector=connector,
        connector_owner=connector_owner,
        loop=rloop,
        ws_response_class=DiscordClientWebSocketResponse,
        trust_env=trust_env,
        version=aiohttp.HttpVersion11,
        response_class=RESTClientResponse,
    )

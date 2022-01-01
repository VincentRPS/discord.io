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

from .websockets import DiscordClientWebSocketResponse
from ..exceptions import RESTError, Forbidden, NotFound, ServerError

_log = logging.getLogger(__name__)

# Handles HTTPExceptions while doing REST Requests.
async def RESTClientResponse(r: aiohttp.ClientResponse) -> RESTError:
        if 300 > r.status >= 200:
                    _log.debug(f"Request was sucessfully sent, {r}")

        if r.status == 429:  # "Handles" Ratelimit's or 429s.
                    _log.critical(
                        f"Detected a possible ratelimit, RPD will try to reconnect every 30 seconds."
                    )

                    await asyncio.sleep(30)  # Need some better alternative to this, Then reconnect every 30s

        if r.status in {500, 502, 504}:
                    await asyncio.sleep(7)

        if r.status == 403:  # 403 Errors.
                    raise Forbidden(r)
        if r.status == 404:  # 404 Errors.
                    raise NotFound(r)
        if r.status >= 500:  # 500 Errors.
                    raise ServerError(r)
        else:  # Handles any exception not covered here.
                    raise RESTError(r)

def CreateClientSession( # makes creating ClientSessions way easier.
    connector: aiohttp.BaseConnector,
    connector_owner: bool = False,
    trust_env: bool = True,
    loop=None

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



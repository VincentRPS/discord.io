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
from typing import Any, Coroutine, Union

import aiohttp

from ..api.rest import RESTClient, Route
from ..state import ConnectionState
from .channels import Channels
from .commands import Commands
from .guilds import Guilds


class RESTFactory:
    """The RESTFactory for most requests.

    .. versionadded:: 0.3.0

    Attributes
    ----------
    rest
        The RESTClient.
    """

    def __init__(
        self,
        *,
        state: typing.Optional[ConnectionState] = None,
        proxy: typing.Optional[str] = None,
        proxy_auth: typing.Optional[str] = None,
        version=10,
    ):
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.state = state or ConnectionState()
        self.rest = RESTClient(
            state=self.state, proxy=proxy, proxy_auth=proxy_auth, version=version
        )
        self.channels = Channels(self.rest)
        self.commands = Commands(self.rest)
        self.guilds = Guilds(self.rest)

    async def login(
        self, token: str
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        self.token = token

        if len(self.token) != 59:
            raise Exception('Invalid Bot Token Was Passed')
        else:
            pass

        r = await self.rest.send(Route('GET', '/users/@me'), token=self.token)

        self.state.bot_info[self.state.app] = r

        return r

    def logout(
        self,
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        return self.rest.send(
            Route('POST', '/auth/logout')
        )  # Log's you out of the bot.

    def get_gateway_bot(
        self,
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        return self.rest.send(Route('GET', '/gateway/bot'))

    async def ws_connect(self, url: str, *, compress: int = 0):
        kwargs = {
            'proxy_auth': self.proxy_auth,
            'proxy': self.proxy,
            'max_msg_size': 0,
            'timeout': 30.0,
            'autoclose': False,
            'headers': {
                'User-Agent': self.rest.user_agent,
            },
            'compress': compress,
        }

        sesh = aiohttp.ClientSession()
        return await sesh.ws_connect(url, **kwargs)

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

from rpd.api import RESTFactory
from rpd.api.gateway import Gateway
from rpd.state import ConnectionState

_log = logging.getLogger(__name__)


def loopu():
    try:
        o = asyncio.get_running_loop()
    except RuntimeError:
        o = asyncio.new_event_loop()

    return o


class BotApp:
    """Represents a Discord bot.

    .. versionadded:: 0.4.0

    Attributes
    ----------
    factory
        The instance of RESTFactory
    state
        The client's connection state
    """

    def __init__(self, **options):
        self.factory = RESTFactory()
        self.state = ConnectionState(loop=loopu())
        self.gateway = Gateway(state=self.state)
        self.ops = options
        self._got_gateway_bot: bool = False

    def login(self):
        """Starts the bot connection

        .. versionadded:: 0.4.0

        """
        return self.factory.login

    async def connect(self):
        """Starts the WebSocket(Gateway) connection with Discord.

        .. versionadded:: 0.4.0
        """
        if self._got_gateway_bot is False:
            await self.factory.get_gateway_bot()

        return self.gateway.connect()

    async def start(self, token):
        """A function to start both the REST & Gateway Connection."""
        await self.login(token)
        await self.connect()

    def run(self, token):
        """A blocking function to start your bot"""

        async def runner():
            await self.start(token)

        def stop(f):
            self.state.loop.stop()

        future = asyncio.ensure_future(runner(), loop=self.state.loop)
        future.add_done_callback(stop)
        try:
            self.state.loop.run_forever()
        except KeyboardInterrupt:
            print("Received request to kill the bot process.")
        finally:
            future.remove_done_callback(stop)

        if not future.cancelled():
            try:
                return future.result()
            except KeyboardInterrupt:
                return None

    @property
    async def is_ready(self):
        """Returns if the bot is ready or not."""
        return self.state._ready.is_set()

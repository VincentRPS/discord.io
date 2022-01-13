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

# Most requests are done here, except for log-ins and outs since they change the header.

import typing
from rpd.internal.rest import RESTClient
from rpd.snowflake import Snowflake

__all__: typing.List[str] = [
    "RESTFactory",
]


class RESTFactory:
    """The RESTFactory for most requests.

    .. versionadded:: 0.3.0

    Attributes
    ----------
    rest
        The RESTClient.
    """

    def __init__(self):
        self.rest = RESTClient()

    async def login(self, token: str) -> None:
        self.token = token

        if len(self.token) != 59:
            raise Exception("Invalid Bot Token Was Passed")
        else:
            pass

        await self.rest.send("GET", "/users/@me", token=self.token)  # Log's in

    async def logout(self) -> None:
        await self.rest.send("POST", "/auth/logout")  # Log's you out of the bot.

    async def get_gateway_bot(self) -> None:
        return await self.rest.send(
            "GET", "/gateway/bot"
        )  # GET's the bot from the gateway endpoint

    def get_channel(self, channel: Snowflake):
        return self.rest.send("GET", f"/channels/{channel}")
    
    def edit_channel(self, name: str, channel: Snowflake, type):
        if type == "group_dm":
            payload = {}
            if name:
                payload["name"] = name
        return self.rest.send("PATCH", f"/channels/{channel}")
    
    def create_invite(
        self, 
        channel_id: Snowflake,
        *,
        reason: typing.Optional[str] = None,
        max_age: int = 0,
        max_uses: int = 0,
        tempoary: bool = False,
        unique: bool = True,
        ):
        payload = {
            "max_age": max_age,
            "max_uses": max_uses,
            "tempoary": tempoary,
            "unique": unique,
        }
        # return self.send("", reason=reason, json=payload)
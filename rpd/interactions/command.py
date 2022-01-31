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
from rpd.api.rest_factory import RESTFactory
from rpd.snowflake import SnowflakeishList
from rpd.state import ConnectionState
from .option import SlashOption
from typing import List


class Command:
    def __init__(
        self,
        state: ConnectionState,
        factory: RESTFactory,
        slash_command: bool = False,
        message_command: bool = False,
        user_command: bool = False,
    ):
        self.state = state
        self.factory = factory
        self._s = slash_command
        self._m = message_command
        self._u = user_command

    async def slash_callback(
        self, 
        name: str,
        options: List[SlashOption],
        description: str = None,
        guild_ids: SnowflakeishList = None,
        default_permission: bool = True
    ):
        if guild_ids > 1:
            raise NotImplementedError
        if guild_ids is not None:
            return await self.factory.create_guild_application_command(
                application_id=self.state._bot_id, 
                guild_id=guild_ids, 
                name=name, 
                description=description, 
                options=options, 
                default_permission=default_permission, 
                type="CHAT_INPUT"
            )

    def message_callback(self):
        ...

    def user_callback(self):
        ...

    def __call__(
        self,
        name: str,
        options: SlashOption,
        description: str = None,
        guild_ids: SnowflakeishList = None,
        default_permission: bool = True
    ):
        if self._s is True:
            self.state.loop.create_task(self.slash_callback(
                name=name,
                options=options,
                description=description,
                guild_ids=guild_ids,
                default_permission=default_permission
            ))
        elif self._m is True:
            return self.message_callback
        elif self._u is True:
            return self.user_callback

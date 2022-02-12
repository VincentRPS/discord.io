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
from typing import Any, Callable, Coroutine, List, Optional

from aio.types.dict import Dict

from ..internal.dispatcher import Dispatcher
from ..state import ConnectionState
from .interaction import Interaction

__all__: List[str] = ['ApplicationCommandRegistry']


class ApplicationCommandRegistry:
    """Handles registration of application commands."""

    def __init__(self, rest_factory, state: ConnectionState):
        self.factory = rest_factory
        self.state = state
        self.dispatcher = Dispatcher(state=self.state)
        self.state.loop.create_task(self.on_ready())
        self.unregistered_commands: asyncio.Event = asyncio.Event()

    async def run(
        self, coro: Callable[..., Coroutine[Any, Any, Any]], data, state, cog=None
    ) -> None:
        try:
            if cog:
                i = Interaction(data, state)
                await coro(cog, i)
            else:
                i = Interaction(data, state)
                await coro(i)
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

    async def on_ready(self):
        await asyncio.sleep(20)
        glob = await self.factory.get_global_application_commands(self.state._bot_id)

        await self.check_application_commands(glob)

        await asyncio.sleep(10)

        for guild in self.state.guilds._cache.values():
            commands = await self.factory.get_guild_application_commands(
                self.state._bot_id, guild['id']
            )
            for command in commands:
                if command not in self.state.application_commands.items():
                    await self.factory.delete_guild_application_command(
                        self.state._bot_id, guild['id'], command['id']
                    )
        self.unregistered_commands.set()

    async def check_application_commands(self, rglobal):
        for command in rglobal:
            await self.factory.delete_global_application_command(
                self.state._bot_id, command['id']
            )

    async def register_guild_slash_command(
        self,
        guild_id,
        name,
        description,
        callback,
        cog: Any = None,
        options: Optional[List[Dict]] = None,
        default_permission: bool = True,
    ) -> dict:
        if not self.unregistered_commands.is_set():
            await self.unregistered_commands.wait()
        r = await self.factory.create_guild_application_command(
            self.state._bot_id,
            guild_id,
            name,
            description,
            options,
            default_permission,
            type=1,
        )
        self.state.application_commands[name] = {
            'd': r,
            'callback': callback,
            'self': self,
            'cog': cog,
        }
        return r

    async def register_global_slash_command(
        self,
        name,
        description,
        callback,
        cog: Any = None,
        options: Optional[List[Dict]] = None,
        default_permission: bool = True,
    ) -> dict:
        if not self.unregistered_commands.is_set():
            await self.unregistered_commands.wait()
        r = await self.factory.create_global_application_command(
            self.state._bot_id, name, description, options, default_permission, type=1
        )
        self.state.application_commands[name] = {
            'd': r,
            'callback': callback,
            'self': self,
            'cog': cog,
        }
        return r

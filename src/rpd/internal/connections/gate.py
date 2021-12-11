"""
Apache-2.0

Copyright 2021 RPS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the LICENSE file for the specific language governing permissions and
limitations under the License.
"""
from asyncio.events import AbstractEventLoop

import aiohttp


# Taken from discord.py
class DiscordClientWebSocketResponse(aiohttp.ClientWebSocketResponse):
    async def close(self, *, code: int = 4000, message: bytes = b"") -> bool:
        return await super().close(code=code, message=message)


# Based Upon Speedcords Impl
class OpcodeDispatch:
    """Dispatches Opcodes"""

    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop
        self.event_handlers = {}

    def dispatch(self, opcode, *args, **kwargs):
        """Dispatch's Opcode Events"""
        for event in self.event_handlers.get(opcode, []):
            self.loop.create_task(event(*args, **kwargs))

    def register(self, opcode, func):
        """Registers Opcode Events"""
        event_handlers = self.event_handlers.get(opcode, [])
        event_handlers.append(func)
        self.event_handlers[opcode] = event_handlers


class EventDispatch:
    """Dispatches Events"""

    def __init__(self, loop: AbstractEventLoop):
        self.loop = loop
        self.event_handlers = {}

    def dispatch(self, my_event, *args, **kwargs):
        """Dispatch's Opcode Events"""
        for event in self.event_handlers.get(my_event, []):
            self.loop.create_task(event(*args, **kwargs))

    def register(self, my_event, func):
        """Registers Opcode Events"""
        event_handlers = self.event_handlers.get(my_event, [])
        event_handlers.append(func)
        self.event_handlers[my_event] = event_handlers

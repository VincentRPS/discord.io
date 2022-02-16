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
"""
Manages events given by discord
"""
import asyncio
import inspect
import logging
from collections import OrderedDict
from typing import Any, Dict, Callable, Coroutine, Optional
import uuid
from ..state import ConnectionState
from ..events import core

_log = logging.getLogger('discord.EventManager')

class EventManager:
    # this is a rewrite of the dispatcher made to make events class based from now on.
    def __init__(self, state: ConnectionState):
        self.state = state
        self.events: Dict[str, core.Event2] = {}
    
    async def run(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        cog,
        one_shot: bool,
        event,
    ) -> None:
        if one_shot:
            delattr(self, name)
        try:
            if cog:
                await coro(cog, event)
            else:
                await coro(event)
        except asyncio.CancelledError:
            pass
        except Exception:
            raise

    def scheduler(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        name: str,
        cog: Any,
        one_shot: bool,
        event,
    ) -> asyncio.Task:
        wrap = self.run(coro, name, cog, one_shot, event)
        return self.state.loop.create_task(wrap, name=f'discord.io: {name}')
    
    def _dispatch(self, name: str, data: Dict):
        for key, event in self.events.items():
            if event.parent == name.lower():
                try:
                    coro = getattr(self, name)
                except AttributeError:
                    return
                else:
                    self.scheduler(coro['func'], name.lower(), coro['cog'], coro['one_shot'], coro['event_cls'](data=data, state=self.state))
    
    def subscribe(self, event: Optional[core.Event2] = None, /):
        def decorator(func: Callable):
            if event is None:
                dict = OrderedDict(inspect.signature(func).parameters)
                name, param = dict.popitem(False)
                _event = param.annotation
            else:
                _event = event

            _log.info(f"Subscribing to {_event.parent}")
            if not asyncio.iscoroutinefunction(func):
                raise TypeError('Function is not a coroutine')

            setattr(self, _event.parent, {'func': func, 'cog': None, 'one_shot': False, 'event_cls': _event})
            self.events[uuid.uuid4()] = _event
            return func

        return decorator

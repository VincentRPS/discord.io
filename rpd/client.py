# MIT License

# Copyright (c) 2021 VincentRPS

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
# SOFTWARE.
from __future__ import annotations

import asyncio
import logging
import sys
import traceback
from typing import Any, Callable, Coroutine, Dict, List, Optional, Tuple, TypeVar, Union

from rpd.exceptions import deprecated
from rpd.helpers import MISSING
# from rpd.internal import HTTPClient

_log = logging.getLogger(__name__)

__all__ = "Client"

Snowflake = Union[str, int]
SnowflakeList = List[Snowflake]

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]
CFT = TypeVar("CFT", bound="CoroFunc")

# Decided to deprecate this until 0.5.0 and not just remove it.
@deprecated("0.5.0", "ext.handler.Bot")
class Client:
    """The base Client for RPD interactions

    .. versionadded:: 2.0
    """

    def __init__(self, loop: Optional[asyncio.AbstractEventLoop] = None):
        self.loop = loop
        self._listeners: Dict[
            str, List[Tuple[asyncio.Future, Callable[..., bool]]]
        ] = {}
        # self.http = HTTPClient()

    def on_error(self, e_meth: str) -> None:
        """Handles errors for :class:`Client` default.

        .. versionadded:: 0.3.0
        """
        print(f"Handling error in {e_meth}", file=sys.stderr)
        traceback.print_exc()

    async def _run_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await self.on_error(event_name, *args, **kwargs)
            except asyncio.CancelledError:
                pass

    def _schedule_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> asyncio.Task:
        wrapped = self._run_event(coro, event_name, *args, **kwargs)
        return asyncio.create_task(wrapped, name=f"rpd: {event_name}")

    def event(self, event: str, *args: Any, **kwargs: Any):
        """Used for dispatching events to `Client.listen`.

        .. versionadded:: 0.3.0
        """
        _log.debug(f"Dispatch of {event} is now starting...")
        event_name = f"on_{event}"

        listeners = self._listeners.get(event)

        if listeners:
            removed = []

            for i, (future, condition) in enumerate(listeners):
                if future.cancelled():
                    removed.append(i)
                    continue

                try:
                    result = condition(*args)
                except Exception as E:
                    future.set_exception(E)
                    removed.append(i)
                else:
                    if result:
                        if len(args) == 0 or MISSING:
                            future.set_result(None)
                        elif len(args) == 1:
                            future.set_result(args[0])
                        else:
                            future.set_result(args)
                        removed.append(i)
            if len(removed) == len(listeners):
                self._listeners.pop(event)
            else:
                for idx in reversed(removed):
                    del listeners[idx]

        try:
            coro = getattr(self, event_name)
        except AttributeError:
            pass
        else:
            self._schedule_event(coro, event_name, *args, **kwargs)

    @deprecated(version="0.4.0")  # will be expanded in 0.4.0.
    async def command(self) -> Callable[[CFT], CFT]:
        """A callable function for commands

        .. versionadded:: 0.1.0
        """
        pass

    async def login(self, token: str):
        """|coro|
        Logs in the client with the specified credentials.

        .. versionadded:: 0.3.0

        Parameters
        -----------
        token: :class:`str`
            Your bot token.
        Raises
        ------
        :exc:`.LoginFailure`
            The token passed was invalid.
        :exc:`.HTTPException`
            An unknown HTTP related error occurred,
            usually when it isn't 200 or the known incorrect credentials
            passing status code.
        """
        self.token = token

        _log.info("Trying to login with the specified credentials")

        # data = await self.http._client_login(token.strip())
        # self._connection.user = ClientUser(data=data)

    # async def logout(self):
        # await self.http._client_logout()

    async def ws_start(self):
        """Starts the WebSocket connection with discord.

        .. versionadded:: 0.3.0
        """

    async def start(self, token: str, auto_reconnect: bool = True) -> None:
        """Combines both :meth:`Client.ws_start` and :meth:`Client.login`"""
        await self.login(token)
        # await self.ws_start(reconnect=auto_reconnect)

    def listen(self, coro: Coro) -> Coro:
        """Listen to a certain event

        .. versionadded:: 0.1.0
        """
        if not asyncio.iscoroutinefunction(coro):
            raise TypeError(
                "The event registered must be a coroutine function, else Client will not parse it."
            )

        setattr(self, coro.__name__, coro)
        _log.debug(f"{coro.__name__} has been registered as a event.")
        return coro

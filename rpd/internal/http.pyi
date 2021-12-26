import asyncio
from types import TracebackType as TracebackType
from typing import Any, ClassVar, Coroutine, Type, TypeVar

import aiohttp

from rpd.exceptions import *

T = TypeVar("T")
BE = TypeVar("BE", bound=BaseException)
MU = TypeVar("MU", bound="MaybeUnlock")
Response = Coroutine[Any, Any, T]

class Route:
    BASE: ClassVar[str]
    method: Any
    path: Any
    url: Any
    channel_id: Any
    guild_id: Any
    def __init__(self, method, path: str, **parameters: Any) -> None: ...
    @property
    def bucket(self) -> str: ...

class MaybeUnlock:
    lock: Any
    def __init__(self, lock: asyncio.Lock) -> None: ...
    def __enter__(self) -> MU: ...
    def defer(self) -> None: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BE]],
        exc: Optional[BE],
        traceback: Optional[TracebackType],
    ) -> None: ...

class HTTPClient:
    loop: Any
    connector: Any
    token: Any
    user_agent: Any
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = ...,
        connector: Optional[aiohttp.BaseConnector] = ...,
    ) -> None: ...
    def handle_close(self) -> None: ...
    async def ws_connect(self, url: str, *, compress: int = ...) -> Any: ...
    async def request(self, route: Route, **kwargs: Any) -> Any: ...
    async def close(self) -> None: ...
    def get_gateway_bot(self) -> None: ...

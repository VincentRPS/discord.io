import asyncio
import typing
from typing import Any

from discord.file import File
from discord.types.dict import Dict

class Route:
    method: Any
    endpoint: Any
    url: Any
    guild_id: Any
    channel_id: Any
    webhook_id: Any
    webhook_token: Any
    def __init__(self, method: str, endpoint: str, **params: typing.Any) -> None: ...
    @property
    def bucket(self) -> str: ...

class PadLock:
    lock: Any
    MaybeUnlock: bool
    def __init__(self, lock: asyncio.Lock) -> None: ...
    def __enter__(self) -> PAD: ...
    def defer(self) -> None: ...
    def __exit__(self, exc_type, exc, traceback) -> None: ...

class RESTClient:
    user_agent: str
    header: Any
    state: Any
    proxy: Any
    proxy_auth: Any
    def __init__(
        self,
        *,
        state: Any | None = ...,
        proxy: Any | None = ...,
        proxy_auth: Any | None = ...
    ) -> None: ...
    async def send(
        self,
        route: Route,
        files: typing.Optional[typing.Sequence[File]] = ...,
        form: typing.Optional[typing.Iterable[Dict]] = ...,
        **params: typing.Any
    ): ...
    async def cdn(self, url) -> bytes: ...
    async def close(self) -> None: ...
    async def create_if_not_exists(self) -> None: ...

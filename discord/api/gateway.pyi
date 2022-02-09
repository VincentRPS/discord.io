from typing import Any, Coroutine

from discord import utils as utils
from discord.events import catalog as catalog
from discord.internal.dispatcher import Dispatcher as Dispatcher
from discord.snowflake import Snowflakeish as Snowflakeish
from discord.types.dict import Dict as Dict

from ..state import ConnectionState as ConnectionState
from .rest_factory import RESTFactory as RESTFactory

ZLIB_SUFFIX: bytes
url_extension: str

class Shard:
    remaining: int
    per: float
    window: float
    max: int
    state: Any
    url: Any
    mobile: Any
    dis: Any
    inflator: Any
    shard_id: Any
    buffer: Any
    last_recv: Any
    last_send: Any
    last_ack: Any
    latency: Any
    def __init__(
        self,
        state: ConnectionState,
        dispatcher: Dispatcher,
        shard_id: int,
        url: str,
        mobile: bool = ...,
    ) -> None: ...
    ws: Any
    token: Any
    async def connect(self, token: str) -> None: ...
    @property
    def is_ratelimited(self) -> bool: ...
    def delay(self) -> float: ...
    async def block(self) -> None: ...
    async def check_connection(self) -> None: ...
    async def send(self, data: Dict) -> None: ...
    async def recv(self) -> None: ...
    async def closed(self, code: int) -> None: ...
    async def heartbeat(self, interval: float) -> None: ...
    async def close(self, code: int = ...) -> None: ...
    async def hello(self, data: Dict) -> None: ...
    async def identify(self) -> None: ...
    async def resume(self) -> None: ...

class Gateway:
    mobile: Any
    count: Any
    shards: Any
    def __init__(
        self,
        state: ConnectionState,
        dispatcher: Dispatcher,
        factory: RESTFactory,
        mobile: bool = ...,
    ) -> None: ...
    s: Any
    async def connect(self, token: str) -> None: ...
    def send(self, payload: Dict) -> Coroutine[Any, Any, None]: ...
    async def voice_state(
        self, guild: int, channel: Snowflakeish, mute: bool, deaf: bool
    ) -> Coroutine[Any, Any, None]: ...

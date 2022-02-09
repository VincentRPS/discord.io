from typing import Any, Callable, Coroutine, List, TypeVar, Union

from discord.types.dict import Dict

T = TypeVar("T")
Coro = Coroutine[Any, Any, T]
CoroFunc = Callable[..., Coro[Any]]

class Hold:
    def __init__(self) -> None: ...
    def view(self) -> List[Dict]: ...
    def list(self): ...
    def new(self, name: str, data: Union[str, int, Dict, Any]): ...
    def edit(self, name: str, data: Union[str, int, Dict, Any]): ...
    def get(self, name: str): ...
    def pop(self, name: str): ...
    def reset(self) -> None: ...

class ConnectionState:
    members: Any
    roles: Any
    guild_events: Any
    channels: Any
    bot_info: Any
    app: Any
    loop: Any
    listeners: Any
    shard_count: Any
    components: Any
    prefixed_commands: Any
    application_commands: Any
    prefix: Any
    def __init__(self, **options) -> None: ...

from typing import Any, Callable, Dict, List, TypeVar

from ...internal import DiscordError

CFT = TypeVar('CFT', bound='dispatcher.CoroFunc')

class ExtensionLoadError(DiscordError): ...

class Cog:
    listeners: Dict[str, Any]
    guild_commands: Dict[str, Any]
    global_commands: Dict[str, Any]
    bot: Any
    @property
    def __cog_name__(self) -> str: ...
    @classmethod
    def slash_command(
        cls,
        name: str = ...,
        options: List[dict] = ...,
        guild_ids: List[int] = ...,
        default_permission: bool = ...,
    ): ...
    @classmethod
    def listener(cls, name: str = ...) -> Callable[[CFT], CFT]: ...

from ...internal import DiscordError
from ..commands import Command
from typing import Any, Callable, List, TypeVar

CFT = TypeVar('CFT', bound='dispatcher.CoroFunc')

class ExtensionLoadError(DiscordError): ...

class Cog:
    listeners: dict[str, Any]
    guild_commands: dict[str, Any]
    global_commands: dict[str, Any]
    bot: Any
    @property
    def __cog_name__(self) -> str: ...
    @classmethod
    def slash_command(cls, name: str = ..., options: List[dict] = ..., guild_ids: List[int] = ..., default_permission: bool = ...): ...
    @classmethod
    def listener(cls, name: str = ...) -> Callable[[CFT], CFT]: ...
    @classmethod
    def command(cls, name: str = ...) -> Command: ...

from typing import Any, Callable, TypeVar

from ...internal.exceptions import DiscordError

CFT = TypeVar("CFT", bound="dispatcher.CoroFunc")

class ExtensionLoadError(DiscordError): ...

class Cog:
    listeners: dict[str, Any]
    bot: Any
    def __init__(self, bot) -> None: ...
    @property
    def __cog_name__(self) -> str: ...
    @classmethod
    def listener(cls, name: str = ...) -> Callable[[CFT], CFT]: ...

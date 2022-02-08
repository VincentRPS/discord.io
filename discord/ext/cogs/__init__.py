"""
discord.ext.cogs
~~~~~~~~~~~~~~~~
Extension module to ensure the creation of Cogs.
"""
from typing import Any, Callable, List, TypeVar

from ...internal import dispatcher
from ...internal.exceptions import DiscordError

__all__: List[str] = ["Cog", "ExtensionLoadError"]

CFT = TypeVar("CFT", bound="dispatcher.CoroFunc")


class ExtensionLoadError(DiscordError):
    ...


class Cog:
    listeners: dict[str, Any] = {}

    def __init__(self, bot):
        self.bot = bot

    @property
    def __cog_name__(self) -> str:
        return type(self).__name__

    @classmethod
    def listener(cls, name: str = None) -> Callable[[CFT], CFT]:
        """Listen to a event

        Parameters
        ----------
        name
            The event to listen to
        """

        def decorator(func: CFT) -> CFT:
            a = func
            if isinstance(a, staticmethod):
                a = a.__func__
            Cog.listeners[name] = a
            return func

        return decorator

    def _inject(self, bot_self):
        return self

    def _eject(self, bot_self):
        for name in self.listeners.values():
            bot_self.state.listeners.pop(name)
            self.listeners.pop(name)

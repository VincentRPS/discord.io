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
    def slash_command(
        cls,
        name: str = None,
        options: List[dict] = None,
        guild_ids: List[int] = None,
        default_permission: bool = True,
    ):
        """Creates a slash command

        Parameters
        ----------
        name: :class:`str`
            The slash command name
        callback
            The slash command callback
        options: :class:`List`
            A list of slash command options
        guild_ids: List[:class:`int`]
            A list of guild ids
        description: :class:`str`
            The application command description
        default_permission: :class:`bool`
            If this slash command should have default permissions
        """

        def decorator(func: CFT) -> CFT:
            name = func.__name__  # if name is None else name # fix this somehow?
            description = func.__doc__

            if guild_ids is not None:
                for guild in guild_ids:
                    cls.bot.state.loop.create_task(
                        cls.bot.application.register_guild_slash_command(
                            guild_id=guild,
                            name=name,
                            description=description,
                            callback=func,
                            options=options,
                            default_permission=default_permission,
                        )
                    )
            else:
                cls.bot.state.loop.create_task(
                    cls.bot.application.register_global_slash_command(
                        name=name,
                        description=description,
                        callback=func,
                        options=options,
                        default_permission=default_permission,
                    )
                )

            return func

        return decorator

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

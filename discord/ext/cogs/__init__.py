"""
discord.ext.cogs
~~~~~~~~~~~~~~~~
Extension module to ensure the creation of Cogs.
"""
from typing import TYPE_CHECKING, Any, Callable, List, TypeVar

from ...internal import DiscordError, dispatcher

__all__: List[str] = ['Cog', 'ExtensionLoadError']

CFT = TypeVar('CFT', bound='dispatcher.CoroFunc')


class ExtensionLoadError(DiscordError):
    ...


class Cog:
    listeners: dict[str, Any] = {}
    guild_commands: dict[str, Any] = {}
    global_commands: dict[str, Any] = {}

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

            a = func
            if isinstance(a, staticmethod):
                a = a.__func__

            if guild_ids is not None:
                Cog.guild_commands[name] = {
                    'guild_id': guild_ids,
                    'name': name,
                    'description': description,
                    'callback': a,
                    'options': options,
                    'default_permission': default_permission,
                }
            else:
                Cog.global_commands[name] = {
                    'name': name,
                    'description': description,
                    'callback': a,
                    'options': options,
                    'default_permission': default_permission,
                }

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
        self.bot = bot_self
        return self

    def _eject(self, bot_self):
        for name in self.listeners.values():
            bot_self.state.listeners.pop(name)
            self.listeners.pop(name)

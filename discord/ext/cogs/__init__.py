"""
discord.ext.cogs
~~~~~~~~~~~~~~~~
Extension module to ensure the creation of Cogs.
"""
from typing import Any, Callable, Dict, List, TypeVar, Optional

from ...internal import DiscordError, dispatcher
from ...bases import CommandBase, SlashCommandBase, ListenerBase

__all__: List[str] = ['Cog', 'ExtensionLoadError']

CFT = TypeVar('CFT', bound='dispatcher.CoroFunc')


class ExtensionLoadError(DiscordError):
    ...



class Cog:
    guild_commands = {}
    global_commands = {}
    prefixed_commands = {}
    listeners = {}
    bot = None

    def __new__(cls, *args, **kwargs):

        listeners: Dict[str, Any] = {}
        guild_commands: Dict[str, Any] = {}
        global_commands: Dict[str, Any] = {}
        prefixed_commands: Dict[str, Any] = {}

        for name, value in cls.__dict__.items():
            if isinstance(value, CommandBase):
                prefixed_commands[name] = value
            elif isinstance(value, ListenerBase):
                listeners[name] = value
            elif isinstance(value, SlashCommandBase):
                if value.guild_ids is None:
                    global_commands[name] = value
                else:
                    guild_commands[name] = value
            

        cls.prefixed_commands = prefixed_commands
        cls.listeners = listeners
        cls.global_commands = global_commands
        cls.guild_commands = guild_commands

        return super(Cog, cls).__new__(cls)

    @property
    def __cog_name__(self) -> str:
        return type(self).__name__

    @classmethod
    def command(cls, name: Optional[str] = None, flags: Optional[list] = []):
        def wrap(func: Callable):
            _name = name or func.__name__
            _description = func.__doc__
            cmd = CommandBase(
                name=_name,
                description=_description,
                func=func
            )

            return cmd

        return wrap

    @classmethod
    def listener(cls, name: str = None):
        """Listen to a event

        Parameters
        ----------
        name
            The event to listen to
        """

        def decorator(func: Callable):
            a = func
            if isinstance(a, staticmethod):
                a = a.__func__
            _name = name or a.__name__
            return ListenerBase(_name, a)

        return decorator

    @classmethod
    def slash_command(
        cls,
        name: str = None,
        options: List[dict] = None,
        guild_ids: List[int] = None,
        default_permission: bool = True
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
        def wrap(func):
            a = func
            if isinstance(a, staticmethod):
                a = a.__func__

            _name = func.__name__ if name is None else name
            description = func.__doc__

            return SlashCommandBase(
                name=_name,
                options=options,
                guild_ids=guild_ids,
                default_permission=default_permission,
                description=description,
                func=func
            )   
        return wrap

    def _inject(self, bot_self):
        self.bot = bot_self
        return self

    def _eject(self, bot_self):
        for name in self.listeners.values():
            bot_self.state.listeners.pop(name)
            self.listeners.pop(name)

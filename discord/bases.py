from typing import Callable, List

class ListenerBase:
    def __init__(self,
        event_name: str = None,
        func: Callable = None
    ):
        self.event_name = event_name
        self.func = func

class CommandBase:
    def __init__(self,
        name: str = None,
        aliases: list[str] = None,
        description: str = None,
        func: Callable = None,
        flags: list = None
    ) -> None:
        self.name = name or func.name
        self.aliases = aliases or []
        self.description = description or func.__doc__
        self.func = func
        self.flags = flags


class SlashCommandBase:
    def __init__(self,
        name: str = None,
        options: List[dict] = None,
        guild_ids: List[int] = None,
        default_permission: bool = True,
        func: Callable = None,
        description: str = None
    ):
        self.name: str = name
        self.options: List[dict] = options
        self.guild_ids: List[int] = guild_ids
        self.default_permission: bool = default_permission
        self.func = func
        self.description = description or func.__doc__
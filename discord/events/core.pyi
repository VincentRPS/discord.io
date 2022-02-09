import abc
from typing import Any

from discord.internal.dispatcher import Dispatcher as Dispatcher
from discord.state import ConnectionState as ConnectionState

class Event(abc.ABC):
    data: Any
    dispatch: Any
    state: Any
    def __init__(
        self, data, dispatcher: Dispatcher, state: ConnectionState
    ) -> None: ...
    @property
    def app(self) -> Any: ...
    def process(self) -> None: ...

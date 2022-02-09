import typing
from typing import Any

from ..internal.dispatcher import Coro
from ..state import ConnectionState

class Button:
    state: Any
    def __init__(self, state: ConnectionState) -> None: ...
    id: Any
    callback: Any
    async def create(
        self,
        label: str,
        callback: Coro,
        style: typing.Literal[1, 2, 3, 4, 5] = ...,
        custom_id: str = ...,
        url: str = ...,
    ): ...

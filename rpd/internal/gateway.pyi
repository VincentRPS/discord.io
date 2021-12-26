import aiohttp
import threading
from typing import Any

class ResumeWebSocket(Exception):
    resume: Any
    op: Any
    def __init__(self, resume: bool = ...) -> None: ...

class WebSocketConnectionClosed(Exception): ...

class DiscordClientWebSocketResponse(aiohttp.ClientWebSocketResponse):
    async def close(self, *, code: int = ..., message: bytes = ...) -> bool: ...

class KeepSocketAlive(threading.Thread):
    ws: Any
    def __init__(self, *args, **kwargs) -> None: ...

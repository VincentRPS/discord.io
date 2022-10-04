"""
discord.api
~~~~~~~~~~~
Implementation of the Discord API.
"""
import json
from typing import Any, Optional

from aiohttp import ClientSession

from discord.__init__ import __version__, utils

from .execution import Executer
from .route import BaseRoute, Route

__all__ = ['Route', 'BaseRoute', 'HTTPClient']

class HTTPClient:
    def __init__(self, token: str, base_url: str = 'https://discord.com/api/v10') -> None:
        self.base_url = base_url
        self._headers = {
            'Authorization': f'Bot {token}',
            'User-Agent': f'DiscordBot (https://github.com/VincentRPS/discord.io, {__version__})',
        }

        self._session: None | ClientSession = None
        self._executers: list[Executer] = []

    async def create_session(self) -> None:
        self._session = ClientSession()

    async def close_session(self) -> None:
        await self._session.close()
        self._session = None

    async def request(
        self, method: str, route: BaseRoute, data: Optional[dict[str, Any]] = None, *, reason: Optional[str] = None
    ) -> None:
        endpoint = route.merge(self.base_url)

        if self._session is None:
            await self.create_session()

        headers = self._headers.copy()

        if reason:
            headers['X-Audit-Log-Reason'] = reason

        if data:
            # TODO: Support msgspec
            data: str = json.dumps(data)
            headers.update({'Content-Type': 'application/json'})

        for executer in self._executers:
            if executer.is_global or executer.route == route:
                await executer.wait()

        for _ in range(5):
            r = await self._session.request(method, endpoint, data=data, headers=headers)

            if r.status == 429:
                executer = Executer(route=route)

                self._executers.append(executer)
                await executer.executed(
                    reset_after=float(r.headers.get('X-RateLimit-Reset-After', 30)),
                    is_global=r.headers.get('X-RateLimit-Scope') == 'global',
                )
                self._executers.remove(executer)

            # TODO: Handle normal errors

            return await utils._text_or_json(cr=r)

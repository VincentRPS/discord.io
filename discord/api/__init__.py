"""
discord.api
~~~~~~~~~~~
Implementation of the Discord API.
"""
import json
import logging
from typing import Any, Optional

from aiohttp import ClientSession

from discord._about import __version__

from .. import utils
from .rate_limiter import Executer
from .route import Route

__all__ = ['Route', 'HTTPClient']

_log = logging.getLogger(__name__)


class HTTPClient:
    def __init__(self, token: str, base_url: str = 'https://discord.com/api/v10') -> None:
        self.base_url = base_url
        self._headers = {
            'Authorization': f'Bot {token}',
            'User-Agent': f'DiscordBot (https://github.com/VincentRPS/discord.io, {__version__})',
        }

        self._session: None | ClientSession = None
        self._executers: list[Executer] = []

    async def create_session(self) -> ClientSession:
        return ClientSession()

    async def close_session(self) -> None:
        if self._session:
            await self._session.close()
            self._session = None

    async def request(
        self, method: str, route: Route, data: Optional[dict[str, Any]] = None, *, reason: Optional[str] = None
    ) -> str | dict[str, Any] | None:
        endpoint = route.merge(self.base_url)

        if self._session is None:
            self._session = await self.create_session()

        headers = self._headers.copy()

        if reason:
            headers['X-Audit-Log-Reason'] = reason

        if data:
            # TODO: Support msgspec
            encoded_data = json.dumps(data)
            headers.update({'Content-Type': 'application/json'})
        else:
            encoded_data = None

        _log.debug(f'Requesting to {endpoint} with {data}, {headers}')

        for executer in self._executers:
            if executer.is_global or executer.route == route:
                _log.debug(f'Pausing request to {endpoint}: Found rate limit executer')
                await executer.wait()

        for _ in range(5):
            r = await self._session.request(method, endpoint, data=encoded_data, headers=headers)

            if r.status == 429:
                _log.debug(f'Request to {endpoint} failed: Request returned rate limit')
                executer = Executer(route=route)

                self._executers.append(executer)
                _json = await r.json()
                await executer.executed(
                    reset_after=_json['retry_after'],
                    is_global=r.headers.get('X-RateLimit-Scope') == 'global',
                    limit=int(r.headers.get('X-RateLimit-Limit', 10)),
                )
                self._executers.remove(executer)
                continue

            # TODO: Handle normal errors

            return await utils._text_or_json(cr=r)

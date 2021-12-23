"""
Apache-2.0

Copyright 2021 VincentRPS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the LICENSE file for the specific language governing permissions and
limitations under the License.
"""
from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING, Any, Dict, Optional

import aiohttp

from rpd import __version__
from rpd.exceptions import (
    Forbidden,
    HTTPException,
    LoginFailure,
    NotFound,
    RateLimitError,
    Unauthorized,
)

from ..helpers.missing import MISSING
from ..helpers.orjson import _from_json
from .gateway import DiscordClientWebSocketResponse

if TYPE_CHECKING:
    from ..data.types.snowflake import Snowflake, SnowflakeList
    from ..data.types.user import User

__all__ = ("Route", "HTTPClient")

POST = "https://discord.com/api/v9"


class Route:
    def __init__(self, method, route, **parameters):
        self.method = method
        self.path = route.format(**parameters)

        # Used for bucket cooldowns
        self.channel_id = parameters.get("channel_id")
        self.guild_id = parameters.get("guild_id")

    @property
    def bucket(self):
        return f"{self.channel_id}:{self.guild_id}:{self.path}"


class HTTPClient:
    def __init__(self):
        pass

    pass

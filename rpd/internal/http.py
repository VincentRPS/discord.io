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
from typing import Any, Dict, Optional, TYPE_CHECKING

import aiohttp
from .gateway import DiscordClientWebSocketResponse

from rpd import __version__
from rpd.exceptions import (
    Forbidden,
    HTTPException,
    NotFound,
    RateLimitError,
    Unauthorized,
    LoginFailure,
)
from ..helpers.missing import MISSING
from ..helpers.orjson import _from_json

if TYPE_CHECKING:
    from ..data.types.user import User
    from ..data.types.snowflake import Snowflake, SnowflakeList

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
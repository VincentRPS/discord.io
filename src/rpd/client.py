"""
Apache-2.0

Copyright 2021 RPS

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

import logging

from aiohttp.helpers import TOKEN

from .internal.client.core import Command, Send

_log = logging.getLogger(__name__)

__all__ = ("Client",)


class Client:
    """Client For Bots"""

    def __init__(self):
        pass

    @callable
    def command(self) -> Command:
        """Command Stuff"""
        return Command

    def send(self) -> Send:
        """Sends Messages For Client"""
        return Send

    async def start(self, token):
        """The non-callable start stuff"""
        self.token = token

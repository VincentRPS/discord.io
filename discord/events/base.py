# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

from types import SimpleNamespace
from typing import TYPE_CHECKING, Any

import typing_extensions

from discord import traits

if TYPE_CHECKING:
    from ..apps import GatewayApp


class BaseEvent(SimpleNamespace):
    _type: str | None = None
    _app: traits.BaseApp

    @classmethod
    def construct(cls, *args, **kwargs) -> None:
        ...

    @property
    def app(self) -> traits.BaseApp:
        return self._app


class GatewayEvent(BaseEvent):
    _app: "GatewayApp"

    @property
    def app(self) -> "GatewayApp":
        return self._app


class Ready(GatewayEvent):
    _type = 'on_ready'
    version: int
    guild_ids: int
    shard: tuple[int, int]
    session_id: str
    resume_url: str

    @classmethod
    def construct(cls, app: "GatewayApp", data: dict[str, Any]) -> typing_extensions.Self:
        self = cls()
        self._app = app
        self.version = data['v']
        self.guild_ids = data['guilds']
        self.session_id = data['session_id']
        self.resume_url = data['resume_gateway_url']
        self.shard = data['shard']
        return self


class UnknownEvent(BaseEvent):
    """
    An event which is either unknown or not subscribed to
    """

    _type: str = 'UNKNOWN'
    unknown_data: dict[str, Any]

    @classmethod
    def construct(cls, app: traits.BaseApp, data: dict[str, Any]) -> typing_extensions.Self:
        self = cls()
        self.unknown_data = data
        self._app = app
        return self

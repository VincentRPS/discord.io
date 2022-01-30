# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE

# Most requests are done here, except for log-ins and outs since they change the header.

import typing

from rpd.api.rest import RESTClient, Route
from rpd.snowflake import Snowflakeish
from rpd.state import ConnectionState

__all__: typing.List[str] = [
    "RESTFactory",
]


class RESTFactory:
    """The RESTFactory for most requests.

    .. versionadded:: 0.3.0

    Attributes
    ----------
    rest
        The RESTClient.
    """

    def __init__(self, state=None):
        self.state = state or ConnectionState()
        self.rest = RESTClient(state=self.state)

    def login(self, token: typing.Optional[str] = None) -> None:
        self.token = token

        if len(self.token) != 59:
            raise Exception("Invalid Bot Token Was Passed")
        else:
            pass

        return self.rest.send(Route("GET", "/users/@me"), token=self.token)  # Log's in

    def logout(self) -> None:
        return self.rest.send(
            Route("POST", "/auth/logout")
        )  # Log's you out of the bot.

    def get_gateway_bot(self) -> None:
        return self.rest.send(Route("GET", "/gateway/bot"))

    def create_message(
        self,
        channel: Snowflakeish,
        content: str,
        tts: typing.Optional[bool] = False,
        embeds: typing.List[typing.Dict[str, typing.Any]] = None,
        allowed_mentions: typing.Optional[bool] = False,
        message_reference: typing.Optional[dict] = None,
        components: typing.Optional[list[dict]] = None,
    ):
        json = {
            "content": content,
            "tts": tts,
            "allowed_mentions": int(allowed_mentions),
        }
        if message_reference is not None:
            json["message_reference"] = message_reference
        if components is not None:
            json["components"] = components
        if embeds is not None:
            json["embeds"] = embeds

        return self.rest.send(
            Route("POST", f"/channels/{channel}/messages", channel_id=channel),
            json=json,
        )

    def get_channel(self, channel: typing.Optional[Snowflakeish] = None):
        return self.rest.send(Route("GET", f"/channels/{channel}"))

    def edit_channel(
        self,
        name: typing.Optional[str] = None,
        channel: typing.Optional[Snowflakeish] = None,
        type: typing.Optional[str] = None,
    ):
        if type == "group_dm":
            payload = {}
            if name:
                payload["name"] = name
        return self.rest.send(Route("PATCH", f"/channels/{channel}"))

    def create_invite(
        self,
        *,
        channel_id: typing.Optional[Snowflakeish] = None,
        reason: typing.Optional[str] = None,
        max_age: typing.Optional[int] = 0,
        max_uses: typing.Optional[int] = 0,
        tempoary: typing.Optional[bool] = False,
        unique: typing.Optional[bool] = True,
    ):
        json = {
            "max_age": max_age,
            "max_uses": max_uses,
            "tempoary": tempoary,
            "unique": unique,
        }
        if channel_id:
            json["channel_id"] = channel_id
        return self.rest.send(Route("POST"), reason=reason, json=json)

    # Application Commands

    # global

    def create_global_application_command(
        self,
        application_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.List[typing.Dict[str, typing.Any]],
        default_permission: typing.Optional[bool] = True,
        type: typing.Literal["CHAT_INPUT", "USER", "MESSAGE"] = "CHAT_INPUT",
    ):
        json = {
            "name": name,
            "description": description,
            "options": options,
            "default_permission": default_permission,
            "type": type,
        }
        return self.rest.send(
            Route("POST", f"/applications/{application_id}/commands"), json=json
        )

    def get_global_application_command(
        self, application_id: Snowflakeish, command: Snowflakeish
    ):
        return self.rest.send(
            Route("GET", f"/applications/{application_id}/commands/{command}")
        )

    def edit_global_application_command(
        self,
        application_id: Snowflakeish,
        command_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.List[typing.Dict[str, typing.Any]],
        default_permission: typing.Optional[bool] = True,
    ):
        json = {
            "name": name,
            "description": description,
            "options": options,
            "default_permission": default_permission,
        }
        return self.rest.send(
            Route("PATCH", f"/applications/{application_id}/commands/{command_id}"),
            json=json,
        )

    # Guild Commands

    def create_global_application_command(
        self,
        application_id: Snowflakeish,
        guild_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.List[typing.Dict[str, typing.Any]],
        default_permission: typing.Optional[bool] = True,
        type: typing.Literal["CHAT_INPUT", "USER", "MESSAGE"] = "CHAT_INPUT",
    ):
        json = {
            "name": name,
            "description": description,
            "options": options,
            "default_permission": default_permission,
            "type": type,
        }
        return self.rest.send(
            Route("POST", f"/applications/{application_id}/guilds/{guild_id}/commands"),
            json=json,
        )

    def get_global_application_command(
        self,
        application_id: Snowflakeish,
        guild_id: Snowflakeish,
        command: Snowflakeish,
    ):
        return self.rest.send(
            Route(
                "GET",
                f"/applications/{application_id}/guilds/{guild_id}/commands/{command}",
            )
        )

    def edit_global_application_command(
        self,
        application_id: Snowflakeish,
        command_id: Snowflakeish,
        guild_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.List[typing.Dict[str, typing.Any]],
        default_permission: typing.Optional[bool] = True,
    ):
        json = {
            "name": name,
            "description": description,
            "options": options,
            "default_permission": default_permission,
        }
        return self.rest.send(
            Route(
                "PATCH",
                f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            ),
            json=json,
        )

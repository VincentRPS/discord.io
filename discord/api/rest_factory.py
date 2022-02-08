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

import datetime
import typing
from json import dumps
from typing import Any, Optional

import aiohttp

from discord import utils

from ..enums import ScheduledEventType
from ..file import File
from ..flags import MessageFlags
from ..snowflake import Snowflakeish
from ..state import ConnectionState
from ..types import allowed_mentions
from ..types.dict import Dict
from .rest import RESTClient, Route

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

    def __init__(
        self,
        state: typing.Optional[ConnectionState] = None,
        proxy: typing.Optional[str] = None,
        proxy_auth: typing.Optional[str] = None,
    ):
        self.proxy = proxy
        self.proxy_auth = proxy_auth
        self.state = state or ConnectionState()
        self.rest = RESTClient(state=self.state, proxy=proxy, proxy_auth=proxy_auth)

    async def login(
        self, token: str
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        self.token = token

        if len(self.token) != 59:
            raise Exception("Invalid Bot Token Was Passed")
        else:
            pass

        r = await self.rest.send(Route("GET", "/users/@me"), token=self.token)

        self.state.bot_info[self.state.app] = r

        return r

    def logout(
        self,
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        return self.rest.send(
            Route("POST", "/auth/logout")
        )  # Log's you out of the bot.

    def get_gateway_bot(
        self,
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        return self.rest.send(Route("GET", "/gateway/bot"))

    def create_message(
        self,
        channel: Snowflakeish,
        content: typing.Optional[str] = None,
        files: typing.Optional[typing.Sequence[File]] = None,
        tts: typing.Optional[bool] = False,
        embeds: typing.List[Dict] = None,
        allowed_mentions: typing.Optional[allowed_mentions.MentionObject] = None,
        message_reference: typing.Optional[dict] = None,
        components: typing.Optional[list[Dict]] = None,
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        json = {
            "tts": tts,
            "allowed_mentions": allowed_mentions,
        }
        if content is not None:
            json["content"] = content
        if message_reference is not None:
            json["message_reference"] = message_reference
        if components is not None:
            json["components"] = components
        if embeds is not None:
            json["embeds"] = embeds

        if files:
            form = []
            form.append({"name": "payload_json", "value": dumps(json)})
            if len(files) == 1:
                file = files[0]
                form.append(
                    {
                        "name": "file",
                        "value": file.fp,
                        "filename": file.filename,
                        "content_type": "application/octet-stream",
                    }
                )
            else:
                for index, file in enumerate(files):
                    form.append(
                        {
                            "name": f"file{index}",
                            "value": file.fp,
                            "filename": file.filename,
                            "content_type": "application/octet-stream",
                        }
                    )

            return self.rest.send(
                Route("POST", f"/channels/{channel}/messages", channel_id=channel),
                json=json,
                form=form,
                files=files,
            )

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
        options: typing.Optional[typing.List[Dict]] = None,
        default_permission: typing.Optional[bool] = True,
        type: int = 1,
    ):
        json = {
            "name": name,
            "description": description,
            "type": type,
        }
        if default_permission is False:
            json["default_permission"] = False
        if options:
            json["options"] = options
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
        options: typing.Optional[typing.List[Dict]] = None,
        default_permission: typing.Optional[bool] = True,
    ):
        json = {
            "name": name,
            "description": description,
            "default_permission": default_permission,
        }
        if options:
            json["options"] = options
        return self.rest.send(
            Route("PATCH", f"/applications/{application_id}/commands/{command_id}"),
            json=json,
        )

    def get_global_application_commands(self, application_id: Snowflakeish):
        return self.rest.send(Route("GET", f"/applications/{application_id}/commands"))

    def delete_global_application_command(
        self,
        application_id: int,
        command: int,
    ):
        return self.rest.send(
            Route(
                "DELETE",
                f"/applications/{application_id}/commands/{command}",
            )
        )

    # Guild Commands

    def create_guild_application_command(
        self,
        application_id: Snowflakeish,
        guild_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.Optional[typing.List[Dict]],
        default_permission: typing.Optional[bool] = True,
        type: int = 1,
    ):
        json = {
            "name": name,
            "description": description,
            "default_permission": default_permission,
            "type": type,
        }
        if default_permission is False:
            json["default_permission"] = False
        if options:
            json["options"] = options
        return self.rest.send(
            Route("POST", f"/applications/{application_id}/guilds/{guild_id}/commands"),
            json=json,
        )

    def get_guild_application_command(
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

    def get_guild_application_commands(
        self,
        application_id: Snowflakeish,
        guild_id: Snowflakeish,
    ):
        return self.rest.send(
            Route(
                "GET",
                f"/applications/{application_id}/guilds/{guild_id}/commands",
            )
        )

    def delete_guild_application_command(
        self,
        application_id: int,
        guild_id: int,
        command: int,
    ):
        return self.rest.send(
            Route(
                "DELETE",
                f"/applications/{application_id}/guilds/{guild_id}/commands/{command}",
                guild_id=guild_id,
            )
        )

    def edit_guild_application_command(
        self,
        application_id: Snowflakeish,
        command_id: Snowflakeish,
        guild_id: Snowflakeish,
        name: str,
        description: str,
        options: typing.Optional[typing.List[Dict]] = None,
        default_permission: typing.Optional[bool] = True,
    ):
        json = {
            "name": name,
            "description": description,
            "default_permission": default_permission,
        }
        if options:
            json["options"] = options
        return self.rest.send(
            Route(
                "PATCH",
                f"/applications/{application_id}/guilds/{guild_id}/commands/{command_id}",
            ),
            json=json,
        )

    # interaction response.

    def create_interaction_response(
        self,
        interaction_id: int,
        interaction_token: str,
        content: str,
        embeds: typing.Optional[typing.List[typing.Dict]] = None,
        tts: typing.Optional[bool] = False,
        allowed_mentions: typing.Optional[allowed_mentions.MentionObject] = None,
        flags: typing.Optional[MessageFlags] = None,
        components: typing.Optional[dict] = None,
    ):
        json = {
            "content": content,
        }
        if embeds is not None:
            json["embeds"] = embeds
        if tts is not False:
            json["tts"] = tts
        if allowed_mentions is not None:
            json["allowed_mentions"] = allowed_mentions
        if flags is not None:
            json["flags"] = flags
        if components is not None:
            json["components"] = components
        return self.rest.send(
            Route(
                "POST",
                f"/interactions/{interaction_id}/{interaction_token}/callback",
            ),
            json=json,
        )

    def get_initial_response(self, application_id, interaction_token):
        return self.rest.send(
            Route("GET", f"/webhooks/{application_id}/{interaction_token}/@original")
        )

    # TODO: Edit and Delete initial reponse.

    def create_followup_message(
        self,
        application_id,
        interaction_token,
        content: str,
        embeds: typing.Optional[typing.List[dict]] = None,
        allowed_mentions: typing.Optional[allowed_mentions.MentionObject] = None,
        components: typing.Optional[typing.List[Dict]] = None,
        flags: typing.Optional[MessageFlags] = None,
    ):
        json = {"content": content}
        if embeds is not None:
            json["embeds"] = embeds
        if allowed_mentions is not None:
            json["allowed_mentions"] = allowed_mentions
        if components is not None:
            json["components"] = components
        if flags is not None:
            json["flags"] = flags
        return self.rest.send(
            Route("POST", f"/webhooks/{application_id}/{interaction_token}"), json=json
        )

    def get_followup_message(
        self,
        application_id,
        interaction_token,
        message,
    ):
        return self.rest.send(
            Route(
                "GET",
                f"/webhooks/{application_id}/{interaction_token}/messages/{message}",
            ),
        )

    # TODO: Edit and Delete followup message

    def get_audit_log_entry(
        self,
        guild: Snowflakeish,
        user_id: typing.Optional[Snowflakeish] = None,
        action_type: typing.Optional[int] = None,
        before: typing.Optional[Snowflakeish] = None,
        limit: typing.Optional[int] = 50,
    ):
        ret = {"limit": limit}
        if user_id:
            ret["user_id"] = user_id
        if action_type:
            ret["action_type"] = action_type
        if before:
            ret["before"] = before
        if limit:
            ret["limit"] = limit
        return self.rest.send(
            Route(
                "GET",
                f"/guilds/{guild}/audit-logs",
                guild_id=guild,
            ),
            json=ret,
        )

    # emojis

    ...

    # guilds

    def get_guild_member(self, guild_id, user):
        return self.rest.send(
            Route("GET", f"/guilds/{guild_id}/members/{user}", guild_id=guild_id)
        )

    def get_guild_members(
        self, guild_id, limit: typing.Optional[int] = 1, after: typing.Optional[int] = 0
    ):
        ret = {"limit": limit, "after": after}
        return self.rest.send(
            Route("GET", f"/guilds/{guild_id}/members", guild_id=guild_id), json=ret
        )

    def modify_guild_member(
        self,
        guild_id: int,
        member: int,
        nick: typing.Optional[str] = None,
        roles: typing.Optional[typing.List[int]] = None,
        mute: typing.Optional[bool] = False,
        deaf: typing.Optional[bool] = False,
        channel_id: typing.Optional[int] = None,
        timeout: typing.Optional[str] = None,
        reason: typing.Optional[str] = None,
    ):
        ret = {
            "nick": nick,
            "roles": roles,
            "mute": mute,
            "deaf": deaf,
            "channel_id": channel_id,
            "communication_disabled_until": timeout,
        }
        return self.rest.send(
            Route("PATCH", f"/guilds/{guild_id}/members/{member}", guild_id=guild_id),
            reason=reason,
            json=ret,
        )

    def get_guild(self, guild_id: int):
        return self.rest.send(Route("GET", f"/guilds/{guild_id}", guild_id=guild_id))

    def modify_guild(
        self,
        guild_id: int,
        reason: Optional[str] = None,
        name: Optional[str] = None,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        afk_channel_id: Optional[int] = None,
        afk_timeout: Optional[int] = None,
    ):
        ...

    # users
    def get_user(self, user: int):
        return self.rest.send(Route("GET", f"/users/{user}"))

    # scheduled events
    def get_scheduled_events(self, guild_id: int):
        return self.rest.send(
            Route("GET", f"/guilds/{guild_id}/scheduled-events", guild_id=guild_id)
        )

    def create_scheduled_event(
        self,
        guild_id: int,
        name: str,
        start_time: datetime.datetime,
        type: ScheduledEventType,
        end_time: Optional[datetime.datetime] = None,
        description: Optional[str] = None,
        privacy_level: Optional[int] = 2,
        channel_id: Optional[int] = None,
        metadata: Optional[Any] = None,
        image: Optional[File] = None,
    ):
        form = []
        json = {
            "name": name,
            "entity_type": type,
            "scheduled_start_time": start_time,
            "privacy_level": privacy_level,
        }
        if end_time:
            json["scheduled_end_time"] = end_time
        if description:
            json["description"]
        if channel_id:
            json["channel_id"] = channel_id
        if metadata:
            json["entity_metadata"] = metadata

        raw = image.fp.read(16)
        if image:
            try:
                mime = utils.img_mime_type(raw)
            except TypeError:
                mime = "application-octet-stream"
            form.append(
                {
                    "name": "image",
                    "value": image.fp,
                    "filename": image.filename,
                    "content_type": mime,
                }
            )

        return self.rest.send(
            Route("POST", f"/guilds/{guild_id}/scheduled-events", guild_id=guild_id),
            json=json,
            form=form,
            files=[image],
        )

    # assets

    def create_guild_sticker(
        self,
        guild_id: int,
        name: str,
        tags: str,
        file: File,
        reason: Optional[str] = None,
        description: Optional[str] = None,
    ):
        raw = file.fp.read(16)

        try:
            mime = utils.img_mime_type(raw)
        except TypeError:
            if raw.startswith(b"{"):
                mime = "application/json"
            else:
                mime = "application/octet-stream"

        finally:
            file.reset()

        form = [
            {
                "name": "file",
                "value": file.fp,
                "filename": file.filename,
                "content_type": mime,
            }
        ]

        if name:
            form.append({"name": "name", "value": name})
        if tags:
            form.append({"name": "tags", "value": tags})
        if description:
            form.append({"name": "description", "value": description})

        return self.rest.send(
            Route("POST", f"/guilds/{guild_id}/stickers", guild_id=guild_id),
            form=form,
            files=[file],
            reason=reason,
        )

    # if your wondering why this is here, it's because it's used in the voice gateway.
    async def ws_connect(self, url: str, *, compress: int = 0) -> Any:
        kwargs = {
            "proxy_auth": self.proxy_auth,
            "proxy": self.proxy,
            "max_msg_size": 0,
            "timeout": 30.0,
            "autoclose": False,
            "headers": {
                "User-Agent": self.rest.user_agent,
            },
            "compress": compress,
        }

        sesh = aiohttp.ClientSession()
        return await sesh.ws_connect(url, **kwargs)

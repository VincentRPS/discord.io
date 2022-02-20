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
from typing import Any, Optional

from discord import utils

from ..api.rest import RESTClient, Route
from ..enums import ScheduledEventType
from ..file import File


class Guilds:
    def __init__(self, rest: RESTClient):
        self.rest = rest

    def get_guild_member(self, guild_id, user):
        return self.rest.send(
            Route('GET', f'/guilds/{guild_id}/members/{user}', guild_id=guild_id)
        )

    def get_guild_members(
        self, guild_id, limit: typing.Optional[int] = 1, after: typing.Optional[int] = 0
    ):
        ret = {'limit': limit, 'after': after}
        return self.rest.send(
            Route('GET', f'/guilds/{guild_id}/members', guild_id=guild_id), json=ret
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
        json = {}
        if nick:
            json['nick'] = (nick,)
        elif roles:
            json['roles'] = (roles,)
        elif mute:
            json['mute'] = (mute,)
        elif deaf:
            json['deaf'] = (deaf,)
        elif channel_id:
            json['channel_id'] = (channel_id,)
        elif timeout:
            json['communication_disabled_until'] = (timeout,)
        return self.rest.send(
            Route('PATCH', f'/guilds/{guild_id}/members/{member}', guild_id=guild_id),
            reason=reason,
            json=json,
        )

    def ban_guild_member(
        self,
        guild_id: int,
        user: int,
        delete_message_days: typing.Optional[int] = 0,
        reason: typing.Optional[str] = None,
    ):
        json = {'delete_message_days': delete_message_days}
        return self.rest.send(
            Route('PUT', f'/guilds/{guild_id}/bans/{user}', guild_id=guild_id),
            reason=reason,
            json=json,
        )

    def kick_guild_member(
        self,
        guild_id: int,
        user: int,
        reason: typing.Optional[str] = None,
    ):
        return self.rest.send(
            Route('DELETE', f'/guilds/{guild_id}/members/{user}', guild_id=guild_id),
            reason=reason,
        )

    def get_guild(self, guild_id: int):
        return self.rest.send(Route('GET', f'/guilds/{guild_id}', guild_id=guild_id))

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

    def get_guild_preview(self, guild_id: int):
        return self.rest.send(
            Route('GET', f'/guilds/{guild_id}/preview', guild_id=guild_id)
        )

    def delete_guild(
        self,
        guild_id: int,
    ):
        return self.rest.send(Route('DELETE', f'/guilds/{guild_id}', guild_id=guild_id))

    def create_guild(
        self,
        name: str,
        region: Optional[str] = None,
        icon: typing.Optional[bytes] = None,
        verification_level: typing.Optional[int] = None,
        default_message_notifications: typing.Optional[int] = None,
        explicit_content_filter: typing.Optional[int] = None,
        roles: typing.Optional[typing.List[int]] = None,
        channels: typing.Optional[typing.List[int]] = None,
        reason: typing.Optional[str] = None,
    ):
        json = {
            'name': name,
            'verification_level': verification_level,
            'default_message_notifications': default_message_notifications,
            'explicit_content_filter': explicit_content_filter,
            'roles': roles,
            'channels': channels,
        }
        if icon is not None:
            json['icon'] = icon

        if region is not None:
            json['region'] = region

        return self.rest.send(Route('POST', '/guilds'), json=json, reason=reason)

    # users
    def get_user(self, user: int):
        return self.rest.send(Route('GET', f'/users/{user}'))

    # scheduled events
    def get_scheduled_events(self, guild_id: int):
        return self.rest.send(
            Route('GET', f'/guilds/{guild_id}/scheduled-events', guild_id=guild_id)
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
            'name': name,
            'entity_type': type,
            'scheduled_start_time': start_time,
            'privacy_level': privacy_level,
        }
        if end_time:
            json['scheduled_end_time'] = end_time
        if description:
            json['description']
        if channel_id:
            json['channel_id'] = channel_id
        if metadata:
            json['entity_metadata'] = metadata

        raw = image.fp.read(16)
        if image:
            try:
                mime = utils.img_mime_type(raw)
            except TypeError:
                mime = 'application-octet-stream'
            form.append(
                {
                    'name': 'image',
                    'value': image.fp,
                    'filename': image.filename,
                    'content_type': mime,
                }
            )

        return self.rest.send(
            Route('POST', f'/guilds/{guild_id}/scheduled-events', guild_id=guild_id),
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
            if raw.startswith(b'{'):
                mime = 'application/json'
            else:
                mime = 'application/octet-stream'

        finally:
            file.reset()

        form = [
            {
                'name': 'file',
                'value': file.fp,
                'filename': file.filename,
                'content_type': mime,
            }
        ]

        if name:
            form.append({'name': 'name', 'value': name})
        if tags:
            form.append({'name': 'tags', 'value': tags})
        if description:
            form.append({'name': 'description', 'value': description})

        return self.rest.send(
            Route('POST', f'/guilds/{guild_id}/stickers', guild_id=guild_id),
            form=form,
            files=[file],
            reason=reason,
        )

    def modify_guild_sticker(
        self,
        guild_id: int,
        sticker_id: int,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[str] = None,
        reason: Optional[str] = None,
    ):
        json = {}

        if name:
            json['name'] = name
        if description:
            json['description'] = description
        if tags:
            json['tags'] = tags
        return self.rest.send(
            Route(
                'PATCH', f'/guilds/{guild_id}/stickers/{sticker_id}', guild_id=guild_id
            ),
            json=json,
            reason=reason,
        )

    def delete_guild_sticker(self, guild_id: int, sticker_id: int):
        return self.rest.send(
            Route(
                'DELETE', f'/guilds/{guild_id}/stickers/{sticker_id}', guild_id=guild_id
            )
        )

    def get_guild_bans(
        self,
        guild_id: int,
    ):
        return self.rest.send(
            Route('GET', f'/guilds/{guild_id}/bans', guild_id=guild_id)
        )

    def get_guild_ban(
        self,
        guild_id: int,
        user: int,
    ):
        return self.rest.send(
            Route('GET', f'/guilds/{guild_id}/bans/{user}', guild_id=guild_id)
        )

    def give_user_role(
        self,
        guild_id: int,
        user: int,
        role: int,
        *,
        reason: Optional[str] = None,
    ):
        return self.rest.send(
            Route(
                'PUT',
                f'/guilds/{guild_id}/members/{user}/roles/{role}',
                guild_id=guild_id,
            ),
            reason=reason,
        )

    def remove_user_role(
        self,
        guild_id: int,
        user: int,
        role: int,
        *,
        reason: Optional[str] = None,
    ):
        return self.rest.send(
            Route(
                'DELETE',
                f'/guilds/{guild_id}/members/{user}/roles/{role}',
                guild_id=guild_id,
            ),
            reason=reason,
        )

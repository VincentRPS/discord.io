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

import typing
from json import dumps
from ..file import File
from ..api.rest import RESTClient, Route
from ..types import allowed_mentions
from typing import Dict, Optional, Sequence
from ..snowflake import Snowflakeish
from ..assets import Attachment

class Channels:
    def __init__(self, rest: RESTClient):
        self.rest = rest

    
    def create_message(
        self,
        channel: Snowflakeish,
        content: typing.Optional[str] = None,
        files: typing.Optional[typing.Sequence[File]] = None,
        tts: typing.Optional[bool] = False,
        embeds: typing.List[Dict] = None,
        allowed_mentions: typing.Optional[allowed_mentions.MentionObject] = None,
        message_reference: typing.Optional[dict] = None,
        components: typing.Optional[typing.List[Dict]] = None,
    ) -> typing.Coroutine[typing.Any, typing.Any, typing.Union[typing.Any, None]]:
        json = {
            'tts': tts,
            'allowed_mentions': allowed_mentions,
        }
        if content is not None:
            json['content'] = content
        if message_reference is not None:
            json['message_reference'] = message_reference
        if components is not None:
            json['components'] = components
        if embeds is not None:
            json['embeds'] = embeds

        if files:
            form = []
            form.append({'name': 'payload_json', 'value': dumps(json)})
            if len(files) == 1:
                file = files[0]
                form.append(
                    {
                        'name': 'file',
                        'value': file.fp,
                        'filename': file.filename,
                        'content_type': 'application/octet-stream',
                    }
                )
            else:
                for index, file in enumerate(files):
                    form.append(
                        {
                            'name': f'file{index}',
                            'value': file.fp,
                            'filename': file.filename,
                            'content_type': 'application/octet-stream',
                        }
                    )

            return self.rest.send(
                Route('POST', f'/channels/{channel}/messages', channel_id=channel),
                json=json,
                form=form,
                files=files,
            )

        return self.rest.send(
            Route('POST', f'/channels/{channel}/messages', channel_id=channel),
            json=json,
        )

    def delete_message(self, message: int, channel: int, reason: Optional[str]):
        return self.rest.send(
            Route('DELETE', f'/channels/{channel}/messages/{message}'), reason=reason
        )

    def edit_message(
        self,
        channel: int,
        message: int,
        content: Optional[str] = None,
        embeds: Optional[typing.List[Dict]] = None,
        flags: Optional[int] = None,
        allowed_mentions: Optional[allowed_mentions.MentionObject] = None,
        components: Optional[typing.List[Dict]] = None,
        files: Optional[Sequence[File]] = None,
        attachments: Optional[typing.List[Attachment]] = None,
    ):
        form = []
        json = {
            'content': content,
            'embeds': embeds,
            'allowed_mentions': allowed_mentions,
            'components': components,
            'flags': flags,
        }
        if files:
            form.append({'name': 'payload_json', 'value': dumps(json)})
            if len(files) == 1:
                file = files[0]
                form.append(
                    {
                        'name': 'file',
                        'value': file.fp,
                        'filename': file.filename,
                        'content_type': 'application-octet-stream',
                    }
                )
            else:
                for index, file in enumerate(files):
                    form.append(
                        {
                            'name': f'file{index}',
                            'value': file.fp,
                            'filename': file.filename,
                            'content_type': 'application-octet-stream',
                        }
                    )
        if attachments:
            json['attachements'] = attachments

        return self.rest.send(
            Route(
                "PATCH",
                f"/channels/{channel}/messages/{message}",
                channel_id=channel,
                message_id=message,
            ),
            json=json,
            form=form,
            files=files,
        )

    def get_channel(self, channel: typing.Optional[Snowflakeish] = None):
        return self.rest.send(Route('GET', f'/channels/{channel}'))

    def edit_channel(
        self,
        name: typing.Optional[str] = None,
        channel: typing.Optional[Snowflakeish] = None,
        type: typing.Optional[str] = None,
    ):
        if type == 'group_dm':
            payload = {}
            if name:
                payload['name'] = name
        return self.rest.send(Route('PATCH', f'/channels/{channel}'))

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
            'max_age': max_age,
            'max_uses': max_uses,
            'tempoary': tempoary,
            'unique': unique,
        }
        if channel_id:
            json['channel_id'] = channel_id
        return self.rest.send(Route('POST'), reason=reason, json=json)

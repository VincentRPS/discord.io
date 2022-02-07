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
from typing import Union

from .enums import FormatType
from .state import ConnectionState
from .user import User


class Category:
    def __init__(self, data: dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    def permission_overwrites(self) -> list[str, Union[int, str]]:
        return self.from_dict["permission_overwrites"]

    @property
    def position(self) -> int:
        return self.from_dict["position"]

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    @property
    def name(self) -> str:
        return self.from_dict["name"]

    def guild_id(self) -> str:
        return self.from_dict["guild_id"]


class TextChannel:
    def __init__(self, data: dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    @property
    def guild_id(self) -> int:
        return self.from_dict["guild_id"]

    @property
    def name(self) -> str:
        return self.from_dict["name"]

    @property
    def position(self) -> int:
        return self.from_dict["position"]

    def permission_overwrites(self) -> list[str, Union[int, str]]:
        return self.from_dict["permission_overwrites"]

    @property
    def nsfw(self) -> bool:
        return self.from_dict["nsfw"]

    def topic(self) -> str:
        return self.from_dict["topic"]

    def last_message_id(self) -> int:
        return self.from_dict["last_message_id"]

    def category_id(self):
        return self.from_dict["parent_id"]


class VoiceChannel:
    def __init__(self, data: dict, state: ConnectionState):
        self.state = state
        self.from_dict = data

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    def guild_id(self) -> int:
        return self.from_dict["guild_id"]

    @property
    def name(self) -> str:
        return self.from_dict["name"]

    @property
    def position(self) -> int:
        return self.from_dict["position"]

    def permission_overwrites(self) -> list[str, Union[int, str]]:
        return self.from_dict["permission_overwrites"]


class DMChannel:
    def __init__(self, data: dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    def last_message_id(self) -> int:
        return self.from_dict["last_message_id"]

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    def recipients(self):
        return [User(user_data) for user_data in self.from_dict["recipients"]]


def parse_groupdm_icon(format: FormatType, group_id: int, group_icon_hash: str) -> str:
    return f"https://cdn.discordapp.com/icons/{group_id}/{group_icon_hash}.{format}"


class GroupDMChannel(DMChannel):
    def name(self) -> str:
        return self.from_dict["name"]

    def icon(self, format: FormatType = FormatType.PNG) -> str:
        parse_groupdm_icon(format, self.id, self.from_dict["icon"])

    def owner(self) -> User:
        user = self.state.app.factory.get_user(self.from_dict["owner"])
        return User(user)


class Thread:
    def __init__(self, data: dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    @property
    def guild_id(self) -> int:
        return self.from_dict["guild_id"]

    @property
    def channel_id(self) -> int:
        return self.from_dict["parent_id"]

    @property
    def owner_id(self) -> int:
        return self.from_dict["owner_id"]

    @property
    def name(self) -> str:
        return self.from_dict["name"]

    def last_message_id(self) -> int:
        return self.from_dict["last_message_id"]

    def message_count(self) -> int:
        return self.from_dict["message_count"]

    def member_count(self) -> int:
        return self.from_dict["member_count"]

    @property
    def metadata(self) -> "ThreadMetadata":
        return ThreadMetadata(self.from_dict["thread_metadata"])


class ThreadMetadata:
    def __init__(self, data: dict):
        self.from_dict = data

    def archived(self) -> bool:
        return self.from_dict["archived"]

    def auto_archive_duration(self) -> int:
        return self.from_dict["auto_archive_duration"]

    def archive_timestamp(self) -> str:
        return self.from_dict["archive_timestamp"]

    def locked(self) -> bool:
        return self.from_dict["locked"]

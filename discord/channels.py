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
from .guild import Guild
from .state import ConnectionState
from .user import User


class Category:
    """Represents a Discord Category
    
    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw category data
    state: :class:`state`
        The connection state
    """
    def __init__(self, data: dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    def permission_overwrites(self) -> list[str, Union[int, str]]:
        """Gives a list of permission overwrites
        
        Returns
        -------
        list[:class:`str`]
        list[:class:`int`]
        """
        return self.from_dict["permission_overwrites"]

    @property
    def position(self) -> int:
        """Gives the category position
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["position"]

    @property
    def id(self) -> int:
        """Gives the snowflake id of the channel
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["id"]

    @property
    def name(self) -> str:
        """Gives the name of the category
        
        Returns
        -------
        :class:`str`
        """
        return self.from_dict["name"]

    def guild_id(self) -> int:
        """Gives the guild' snowflake id
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["guild_id"]


class TextChannel:
    """Represents a Discord Text Channel
    
    Parameters
    ----------
    """
    def __init__(self, data: dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    @property
    def id(self) -> int:
        """Gives the channel' id
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["id"]

    @property
    def guild_id(self) -> int:
        """Gives the guild id of the channel
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["guild_id"]

    @property
    def name(self) -> str:
        """Gives the name of the channel
        
        Returns
        -------
        :class:`str`
        """
        return self.from_dict["name"]

    @property
    def position(self) -> int:
        """Gives the position of the channel
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["position"]

    def permission_overwrites(self) -> list[str, Union[int, str]]:
        """Gives the permission overwrites of the channel"""
        return self.from_dict["permission_overwrites"]

    @property
    def nsfw(self) -> bool:
        """If the channel is nsfw
        
        Returns
        -------
        :class:`bool`
        """
        return self.from_dict["nsfw"]

    def topic(self) -> str:
        """Gives the channel' topic
        
        Returns
        -------
        :class:`str`
        """
        return self.from_dict["topic"]

    def last_message_id(self) -> int:
        """Gives the snowflake id of the last message
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["last_message_id"]

    def category_id(self) -> int:
        """Gives the id of the category this channel is in
        
        Returns
        -------
        :class:`int`
        """
        return self.from_dict["parent_id"]


class VoiceChannel:
    def __init__(self, data: dict, state: ConnectionState):
        self.state = state
        self.from_dict = data

    @property
    def id(self) -> int:
        return self.from_dict["id"]

    @property
    def guild(self) -> Guild:
        id = self.from_dict["guild_id"]
        raw = self.state.app.fetch_raw_guild(guild_id=id)
        return Guild(raw, self.state.app.factory)

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

    @property
    def archived(self) -> bool:
        return self.from_dict["archived"]

    @property
    def auto_archive_duration(self) -> int:
        return self.from_dict["auto_archive_duration"]

    @property
    def archive_timestamp(self) -> str:
        return self.from_dict["archive_timestamp"]

    @property
    def locked(self) -> bool:
        return self.from_dict["locked"]

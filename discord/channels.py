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

from typing import Dict, List, Union

from .enums import FormatType
from .state import ConnectionState
from .user import User


def channel_parse(type, data: Dict, state: ConnectionState):
    if type == 0:
        return TextChannel(data, state)

    elif type == 1:
        return DMChannel(data, state)

    elif type == 2:
        return VoiceChannel(data, state)

    elif type == 3:
        return GroupDMChannel(data, state)

    elif type == 4:
        return Category(data, state)

    elif type == 5:
        return TextChannel(data, state)

    elif type in (10, 11, 12):
        return Thread(data, state)

    elif type == 13:
        return VoiceChannel(data, state)

    else:
        raise NotImplementedError('Channel is not a currently provided type')


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

    def __init__(self, data: Dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    def permission_overwrites(self) -> List[Union[int, str]]:
        """Gives a list of permission overwrites

        Returns
        -------
        list[:class:`str`]
        list[:class:`int`]
        """
        return self.from_dict['permission_overwrites']

    @property
    def position(self) -> int:
        """Gives the category position

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['position']

    @property
    def id(self) -> int:
        """Gives the snowflake id of the channel

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def name(self) -> str:
        """Gives the name of the category

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    def guild_id(self) -> int:
        """Gives the guild' snowflake id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['guild_id']


class TextChannel:
    """Represents a Discord Text Channel

    Parameters
    ----------
    data: :class:`dict`
        The raw json data
    state: :class:`ConnectionState`
        The connection state
    """

    def __init__(self, data: Dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    @property
    def id(self) -> int:
        """Gives the channel' id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def guild(self):
        """The guild this channel is in

        Returns
        -------
        :class:`Guild`
        """
        id = self.from_dict['guild_id']
        raw = self.state.app.fetch_guild(guild_id=id)
        return raw

    @property
    def guild_id(self) -> int:
        """Gives the guild id of the channel

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['guild_id']

    @property
    def name(self) -> str:
        """Gives the name of the channel

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    @property
    def position(self) -> int:
        """Gives the position of the channel

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['position']

    def permission_overwrites(self) -> List[Union[int, str]]:
        """Gives the permission overwrites of the channel"""
        return self.from_dict['permission_overwrites']

    @property
    def nsfw(self) -> bool:
        """If the channel is nsfw

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['nsfw']

    def topic(self) -> str:
        """Gives the channel' topic

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['topic']

    def last_message_id(self) -> int:
        """Gives the snowflake id of the last message

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['last_message_id']

    def category_id(self) -> int:
        """Gives the id of the category this channel is in

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['parent_id']


class VoiceChannel:
    """Represents a Discord Voice Channel

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw channel data
    state: :class:`ConnectionState`
        The connection state
    """

    def __init__(self, data: Dict, state: ConnectionState):
        self.state = state
        self.from_dict = data

    @property
    def id(self) -> int:
        """Gives the Voice Channel' Snowflake ID

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def guild(self):
        """The guild this channel is in

        Returns
        -------
        :class:`Guild`
        """
        id = self.from_dict['guild_id']
        raw = self.state.app.fetch_guild(guild_id=id)
        return raw

    @property
    def name(self) -> str:
        """The name of the voice channel

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    @property
    def position(self) -> int:
        """The voice channel' position

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['position']

    def permission_overwrites(self) -> List[Union[int, str]]:
        return self.from_dict['permission_overwrites']


class DMChannel:
    """Represents a Discord DM Channel

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw data
    state: :class:`ConnectionState`
        The connection state
    """

    def __init__(self, data: Dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    def last_message_id(self) -> int:
        """The snowflake id of the last message

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['last_message_id']

    @property
    def id(self) -> int:
        """The snowflake id of the channel

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    def recipients(self):
        """The list of users in the channel

        Returns
        -------
        List[:class:`User`]
        """
        return [User(user_data) for user_data in self.from_dict['recipients']]


def parse_groupdm_icon(format: FormatType, group_id: int, group_icon_hash: str) -> str:
    return f'https://cdn.discordapp.com/icons/{group_id}/{group_icon_hash}.{format}'


class GroupDMChannel(DMChannel):
    """Represents a Discord Group DM Channel

    .. versionadded:: 0.8.0

    Parameters
    -----------
    data: :class:`dict`
    """

    def name(self) -> str:
        """Gives the name of the Group DM

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    def icon(self, format: FormatType = FormatType.PNG) -> str:
        """Gives the link of the channel' icon

        Returns
        -------
        :class:`str`
        """
        return parse_groupdm_icon(format, self.id, self.from_dict['icon'])

    def owner(self) -> User:
        """Returns the User which is the owner of this Group DM

        Returns
        -------
        :class:`User`
        """
        user = self.state.app.factory.guilds.get_user(self.from_dict['owner'])
        return User(user)


class Thread:
    """Represents a Discord Thread

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw thread data
    state: :class:`ConnectionState`
        The connection state
    """

    def __init__(self, data: Dict, state: ConnectionState):
        self.from_dict = data
        self.state = state

    @property
    def id(self) -> int:
        """The thread' snowflake id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def guild_id(self) -> int:
        """The guild id of the thread

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['guild_id']

    @property
    def channel_id(self) -> int:
        """The channel id of the thread

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['parent_id']

    @property
    def owner_id(self) -> int:
        """Gives the owner id of the Thread

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['owner_id']

    @property
    def name(self) -> str:
        """Gives the name of the thread

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    def last_message_id(self) -> int:
        """Gives the last message id in the thread

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['last_message_id']

    def message_count(self) -> int:
        """Gives the amount of messages in the thread

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['message_count']

    def member_count(self) -> int:
        """Gives the thread' member count

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['member_count']

    @property
    def metadata(self) -> 'ThreadMetadata':
        """Gives the thread' metadata

        Returns
        -------
        :class:`ThreadMetadata`
        """
        return ThreadMetadata(self.from_dict['thread_metadata'])


class ThreadMetadata:
    """Represents a Thread' metadata

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The metadata
    """

    def __init__(self, data: Dict):
        self.from_dict = data

    @property
    def archived(self) -> bool:
        """If the thread is archived

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['archived']

    @property
    def auto_archive_duration(self) -> int:
        """The archived duration

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['auto_archive_duration']

    @property
    def archive_timestamp(self) -> str:
        """The archived timestamp

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['archive_timestamp']

    @property
    def locked(self) -> bool:
        """If the thread is locked or not

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['locked']


class ThreadMember:
    """Represents a Discord Thread Member

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw Member data
    """

    def __init__(self, data: Dict):
        self.from_dict = data

    @property
    def id(self) -> int:
        """Gives the thread id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def user_id(self) -> int:
        """Gives the thread members user id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['user_id']

    @property
    def join_timestamp(self) -> str:
        """Gives the thread members join time

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['join_timestamp']

    @property
    def flags(self) -> int:
        """Gives the thread members flags

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['flags']


class StageInstance:
    """Represents a Discord Stage Instance

    .. versionadded:: 0.8.0

    Parameters
    -----------
    data: :class:`dict`
        The raw stage instance data
    """

    def __init__(self, data: Dict):
        self.from_dict = data

    @property
    def id(self) -> int:
        """Gives the stage instance id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def guild_id(self) -> int:
        """Gives the guild id of the stage instance

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['guild_id']

    @property
    def channel_id(self) -> int:
        """Gives the channel id of the stage instance

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['channel_id']

    @property
    def topic(self) -> str:
        """Gives the stage instance' topic

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['topic']

    def privacy_level(self) -> int:
        """Gives the stage instance' privacy level

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['privacy_level']

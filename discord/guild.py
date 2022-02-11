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
"""Represents a Discord Guild.

ref: https://discord.dev/resources/guild
"""
from typing import List, Optional, Union

from .assets import Emoji
from .enums import FormatType, ScheduledEventStatusType, ScheduledEventType
from .member import Member
from .user import User

__all__: List[str] = ['Guild']


class Guild:
    """Represents a Discord Guild.

    .. versionadded:: 0.6.0

    Parameters
    ----------
    guild
        The raw guild object
    rest_factory
        The current :class:`RESTFactory`
    """

    # cache helpers for guilds.
    def __init__(self, guild: dict, rest_factory):
        self.from_dict = guild
        self._factory = rest_factory

    def joined_at(self) -> str:
        return self.from_dict['joined_at']

    def vanity(self) -> str:
        """The vanity url, if None returns None

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['vanity_url_code']

    def splash(self) -> str:
        """The splash screen, if None returns None

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['splash']

    def discovery_splash(self) -> str:
        """The discovery splash, if None returns None

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['discovery_splash']

    def sub_count(self) -> int:
        """The subscription count, returns a int

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['premium_subscription_count']

    def emojis(self) -> List[Emoji]:
        """A list of :class:`Emoji`

        Returns
        -------
        list[:class:`Emoji`]
        """
        return [Emoji(emoji) for emoji in self.from_dict['emojis']]

    @property
    def id(self) -> int:
        """The guild id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    async def get_member(self, id: int):
        """Gets a member and returns a :class:`Member` object

        Parameters
        ----------
        id
            The members id

        Returns
        -------
        :class:`Member`
        """
        unparsed = await self._factory.get_guild_member(self.id(), id)
        return Member(unparsed, self.id, self._factory)

    async def change_voice_state(
        self,
        *,
        channel: Optional[int] = None,
        self_mute: Optional[bool] = False,
        self_deaf: Optional[bool] = False,
    ):
        """Changes the bot's voice state in a guild

        .. versionadded:: 0.8.0

        Parameters
        ----------
        channel: :class:`int`
            The channel to connect to, None if to disconnect.
        self_mute
            Should the bot be muted?
        self_deaf
            Should the bot be deaf?
        """
        await self._factory.state.app.gateway.voice_state(
            guild=self.id, channel=channel, mute=self_mute, deaf=self_deaf
        )


def parse_role_icon(format: FormatType, role_id: int, role_icon: str) -> str:
    return f'https://cdn.discordapp.com/role-icons/{role_id}/{role_icon}.{format}'


def _parse_tags(data: dict) -> str:
    return data.get('bot_id') or data.get('integration_id') or ''


class Role:
    """Represents a Discord Role

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw role data
    """

    def __init__(self, data: dict):
        self.from_dict = data

    @property
    def id(self) -> int:
        """Gives the snowflake id of the role

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    @property
    def name(self) -> str:
        """Gives the name of the role

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    @property
    def color(self) -> int:
        """Returns the roles color

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['color']

    def hoist(self) -> bool:
        """If the role is hoisted or not

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['hoist']

    def icon(self, format: Optional[FormatType] = FormatType.PNG) -> str:
        """Gives the role icon's link, if any.

        Returns
        -------
        :class:`str`
        """
        return parse_role_icon(
            format=format, role_id=self.id, role_icon=self.from_dict['icon']
        )

    def unicode_emoji(self) -> str:
        """Gives the roles unicode emoji

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['unicode_emoji']

    @property
    def position(self) -> int:
        """Gives the current role position

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['position']

    def permissions(self) -> str:
        """Gives the role permissions

        Returns
        -------
        :class:`str`
        """
        # TODO: Replace with a Permission class?
        return self.from_dict['permissions']

    def managed(self) -> bool:
        """If the role is managed or not

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['managed']

    def mentionable(self) -> bool:
        """If the role is publicly mentionable

        Returns
        -------
        :class:`bool`
        """
        return self.from_dict['mentionable']

    def tags(self) -> str:
        """The current role' tags

        Returns
        -------
        :class:`str`
        """
        return _parse_tags(self.from_dict)


def parse_event_banner(format: FormatType, event_id: int, event_hash: str) -> str:
    return f'https://cdn.discordapp.com/guild-events/{event_id}/{event_hash}.{format}'


class ScheduledEvent:
    """Represents a Discord Guild Scheduled Event

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw event data
    """

    def __init__(self, data: dict):
        self.from_dict = data

    @property
    def id(self) -> int:
        """Gives the scheduled events snowflake id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['id']

    def guild_id(self) -> int:
        """Gives the scheduled event' current guild

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['guild_id']

    def channel_id(self) -> Union[int, None]:
        """Gives the scheduled events current channel, if any

        Returns
        -------
        :class:`int`
        :class:`None`
        """
        return self.from_dict.get('channel_id')

    @property
    def creator(self) -> User:
        """Gives a :class:`User` of the creator of this scheduled event

        Returns
        -------
        :class:`User`
        """
        return User(self.from_dict['creator'])

    @property
    def name(self) -> str:
        """Gives the scheduled event' name

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['name']

    @property
    def description(self) -> str:
        """Gives the description of the scheduled event

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['description']

    def start_time(self) -> str:
        """Gives the start time of the scheduled event

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['scheduled_start_time']

    def status(self) -> ScheduledEventStatusType:
        """Gives the current event' status

        Returns
        -------
        :class:`int`
        """
        if self.from_dict['status'] == ScheduledEventStatusType.ACTIVE:
            return ScheduledEventStatusType.ACTIVE
        elif self.from_dict['status'] == ScheduledEventStatusType.COMPLETED:
            return ScheduledEventStatusType.COMPLETED
        elif self.from_dict['status'] == ScheduledEventStatusType.SCHEDULED:
            return ScheduledEventStatusType.SCHEDULED
        elif self.from_dict['status'] == ScheduledEventStatusType.CANCELED:
            return ScheduledEventStatusType.CANCELED

    def end_time(self) -> Union[None, str]:
        """Gives the endtime of the scheduled event

        Returns
        -------
        :class:`str`
        :class:`None`
        """
        return self.from_dict.get('scheduled_end_time')

    def type(self) -> ScheduledEventType:
        """Gives the type of scheduled event

        Returns
        -------
        :class:`int`
        """
        if self.from_dict['entity_type'] == ScheduledEventType.STAGE_INSTANCE:
            return ScheduledEventType.STAGE_INSTANCE
        elif self.from_dict['entity_type'] == ScheduledEventType.VOICE:
            return ScheduledEventType.VOICE
        elif self.from_dict['entity_type'] == ScheduledEventType.EXTERNAL:
            return ScheduledEventType.EXTERNAL

    def entity_id(self) -> int:
        """Gives the current entity id

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['entity_id']

    @property
    def metadata(self) -> 'ScheduledEventMetadata':
        """Gives the scheduled event metadata

        Returns
        -------
        :class:`ScheduledEventMetadata`
        """
        return ScheduledEventMetadata(self.from_dict['entity_metadata'])

    def joined(self) -> int:
        """Gives the amount of users which joined the event

        Returns
        -------
        :class:`int`
        """
        return self.from_dict['user_count']

    def image(self, format: FormatType = FormatType.PNG):
        """Gives the url of the scheduled event' banner

        Returns
        -------
        :class:`str`
        """
        return parse_event_banner(
            format=format, event_id=self.id, event_hash=self.from_dict['image']
        )


class ScheduledEventMetadata:
    """Represents a Discord Scheduled event metadata

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw metadata' data
    """

    def __init__(self, data: dict):
        self.from_dict = data

    @property
    def location(self) -> Union[str, None]:
        """Gives the location the event is happening in

        Returns
        -------
        :class:`str`
        :class:`None`
        """
        return self.from_dict['location']


class WelcomeScreen:
    """Represents a Discord Guild WelcomeScreen

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
    """

    def __init__(self, data: dict):
        self.from_dict = data

    @property
    def description(self) -> str:
        """Gives the WelcomeScreen' description

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['description']

    def channels(self) -> list['WelcomeChannel']:
        """Gives a list of :class:`WelcomeChannel`

        Returns
        -------
        list[:class:`WelcomeChannel`]
        """
        return [
            WelcomeChannel(channel) for channel in self.from_dict['welcome_channels']
        ]


class WelcomeChannel:
    """Represents a Discord WelcomeScreen Channel

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw WelcomeChannel data
    """

    def __init__(self, data: dict):
        self.from_dict = data

    @property
    def channel_id(self) -> int:
        """Gives the Channel' id


        Returns
        -------
        :class:`int`
        """
        return self.from_dict['channel_id']

    @property
    def description(self) -> str:
        """Gives the description of the channel

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['description']

    def emoji_id(self) -> Union[int, None]:
        """Gives the Emoji id, if any

        Returns
        -------
        :class:`int`
        :class:`None`
        """
        return self.from_dict.get('emoji_id')

    def emoji_name(self) -> Union[str, None]:
        """Gives the Emoji name, if any

        Returns
        -------
        :class:`str`
        :class:`None`
        """
        return self.from_dict.get('emoji_name')

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
from typing import Dict, List, Optional, Union

from .assets import Emoji, Sticker
from .channels import channel_parse
from .enums import FormatType, ScheduledEventStatusType, ScheduledEventType
from .http import RESTFactory
from .member import Member
from .user import User

__all__: List[str] = [
    'Guild',
    'Role',
    'WelcomeScreen',
    'WelcomeChannel',
    'ScheduledEvent',
    'ScheduledEventMetadata',
]


class BanObject:
    """Represents a Discord Ban Object

    .. versionadded:: 1.0

    Parameters
    ----------
    data: :class:`dict`
        The raw data
    """

    def __init__(self, data: Dict):
        self.from_dict = data

    @property
    def reason(self) -> str:
        """The reason of the ban

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['reason']

    @property
    def user(self) -> User:
        """The user which invoked the ban

        Returns
        -------
        :class:`User`
        """
        return User(self.from_dict['user'])


def parse_guild_hash(type: int, id, hash: str):

    if type == 1:
        return f"https://cdn.discordapp.com/icons/{id}/{hash}"

    elif type == 2:
        return f"https://cdn.discordapp.com/splashes/{id}/{hash}"

    elif type == 3:
        return f'https://cdn.discordapp.com/discovery-splashes/{id}/{hash}'


class GuildPreview:
    """Represents a Discord Guild Preview.

    .. versionadded:: 1.0

    Parameters
    ----------
    data: :class:`dict`
        The raw preview data
    """

    def __init__(self, data: dict):
        self.from_dict = data

    @property
    def id(self) -> int:
        return self.from_dict['id']

    @property
    def name(self) -> str:
        return self.from_dict['name']

    @property
    def icon_url(self) -> str:
        return parse_guild_hash(1, self.id, self.from_dict['icon'])

    @property
    def splash_url(self) -> str:
        return parse_guild_hash(2, self.id, self.from_dict['splash'])

    @property
    def discovery_splash_url(self) -> str:
        return parse_guild_hash(3, self.id, self.from_dict['discovery_splash'])

    @property
    def emojis(self) -> List[Emoji]:
        return [Emoji(emoji) for emoji in self.from_dict['emojis']]

    def features(self) -> str:
        return self.from_dict['features']

    def approximate_member_count(self) -> int:
        return self.from_dict['approximate_member_count']

    def approximate_presence_count(self) -> int:
        return self.from_dict['approximate_presence_count']

    @property
    def description(self) -> str:
        return self.from_dict.get('description')

    @property
    def stickers(self) -> List[Sticker]:
        return [Sticker(sticker) for sticker in self.from_dict['stickers']]


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
    def __init__(self, guild: Dict, rest_factory):
        self.from_dict = guild
        self._factory: RESTFactory = rest_factory

    def __repr__(self):
        return f"<Guild guild_id={self.id!r}>"

    @property
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
        unparsed = await self._factory.guilds.get_guild_member(self.id, id)
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

    def leave(self):
        """Leaves the guild"""
        return self._factory.guilds.leave_guild(self.id)

    async def get_channels(self):
        """Gives a list of Channel objects

        Returns
        -------
        List[Union[:class:`TextChannel`, :class:`VoiceChannel`, :class:`Category`, :class:`DMChannel`, :class:`GroupDMChannel`, :class:`Thread`]]
        """
        raw = await self._factory.channels.get_guild_channels(self.id)
        return [
            channel_parse(channel['type'], channel, self._factory.state)
            for channel in raw
        ]

    async def get_bans(self):
        """Gives a list of :class:`Ban`

        Returns
        -------
        List[:class:`Ban`]
        """
        raw = await self._factory.guilds.get_guild_bans(self.id)
        return [BanObject(ban) for ban in raw]

    async def get_ban(self, user_id: int):
        """Gets a ban for a user

        Parameters
        ----------
        user_id: :class:`int`
            The user id to get the ban for

        Returns
        -------
        :class:`Ban`
        """
        raw = await self._factory.guilds.get_guild_ban(self.id, user_id)
        return BanObject(raw)

    async def get_preview(self):
        raw = await self._factory.guilds.get_guild_preview(self.id)
        return GuildPreview(raw)


def parse_role_icon(format: FormatType, role_id: int, role_icon: str) -> str:
    return f'https://cdn.discordapp.com/role-icons/{role_id}/{role_icon}.{format}'


def _parse_tags(data: Dict) -> str:
    return data.get('bot_id') or data.get('integration_id') or ''


class Role:
    """Represents a Discord Role

    .. versionadded:: 0.8.0

    Parameters
    ----------
    data: :class:`dict`
        The raw role data
    """

    def __init__(self, data: Dict, factory):
        self.from_dict = data
        self.factory: RESTFactory = factory

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

    def give_to(self, user_id: int, reason: Optional[str] = None):
        """Gives a user the role"""
        return self.factory.guilds.give_user_role(user_id, self.id, reason=reason)

    def remove_from(
        self,
        user_id: int,
        reason: Optional[str] = None,
    ):
        """Removes a user from the role"""
        return self.factory.guilds.remove_user_role(user_id, self.id, reason=reason)


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

    def __init__(self, data: Dict, factory):
        self.from_dict = data
        self.factory: RESTFactory = factory

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

    def __init__(self, data: Dict):
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

    def __init__(self, data: Dict, factory):
        self.from_dict = data
        self.factory: RESTFactory = factory

    @property
    def description(self) -> str:
        """Gives the WelcomeScreen' description

        Returns
        -------
        :class:`str`
        """
        return self.from_dict['description']

    def channels(self) -> List['WelcomeChannel']:
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

    def __init__(self, data: Dict):
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

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

from typing import TYPE_CHECKING, Dict, Union
from .user import User
from .enums import FormatType, ScheduledEventStatusType, ScheduledEventType

if TYPE_CHECKING:
    from .http import RESTFactory

def parse_event_banner(format: FormatType, event_id: int, event_hash: str) -> str:
    return f'https://cdn.discordapp.com/guild-events/{event_id}/{event_hash}.{format}'

__all__ = (
    'ScheduledEvent',
    'ScheduledEventMetadata'
)

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
        return int(self.from_dict['id'])

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
        return parse_event_banner(format=format, event_id=self.id, event_hash=self.from_dict['image'])


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


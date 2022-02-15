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

from typing import Callable, List, TypeVar

__all__ = ['MessageFlags', 'Intents']

T = TypeVar('T')

class flag_value:
    def __init__(self, func: Callable):
        self.flag = func(None)
        self.__doc__ = func.__doc__


class MessageFlags:
    """Represents a discord message flag object

    .. versionadded:: 0.7.0
    """

    @classmethod
    def CROSSPOSTED(self):
        return 1 << 0

    @classmethod
    def IS_CROSSPOSTED(self):
        return 1 << 1

    @classmethod
    def SUPPRESS_EMBEDS(self):
        return 1 << 2

    @classmethod
    def SOURCE_MESSAGE_DELETED(self):
        return 1 << 3

    @classmethod
    def URGENT(self):
        return 1 << 4

    @classmethod
    def HAS_THREAD(self):
        return 1 << 5

    @classmethod
    def EPHEMERAL(self):
        return 1 << 6

    @classmethod
    def LOADING(self):
        return 1 << 7


class Intents:
    """Helps defining your Intents.
    For a full list of intents and there usage please visit
    https://discord.dev/topics/gateway#gateway-intents

    .. versionadded:: 0.3.0
    """

    GUILDS = 1 << 0
    """Adding this will allow your bot to listen to:
    
    - `GUILD_JOIN`
    - `GUILD_UPDATE`
    - `GUILD_DELETE`
    - `GUILD_ROLE_CREATE`
    - `GUILD_ROLE_UPDATE`
    - `GUILD_ROLE_DELETE`
    - `CHANNEL_CREATE`
    - `CHANNEL_EDIT`
    - `CHANNEL_DELETE`
    - `CHANNEL_PINS_UPDATE`
    """

    GUILD_MEMBERS = 1 << 1
    """Adding this will allow your bot to listen to:

    .. warning::

        This is a **priviledged intent**, and requires you to enable it to use.
    
    - `GUILD_MEMBER_ADD`
    - `GUILD_MEMBER_UPDATE`
    - `GUILD_MEMBER_REMOVE`
    """

    GUILD_BANS = 1 << 2
    """Adding this will allow your bot to listen to:
    
    .. warning::

        This is a **priviledged intent**, and requires you to enable it to use.
    
    - `GUILD_BAN_ADD`
    - `GUILD_BAN_REMOVE`
    """

    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    """Adding this will allow your bot to listen to:
    
    - `GUILD_EMOJIS_UPDATE`
    - `GUILD_STICKERS_UPDATE`
    """

    GUILD_INTEGRATIONS = 1 << 4
    """Adding this will allow your bot to listen to:
    
    .. note:: this event(s) hasn't been added to the core library yet

    - `INTEGRATION_CREATE`
    - `INTEGRATION_UPDATE`
    - `INTEGRATION_DELETE`
    """

    GUILD_WEBHOOKS = 1 << 5
    """Adding this will allow your bot to listen to:

    - `WEBHOOKS_UPDATE`
    """

    GUILD_INVITES = 1 << 6
    """Adding this will allow your bot to listen to:
    
    - `INVITE_CREATE`
    - `INVITE_DELETE`
    """

    GUILD_VOICE_STATES = 1 << 7
    """Adding this will allow your bot to listen to:
    
    - `RAW_VOICE_STATE_UPDATE`
    """

    GUILD_PRESENCES = 1 << 8
    """Adding this will allow your bot to listen to:
    
    .. warning::

        This is a **priviledged intent**, and requires you to enable it to use.
    
    - `PRESENCE_UPDATE`
    """

    GUILD_MESSAGES = 1 << 9
    """Adding this will allow your bot to listen to:
    
    - `MESSAGE_CREATE`
    - `MESSAGE_UPDATE`
    - `MESSAGE_DELETE`
    - `MESSAGE_BULK_DELETE`
    """

    GUILD_MESSAGE_REACTIONS = 1 << 10
    """Adding this will allow your bot to listen to:
    
    - `REACTION_ADD`
    - `REACTION_REMOVE`
    - `REACTION_REMOVE_ALL`
    - `REACTION_REMOVE_EMOJI`
    """

    GUILD_MESSAGE_TYPING = 1 << 11
    """Adding this will allow your bot to listen to:
    
    - `TYPING`
    """

    DIRECT_MESSAGES = 1 << 12
    """Adding this will allow your bot to listen to:
    
    - `MESSAGE_CREATE`
    - `MESSAGE_UPDATE`
    - `MESSAGE_DELETE`
    """

    DIRECT_MESSAGE_REACTIONS = 1 << 13
    """Adding this will allow your bot to listen to:
    
    - `REACTION_ADD`
    - `REACTION_REMOVE`
    - `REACTION_REMOVE_ALL`
    - `REACTION_REMOVE_EMOJI`
    """

    DIRECT_MESSAGE_TYPING = 1 << 14
    """Adding this will allow your bot to listen to:
    
    - `TYPING`
    """

    MESSAGE_CONTENT = 1 << 15
    """Adding this will allow your bot to receive content 
    within `MESSAGE` events which aren't in direct messages.
    """

    GUILD_SCHEDULED_EVENTS = 1 << 16
    """Adding this will allow your bot to listen to:
    
    - `SCHEDULED_EVENT` (`SCHEDULED_EVENT_CREATE`)
    - `SCHEDULED_EVENT_EDIT` (`SCHEDULED_EVENT_UPDATE`)
    - `SCHEDULED_EVENT_DELETE`
    - `SCHEDULED_EVENT_JOIN`
    - `SCHEDULED_EVENT_LEAVE`
    """

    UNPRIVLEDGED_GUILD = (
        GUILD_BANS
        | GUILD_EMOJIS_AND_STICKERS
        | GUILD_INTEGRATIONS
        | GUILD_WEBHOOKS
        | GUILD_INVITES
        | GUILD_VOICE_STATES
    )
    """Adding this will give you every non-privledged guild intent"""

    PRIVLEDGED_GUILD = GUILD_MEMBERS | GUILD_PRESENCES
    """Adding this will give you every priviledged and non-privledged guild intent"""

    ALL_DM = DIRECT_MESSAGES | DIRECT_MESSAGE_REACTIONS | DIRECT_MESSAGE_TYPING
    """Adding this will give you every dm intent"""

    ALL_UNPRIVLEDGED = ALL_DM | UNPRIVLEDGED_GUILD
    """Adding this will give you every un-priviledged intent"""

    ALL_PRIVLEDGED = ALL_UNPRIVLEDGED | MESSAGE_CONTENT | PRIVLEDGED_GUILD
    """Adding this will give you every un-priviledged and priviledged intent"""



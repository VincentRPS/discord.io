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


class Intents:
    """Helps defining your Intents
    For a full list of intents and there usage please visit
    https://discord.dev/topics/gateway#gateway-intents

    .. versionadded:: 0.3.0

    Values
    ------
    default

    all

    GUILDS

    GUILD_MEMBERS

    GUILD_BANS

    GUILD_EMOJIS_AND_STICKERS

    GUILD_INTEGRATIONS

    GUILD_WEBHOOKS

    GUILD_INVITES

    GUILD_VOICE_STATES

    GUILD_PRESENCES

    GUILD_MESSAGES

    GUILD_MESSAGE_REACTIONS

    GUILD_MESSAGE_TYPING

    DIRECT_MESSAGES

    DIRECT_MESSAGE_REACTIONS

    DIRECT_MESSAGE_TYPING

    GUILD_SCHEDULED_EVENTS
    """

    def __init__(self, intents: int = 0):
        self.intents = intents
        if self.intents == "0":
            intents = self.default()

    @classmethod
    def default():
        """Gives every non-privledged Intent"""
        return 32509

    @classmethod
    def all():
        """Gives every Intent"""
        return 32767

    def GUILDS(self):
        return 1 << 0

    def GUILD_MEMBERS(self):
        return 1 << 1

    def GUILD_BANS(self):
        return 1 << 2

    def GUILD_EMOJIS_AND_STICKERS(self):
        return 1 << 3

    def GUILD_INTEGRATIONS(self):
        return 1 << 4

    def GUILD_WEBHOOKS(self):
        return 1 << 5

    def GUILD_INVITES(self):
        return 1 << 6

    def GUILD_VOICE_STATES(self):
        return 1 << 7

    def GUILD_PRESENCES(self):
        return 1 << 8

    def GUILD_MESSAGES(self):
        return 1 << 9

    def GUILD_MESSAGE_REACTIONS(self):
        return 1 << 10

    def GUILD_MESSAGE_TYPING(self):
        return 1 << 11

    def DIRECT_MESSAGES(self):
        return 1 << 12

    def DIRECT_MESSAGE_REACTIONS(self):
        return 1 << 13

    def DIRECT_MESSAGE_TYPING(self):
        return 1 << 14

    def GUILD_SCHEDULED_EVENTS(self):
        return 1 << 16

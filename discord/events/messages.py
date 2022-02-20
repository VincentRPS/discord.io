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


from typing import Any, Dict, List

from ..assets import Emoji
from ..channels import TextChannel
from ..guild import Guild
from ..member import Member
from ..message import Message
from .core import Event

__all__: List[str] = ['OnMessage', 'OnMessageEdit', 'OnMessageDelete']


class OnMessage(Event):
    """Returns a :class:`Message`"""

    def process(self) -> None:
        ret = Message(self.data, self.state.app)
        self.state.messages.new(self.data['id'], self.data)

        try:
            self.state.channels.edit(ret.channel.id, ret.channel.from_dict)
        except TypeError:
            # DM Channels
            pass
        self.dispatch('MESSAGE', ret)

        # ext.commands
        for command in self.state.prefixed_commands:
            if ret.content.startswith(command.prefix):
                content = ret.content[len(command.prefix) :]
                if content.startswith(command.name):
                    command.invoke(ret, content=content)


class OnMessageEdit(Event):
    """Returns the new :class:`Message` and if cached the old :class:`Message`"""

    def process(self):
        try:
            before = Message(self.state.messages.get(self.data['id']), self.state.app)
        except KeyError:
            # if the message is not in the cache we cant really save it.
            before = None
        after = Message(self.data, self.state.app)
        self.dispatch('MESSAGE_EDIT', before, after)

        self.state.messages.edit(self.data['id'], self.data)


class OnMessageDelete(Event):
    """Gives the deleted :class:`Message`"""

    def process(self):
        try:
            message = Message(self.state.messages.pop(self.data['id']), self.state.app)
        except KeyError:
            message = None
        self.dispatch('MESSAGE_DELETE', message)


class OnMessageDeleteBulk(Event):
    """A event which gets called when multiple messages are deleted

    Returns
    -------
    Messages: list[:class:`Message`]
    Channel: :class:`TextChannel`
    Guild: :class:`Guild`
    """

    def process(self):
        msgs: List[Dict[str, Any]] = [
            msg for msg in self.state.messages.get(self.data['ids'])
        ]
        messages = [Message(msg, self.state.app) for msg in msgs]
        channel = TextChannel(
            self.state.channels.get(self.data['channel_id']), self.state
        )
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.dispatch('MESSAGE_BULK_DELETE', messages, channel, guild)

        for msg in self.data['ids']:
            self.state.messages.pop(msg)


class OnMessageReactionAdd(Event):
    """Gives a :class:`Message` and a :class:`Emoji` that was added."""

    def process(self):
        emoji = Emoji(self.data['emoji'])
        channel = TextChannel(
            self.state.channels.get(self.data['channel_id']), self.state
        )
        try:
            message = Message(self.state.messages.get('message_id'), self.state.app)
        except AttributeError:
            message = None
        guild = Guild(self.state.guilds.get('guild_id'), self.state.app.factory)
        member = Member(
            self.state.members.get(self.data['user_id']),
            guild.id,
            self.state.app.factory,
        )

        self.dispatch('MESSAGE_REACTION_ADD', emoji, message, channel, guild, member)


class OnMessageReactionRemove(Event):
    """Gives a :class:`Message` and a :class:`Emoji` that was removed."""

    def process(self):
        emoji = Emoji(self.data['emoji'])
        channel = TextChannel(self.state.channels.get(self.data['channel_id']))
        message = Message(self.state.messages.get('message_id'), self.state.app)
        guild = Guild(self.state.guilds.get('guild_id'), self.state.app.factory)
        member = Member(
            self.state.members.get(self.data['user_id']),
            guild.id,
            self.state.app.factory,
        )

        self.dispatch('MESSAGE_REACTION_REMOVE', emoji, message, channel, guild, member)


class OnMessageReactionRemoveAll(Event):
    """Event called when all reactions are removed from a message

    Returns
    -------
    Channel: :class:`TextChannel`
    Message: :class:`Message`
    Guild: :class:`Guild`
    """

    def process(self):
        channel = TextChannel(self.state.channels.get(self.data['channel_id']))
        message = Message(self.state.messages.get('message_id'), self.state.app)
        guild = Guild(self.state.guilds.get('guild_id'), self.state.app.factory)

        self.dispatch('MESSAGE_REACTION_REMOVE_ALL', message, channel, guild)


class OnMessageReactionRemoveEmoji(Event):
    """A event which happens when a emoji is removed from a guild and therefore the message

    Returns
    -------
    Emoji: :class:`Emoji`
    Channel: :class:`TextChannel`
    Message: :class:`Message`
    Guild: :class:`Guild`
    """

    def process(self):
        emoji = Emoji(self.data['emoji'])
        channel = TextChannel(self.state.channels.get(self.data['channel_id']))
        message = Message(self.state.messages.get('message_id'), self.state.app)
        guild = Guild(self.state.guilds.get('guild_id'), self.state.app.factory)

        self.dispatch('MESSAGE_REACTION_REMOVE_EMOJI', emoji, message, channel, guild)

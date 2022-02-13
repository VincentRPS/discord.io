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

from ..assets import Emoji, Sticker
from ..guild import Guild, Role, ScheduledEvent
from ..member import Member
from ..user import User
from .core import Event


# join/leave/update
class OnGuildJoin(Event):
    """A event that gets called when you join a guild

    Returns
    -------
    Guild: :class:`Guild`
    """

    def process(self):
        ret = Guild(self.data, self.state.app.factory)

        self.dispatch('GUILD_JOIN', ret)


class OnGuildUpdate(Event):
    """A event which is called when a guild is updated

    Returns
    -------
    before: :class:`Guild`
    after: :class:`Guild`
    """

    def process(self):
        before = Guild(self.state.guilds.get(self.data['id']), self.state.app.factory)
        after = Guild(self.data, self.state.app.factory)
        self.state.guilds.edit(self.data['id'], self.data)

        self.dispatch('GUILD_UPDATE', before, after)


class OnGuildLeave(Event):
    """Gets called when your bot leaves or gets kicked from a guild

    Returns
    -------
    Guild: :class:`Guild`
    """

    def process(self):
        guild = Guild(self.state.guilds.pop(self.data['id']), self.state.app.factory)
        self.dispatch('GUILD_LEAVE', guild)


# bans
class OnGuildBan(Event):
    """Gets called when a member is banned from a guild

    Returns
    -------
    User: :class:`User`
    Guild: :class:`Guild`
    """

    def process(self):
        user = User(self.data['user'])
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.dispatch('GUILD_BAN', user, guild)


class OnGuildBanRemove(Event):
    """Gets called when a guild ban gets removed

    Returns
    -------
    User: :class:`User`
    Guild: :class:`Guild`
    """

    def process(self):
        user = User(self.data['user'])
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.dispatch('GUILD_BAN_REMOVE', user, guild)


class OnGuildIntegrationsUpdate(Event):
    """Called when a integration is updated

    Returns
    -------
    Guild: :class:`Guild`
    """

    def process(self):
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.dispatch('GUILD_INTEGRATIONS_UPDATE', guild)


# assets


class OnGuildEmojisUpdate(Event):
    """Called when 1 or more guild emojis is updated

    Returns
    -------
    Emojis: list[:class:`Emoji`]
    Guild: :class:`Guild`
    """

    def process(self):
        emojis = [Emoji(emoji) for emoji in self.data['emojis']]
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )
        self.dispatch('GUILD_EMOJIS_UPDATE', emojis, guild)


class OnGuildStickersUpdate(Event):
    """Called when 1 or more guild stickers are updated

    Returns
    -------
    Stickers: list[:class:`Sticker`]
    Guild: :class:`Guild`
    """

    def process(self):
        stickers = [Sticker(sticker, self.state) for sticker in self.data['stickers']]
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.dispatch('GUILD_STICKERS_UPDATE', stickers, guild)


# members
class OnMemberJoin(Event):
    """Gets called when a member joins a guild

    Returns
    -------
    Member: :class:`Member`
    Guild: :class:`Guild`
    """

    def process(self):
        # it says inner payload so i would guess it's a member keyword?
        member = Member(self.data, self.data['guild_id'], self.state.app.factory)
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.dispatch('MEMBER_JOIN', member, guild)


class OnMemberLeave(Event):
    """Gets called when a member leaves a guild

    Returns
    -------
    User: :class:`User`
    Guild: :class:`Guild`
    """

    def process(self):
        user = User(self.data['user'])
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        for member in self.state.members._cache.values():
            if member.user.id == user.id:
                self.state.members.pop(member)

        self.dispatch('MEMBER_LEAVE', user, guild)


class OnMemberUpdate(Event):
    """Called when a member is updated

    Returns
    -------
    before: :class:`Member`, could be :class:`None`
    after: :class:`Member`
    """

    def process(self):
        before = None
        for member in self.state.members._cache.values():
            if member.user.id == self.data['user']['id']:
                before = member
                self.state.members.pop(member)

        after = Member(self.data, self.data['guild_id'], self.state.app.factory)

        self.dispatch('MEMBER_UPDATE', before, after)


# roles
class OnRoleCreate(Event):
    """Gets called when a role is created

    Returns
    -------
    Role: :class:`Role`
    Guild: :class:`Guild`
    """

    def process(self):
        role = Role(self.data['role'])
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.state.roles.new(role.id, role)

        self.dispatch('ROLE_CREATE', role, guild)


class OnRoleUpdate(Event):
    """Gets called when a role is updated

    Returns
    -------
    before: :class:`Role`, can be :class:`None`
    after: :class:`Role`
    Guild: :class:`Guild`
    """

    def process(self):
        before = Role(self.state.roles.get(self.data['role']['id']))
        after = Role(self.data['role'])
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )
        self.state.roles.edit(after.id, after)

        self.dispatch('ROLE_UPDATE', before, after, guild)


class OnRoleDelete(Event):
    """Gets caleld when a role is deleted

    Returns
    -------
    role: :class:`Role`, can be :class:`None`
    Guild: :class:`Guild`
    """

    def process(self):
        role = Role(self.state.roles.pop(self.data['role_id']))
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )

        self.dispatch('ROLE_DELETE', role, guild)


class OnScheduledEventCreate(Event):
    """Gets called when a scheduled event is created

    Returns
    -------
    Event: :class:`ScheduledEvent`
    """

    def process(self):
        ret = ScheduledEvent(self.data)
        self.state.guild_events.new(ret.id, self.data)
        self.dispatch('scheduled_event', ret)


class OnScheduledEventUpdate(Event):
    """Gets called when a scheduled event is updated

    Returns
    -------
    before: :class:`ScheduledEvent`, can be :class:`None`
    after: :class:`SchduledEvent`
    """

    def process(self):
        after = ScheduledEvent(self.data)
        raw_before = self.state.guild_events.get(after.id)
        before = raw_before

        self.dispatch('scheduled_event_edit', before, after)
        self.state.guild_events.edit(after.id, self.data)


class OnScheduledEventDelete(Event):
    """Gets called when a scheduled event is deleted

    Returns
    -------
    Event: :class:`ScheduledEvent`
    """

    def process(self):
        event = ScheduledEvent(self.data)
        self.dispatch('scheduled_event_delete', event)
        self.state.guild_events.pop(event)


class OnScheduledEventJoin(Event):
    """Gets called when a scheduled event is joined by a member

    Returns
    -------
    Event: :class:`ScheduledEvent`
    User: :class:`User`
    Guild: :class:`Guild`
    """

    def process(self):
        raw_event_id = self.data['guild_scheduled_event_id']
        raw_user_id = self.data['user_id']
        raw_guild_id = self.data['guild_id']
        raw_event = self.state.guild_events.get(raw_event_id)
        raw_user = self.state.members.get(raw_user_id)
        raw_guild = self.state.guilds.get(raw_guild_id)
        event = ScheduledEvent(raw_event)
        user = User(raw_user)
        guild = Guild(raw_guild)

        self.dispatch('scheduled_event_join', event, user, guild)


class OnScheduledEventLeave(Event):
    """Gets called when a user leaves a scheduled event

    Returns
    -------
    Event: :class:`ScheduledEvent`
    User: :class:`Member`
    Guild: :class:`Guild`
    """

    def process(self):
        raw_event_id = self.data['guild_scheduled_event_id']
        raw_user_id = self.data['user_id']
        raw_guild_id = self.data['guild_id']
        raw_event = self.state.guild_events.get(raw_event_id)
        raw_user = self.state.members.get(raw_user_id)
        raw_guild = self.state.guilds.get(raw_guild_id)
        event = ScheduledEvent(raw_event)
        user = Member(raw_user)
        guild = Guild(raw_guild)

        self.dispatch('scheduled_event_join', event, user, guild)

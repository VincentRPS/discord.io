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
    def process(self):
        ret = Guild(self.data, self.state.app.factory)

        self.dispatch("GUILD_JOIN", ret)


class OnGuildUpdate(Event):
    def process(self):
        before = Guild(
            self.state._guilds_cache.get(self.data["id"]), self.state.app.factory
        )
        after = Guild(self.data, self.state.app.factory)
        self.state._guilds_cache.edit(self.data["id"], self.data)

        self.dispatch("GUILD_UPDATE", before, after)


class OnGuildLeave(Event):
    def process(self):
        guild = Guild(
            self.state._guilds_cache.pop(self.data["id"]), self.state.app.factory
        )
        self.dispatch("GUILD_LEAVE", guild)


# bans
class OnGuildBan(Event):
    def process(self):
        user = User(self.data["user"])
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        self.dispatch("GUILD_BAN", user, guild)


class OnGuildBanRemove(Event):
    def process(self):
        user = User(self.data["user"])
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        self.dispatch("GUILD_BAN_REMOVE", user, guild)


class OnGuildIntegrationsUpdate(Event):
    def process(self):
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        self.dispatch("GUILD_INTEGRATIONS_UPDATE", guild)


# assets


class OnGuildEmojisUpdate(Event):
    def process(self):
        emojis = [Emoji(emoji) for emoji in self.data["emojis"]]
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )
        self.dispatch("GUILD_EMOJIS_UPDATE", emojis, guild)


class OnGuildStickersUpdate(Event):
    def process(self):
        stickers = [Sticker(sticker, self.state) for sticker in self.data["stickers"]]
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        self.dispatch("GUILD_STICKERS_UPDATE", stickers, guild)


# members
class OnMemberJoin(Event):
    def process(self):
        # it says inner payload so i would guess it's a member keyword?
        member = Member(self.data, self.data["guild_id"], self.state.app.factory)
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        self.dispatch("MEMBER_JOIN", member, guild)


class OnMemberLeave(Event):
    def process(self):
        user = User(self.data["user"])
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        for member in self.state.members._cache.values():
            if member.user.id == user.id:
                self.state.members.pop(member)

        self.dispatch("MEMBER_LEAVE", user, guild)


class OnMemberUpdate(Event):
    def process(self):
        before = None
        for member in self.state.members._cache.values():
            if member.user.id == self.data["user"]["id"]:
                before = member
                self.state.members.pop(member)

        after = Member(self.data, self.data["guild_id"], self.state.app.factory)

        self.dispatch("MEMBER_UPDATE", before, after)


# roles
class OnRoleCreate(Event):
    def process(self):
        role = Role(self.data["role"])
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        self.state.roles.new(role.id, role)

        self.dispatch("ROLE_CREATE", role, guild)


class OnRoleUpdate(Event):
    def process(self):
        before = Role(self.state.roles.get(self.data["role"]["id"]))
        after = Role(self.data["role"])
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )
        self.state.roles.edit(after.id, after)

        self.dispatch("ROLE_UPDATE", before, after, guild)


class OnRoleDelete(Event):
    def process(self):
        role = Role(self.state.roles.pop(self.data["role_id"]))
        guild = Guild(
            self.state._guilds_cache.get(self.data["guild_id"]), self.state.app.factory
        )

        self.dispatch("ROLE_DELETE", role, guild)


class OnScheduledEventCreate(Event):
    def process(self):
        ret = ScheduledEvent(self.data)
        self.state.guild_events.new(ret.id, self.data)
        self.dispatch("scheduled_event", ret)


class OnScheduledEventUpdate(Event):
    def process(self):
        after = ScheduledEvent(self.data)
        raw_before = self.state.guild_events.get(after.id)
        before = raw_before

        self.dispatch("scheduled_event_edit", before, after)
        self.state.guild_events.edit(after.id, self.data)


class OnScheduledEventDelete(Event):
    def process(self):
        event = ScheduledEvent(self.data)
        self.dispatch("scheduled_event_delete", event)
        self.state.guild_events.pop(event)


class OnScheduledEventJoin(Event):
    def process(self):
        raw_event_id = self.data["guild_scheduled_event_id"]
        raw_user_id = self.data["user_id"]
        raw_guild_id = self.data["guild_id"]
        raw_event = self.state.guild_events.get(raw_event_id)
        raw_user = self.state.members.get(raw_user_id)
        raw_guild = self.state._guilds_cache.get(raw_guild_id)
        event = ScheduledEvent(raw_event)
        user = User(raw_user)
        guild = Guild(raw_guild)

        self.dispatch("scheduled_event_join", event, user, guild)


class OnScheduledEventLeave(Event):
    def process(self):
        raw_event_id = self.data["guild_scheduled_event_id"]
        raw_user_id = self.data["user_id"]
        raw_guild_id = self.data["guild_id"]
        raw_event = self.state.guild_events.get(raw_event_id)
        raw_user = self.state.members.get(raw_user_id)
        raw_guild = self.state._guilds_cache.get(raw_guild_id)
        event = ScheduledEvent(raw_event)
        user = Member(raw_user)
        guild = Guild(raw_guild)

        self.dispatch("scheduled_event_join", event, user, guild)

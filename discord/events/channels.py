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

from ..channels import TextChannel, Thread, ThreadMember, channel_parse
from ..guild import Guild
from ..member import Member
from .core import Event


class OnChannelCreate(Event):
    """Called when a channel is created

    Returns
    -------
    A channel type
    """

    def process(self):
        channel = channel_parse(self.data["type"], self.data, self.state)
        self.state.channels.new(channel.id, self.data)
        self.dispatch("channel_create", channel)


class OnChannelUpdate(Event):
    """Gets called when a channel is updated

    Returns
    -------
    A channel type
    """

    def process(self):
        before_raw = self.state.channels.get(self.data["id"])
        before = channel_parse(before_raw["type"], self.data, self.state)
        after = channel_parse(self.data["type"], self.data, self.state)
        self.dispatch("channel_edit", before, after)
        self.state.channels.edit(before.id, self.data)


class OnChannelDelete(Event):
    """Called when a channel is deleted

    Returns
    -------
    A channel type, can be :class:`None`
    """

    def process(self):
        raw = self.state.channels.get(self.data["id"])
        channel = channel_parse(raw["type"], self.data, self.state)
        self.dispatch("channel_delete", channel)
        self.state.channels.pop(self.data["id"])


class OnChannelPinsUpdate(Event):
    """Called when channel pins are updated

    Returns
    -------
    Channel: :class:`TextChannel`
    Guild: :class:`Guild`
    last_pin: :class:`str`
    """

    def process(self):
        raw = self.state.channels.get(self.data["channel_id"])
        raw_guild = self.state.guilds.get(self.data["guild_id"])
        last_pin = self.data.get("last_pin_timestamp")
        channel = TextChannel(raw, self.state)
        guild = Guild(raw_guild, self.state.app.factory)

        self.dispatch("CHANNEL_PINS_UPDATE", channel, guild, last_pin)


class OnThreadCreate(Event):
    """Called when a thread is created

    Returns
    -------
    Thread: :class:`Thread`
    """

    def process(self):
        thread = Thread(self.data, self.state)
        self.dispatch("thread_create", thread)


class OnThreadUpdate(Event):
    """Called when a thread is updated

    Returns
    -------
    before: :class:`Thread`, can be :class:`None`
    after: :class:`Thread`
    """

    def process(self):
        before_raw = self.state.channels.get(self.data["id"])
        before = Thread(before_raw)
        after = Thread(self.data, self.state)
        self.dispatch("thread_edit", before, after)
        self.state.channels.edit(before.id, self.data)


class OnThreadDelete(Event):
    """Called when a thread is deleted

    .. note::

        This event shouldn't accur on archival

    Returns
    -------
    Thread: :class:`Thread`, can be :class:`None`
    """

    def process(self):
        thread_raw = self.state.channels.get(self.data["id"])
        thread = Thread(thread_raw)
        self.dispatch("thread_delete", thread)
        self.state.channels.pop(self.data["id"])


class OnThreadListSync(Event):
    """Called when discord syncs the current threads

    Returns
    -------
    Channels: List[:class:`TextChannel`]
    threads: List[:class:`Thread`]
    members: List[:class:`Member`]
    """

    def process(self):
        guild = Guild(
            self.state.guilds.get(self.data.get("guild_id")), self.state.app.factory
        )
        channels = [
            TextChannel(channel, self.state) for channel in self.data.get("channel_ids")
        ]
        threads = [Thread(thread, self.state) for thread in self.data.get("threads")]
        members = [
            Member(member, guild.id, self.state.app.factory)
            for member in self.data.get("members")
        ]
        self.dispatch("thread_list_sync", channels, threads, members)


class OnThreadMemberUpdate(Event):
    """Called when a thread member is updated

    Returns
    -------
    Member: :class:`ThreadMember`
    Guild: :class:`Guild`
    """

    def process(self):
        member = ThreadMember(self.data)
        guild = Guild(self.data["guild_id"], self.state.app.factory)

        self.dispatch("thread_member_update", member, guild)


class OnThreadMembersUpdate(Event):
    """Called when multiple thread members are updated

    Returns
    -------
    Thread: :class:`Thread`
    Guild: :class:`Guild`
    added_members: List[:class:`ThreadMember`]
    removed_members: List[:class:`ThreadMember`]
    member_count: :class:`int`
    """

    def process(self):
        added_members = [ThreadMember(member) for member in self.data["added_members"]]
        guild = Guild(self.data["guild_id"], self.state.app.factory)
        thread = Thread(self.state.channels.get(self.data["id"]), self.state)
        member_count: int = self.data["member_count"]
        removed_members = self.data.get("removed_member_ids")

        self.dispatch(
            "thread_members_update",
            thread,
            guild,
            added_members,
            removed_members,
            member_count,
        )

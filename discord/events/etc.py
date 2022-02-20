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


from ..channels import StageInstance, TextChannel
from ..guild import Guild
from ..member import Member
from ..user import User
from .core import Event


class OnStageInstanceCreate(Event):
    """Called when a stage instance is created

    Returns
    -------
    Stage: :class:`StageInstance`
    """

    def process(self):
        ret = StageInstance(self.data)
        self.state.stage_instances.new(self.data['id'], self.data)

        self.dispatch('stage_instance_create', ret)


class OnStageInstanceEdit(Event):
    """Gets called when a stage instance is edited

    Returns
    -------
    before: :class:`StageInstance`, can be :class:`None`
    after: :class:`StageInstance`
    """

    def process(self):
        before = StageInstance(self.state.stage_instances.get(self.data['id']))
        after = StageInstance(self.data)
        self.state.stage_instances.edit()

        self.dispatch('stage_instance_edit', before, after)


class OnStageInstanceDelete(Event):
    """Called when a stage instance is deleted

    Returns
    -------
    Stage: :class:`StageInstance`
    """

    def process(self):
        ret = StageInstance(self.data)
        self.state.stage_instances.pop(self.data['id'])

        self.dispatch('stage_instance_delete', ret)


class OnTyping(Event):
    """Gets called when a user starts typing

    Returns
    -------
    Member: :class:`Member`
    User: :class:`User`
    Channel: :class:`TextChannel`
    timestamp: :class:`str`
    """

    def process(self):
        channel = TextChannel(
            self.state.channels.get(self.data['channel_id']), self.state
        )

        try:
            guild = Guild(
                self.state.guilds.get(self.data['guild_id']), self.state.app.factory
            )
        except KeyError:
            guild = None
        user = User(self.state.members.get(self.data['user_id']))
        timestamp: int = self.data['timestamp']

        try:
            member = Member(self.data['member'], guild.id, self.state.app.factory)
        except KeyError:
            member = None

        self.dispatch('typing', member, user, channel, timestamp)


class OnInviteCreate(Event):
    """Called when a invite is created

    Returns
    -------
    Channel: :class:`TextChannel`
    Code: :class:`str`
    created_at: :class:`str`
    guild: :class:`Guild`
    inviter: :class:`User`
    max_age: :class:`int`
    max_uses: :class:`int`
    target_type: :class:`int`
    target_user: :class:`User`
    target_application: :class:`Any`
    tempoary: :class:`bool`
    uses: :class:`int`
    """

    def process(self):
        channel = TextChannel(
            self.state.channels.get(self.data.get('channel_id')), self.state
        )
        code: str = self.data.get('code')
        created_at: str = self.data.get('created_at')
        guild = Guild(self.state.guilds.get(self.data['guild_id']))
        inviter = User(self.data['inviter'])
        max_age: int = self.data.get('max_age')
        max_uses: int = self.data.get('max_uses')
        target_type: int = self.data.get('target_type')
        target_user = User(self.data.get('target_user'))
        target_application = self.data.get('target_application')
        tempoary: bool = self.data.get('tempoary')
        uses: int = self.data.get('uses')

        self.dispatch(
            'invite_create',
            channel,
            code,
            created_at,
            guild,
            inviter,
            max_age,
            max_uses,
            target_type,
            target_user,
            target_application,
            tempoary,
            uses,
        )


class OnInviteDelete(Event):
    """Gets called when a invite is deleted

    Returns
    -------
    Channel: :class:`TextChannel`
    Guild: :class:`Guild`
    Code: :class:`str`
    """

    def process(self):
        channel = TextChannel(
            self.state.channels.get(self.data.get('channel_id')), self.state
        )
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )
        code: str = self.data.get('code')

        self.dispatch('invite_delete', channel, guild, code)


class OnUserUpdate(Event):
    """Gets called when a user is updated

    Returns
    -------
    User: :class:`User`
    """

    def process(self):
        user = User(self.data)

        self.dispatch('user_update', user)


class OnWebhooksUpdate(Event):
    """Gets called when webhooks are updated

    Returns
    -------
    Guild: :class:`Guild`
    Channel: :class:`TextChannel`
    """

    def process(self):
        guild = Guild(
            self.state.guilds.get(self.data['guild_id']), self.state.app.factory
        )
        channel = TextChannel(
            self.state.channels.get(self.data['channel_id']), self.state
        )

        self.dispatch('webhooks_update', guild, channel)

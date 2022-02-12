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
from aio.types import Dict

from ..guild import ScheduledEvent
from ..state import ConnectionState, member_cacher
from .channels import (
    OnChannelCreate,
    OnChannelDelete,
    OnChannelPinsUpdate,
    OnChannelUpdate,
    OnThreadCreate,
    OnThreadDelete,
    OnThreadListSync,
    OnThreadMembersUpdate,
    OnThreadMemberUpdate,
    OnThreadUpdate,
)
from .etc import (
    OnInviteCreate,
    OnInviteDelete,
    OnStageInstanceCreate,
    OnStageInstanceDelete,
    OnStageInstanceEdit,
    OnTyping,
    OnUserUpdate,
    OnWebhooksUpdate,
)
from .guilds import (
    OnGuildBan,
    OnGuildBanRemove,
    OnGuildEmojisUpdate,
    OnGuildIntegrationsUpdate,
    OnGuildJoin,
    OnGuildLeave,
    OnGuildStickersUpdate,
    OnGuildUpdate,
    OnMemberJoin,
    OnMemberLeave,
    OnMemberUpdate,
    OnRoleCreate,
    OnRoleDelete,
    OnRoleUpdate,
    OnScheduledEventCreate,
    OnScheduledEventDelete,
    OnScheduledEventJoin,
    OnScheduledEventLeave,
    OnScheduledEventUpdate,
)
from .interactions import OnInteraction
from .messages import (
    OnMessage,
    OnMessageDelete,
    OnMessageDeleteBulk,
    OnMessageEdit,
    OnMessageReactionAdd,
    OnMessageReactionRemove,
    OnMessageReactionRemoveAll,
    OnMessageReactionRemoveEmoji,
)


# https://discord.dev/topics/gateway#commands-and-events-gateway-events
class Cataloger:
    def __init__(self, data: Dict, dis, state: ConnectionState):

        # guilds
        if data['t'] == 'GUILD_CREATE':
            state.guilds.new(data['d']['id'], data['d'])
            # roles, channels
            for channel in data['d']['channels']:
                state.channels.new(channel['id'], channel)
            for role in data['d']['roles']:
                state.roles.new(role['id'], role)
            for event in data['d']['guild_scheduled_events']:
                even = ScheduledEvent(event)
                state.guild_events.new(even.id, even)
            dis.dispatch('RAW_GUILD_CREATE', data['d'])
            OnGuildJoin(data['d'], dis, state)

        elif data['t'] == 'GUILD_DELETE':
            dis.dispatch('RAW_GUILD_DELETE', data['d'])
            OnGuildLeave(data['d'], dis, state)

        elif data['t'] == 'GUILD_UPDATE':
            dis.dispatch('RAW_GUILD_UPDATE', data['d'])
            OnGuildUpdate(data['d'], dis, state)

        elif data['t'] == 'GUILD_BAN_ADD':
            dis.dispatch('RAW_BAN_ADD', data['d'])
            OnGuildBan(data['d'], dis, state)

        elif data['t'] == 'GUILD_BAN_REMOVE':
            dis.dispatch('RAW_BAN_REMOVE', data['d'])
            OnGuildBanRemove(data['d'], dis, state)

        elif data['t'] == 'GUILD_EMOJIS_UPDATE':
            dis.dispatch('RAW_EMOJIS_UPDATE', data['d'])
            OnGuildEmojisUpdate(data['d'], dis, state)

        elif data['t'] == 'GUILD_STICKERS_UPDATE':
            dis.dispatch('RAW_STICKERS_UPDATE', data['d'])
            OnGuildStickersUpdate(data['d'], dis, state)

        elif data['t'] == 'GUILD_INTEGRATIONS_UPDATE':
            dis.dispatch('RAW_GUILD_INTEGRATIONS_UPDATE', data['d'])
            OnGuildIntegrationsUpdate(data['d'], dis, state)

        elif data['t'] == 'GUILD_MEMBER_ADD':
            dis.dispatch('RAW_GUILD_MEMBER_ADD', data['d'])
            OnMemberJoin(data['d'], dis, state)

        elif data['t'] == 'GUILD_MEMBER_REMOVE':
            dis.dispatch('RAW_GUILD_MEMBER_REMOVE', data['d'])
            OnMemberLeave(data['d'], dis, state)

        elif data['t'] == 'GUILD_MEMBER_UPDATE':
            dis.dispatch('RAW_MEMBER_UPDATE', data['d'])
            OnMemberUpdate(data['d'], dis, state)

        elif data['t'] == 'GUILD_MEMBERS_CHUNK':
            dis.dispatch('RAW_GUILD_MEMBERS_CHUNK', data['d'])
            member_cacher(state, data['d']['members'])

        elif data['t'] == 'ROLE_CREATE':
            dis.dispatch('RAW_ROLE_CREATE', data['d'])
            OnRoleCreate(data['d'], dis, state)

        elif data['t'] == 'ROLE_UPDATE':
            dis.dispatch('RAW_ROLE_UPDATE', data['d'])
            OnRoleUpdate(data['d'], dis, state)

        elif data['t'] == 'ROLE_DELETE':
            dis.dispatch('RAW_ROLE_DELETE', data['d'])
            OnRoleDelete(data['d'], dis, state)

        elif data['t'] == 'GUILD_SCHEDULED_EVENT_CREATE':
            dis.dispatch('RAW_SCHEDULED_EVENT_CREATE', data['d'])
            OnScheduledEventCreate(data['d'], dis, state)

        elif data['t'] == 'GUILD_SCHEDULED_EVENT_UPDATE':
            dis.dispatch('RAW_SCHEDULED_EVENT_UPDATE', data['d'])
            OnScheduledEventUpdate(data['d'], dis, state)

        elif data['t'] == 'GUILD_SCHEDULED_EVENT_DELETE':
            dis.dispatch('RAW_SCHEDULED_EVENT_DELETE', data['d'])
            OnScheduledEventDelete(data['d'], dis, state)

        elif data['t'] == 'GUILD_SCHEDULED_EVENT_USER_ADD':
            dis.dispatch('RAW_SCHEDULED_EVENT_JOIN', data['d'])
            OnScheduledEventJoin(data['d'], dis, state)

        elif data['t'] == 'GUILD_SCHEDULED_EVENT_USER_REMOVE':
            dis.dispatch('RAW_SCHEDULED_EVENT_LEAVE', data['d'])
            OnScheduledEventLeave(data['d'], dis, state)

        # channels
        elif data['t'] == 'CHANNEL_CREATE':
            dis.dispatch('RAW_CHANNEL_CREATE', data['d'])
            OnChannelCreate(data['d'], dis, state)

        elif data['t'] == 'CHANNEL_UPDATE':
            dis.dispatch('RAW_CHANNEL_UPDATE', data['d'])
            OnChannelUpdate(data['d'], dis, state)

        elif data['t'] == 'CHANNEL_DELETE':
            dis.dispatch('RAW_CHANNEL_DELETE', data['d'])
            OnChannelDelete(data['d'], dis, state)

        elif data['t'] == 'CHANNEL_PINS_UPDATE':
            dis.dispatch('RAW_CHANNEL_PINS_UPDATE', data['t'])
            OnChannelPinsUpdate(data['d'], dis, state)

        elif data['t'] == 'THREAD_CREATE':
            dis.dispatch('RAW_THREAD_CREATE', data['d'])
            OnThreadCreate(data['d'], dis, state)

        elif data['t'] == 'THREAD_UPDATE':
            dis.dispatch('RAW_THREAD_UPDATE', data['d'])
            OnThreadUpdate(data['d'], dis, state)

        elif data['t'] == 'THREAD_DELETE':
            dis.dispatch('RAW_THREAD_DELETE', data['d'])
            OnThreadDelete(data['d'], dis, state)

        elif data['t'] == 'THREAD_LIST_SYNC':
            dis.dispatch('RAW_THREAD_LIST_SYNC', data['d'])
            OnThreadListSync(data['d'], dis, state)

        elif data['t'] == 'THREAD_MEMBER_UPDATE':
            dis.dispatch('RAW_THREAD_MEMBER_UPDATE', data['d'])
            OnThreadMemberUpdate(data['d'], dis, state)

        elif data['t'] == 'THREAD_MEMBERS_UPDATE':
            dis.dispatch('RAW_THREAD_MEMBERS_UPDATE', data['d'])
            OnThreadMembersUpdate(data['d'], dis, state)

        # messages
        elif data['t'] == 'MESSAGE_CREATE':
            dis.dispatch('RAW_MESSAGE', data['d'])
            OnMessage(data['d'], dis, state)

        elif data['t'] == 'MESSAGE_DELETE':
            dis.dispatch('RAW_MESSAGE_DELETE', data['d'])
            OnMessageDelete(data['d'], dis, state)

        elif data['t'] == 'MESSAGE_UPDATE':
            dis.dispatch('RAW_MESSAGE_EDIT', data['d'])
            OnMessageEdit(data['d'], dis, state)

        elif data['t'] == 'MESSAGE_DELETE_BULK':
            dis.dispatch('RAW_MESSAGE_DELETE_BULK', data['d'])
            OnMessageDeleteBulk(data['d'], dis, state)

        elif data['t'] == 'MESSAGE_REACTION_ADD':
            dis.dispatch('RAW_MESSAGE_REACTION_ADD', data['d'])
            OnMessageReactionAdd(data['d'], dis, state)

        elif data['t'] == 'MESSAGE_REACTION_REMOVE':
            dis.dispatch('RAW_MESSAGE_REACTION_REMOVE', data['d'])
            OnMessageReactionRemove(data['d'], dis, state)

        elif data['t'] == 'MESSAGE_REACTION_REMOVE_ALL':
            dis.dispatch('RAW_MESSAGE_REACTION_REMOVE_ALL', data['d'])
            OnMessageReactionRemoveAll(data['d'], dis, state)

        elif data['t'] == 'MESSAGE_REACTION_REMOVE_EMOJI':
            dis.dispatch('RAW_MESSAGE_REACTION_REMOVE_EMOJI', data['d'])
            OnMessageReactionRemoveEmoji(data['d'], dis, state)

        # interactions
        elif data['t'] == 'INTERACTION_CREATE':
            dis.dispatch('RAW_INTERACTION', data['d'])
            OnInteraction(data['d'], dis, state)

        # etc
        elif data['t'] == 'TYPING_START':
            dis.dispatch('RAW_TYPING_START', data['d'])
            OnTyping(data['d'], dis, state)

        elif data['t'] == 'STAGE_INSTANCE_CREATE':
            dis.dispatch('RAW_STAGE_INSTANCE_CREATE', data['d'])
            OnStageInstanceCreate(data['d'], dis, state)

        elif data['t'] == 'STAGE_INSTANCE_DELETE':
            dis.dispatch('RAW_STAGE_INSTANCE_DELETE', data['d'])
            OnStageInstanceDelete(data['d'], dis, state)

        elif data['t'] == 'STAGE_INSTANCE_UPDATE':
            dis.dispatch('RAW_STAGE_INSTANCE_UPDATE', data['d'])
            OnStageInstanceEdit(data['d'], dis, state)

        elif data['t'] == 'USER_UPDATE':
            dis.dispatch('RAW_USER_UPDATE', data['d'])
            OnUserUpdate(data['d'], dis, state)

        elif data['t'] == 'WEBHOOKS_UPDATE':
            dis.dispatch('RAW_WEBHOOKS_UPDATE', data['d'])
            OnWebhooksUpdate(data['d'], dis, state)

        elif data['t'] == 'INVITE_CREATE':
            dis.dispatch('RAW_INVITE_CREATE', data['d'])
            OnInviteCreate(data['d'], dis, state)

        elif data['t'] == 'INVITE_DELETE':
            dis.dispatch('RAW_INVITE_DELETE', data['d'])
            OnInviteDelete(data['d'], dis, state)

        # there are some non-included events.
        else:
            dis.dispatch(f'RAW_{data["t"]}', data['d'])

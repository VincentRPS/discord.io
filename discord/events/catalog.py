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
from discord.types import Dict

from ..state import ConnectionState, member_cacher
from .guilds import *
from .interactions import OnInteraction
from .messages import OnMessage, OnMessageDelete, OnMessageEdit


# https://discord.dev/topics/gateway#commands-and-events-gateway-events
class Cataloger:
    def __init__(self, data: Dict, dis, state: ConnectionState):

        # guilds
        if data["t"] == "GUILD_CREATE":
            state._guilds_cache.new(data["d"]["id"], data["d"])
            dis.dispatch("RAW_GUILD_CREATE", data["d"])
            OnGuildJoin(data["d"], dis, state)

        elif data["t"] == "GUILD_DELETE":
            dis.dispatch("RAW_GUILD_DELETE", data["d"])
            OnGuildLeave(data["d"], dis, state)

        elif data["t"] == "GUILD_UPDATE":
            dis.dispatch("RAW_GUILD_UPDATE", data["d"])
            OnGuildUpdate(data["d"], dis, state)

        elif data["t"] == "GUILD_BAN_ADD":
            dis.dispatch("RAW_BAN_ADD", data["d"])
            OnGuildBan(data["d"], dis, state)

        elif data["t"] == "GUILD_BAN_REMOVE":
            dis.dispatch("RAW_BAN_REMOVE", data["d"])
            OnGuildBanRemove(data["d"], dis, state)

        elif data["t"] == "GUILD_EMOJIS_UPDATE":
            dis.dispatch("RAW_EMOJIS_UPDATE", data["d"])
            OnGuildEmojisUpdate(data["d"], dis, state)

        elif data["t"] == "GUILD_STICKERS_UPDATE":
            dis.dispatch("RAW_STICKERS_UPDATE", data["d"])
            OnGuildStickersUpdate(data["d"], dis, state)

        elif data["t"] == "GUILD_INTEGRATIONS_UPDATE":
            dis.dispatch("RAW_GUILD_INTEGRATIONS_UPDATE", data["d"])
            OnGuildIntegrationsUpdate(data["d"], dis, state)

        elif data["t"] == "GUILD_MEMBER_ADD":
            dis.dispatch("RAW_GUILD_MEMBER_ADD", data["d"])
            OnMemberJoin(data["d"], dis, state)

        elif data["t"] == "GUILD_MEMBER_REMOVE":
            dis.dispatch("RAW_GUILD_MEMBER_REMOVE", data["d"])
            OnMemberLeave(data["d"], dis, state)

        elif data["t"] == "GUILD_MEMBER_UPDATE":
            dis.dispatch("RAW_MEMBER_UPDATE", data["d"])
            OnMemberUpdate(data["d"], dis, state)

        elif data["t"] == "GUILD_MEMBERS_CHUNK":
            dis.dispatch("RAW_GUILD_MEMBERS_CHUNK", data["d"])
            member_cacher(state, data["d"]["members"], data["d"]["guild_id"], Member)

        # messages
        elif data["t"] == "MESSAGE_CREATE":
            dis.dispatch("RAW_MESSAGE", data["d"])
            OnMessage(data["d"], dis, state)

        elif data["t"] == "MESSAGE_DELETE":
            dis.dispatch("RAW_MESSAGE_DELETE", data["d"])
            OnMessageDelete(data["d"], dis, state)

        elif data["t"] == "MESSAGE_UPDATE":
            dis.dispatch("RAW_MESSAGE_EDIT", data["d"])
            OnMessageEdit(data["d"], dis, state)

        # interactions
        elif data["t"] == "INTERACTION_CREATE":
            dis.dispatch("RAW_INTERACTION", dis, state)
            OnInteraction(data["d"], dis, state)

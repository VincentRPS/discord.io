"""
Apache-2.0

Copyright 2021 RPS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the LICENSE file for the specific language governing permissions and
limitations under the License.
"""
from enum import Enum


class GatewayOpcodes(Enum):
    """Gateway Opcodes
    https://discord.com/developers/docs/topics/opcodes-and-status-codes#gateway-gateway-opcodes
    """

    Dispatch = 0
    Heartbeat = 1
    Identify = 2
    Presence_Update = 3
    Voice_State_Update = 4
    Resume = 6
    Reconnect = 7
    Request_Guild_Members = 8
    Invalid_Session = 9
    Hello = 10
    Heartbeat_ACK = 11

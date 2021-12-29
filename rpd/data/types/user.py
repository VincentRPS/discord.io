# Apache-2.0
#
# Copyright 2021 VincentRPS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the LICENSE file for the specific language governing permissions and
# limitations under the License.
import typing

from .snowflake import Snowflake


class PartialUser(typing.TypedDict):
    id: Snowflake
    username: str
    discriminator: str
    avatar: typing.Optional[str]


PremiumType = typing.Literal[0, 1, 2]


class User(PartialUser, total=False):
    bot: bool
    system: bool
    mfa_enabled: bool
    local: str
    verified: bool
    email: typing.Optional[str]  # might be stupid but i don't think this is needed?
    flags: int
    premium_type: PremiumType
    public_flags: int

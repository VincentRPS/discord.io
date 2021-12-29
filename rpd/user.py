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
from rpd import helpers
from rpd.data.types.user import User
from rpd.internal.http import HTTPClient

class ClientUser:
    __slots__ = ('locale', '_flags', 'verified', 'mfa_enabled', '__weakref__')

    if typing.TYPE_CHECKING:
        verified: bool
        locale: typing.Optional[str]
        mfa_enabled: bool
        _flags: int

    def __init__(self, *, data: User) -> None:
        super().__init__(data=data)
        self.http = HTTPClient()

    def __repr__(self) -> str:
        return (
            f'<ClientUser id={self.id} name={self.name!r} discriminator={self.discriminator!r}'
            f' bot={self.bot} verified={self.verified} mfa_enabled={self.mfa_enabled}>'
        )

    def _update(self, data: User) -> None:
        super()._update(data)
        # There's actually an Optional[str] phone field as well but I won't use it
        self.verified = data.get('verified', False)
        self.locale = data.get('locale')
        self._flags = data.get('flags', 0)
        self.mfa_enabled = data.get('mfa_enabled', False)

    async def edit(self, *, username: str = helpers.MISSING, avatar: bytes = helpers.MISSING) -> ClientUser:
        payload: typing.Dict[str, typing.Any] = {}
        if username is not typing.MISSING:
            payload['username'] = username

        if avatar is not typing.MISSING:
            payload['avatar'] = helpers._bytes_to_base64_data(avatar)

        data: User = await self.http.edit_profile(payload)
        return ClientUser(data=data)
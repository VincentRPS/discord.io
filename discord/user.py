# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
from discord_typings import UserData

from .cache import Cache
from .internal import undefined


class User:
    def __init__(self, data: UserData, cache: Cache) -> None:
        self._cache = cache

        self.id = data['id']
        self.username = data['username']
        self.discriminator = data['discriminator']
        self.avatar = data['avatar']
        self.bot = data.get('bot', undefined.UNDEFINED)
        self.system = data.get('system', undefined.UNDEFINED)
        self.mfa_enabled = data.get('mfa_enabled', undefined.UNDEFINED)
        self.banner = data.get('banner', undefined.UNDEFINED)
        self.accent_color = data.get('accent_color', undefined.UNDEFINED)
        self.locale = data.get('locale', undefined.UNDEFINED)
        self.verified = data.get('verified', undefined.UNDEFINED)
        self.email = data.get('email', undefined.UNDEFINED)
        self.flags = data.get('flags', undefined.UNDEFINED)
        self.premium_type = data.get('premium_type', undefined.UNDEFINED)
        self.public_flags = data.get('public_flags', undefined.UNDEFINED)

    @property
    def name(self) -> str:
        return self.username

    @property
    def is_human(self) -> bool:
        return self.bot is False

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
from discord.state import ConnectionState


class TestCache:
    state = ConnectionState()
    json = {  # this isn't exactly what the payload would be.
        "name": "discord.io",
        "members": 0,
        "bots": 0,
        "shard": 0,
        "school_hub": False,
    }

    def test_a_cache(self):
        # caching a simple fake guild
        self.state._guilds_cache["935701676948590642"] = self.json

    def get_cache(self):
        assert self.state._guilds_cache["935701676948590642"] == self.json

    def intents(self):
        assert self.state._bot_intents == 1

    def not_ready(self):
        assert self.state._ready.is_set() is False

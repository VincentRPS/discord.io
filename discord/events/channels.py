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

from ..channels import Thread, channel_parse

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
from .core import Event


class OnChannelCreate(Event):
    def process(self):
        channel = channel_parse(self.data["type"], self.data, self.state)
        self.state.channels.new(channel.id, self.data)
        self.dispatch("channel_create", channel)


class OnChannelUpdate(Event):
    def process(self):
        before_raw = self.state.channels.get(self.data["id"])
        before = channel_parse(before_raw["type"], self.data, self.state)
        after = channel_parse(self.data["type"], self.data, self.state)
        self.dispatch("channel_edit", before, after)
        self.state.channels.edit(before.id, self.data)


class OnChannelDelete(Event):
    def process(self):
        raw = self.state.channels.get(self.data["id"])
        channel = channel_parse(raw["type"], self.data, self.state)
        self.dispatch("channel_delete", channel)
        self.state.channels.pop(self.data["id"])


class OnThreadCreate(Event):
    def process(self):
        thread = Thread(self.data, self.state)
        self.dispatch("thread_create", thread)


class OnThreadUpdate(Event):
    def process(self):
        before_raw = self.state.channels.get(self.data["id"])
        before = Thread(before_raw)
        after = Thread(self.data, self.state)
        self.dispatch("thread_edit", before, after)
        self.state.channels.edit(before.id, self.data)


class OnThreadDelete(Event):
    def process(self):
        thread_raw = self.state.channels.get(self.data["id"])
        thread = Thread(thread_raw)
        self.dispatch("thread_delete", thread)
        self.state.channels.pop(self.data["id"])


class OnThreadListSync(Event):
    ...

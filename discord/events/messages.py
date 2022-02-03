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
from discord.cache import Message

from .core import Event


class OnMessage(Event):
    """Returns a :class:`Message`"""

    def process(self) -> None:
        ret = Message(self.data, self.state.app)
        self.state._sent_messages_cache.new(self.data["id"], self.data)
        self.dispatch("MESSAGE", ret)


class OnMessageEdit(Event):
    """Returns the new :class:`Message` and if cached the old :class:`Message`"""

    def process(self):
        try:
            before = Message(
                self.state._sent_messages_cache[self.data["id"]], self.state.app
            )
        except KeyError:
            # if the message is not in the cache we cant really save it.
            before = None
        self.state._edited_messages_cache.new(self.data["id"], self.data)
        after = Message(self.data, self.state.app)
        self.dispatch("MESSAGE_EDIT", before, after)


class OnMessageDelete(Event):
    """Gives the deleted :class:`Message`"""

    def process(self):
        message = Message(
            self.state._sent_messages_cache.pop(self.data["id"]), self.state.app
        )
        self.state._deleted_messages_cache.new(self.data["id"], self.data)
        self.dispatch("MESSAGE_DELETE", message)


class OnMessageReactionAdd(Event):
    """Gives a :class:`Message` and a :class:`Emoji` that was added."""

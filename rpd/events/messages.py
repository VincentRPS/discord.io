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
from rpd.cache import Message
from rpd.internal.dispatcher import Dispatcher
from rpd.state import ConnectionState


class OnMessage:
    def __init__(self, data, dispatcher: Dispatcher, state: ConnectionState):
        ret = Message(data, state.app)
        state._sent_messages_cache[data["id"]] = data
        dispatcher.dispatch("MESSAGE", ret)

class OnMessageEdit:
    def __init__(self, data, dispatcher: Dispatcher, state: ConnectionState):
        try:
            before = Message(state._sent_messages_cache[data["id"]], state.app)
        except KeyError:
            before = None
        state._edited_messages_cache[data["id"]] = data
        after = Message(data, state.app)
        dispatcher.dispatch("MESSAGE_EDIT", before, after)

class OnMessageDelete:
    def __init__(self, data, dispatcher: Dispatcher, state: ConnectionState):
        message = Message(state._sent_messages_cache[data["id"]], state.app)
        dispatcher.dispatch("MESSAGE_DELETE", message)

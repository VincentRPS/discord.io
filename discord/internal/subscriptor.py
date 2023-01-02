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

from typing import Any, Coroutine, Callable, Type
from attrs import define

from discord import traits

from ..events.base import BaseEvent

AsyncFunc = Callable[..., Coroutine[Any, Any, Any]]

@define(weakref_slot=False)
class Subscription:
    event_class: Type[BaseEvent]
    """
    The Event this Subscription is tied to
    """

    type: str
    """
    The Discord event this Subscriptions event class uses
    """

    callback: AsyncFunc
    """
    The function to call when this subscription is activated
    """

class Subscriptor:
    def __init__(self, app: traits.BaseApp) -> None:
        self.subscriptions: list[Subscription] = []
        self.app = app

    def add_subscription(self, subscription: Subscription) -> None:
        self.subscriptions.append(subscription)

    def remove_subscription(self, subscription: Subscription) -> None:
        try:
            self.subscriptions.remove(subscription)
        except ValueError:
            raise ValueError('Subscription is dormant')

    async def dispatch(self, event_name: str, event_data: dict[str, Any]):
        name = 'on_' + event_name.lower()

        for sub in self.subscriptions:
            if sub.type == name:
                await sub.callback(sub.event_class.construct(app=self.app, data=event_data))
 
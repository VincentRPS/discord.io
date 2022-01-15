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
import abc

import attr

from ..webhooks import Webhook


@attr.s(init=True)
class BasicWebhook(abc.ABC):
    """Provides basic functionality of a webhook,
    like sending, deleting and editing messages
    If you want to fetch messages or the webhook itself,
    please use :class:`WebhookFetchers` or :class:`WebhookApp`

    .. versionadded:: 0.3.0
    """

    webhook_id: int
    webhook_token: str

    def init(self):
        self.basichook = Webhook(self.webhook_id, self.webhook_token)

    def send(self):
        """Sends a message via the webhook id & token"""
        return self.basichook.send_message

    def delete(self):
        """Deletes a message via the webhook id & token"""
        return self.basichook.delete_message

    def edit(self):
        """Edits a message via the webhook id & token"""
        return self.basichook.edit_message

    def fetch_message(self):
        return self.basichook.fetch_message

    def fetch_self(self):
        return self.basichook.fetch_webhook


@attr.s(init=True)
class WebhookApp(BasicWebhook, abc.ABC):
    """A subclass of :class:`BasicWebhook`
    providing a fully featured webhook experience.
    This class also adds the modify method
    for modifying the current webhook.

    .. versionadded:: 0.3.0

    Attributes
    ----------
    webhook_id
        The webhook id
    webhook_token
        The webhook token
    """

    def __init__(self, webhook_id: int, webhook_token: str):
        self.webhook = Webhook(webhook_id, webhook_token)
        super().__init__(webhook_id, webhook_token)

    def modify(self):
        return self.webhook.modify_webhook

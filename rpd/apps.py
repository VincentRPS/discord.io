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

# These apps are the building blocks for the library.
# While RESTClient.blah will give you the payload, that isn't what you would want
# most classes will use these bases because they parse the payload data to useable, readable human data.
# or except for RESTClient.fetch_user(json bull) it's just RESTApp.fetch_user(user).
import abc
from .webhooks import Webhook


class WebhookApp(abc.ABC):
    def __init__(self, webhook_id, webhook_token):
        self.webhook = Webhook(webhook_id, webhook_token)

    async def send(self):
        """Sends a message via the webhook id & token"""
        return self.webhook.send_message

    async def delete(self):
        """Deletes a message via the webhook id & token"""
        return self.webhook.delete_message

    async def edit(self):
        """Edits a message via the webhook id & token"""
        return self.webhook.edit_message

    async def fetch_message(self):
        return self.webhook.fetch_message

    async def fetch_self(self):
        return self.webhook.fetch_webhook

    async def modify(self):
        return self.webhook.modify_webhook

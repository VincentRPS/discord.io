import pytest

from discord.apps import BasicWebhook, WebhookApp
from discord.internal import Forbidden


class TestWebhookApp:
    webhook = WebhookApp("r", "1")

    async def modify(self):
        await self.webhook.modify()

    def assert_self(self):
        assert self.webhook.webhook_id == "r"
        assert self.webhook.webhook_token == "1"


class TestBasicWebhook:
    webhook = BasicWebhook("r", "2")

    async def send(self):
        with pytest.raises(Forbidden):
            await self.webhook.send("f")

    async def delete(self):
        with pytest.raises(Forbidden):
            await self.webhook.delete("0")

    async def edit(self):
        with pytest.raises(Forbidden):
            await self.webhook.edit("0")

    async def get_msg(self):
        with pytest.raises(Forbidden):
            await self.webhook.get_message("m")

    def assert_self(self):
        assert self.webhook.webhook_id == "r"
        assert self.webhook.webhook_token == "2"

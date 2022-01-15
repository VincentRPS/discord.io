import asyncio

from rpd.apps import WebhookApp  # import Webhook

webhook = WebhookApp(
    "id",
    "token",
)  # The webhook id and token.


async def connection():
    await webhook.send(content="Hello!")  # Send a message.


asyncio.run(connection())

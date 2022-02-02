import asyncio

from discord.apps import WebhookApp  # import Webhook

webhook = WebhookApp(
    "id",
    "token",
)  # The webhook id and token.


async def connection():
    await webhook.send("Hello!")  # Send a message.


asyncio.run(connection())

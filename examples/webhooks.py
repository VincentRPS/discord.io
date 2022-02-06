import asyncio

import discord

webhook = discord.Webhook("id", "token")


async def send():
    await webhook.execute("i am alive!")


asyncio.run(send())

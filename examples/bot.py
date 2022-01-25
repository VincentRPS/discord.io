# This shows a simple rest connection with Discord.
import asyncio

from rpd.api import rest_factory

rest = rest_factory.RESTFactory()


async def connection():
    await rest.login("my_token")


asyncio.run(connection())

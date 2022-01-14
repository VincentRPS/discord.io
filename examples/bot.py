# This shows a simple rest connection with Discord.
import asyncio
import logging

from rpd.api import rest_factory

logging.basicConfig(level=logging.DEBUG)

rest = rest_factory.RESTFactory()


async def connection():
    await rest.login("my_token")
    await asyncio.sleep(99)
    await rest.logout()


asyncio.run(connection())

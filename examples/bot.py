# This shows a simple rest connection with Discord.
import asyncio

from rpd import ConnectionState
from rpd.api import Gateway, rest_factory

state = ConnectionState(intents=0)
rest = rest_factory.RESTFactory()
gate = Gateway(state=state)


async def connection():
    await rest.login("my_token")
    await gate.connect()


asyncio.run(connection())

import asyncio

import aio

webhook = aio.Webhook('id', 'token')


async def send():
    await webhook.execute('i am alive!')


asyncio.run(send())

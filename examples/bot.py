from aio import Client, Intents

intents = Intents.default()  # type: ignore

# the instance of your bot
client = Client(intents=intents)


@client.event  # type: ignore
async def on_ready() -> None:
    print('bot is ready!')


client.run('my_bot_token')

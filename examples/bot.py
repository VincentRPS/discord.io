from discord import Client, Intents

intents = Intents.default()  # type: ignore

# the instance of your bot
bot = Client(intents=intents)


@bot.event  # type: ignore
async def on_ready() -> None:
    print("bot is ready!")


bot.run("my_bot_token")

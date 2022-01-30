from rpd import BotApp, Intents

intents = Intents.default()

# the instance of your bot
bot = BotApp(intents=intents)


@bot.listen
async def on_ready():
    print("bot is ready!")


bot.run("my_bot_token")

from rpd import BotApp

# the instance of your bot,
# intents are required
bot = BotApp(token="my_bot_token", intents=0)


@bot.listen
async def on_ready():
    print("bot is ready!")


bot.run()

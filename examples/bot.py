from rpd import BotApp

# the instance of your bot,
# a few notes, 1 intents are required
# 2 you need to provide your own event loop!
bot = BotApp(token="my_bot_token", intents=0)


@bot.listen
async def on_ready():
    print("bot is ready!")


bot.run()

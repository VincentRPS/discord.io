from rpd import BotApp

# the instance of your bot
bot = BotApp()


@bot.listen
async def on_ready():
    print("bot is ready!")


bot.run("my_bot_token")

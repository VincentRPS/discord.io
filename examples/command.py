from rpd import BotApp, cache

bot = BotApp()


@bot.listen
async def on_ready():
    print("ready!")


# normal
@bot.listen
async def on_message(msg):
    message = cache.Message(msg, bot)
    if message.content.startswith("!ping"):
        await message.reply("pong!")


# with embeds
@bot.listen
async def on_message(msg):
    message = cache.Message(msg, bot)
    embed = cache.Embed(title="bonk", description="boop")
    if message.content.startswith("!ping"):
        await message.reply("pong!", embed)


bot.run("my_token")

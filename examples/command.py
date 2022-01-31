from rpd import BotApp, Embed, Message

bot = BotApp()


@bot.event
async def on_ready():
    print("ready!")


# normal
@bot.event
async def on_message(msg):
    message = Message(msg, bot)
    if message.content.startswith("!ping"):
        await message.reply("pong!")


# with embeds
@bot.event
async def on_message(msg):
    message = Message(msg, bot)
    embed = Embed(title="bonk", description="boop")
    if message.content.startswith("!ping"):
        await message.reply("pong!", embed)


bot.run("my_token")

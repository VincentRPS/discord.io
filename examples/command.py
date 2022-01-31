import rpd

bot = rpd.BotApp()


@bot.event
async def on_ready():
    print("ready!")


# normal
@bot.listen("on_message")
async def ping_command(msg):
    if msg.content.startswith("!ping"):
        await msg.reply("pong!")


# with embeds
@bot.listen("on_message")
async def embed_command(msg):
    embed = rpd.Embed(title="bonk", description="boop")
    if msg.content.startswith("!embed"):
        await msg.reply("here is your embed", embed)


bot.run("my_token")

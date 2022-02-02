import discord

bot = discord.BotApp()


@bot.event  # type: ignore
async def on_ready() -> None:
    print("ready!")


# normal
@bot.listen("on_message")
async def ping_command(msg: discord.Message) -> None:
    if msg.content.startswith("!ping"):
        await msg.reply("pong!")


# with embeds
@bot.listen("on_message")
async def embed_command(msg: discord.Message) -> None:
    embed = discord.Embed(title="bonk", description="boop", color=discord.Color.teal())  # type: ignore
    if msg.content.startswith("!embed"):
        await msg.reply("here is your embed", embed)


bot.run("my_token")

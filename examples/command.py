import discord

intents = (
    discord.Intents.MESSAGE_CONTENT
    | discord.Intents.GUILD_MESSAGES
    | discord.Intents.GUILDS
)

client = discord.Client()


@client.event  # type: ignore
async def on_ready() -> None:
    print('ready!')


# normal
@client.listen('on_message')
async def ping_command(msg: discord.Message) -> None:
    if msg.content.startswith('!ping'):
        await msg.reply('pong!')


# with embeds
@client.listen('on_message')
async def embed_command(msg: discord.Message) -> None:
    embed = discord.Embed(title='bonk', description='boop', color=discord.Color.teal())  # type: ignore
    if msg.content.startswith('!embed'):
        await msg.reply('here is your embed', embed)


client.run('my_token')

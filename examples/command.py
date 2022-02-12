import aio

client = aio.Client()


@client.event  # type: ignore
async def on_ready() -> None:
    print('ready!')


# normal
@client.listen('on_message')
async def ping_command(msg: aio.Message) -> None:
    if msg.content.startswith('!ping'):
        await msg.reply('pong!')


# with embeds
@client.listen('on_message')
async def embed_command(msg: aio.Message) -> None:
    embed = aio.Embed(title='bonk', description='boop', color=aio.Color.teal())  # type: ignore
    if msg.content.startswith('!embed'):
        await msg.reply('here is your embed', embed)


client.run('my_token')

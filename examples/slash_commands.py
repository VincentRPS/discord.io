import aio

client = aio.Client()  # defining our client


@client.event
async def on_ready():
    print('ready!')


# without options
@client.slash_command()
async def ping(inter: aio.Interaction):
    await inter.respond('pong!')


# with options
@client.slash_command(
    options=[aio.Option('anime_good', 'is anime good', type=bool, required=True)]
)
async def anime_good(inter: aio.Interaction):
    if inter.options[0]['value'] == True:
        await inter.respond('Nice')
    elif inter.options[0]['value'] == False:
        await inter.defer(invisable=True)
        await inter.followup('i cant believe he no like the animes oh my god...')


client.run('my_bot_token')

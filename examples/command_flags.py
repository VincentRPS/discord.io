from discord.ext.commands import Bot, Context, Flag
from discord.flags import Intents

intents = Intents.GUILD_MESSAGES | Intents.GUILDS | Intents.MESSAGE_CONTENT

bot = Bot(command_prefix='!', intents=intents)


@bot.listen('on_ready')
async def on_ready():
    print(f'{bot.user} has logged in!')


@bot.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(bot.latency * 1000)}ms')


@bot.command(
    flags=[
        Flag('--test', '-t', type=Flag.STRING, default=''),
        Flag('--bool', '-b', type=Flag.BOOLEAN, default=False),
        Flag('--int', '-i', type=Flag.INT),
        Flag('--float', '-f', type=Flag.FLOAT),
    ]
)
async def flags(ctx: Context, word: str):
    await ctx.send(
        f'word: {word}\ntest: {ctx.test!s}\nbool: {ctx.bool}\nint: {ctx.int}\nfloat {ctx.float}'
    )


bot.run('my_token')

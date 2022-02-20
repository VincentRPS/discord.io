import discord
from discord.ext import commands

intents = (
    discord.Intents.MESSAGE_CONTENT
    | discord.Intents.GUILD_MESSAGES
    | discord.Intents.GUILDS
)

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


# arguments
@bot.command()
async def fav_animal(ctx, animal: str):
    await ctx.send(f'Your favorite animal is {animal}')


bot.run('my_token')

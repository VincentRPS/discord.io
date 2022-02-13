from discord.ext import commands

bot = commands.Bot(command_prefix='!')


@bot.command()
async def ping(ctx):
    await ctx.send('pong!')


# arguments
@bot.command()
async def fav_animal(ctx, animal: str):
    await ctx.send(f'Your favorite animal is {animal}')


bot.run('my_token')

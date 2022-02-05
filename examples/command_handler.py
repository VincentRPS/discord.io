import discord

client = discord.Client()


@client.command()
async def ping(ctx):
    await ctx.send("pong!")


client.run("my_bot_token")

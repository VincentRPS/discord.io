import discord

client = discord.Client(command_prefix=">")


@client.command()
async def ping(ctx):
    await ctx.send("pong!")


client.run("my_bot_token")

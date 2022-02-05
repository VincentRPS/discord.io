import discord

client = discord.Client(command_prefix=">")


@client.command()
async def boop(ctx):
    button = await client.create_button("booper button", booper_button_callback)
    await ctx.send("boop", component=button)


async def booper_button_callback(interaction):
    await interaction.respond("you've been booped!")

client.run("my_bot_token")

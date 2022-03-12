<div align='center'>
    <br />
    <p>
        <a href="https://github.com/VincentRPS/discord.io"><img src="https://raw.githubusercontent.com/VincentRPS/discord.io/master/docs/assets/discord.io.png" width="546" alt="discord.io" /></a>
    </p>
    <br />
    <p>
        <a href="https://discord.gg/cvCAwntVhm"><img src="https://img.shields.io/discord/935701676948590642?color=5865F2&logo=discord&logoColor=white" alt="discord"> </a>
        <a href="https://pypi.org/project/discord.io"><img src="https://img.shields.io/pypi/v/discord.io?label=pip" alt="pip version"> </a>
        <a href="https://pypi.org/project/discord.io"><img src="https://static.pepy.tech/personalized-badge/discord-io?period=total&units=abbreviation&left_color=grey&right_color=green&left_text=downloads" alt="pip downloads"> </a>
    </p>
</div>

<p align='center'>
Asynchronous Discord API Wrapper for Python
</p>

## Features

- Sane Handling of 429s
- User friendly interface
- Most Gateway events

## Installing

To Install discord.io Just run the following command:

```py
pip install discord.io
```

To install our speed requirements just run the following command:

```py
pip install discord.io[speed]
```

For voice support run the following command:

```py
pip install discord.io[voice]
```

## Examples
This is a quick usecase example for the library!

```py
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('ready!')

@client.slash_command()
async def ping(interaction):
    await interaction.respond('pong!')

client.run('my_bot_token')
```

This is another example but with a prefixed command

```py
from discord.ext import commands

bot = commands.Bot(command_prefix='!')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

bot.run('my_bot_token')
```

## Useful Links

The d.io [discord server](https://discord.gg/cvCAwntVhm)
The d.io [docs](https://discordio.readthedocs.io/)

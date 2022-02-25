<p align='center'>
  <img src='https://raw.githubusercontent.com/VincentRPS/discord.io/master/docs/assets/discord.io.png' />
</p>

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

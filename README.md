<p align="center">
  <img src="https://raw.githubusercontent.com/VincentRPS/discord.io/master/docs/assets/discord.io-small.png" />
</p>

<p align="center">
A asynchronous Discord API Wrapper for Python
</p>

## Features

- Sane Handling of 429s
- Customizable
- Gateway Support

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

## Example
This is a quick usecase example for the library!

```py
import discord

client = discord.Client()

@client.event
async def on_ready():
    print('ready!')
    client.slash_command(bonk_callback, 'bonk')

async def bonk_callback(interaction):
    await interaction.respond('Bonk!')

client.run('my_bot_token')
```

This is another example but with a prefixed command

```py
import discord

client = discord.Client(command_prefix=">")

@client.event
async def on_ready():
    print('ready!')

@client.command()
async def ping(ctx):
    await ctx.send('pong!')

client.run('my_bot_token')
```

## Useful Links

The discord.io [Discord Server](https://discord.gg/cvCAwntVhm)

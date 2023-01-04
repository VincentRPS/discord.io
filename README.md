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
Discord's <b>Bot Framework</b>
</p>

## Features

**Discord.io is currently facing a rewrite, we'll make sure to beautify this when we have time and features are partially stable.**

## Installing

To Install discord.io, just run the following command:

```py
pip install discord.io
```

To install our speed requirements, just run the following command:

```py
pip install discord.io[speed]
```

## Basic Example

This is a basic example of a Discord bot which prints its `session_id` when it becomes ready:

```py
import discord

app = discord.GatewayApp(intents=0)

@app.subscribe()
async def on_ready(event: discord.Ready) -> None:
    print(f'Ready on {event.user.name}!')

app.run('token')
```

## Useful Links

- [Discord server](https://discord.gg/cvCAwntVhm)
- [Documentation](https://discord.readthedocs.io/)

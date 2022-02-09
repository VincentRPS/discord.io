import os

folders = [
    "discord/__init__.py",
    "discord/api/__init__.py",
    "discord/voice/__init__.py",
    "discord/events/__init__.py",
    "discord/interactions/__init__.py",
    "discord/components/__init__.py",
    "discord/internal/__init__.py",
    "discord/types/__init__.py",
    "discord/ext/cogs/__init__.py",
]

for dir in folders:
    os.system(f"stubgen {dir} -o .")

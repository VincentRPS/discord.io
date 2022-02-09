import os

list_dirs = [
    "discord",
    "discord/ext/cogs",
    "discord/interactions",
    "discord/api",
    "discord/components",
    "discord/events",
    "discord/internal",
    "discord/types",
    "discord/voice",
]

for dir in list_dirs:
    for file in os.listdir(dir):
        if file.endswith(".py"):
            os.system(f"stubgen {dir}/{file} -o .")

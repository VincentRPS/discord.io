import os

# probably missed one here.
folders = [
    'aio/__init__.py',
    'aio/api/__init__.py',
    'aio/voice/__init__.py',
    'aio/events/__init__.py',
    'aio/interactions/__init__.py',
    'aio/components/__init__.py',
    'aio/internal/__init__.py',
    'aio/types/__init__.py',
    'aio/ext/cogs/__init__.py',
    'aio/ext/commands/__init__.py',
]

for dir in folders:
    os.system(f'stubgen {dir} -o .')

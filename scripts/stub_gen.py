import os

folders = [
    "rpd/__init__.py",
    "rpd/apps/__init__.py",
    "rpd/api/__init__.py",
    "rpd/audio/__init__.py",
    "rpd/modules/__init__.py",
    "rpd/cache/__init__.py",
    "rpd/events/__init__.py",
    "rpd/interactions/__init__.py",
    "rpd/components/__init__.py",
    "rpd/internal/__init__.py",
    "rpd/types/__init__.py",
]

for dir in folders:
    os.system(f"stubgen {dir} -o .")

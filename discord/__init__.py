"""
discord.io
~~~~~~~~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021-present VincentRPS
:license: MIT
"""

__title__: str = 'discord.io'
__author__: str = 'VincentRPS'
__license__: str = 'MIT'
__copyright__: str = 'Copyright 2021-present VincentRPS'
__version__: str = '0.8.3'
__git_sha1__: str = 'HEAD'

import logging
from typing import List, Literal, NamedTuple

from .api import *
from .assets import *
from .channels import *
from .client import *
from .color import *
from .colour import *
from .components import *
from .embed import *
from .enums import *
from .events import *
from .file import *
from .flags import *
from .guild import *
from .http import *
from .interactions import *
from .internal import *
from .member import *
from .message import *
from .snowflake import *
from .state import *
from .types import *
from .ui import *
from .user import *
from .utils import *
from .voice import *
from .webhooks import *


class VersionInfo(NamedTuple):
    major: str
    minor: str
    micro: str
    releaselevel: Literal['alpha', 'beta', 'candidate', 'final']
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=8, micro=3, releaselevel='final', serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
    'VersionInfo',
    'version_info',
]

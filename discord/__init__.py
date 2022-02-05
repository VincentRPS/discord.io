"""
discord.io
~~~~~~~~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021-present VincentRPS
:license: MIT
"""

__title__: str = "discord.io"
__author__: str = "VincentRPS"
__license__: str = "MIT"
__copyright__: str = "Copyright 2021-present VincentRPS"
__version__: str = "0.7.0"
__git_sha1__: str = "HEAD"

import logging
import typing

from .api import *
from .audio import *
from .client import *
from .color import *
from .colour import *
from .components import *
from .context import *
from .events import *
from .file import *
from .intents import *
from .interactions import *
from .internal.exceptions import *
from .internal.warnings import *
from .member import *
from .snowflake import *
from .state import *
from .types import *
from .ui import *
from .util import *
from .webhooks import *
from .guild import *
from .user import *


class VersionInfo(typing.NamedTuple):
    major: str
    minor: str
    micro: str
    releaselevel: typing.Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=7, micro=0, releaselevel="final", serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__: typing.List[str] = [
    "__title__",
    "__author__",
    "__license__",
    "__copyright__",
    "__version__",
    "VersionInfo",
    "version_info",
]

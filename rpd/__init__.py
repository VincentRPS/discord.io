"""
RPD
~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021-present VincentRPS
:license: MIT
"""

__title__: str = "RPD"
__author__: str = "VincentRPS"
__license__: str = "MIT"
__copyright__: str = "Copyright 2021-present VincentRPS"
__version__: str = "0.3.0"

import logging
import typing

from rpd.api import *
from rpd.apps import *
from rpd.boot_text import *
from rpd.color import *
from rpd.colour import *
from rpd.intents import *
from rpd.internal.exceptions import *
from rpd.internal.warnings import *
from rpd.snowflake import *
from rpd.util import *
from rpd.webhooks import *


class VersionInfo(typing.NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: typing.Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=3, micro=0, releaselevel="final", serial=0
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

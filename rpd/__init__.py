"""
RPD
~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021 VincentRPS
:license: Apache-2.0
"""

__title__ = "RPD"
__author__ = "VincentRPS"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2021 VincentRPS"
__version__ = "0.3.0"

import logging
from typing import Literal, NamedTuple

from .abc import *
from .client import Client  # type: ignore
from .data import *
from .exceptions import *
from .helpers import *
from .internal import *
from .user import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=3, micro=0, releaselevel="final", serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

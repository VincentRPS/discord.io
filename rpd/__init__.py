"""
RPD
~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021 VincentRPS
:license: Apache-2.0
"""

__title__ = "RPD"
__author__ = "RPS"
__license__ = "Apache-2.0"
__copyright__ = "Copyright 2021 RPS"
__version__ = "0.2.0"
__discord__ = "9"

import logging
from typing import Literal, NamedTuple

from .client import Client  # type: ignore
from .exceptions import *
from .internal import *


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


version_info: VersionInfo = VersionInfo(
    major=0, minor=2, micro=0, releaselevel="candidate", serial=0
)

logging.getLogger(__name__).addHandler(logging.NullHandler())

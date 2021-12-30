"""
RPD
~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021 VincentRPS
:license: MIT
"""

__title__ = "RPD"
__author__ = "VincentRPS"
__license__ = "MIT"
__copyright__ = "Copyright 2021 VincentRPS"
__version__ = "0.3.0"

import logging
import typing

from rpd.abc import *
from rpd.data import *
from rpd.helpers import *
from rpd.internal.rest import *
from rpd.internal.websockets import *
from rpd.factorys import *

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

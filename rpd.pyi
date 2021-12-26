from typing import Literal, NamedTuple

from .exceptions import *
from .internal import *

__discord__: str

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal[alpha, beta, candidate, final]
    serial: int

version_info: VersionInfo

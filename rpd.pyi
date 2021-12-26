from .exceptions import *
from .internal import *
from typing import Literal, NamedTuple

__discord__: str

class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal[alpha, beta, candidate, final]
    serial: int

version_info: VersionInfo

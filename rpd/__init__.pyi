from rpd.abc import *
from rpd.boot_text import *
from rpd.data import *
from rpd.factories import *
from rpd.helpers import *
from rpd.internal.rest import *
from rpd.internal.websockets import *
import typing

class VersionInfo(typing.NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: typing.Literal['alpha', 'beta', 'candidate', 'final']
    serial: int

version_info: VersionInfo

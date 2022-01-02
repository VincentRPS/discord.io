import typing

from rpd.boot_text import *
from rpd.data import *
from rpd.factories import *
from rpd.helpers import *
from rpd.internal import *

class VersionInfo(typing.NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: typing.Literal["alpha", "beta", "candidate", "final"]
    serial: int

version_info: VersionInfo

# Names in __all__ with no definition:
#   __author__
#   __copyright__
#   __license__
#   __title__
#   __version__

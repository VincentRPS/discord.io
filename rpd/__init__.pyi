import typing

from rpd.boot_text import *
from rpd.color import *
from rpd.colour import *
from rpd.exceptions import *
from rpd.factories import *
from rpd.intents import *
from rpd.internal import *
from rpd.snowflake import *
from rpd.warnings import *
from rpd.webhooks import *

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

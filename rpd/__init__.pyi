from rpd.api import *
from rpd.boot_text import *
from rpd.color import *
from rpd.colour import *
from rpd.intents import *
from rpd.internal.exceptions import *
from rpd.internal.warnings import *
from rpd.snowflake import *
from rpd.util import *
from rpd.webhooks import *
from rpd.apps import *
import typing

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

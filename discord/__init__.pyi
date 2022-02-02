from .api import *
from .audio import *
from .cache import *
from .client import *
from .color import *
from .colour import *
from .components import *
from .events import *
from .intents import *
from .interactions import *
from .internal.exceptions import *
from .internal.warnings import *
from .modules import *
from .snowflake import *
from .state import *
from .types import *
from .ui import *
from .util import *
from .webhooks import *
import typing

class VersionInfo(typing.NamedTuple):
    major: str
    minor: str
    micro: str
    releaselevel: typing.Literal['alpha', 'beta', 'candidate', 'final']
    serial: int

version_info: VersionInfo

# Names in __all__ with no definition:
#   __author__
#   __copyright__
#   __license__
#   __title__
#   __version__

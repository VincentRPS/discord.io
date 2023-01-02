from enum import Enum
from typing import Literal


class Undefined(Enum):
    UNDEFINED = None


UNDEFINED: Literal[Undefined.UNDEFINED] = Undefined.UNDEFINED

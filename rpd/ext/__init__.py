"""
rpd.ext
~~~~~~~
A assortment of extensions and utilies for RPD.
"""
import rpd

from .ciso_parse import *
from .missing import *
from .whichjson import *

ext_version = (
    rpd.version_info.major
    + "."
    + rpd.version_info.minor
    + "."
    + rpd.version_info.micro
    + ".2022.1"
)

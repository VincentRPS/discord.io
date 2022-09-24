"""
discord.io
~~~~~~~~~~
Asynchronous Discord API Wrapper For Python

:copyright: 2021-present VincentRPS
:license: MIT
"""

__title__: str = 'discord.io'
__author__: str = 'VincentRPS'
__license__: str = 'MIT'
__copyright__: str = 'Copyright 2021-present VincentRPS'
__version__: str = '2.0.0'
__git_sha1__: str = 'HEAD'

import logging
import typing


class VersionInfo(typing.NamedTuple):
    major: str
    minor: str
    micro: str
    releaselevel: typing.Literal['alpha', 'beta', 'candidate', 'final']
    serial: int


version_info: VersionInfo = VersionInfo(major=2, minor=0, micro=0, releaselevel='alpha', serial=0)

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__: typing.List[str] = [
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
    'VersionInfo',
    'version_info',
]

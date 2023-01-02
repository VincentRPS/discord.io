import logging
import typing

__title__: str = 'discord.io'
__author__: str = 'VincentRPS'
__license__: str = 'MIT'
__copyright__: str = 'Copyright 2021-present VincentRPS'
__version__: str = '2.0.0'
__git_sha1__: str = 'HEAD'


class VersionInfo(typing.NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: typing.Literal['alpha', 'beta', 'candidate', 'final']
    serial: int


version_info: VersionInfo = VersionInfo(major=1, minor=0, micro=0, releaselevel='alpha', serial=0)

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

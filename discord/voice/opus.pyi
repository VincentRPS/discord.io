import ctypes.util
from ..internal.exceptions import DiscordError
from enum import Enum
from typing import Any

class EncoderStruct(ctypes.Structure): ...
class DecoderStuct(ctypes.Structure): ...

class AppEnum(Enum):
    AUDIO: int
    VOIP: int
    LOWDELAY: int

class CntrlEnum(Enum):
    SET_BITRATE: int
    SET_BANDWIDTH: int
    SET_FEC: int
    SET_PLP: int

class OpusError(DiscordError): ...

class Opus:
    EXP: Any
    lib: Any
    def __init__(self) -> None: ...

class Encoder(Opus):
    EXP: Any
    def __init__(self) -> None: ...
    @property
    def inst(self): ...
    def set_bitrate(self, kbps) -> None: ...
    def set_fec(self, value) -> None: ...
    def set_expected_plp(self, perc) -> None: ...
    def create(self): ...
    def __del__(self) -> None: ...
    def encode(self, pcm, frame_size): ...

# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
"""Implementation of Opus."""
# based off the implementation of discord.py and disco.
import array
import ctypes
import ctypes.util
import os
import struct
import sys
import threading
from enum import Enum
from typing import List

from ..internal.exceptions import DiscordError

__all__ = ('Encoder',)

# structs
class EncoderStruct(ctypes.Structure):  # noqa: ignore

    pass


# if your curious, the 'decoder' handles, voice recv.
class DecoderStuct(ctypes.Structure):  # noqa: ignore

    pass


# pointers
c_int_ptr = ctypes.POINTER(ctypes.c_int)
c_int16_ptr = ctypes.POINTER(ctypes.c_int16)
c_float_ptr = ctypes.POINTER(ctypes.c_float)

EncoderStructPtr = ctypes.POINTER(EncoderStruct)
DecoderStructPtr = ctypes.POINTER(DecoderStuct)

opus_loaded: threading.Event = threading.Event()


# options
default_options = {
    # generic stuff
    'opus_get_version_string': (None, ctypes.c_char_p, None),
    'opus_strerror': ([ctypes.c_int], ctypes.c_char_p, None),
    # packets
    'opus_packet_get_bandwidth': ([ctypes.c_char_p], ctypes.c_int),
    'opus_packet_get_nb_channels': ([ctypes.c_char_p], ctypes.c_int),
    'opus_packet_get_nb_frames': ([ctypes.c_char_p, ctypes.c_int], ctypes.c_int),
    'opus_packet_get_samples_per_frame': (
        [ctypes.c_char_p, ctypes.c_int],
        ctypes.c_int,
    ),
}

# Enums


class AppEnum(Enum):
    AUDIO = 2049
    VOIP = 2048
    LOWDELAY = 2051


class CntrlEnum(Enum):
    SET_BITRATE = 4002
    SET_BANDWIDTH = 4008
    SET_FEC = 4012
    SET_PLP = 4014


# Errors


class OpusError(DiscordError):
    pass


# loader


def loader(name: str):
    opus = ctypes.cdll.LoadLibrary(name)

    return opus


def load_opus() -> bool:
    global lib
    try:
        if sys.platform == 'win32':
            basedir = os.path.dirname(os.path.abspath(__file__))
            bitness = struct.calcsize('P') * 8
            target = 'x64' if bitness > 32 else 'x86'
            filename = os.path.join(basedir, 'bin', f'opus-{target}.dll')
            lib = loader(filename)
            opus_loaded.set()
        else:
            lib = loader(ctypes.util.find_library('opus'))
            opus_loaded.set()
    except Exception as exc:
        lib = None
        raise OpusError from exc

    return lib is not None


def check_load():
    if opus_loaded.is_set() is not True:
        return load_opus()
    else:
        return lib


class Opus:
    EXP = {}

    def __init__(self):
        self.lib = check_load()
        meths = {}
        meths.update(default_options)
        meths.update(self.EXP)

        for name, option in meths.items():  # type: ignore # noqa: ignore
            func = getattr(loader, name)

            try:
                if option[1]:
                    func.argtypes = option[0]

                func.restype = option[1]

                setattr(self, name, func)
            except KeyError:
                pass


# encoder
class Encoder(Opus):
    """A class used to encode `.pcm` data into opus data for the discord voice gateway"""

    EXP = {
        'opus_encoder_get_size': ([ctypes.c_int], ctypes.c_int, None),
        'opus_encoder_create': (
            [ctypes.c_int, ctypes.c_int, ctypes.c_int, c_int_ptr],
            EncoderStructPtr,
        ),
        'opus_encode': (
            [
                EncoderStructPtr,
                c_int16_ptr,
                ctypes.c_int,
                ctypes.c_char_p,
                ctypes.c_int32,
            ],
            ctypes.c_int32,
        ),
        'opus_encode_float': (
            [
                EncoderStructPtr,
                c_float_ptr,
                ctypes.c_int,
                ctypes.c_char_p,
                ctypes.c_int32,
            ],
            ctypes.c_int32,
        ),
        'opus_encoder_ctl': (None, ctypes.c_int32),
        'opus_encoder_destroy': ([EncoderStructPtr], None, None),
    }

    def __init__(self):
        self._inst = None

    @property
    def inst(self):
        if not self._inst:
            self._inst = self.create()
            self.set_bitrate(128)
            self.set_fec(True)
            self.set_expected_plp(0.15)

        return self._inst

    def set_bitrate(self, kbps):
        kbps = min(128, max(16, int(kbps)))
        ret = self.opus_encoder_ctl(
            self.inst, int(CntrlEnum.SET_BITRATE.value), kbps * 1024
        )

        if ret < 0:
            raise RuntimeError('Failed to set bitrate, %s: %s', kbps, ret)

    def set_fec(self, value):
        ret = self.opus_encoder_ctl(self.inst, int(CntrlEnum.SET_FEC.value), int(value))

        if ret < 0:
            raise RuntimeError('Failed to set bitrate, %s: %s', value, ret)

    def set_expected_plp(self, perc):
        ret = self.opus_encoder_ctl(
            self.inst, int(CntrlEnum.SET_PLP.value), min(100, max(0, int(perc * 100)))
        )

        if ret < 0:
            raise RuntimeError('Failed to set bitrate, %s: %s', perc, ret)

    def create(self):
        ret = ctypes.c_int()
        result = self.opus_encoder_create(
            self.sampling_rate, self.channels, self.application.value, ctypes.byref(ret)
        )

        if ret.value != 0:
            raise RuntimeError

        return result

    def __del__(self):
        if hasattr(self, '_inst') and self._inst:
            self.opus_encoder_destroy(self._inst)
            self._inst = None

    def encode(self, pcm, frame_size):
        m_data_bytes = len(pcm)
        pcm = ctypes.cast(pcm, c_int16_ptr)
        data = (ctypes.c_char * m_data_bytes)()

        ret = self.opus_encode(self.inst, pcm, frame_size, data, m_data_bytes)

        if ret < 0:
            raise RuntimeError

        return array.array('b', data[:ret].tobytes())

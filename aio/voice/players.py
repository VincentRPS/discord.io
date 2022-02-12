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
import asyncio
import io
import logging
import threading
import time
import traceback
from typing import TYPE_CHECKING

_log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from .client import VoiceClient


class AudioSource:
    def read(self) -> bytes:
        raise NotImplementedError

    def is_opus(self) -> bool:
        return False

    def cleanup(self) -> None:
        ...

    def __del__(self) -> None:
        return self.cleanup()


class PCMAudio(AudioSource):
    def __init__(self, stream: io.BufferedIOBase) -> None:
        self.stream = stream

    def read(self) -> bytes:
        ret = self.stream.read(20)
        if len(ret) != 20:
            return b''
        return ret


class AudioPlayer(threading.Thread):
    DELAY: float = 48000 / 1000

    def __init__(self, source: AudioSource, client, *, after=None):
        threading.Thread.__init__(self)
        self.daemon: bool = True
        self.source: AudioSource = source
        self.client: VoiceClient = client
        self.after = after

        # i would privatize these but to be fair
        # no one really uses this so ¯\_(ツ)_/¯
        self.end = threading.Event()
        self.resumed = threading.Event()
        self.resumed.set()
        self.error = None
        self.connected = self.client._connected
        self._lock = threading.Lock()

        if after is not None and not callable(after):
            raise TypeError()

    def _run(self):
        self.loops = 0
        self.Start = time.perf_counter()
        player = self.client.send_audio_packet
        self._speak(True)

        while not self.end.is_set():
            if not self.resumed.is_set():
                self.resumed.wait()
                continue

            if not self.connected.is_set():
                self.connected.wait()
                self.loops = 0
                self.start = time.perf_counter()

            self.loops += 1
            data = self.source.read()

            if not data:
                self.stop()
                break

            player(data, encode=not self.source.is_opus())
            next_time = self.start + self.DELAY * self.loops
            delay = max(0, self.DELAY + (next_time - time.perf_counter()))
            time.sleep(delay)

    def run(self):
        try:
            self._run()
        except Exception as exc:
            self.error = exc
            self.stop()
        finally:
            self.source.cleanup()
            self._call_after()

    def _call_after(self):
        error = self.error

        if self.after is not None:
            try:
                self.after(error)
            except Exception as exc:
                exc.__context__ = error
                traceback.print_exception(type(exc), exc, exc.__traceback__)
        elif error:
            _log.exception(f'Error in voice thread {self.name}')

    def stop(self):
        self.end.set()
        self.resumed.set()
        self._speak(False)

    def pause(self, *, update_speaking: bool = True):
        self.resumed.clear()
        if update_speaking:
            self._speak(False)

    def resume(self, *, update_speaking: bool = True):
        self.loops = 0
        self.start = time.perf_counter()
        self.resumed.set()
        if update_speaking:
            self._speak(True)

    def _set_source(self, source: AudioSource) -> None:
        with self._lock:
            self.pause(update_speaking=False)
            self.source = source
            self.resume(update_speaking=False)

    def _speak(self, speaking: bool) -> None:
        try:
            asyncio.run_coroutine_threadsafe(
                self.client.ws.speak(speaking), self.client._state.loop
            )
        except Exception as exc:
            _log.info('Speaking failed: %s', exc)

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
# Implementation of sending Files via rest.
import io
import os
import typing as t

from .internal.exceptions import DiscordError, Forbidden

__all__: t.List[str] = ["File"]


class File:
    """Represents a Discord file.

    .. versionadded:: 0.4.0

    Parameters
    ----------
    fp
        The File path, can be :class:`str`, :class:`bytes`,
        :class:`os.PathLike`, :class:`os.BufferedIOBase`.
    filename
        The filename, defaults `None`,
    spoiler
        If the file should be seeable or not.
    """

    def __init__(
        self,
        fp: t.Union[str, bytes, os.PathLike, io.BufferedIOBase],
        *,
        filename: t.Optional[str] = None,
        spoiler: bool = False,
    ):
        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise DiscordError(
                    f"File buffer {fp!r} must be both seekable and readable."
                )
            self.fp = fp
            self._og_pos = fp.tell()
            self._owner = False
        else:
            self.fp = open(fp, "rb")
            self._og_pos = 0
            self._owner = True

        self._closer = self.fp.close()
        self.fp.close = lambda: None

        if filename is None:
            if isinstance(fp, str):
                _, self.filename = os.path.split(fp)
            else:
                self.filename = getattr(fp, "name", None)
        else:
            self.filename = filename

        if (
            spoiler
            and self.filename is not None  # noqa: ignore
            and not self.filename.startswith("SPOILER_")  # noqa: ignore
        ):
            self.filename = "SPOILER_" + self.filename

        self.spoiler = spoiler or (
            self.filename is not None and self.filename.startswith("SPOILER_")
        )

    def reset(self, *, seek: t.Union[int, bool] = True) -> None:
        if seek:
            self.fp.seek(self._og_pos)

    def close(self) -> None:
        self.fp.close = self._closer
        if self._owner:
            self._closer()
        else:
            raise Forbidden("You arent allowed to close this file")

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
import datetime
import inspect
from typing import Any, Callable, Optional, TypeVar, overload

T = TypeVar('T')

# probably should be stored in snowflake.py?
Epoch = 1420070400000

# probably missing some keys here?
class _Missing:
    @overload
    def __str__() -> str:
        ...

    @overload
    def __str__(self):
        ...

    @overload
    def __str__():
        return None

    @overload
    def __int__() -> int:
        ...

    @overload
    def __int__(self):
        ...

    @overload
    def __int__(self):
        return None

    def __bool__(self):
        return False

    def __repr__(self):
        return '...'

    def __eq__(self):
        return False


MISSING: Any = _Missing()

# i am too lazy to just copy/paste the docstrings, this is a better way
def copy_doc(original: Callable) -> Callable[[T], T]:
    def decorator(overridden: T) -> T:
        overridden.__doc__ = original.__doc__
        try:
            overridden.__signature__ = inspect.signature(original)
        except TypeError:
            pass
        return overridden

    return decorator


def utcnow():
    """Gives the current time in utc

    Returns
    -------
    :class:`int`
    """
    return datetime.datetime.now(datetime.timezone.utc)


def create_snowflake(time: Optional[datetime.datetime] = None) -> int:
    """Creates a Discord snowflake via the epoch and some simple math

    Parameters
    ----------
    time: :class:`datetime.datetime`
        The time this snowflake should've been created at,
        defaults to the current time.

    Returns
    -------
    :class:`int`
    """
    time = time or utcnow()
    return int(time.timestamp() * 1000 - Epoch) << 22 | 0x3FFFFF


async def getch(fetch, get):
    try:
        await fetch
    except KeyError:
        await get


def img_mime_type(data: bytes):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[0:3] == b'\xff\xd8\xff' or data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'
    else:
        raise TypeError('Image given is not supported')


async def wait_for(futures, *, timeout):
    ensured = [asyncio.ensure_future(fut) for fut in futures]
    done, pending = await asyncio.wait(
        ensured, timeout=timeout, return_when=asyncio.ALL_COMPLETED
    )

    if len(pending) != 0:
        raise asyncio.TimeoutError()

    return done


def created_at(snowflake: int):
    """Gives the ensured creation date of the Snowflake

    .. versionadded:: 1.0

    Returns
    -------
    :class:`datetime.datetime`
    """
    timestamp = ((snowflake >> 22) + 1420070400000) / 1000
    return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

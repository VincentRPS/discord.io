# MIT License

# Copyright (c) 2021 VincentRPS

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
# SOFTWARE.
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple, Union

warnings.filterwarnings("default", category=DeprecationWarning)


class Base(Exception):
    """The Base Exception"""

    pass


# Used to show something has been deprecated
def deprecated(version: str, alternative: str = None):
    warning = f"This class/function has been deprecated, and will be removed in version {version}"

    if alternative is not None:
        warning += f" you can use {alternative} instead."

    warnings.warn(
        warning,
        DeprecationWarning,
        stacklevel=2,
    )


# Mostly inspired by discord.py
def _flatten_error_dict(d: Dict[str, Any], key: str = "") -> Dict[str, str]:
    items: List[Tuple[str, str]] = []
    for k, v in d.items():
        new_key = key + "." + k if key else k

        if isinstance(v, dict):
            try:
                _errors: List[Dict[str, Any]] = v["_errors"]
            except KeyError:
                items.extend(_flatten_error_dict(v, new_key).items())
            else:
                items.append((new_key, " ".join(x.get("message", "") for x in _errors)))
        else:
            items.append((new_key, v))

    return dict(items)


class ClientException(Base):
    """Core Exception For All Client Modules"""

    pass


class LoginFailure(ClientException):
    """Handles Bot Login Failures"""

    pass

class HTTPException(Base):
    """Handles HTTPExceptions"""

class Forbidden(HTTPException):
    pass


class NotFound(HTTPException):
    def __init__(self, request):
        self.request = request
        Exception.__init__(self, "The selected resource was not found")


class Unauthorized(HTTPException):
    def __init__(self, request):
        self.request = request
        Exception.__init__(self, "You are not authorized to view this resource")


class RateLimitError(HTTPException):
    """ono D:"""


class ServerError(HTTPException):
    """Happens when a discord server error happens"""


class TokenNotFound(HTTPException):
    """Token Has Not Been Found :("""

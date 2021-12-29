# Apache-2.0
#
# Copyright 2021 VincentRPS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the LICENSE file for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import warnings
import typing

if typing.TYPE_CHECKING:
    import aiohttp

    try:
        import requests

        _ResponseType = typing.Union[aiohttp.ClientResponse, requests.Response]
    except ModuleNotFoundError:
        _ResponseType = aiohttp.ClientResponse

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
def _flatten_error_dict(d: typing.Dict[str, typing.Any], key: str = "") -> typing.Dict[str, str]:
    items: typing.List[typing.Tuple[str, str]] = []
    for k, v in d.items():
        new_key = key + "." + k if key else k

        if isinstance(v, dict):
            try:
                _errors: typing.List[typing.Dict[str, typing.Any]] = v["_errors"]
            except KeyError:
                items.extend(_flatten_error_dict(v, new_key).items())
            else:
                items.append((new_key, " ".join(x.get("message", "") for x in _errors)))
        else:
            items.append((new_key, v))

    return dict(items)


class HTTPException(Base):
    def __init__(
        self, response: _ResponseType, message: typing.Optional[typing.Union[str, typing.Dict[str, typing.Any]]]
    ):
        self.response: _ResponseType = response
        self.status: int = response.status  # type: ignore
        self.code: int
        self.text: str
        if isinstance(message, dict):
            self.code = message.get("code", 0)
            base = message.get("message", "")
            errors = message.get("errors")
            if errors:
                errors = _flatten_error_dict(errors)
                helpful = "\n".join("In %s: %s" % t for t in errors.items())
                self.text = base + "\n" + helpful
            else:
                self.text = base
        else:
            self.text = message or ""
            self.code = 0

        fmt = "{0.status} {0.reason} (error code: {1})"
        if len(self.text):
            fmt += ": {2}"

        super().__init__(fmt.format(self.response, self.code, self.text))


class ClientException(Base):
    """Core Exception For All Client Modules"""

    pass


class LoginFailure(ClientException):
    """Handles Bot Login Failures"""

    pass


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

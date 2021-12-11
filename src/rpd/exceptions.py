"""
Apache-2.0

Copyright 2021 RPS

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the LICENSE file for the specific language governing permissions and
limitations under the License.
"""


class Base(Exception):
    """The Base Exception"""

    pass


class HTTPException(Base):
    def __init__(self, request, data):
        self.request = request
        self.data = data
        super().__init__(data)


class ClientException(Base):
    """Core Exception For All Client Modules"""

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

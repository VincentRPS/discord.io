"""
Apache-2.0

Copyright 2021 VincentRPS

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
from __future__ import annotations

from typing import Any

try:
    import orjson
    SPEED: bool = True

except Exception:
    import json
    SPEED: bool = False

if SPEED is True:

    def _to_json(obj: Any) -> str:  # type: ignore
        return orjson.dumps(obj).decode("utf-8")

    _from_json = orjson.loads  # type: ignore
else:
    def _to_json(obj: Any) -> str:
        return json.dumps(obj, separators=(",", ":"), ensure_ascii=True)

    _from_json = json.loads

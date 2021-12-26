from typing import Any

class _Missing:
    def __eq__(self, other): ...
    def __bool__(self) -> None: ...

MISSING: Any

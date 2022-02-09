import io
import os
import typing as t
from typing import Any

class File:
    fp: Any
    filename: Any
    spoiler: Any
    def __init__(
        self,
        fp: t.Union[str, bytes, os.PathLike, io.BufferedIOBase],
        *,
        filename: t.Optional[str] = ...,
        spoiler: bool = ...
    ) -> None: ...
    def reset(self, *, seek: t.Union[int, bool] = ...) -> None: ...
    def close(self) -> None: ...

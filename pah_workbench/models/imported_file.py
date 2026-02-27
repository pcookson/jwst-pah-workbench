"""Model for an imported file."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class ImportedFile:
    path: Path
    name: str
    extension: str
    size_bytes: int

    @classmethod
    def from_path(cls, file_path: str | Path) -> "ImportedFile":
        path = Path(file_path).expanduser().resolve()
        stat = path.stat()
        return cls(
            path=path,
            name=path.name,
            extension=path.suffix.lower(),
            size_bytes=stat.st_size,
        )

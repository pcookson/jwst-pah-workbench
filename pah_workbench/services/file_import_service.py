"""Service for validating and registering imported FITS files."""

from __future__ import annotations

from pathlib import Path

from pah_workbench.models.imported_file import ImportedFile

ALLOWED_EXTENSIONS = {".fits", ".fit"}


class FileImportService:
    def __init__(self) -> None:
        self._files: list[ImportedFile] = []
        self._index_by_path: dict[Path, ImportedFile] = {}

    @property
    def files(self) -> list[ImportedFile]:
        return list(self._files)

    def import_paths(self, paths: list[str]) -> list[ImportedFile]:
        imported: list[ImportedFile] = []
        for raw_path in paths:
            record = self.import_path(raw_path)
            if record is not None:
                imported.append(record)
        return imported

    def import_path(self, raw_path: str) -> ImportedFile | None:
        path = Path(raw_path).expanduser().resolve()
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            return None
        if not path.exists() or not path.is_file():
            return None
        if path in self._index_by_path:
            return self._index_by_path[path]

        imported_file = ImportedFile.from_path(path)
        self._files.append(imported_file)
        self._index_by_path[path] = imported_file
        return imported_file

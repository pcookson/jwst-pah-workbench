"""QSettings wrapper for UI persistence."""

from __future__ import annotations

from PySide6.QtCore import QSettings


class SettingsService:
    GEOMETRY_KEY = "main_window/geometry"
    STATE_KEY = "main_window/state"

    def __init__(self) -> None:
        self._settings = QSettings("JWST", "PAHWorkbench")

    def save_main_window(self, geometry: bytes, state: bytes) -> None:
        self._settings.setValue(self.GEOMETRY_KEY, geometry)
        self._settings.setValue(self.STATE_KEY, state)

    def restore_main_window(self) -> tuple[bytes | None, bytes | None]:
        geometry = self._settings.value(self.GEOMETRY_KEY)
        state = self._settings.value(self.STATE_KEY)
        return geometry, state

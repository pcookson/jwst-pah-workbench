"""Project Explorer dock."""

from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QDockWidget, QListWidget

from pah_workbench.models.imported_file import ImportedFile


class ProjectExplorerDock(QDockWidget):
    file_selected = Signal(str)

    def __init__(self, parent=None) -> None:
        super().__init__("Project Explorer", parent)
        self.list_widget = QListWidget(self)
        self.setWidget(self.list_widget)
        self.list_widget.currentRowChanged.connect(self._on_row_changed)

        self._items: list[ImportedFile] = []

    def add_imported_file(self, imported_file: ImportedFile) -> None:
        if imported_file in self._items:
            return
        self._items.append(imported_file)
        self.list_widget.addItem(imported_file.name)

    def _on_row_changed(self, row: int) -> None:
        if 0 <= row < len(self._items):
            self.file_selected.emit(str(self._items[row].path))

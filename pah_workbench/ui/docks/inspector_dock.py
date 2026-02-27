"""Inspector dock."""

from __future__ import annotations

from PySide6.QtWidgets import QDockWidget, QTextEdit

from pah_workbench.models.imported_file import ImportedFile


class InspectorDock(QDockWidget):
    def __init__(self, parent=None) -> None:
        super().__init__("Inspector", parent)
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.setWidget(self.text)
        self.set_placeholder()

    def set_placeholder(self) -> None:
        self.text.setPlainText("Select an imported file...")

    def show_file(self, imported_file: ImportedFile) -> None:
        details = [
            f"Path: {imported_file.path}",
            f"Filename: {imported_file.name}",
            f"Extension: {imported_file.extension}",
            f"Size (bytes): {imported_file.size_bytes}",
            "Instrument: Mock value",
            "Observation ID: Mock value",
        ]
        self.text.setPlainText("\n".join(details))

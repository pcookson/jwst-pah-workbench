"""Logs dock."""

from __future__ import annotations

from PySide6.QtWidgets import QDockWidget, QTextEdit


class LogsDock(QDockWidget):
    def __init__(self, parent=None) -> None:
        super().__init__("Logs", parent)
        self.text = QTextEdit(self)
        self.text.setReadOnly(True)
        self.setWidget(self.text)

    def append_log(self, message: str) -> None:
        self.text.append(message)

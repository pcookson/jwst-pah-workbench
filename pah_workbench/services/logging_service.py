"""Logging setup for app and UI log viewer."""

from __future__ import annotations

import logging

from PySide6.QtCore import QObject, Signal


class _LogEmitter(QObject):
    message = Signal(str)


class QTextEditLogHandler(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.emitter = _LogEmitter()

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        self.emitter.message.emit(message)


class LoggingService:
    LOGGER_NAME = "pah_workbench"

    def __init__(self) -> None:
        self._logger = logging.getLogger(self.LOGGER_NAME)
        self._logger.setLevel(logging.INFO)
        self._logger.propagate = False

        # Keep setup idempotent if services are recreated.
        self._logger.handlers.clear()

        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S"
        )

        self.text_handler = QTextEditLogHandler()
        self.text_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        self._logger.addHandler(self.text_handler)
        self._logger.addHandler(stream_handler)

    @property
    def logger(self) -> logging.Logger:
        return self._logger

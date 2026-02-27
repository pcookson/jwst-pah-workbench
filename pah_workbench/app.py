"""QApplication bootstrap logic."""

from __future__ import annotations

import logging
import sys

from PySide6.QtWidgets import QApplication

from pah_workbench.services.file_import_service import FileImportService
from pah_workbench.services.logging_service import LoggingService
from pah_workbench.services.settings_service import SettingsService
from pah_workbench.ui.main_window import MainWindow


def run() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("JWST PAH Workbench")
    app.setOrganizationName("JWST")

    settings_service = SettingsService()
    file_import_service = FileImportService()
    logging_service = LoggingService()

    window = MainWindow(
        file_import_service=file_import_service,
        settings_service=settings_service,
        logging_service=logging_service,
    )
    window.show()

    logging.getLogger("pah_workbench").info("Application started")
    return app.exec()

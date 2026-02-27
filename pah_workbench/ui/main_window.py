"""Main window and top-level UI orchestration."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QCloseEvent, QDragEnterEvent, QDropEvent
from PySide6.QtWidgets import (
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTabWidget,
)

from pah_workbench.models.imported_file import ImportedFile
from pah_workbench.services.file_import_service import FileImportService
from pah_workbench.services.logging_service import LoggingService
from pah_workbench.services.settings_service import SettingsService
from pah_workbench.ui.docks.inspector_dock import InspectorDock
from pah_workbench.ui.docks.logs_dock import LogsDock
from pah_workbench.ui.docks.project_explorer_dock import ProjectExplorerDock
from pah_workbench.ui.views.image_view import ImageView
from pah_workbench.ui.views.spectrum_view import SpectrumView


class MainWindow(QMainWindow):
    def __init__(
        self,
        file_import_service: FileImportService,
        settings_service: SettingsService,
        logging_service: LoggingService,
    ) -> None:
        super().__init__()
        self.setWindowTitle("JWST PAH Workbench")
        self.resize(1200, 800)
        self.setAcceptDrops(True)

        self.file_import_service = file_import_service
        self.settings_service = settings_service
        self.logger = logging_service.logger

        self._files_by_path: dict[str, ImportedFile] = {}

        self.project_explorer_dock = ProjectExplorerDock(self)
        self.inspector_dock = InspectorDock(self)
        self.logs_dock = LogsDock(self)

        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.project_explorer_dock)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.inspector_dock)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, self.logs_dock)

        self.project_explorer_dock.file_selected.connect(self._on_file_selected)
        logging_service.text_handler.emitter.message.connect(self.logs_dock.append_log)

        self._setup_central_tabs()
        self._create_menus()
        self._restore_layout()

    def _setup_central_tabs(self) -> None:
        tabs = QTabWidget(self)
        tabs.addTab(SpectrumView(self), "Spectrum")
        tabs.addTab(ImageView(self), "Image")
        self.setCentralWidget(tabs)

    def _create_menus(self) -> None:
        menu_file = self.menuBar().addMenu("&File")
        menu_view = self.menuBar().addMenu("&View")

        action_new = QAction("New Project", self)
        action_new.triggered.connect(self._show_not_implemented)

        action_open = QAction("Open Project", self)
        action_open.triggered.connect(self._show_not_implemented)

        action_import = QAction("Import FITS...", self)
        action_import.triggered.connect(self._import_fits_dialog)

        action_exit = QAction("Exit", self)
        action_exit.triggered.connect(self.close)

        menu_file.addAction(action_new)
        menu_file.addAction(action_open)
        menu_file.addSeparator()
        menu_file.addAction(action_import)
        menu_file.addSeparator()
        menu_file.addAction(action_exit)

        menu_view.addAction(self.project_explorer_dock.toggleViewAction())
        menu_view.addAction(self.inspector_dock.toggleViewAction())
        menu_view.addAction(self.logs_dock.toggleViewAction())

    def _show_not_implemented(self) -> None:
        QMessageBox.information(self, "Not implemented", "Not implemented yet")

    def _import_fits_dialog(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Import FITS Files",
            "",
            "FITS files (*.fits *.fit)",
        )
        if paths:
            self._register_paths(paths, source="dialog")

    def _register_paths(self, paths: list[str], source: str) -> None:
        imported = self.file_import_service.import_paths(paths)
        for item in imported:
            key = str(item.path)
            if key in self._files_by_path:
                continue
            self._files_by_path[key] = item
            self.project_explorer_dock.add_imported_file(item)
            self.logger.info("Imported FITS (%s): %s", source, item.path)

        rejected = len(paths) - len(imported)
        if rejected > 0:
            self.logger.warning("Skipped %s invalid or unsupported file(s)", rejected)

    def _on_file_selected(self, path: str) -> None:
        selected = self._files_by_path.get(path)
        if selected is None:
            self.inspector_dock.set_placeholder()
            return
        self.inspector_dock.show_file(selected)
        self.logger.info("Selected file: %s", Path(path).name)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        if self._extract_fits_paths(event):
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent) -> None:
        fits_paths = self._extract_fits_paths(event)
        if not fits_paths:
            event.ignore()
            return

        self._register_paths(fits_paths, source="drag-drop")
        event.acceptProposedAction()

    def _extract_fits_paths(self, event: QDragEnterEvent | QDropEvent) -> list[str]:
        mime = event.mimeData()
        if not mime.hasUrls():
            return []

        paths: list[str] = []
        for url in mime.urls():
            if not url.isLocalFile():
                continue
            local_path = url.toLocalFile()
            suffix = Path(local_path).suffix.lower()
            if suffix in {".fits", ".fit"}:
                paths.append(local_path)
        return paths

    def _restore_layout(self) -> None:
        geometry, state = self.settings_service.restore_main_window()
        if geometry:
            self.restoreGeometry(geometry)
        if state:
            self.restoreState(state)

    def closeEvent(self, event: QCloseEvent) -> None:
        self.settings_service.save_main_window(
            geometry=self.saveGeometry(),
            state=self.saveState(),
        )
        self.logger.info("Application closed")
        super().closeEvent(event)

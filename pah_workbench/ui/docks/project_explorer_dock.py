"""Project Explorer dock."""

from __future__ import annotations

from PySide6.QtCore import QItemSelectionModel, QModelIndex, Qt, Signal
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QAbstractItemView, QDockWidget, QTreeView

from pah_workbench.models.imported_file import ImportedFile


class ProjectExplorerTreeBuilder:
    def __init__(self, parent, file_item_role: int, node_type_role: int) -> None:
        self._parent = parent
        self._file_item_role = file_item_role
        self._node_type_role = node_type_role

    def build(self, files: list[ImportedFile]) -> QStandardItemModel:
        model = QStandardItemModel(self._parent)
        model.setHorizontalHeaderLabels(["Project"])

        folder_icon = self._parent.style().standardIcon(
            self._parent.style().StandardPixmap.SP_DirIcon
        )
        file_icon = self._parent.style().standardIcon(
            self._parent.style().StandardPixmap.SP_FileIcon
        )

        workspace_item = QStandardItem(folder_icon, "Workspace")
        workspace_item.setEditable(False)
        workspace_item.setData("workspace", self._node_type_role)

        imported_files_item = QStandardItem(folder_icon, "Imported Files")
        imported_files_item.setEditable(False)
        imported_files_item.setData("imported_files", self._node_type_role)

        for imported_file in sorted(files, key=lambda item: item.name.lower()):
            file_item = QStandardItem(file_icon, imported_file.name)
            file_item.setEditable(False)
            file_item.setData(imported_file, self._file_item_role)
            file_item.setData("file", self._node_type_role)
            imported_files_item.appendRow(file_item)

        workspace_item.appendRow(imported_files_item)
        model.appendRow(workspace_item)
        return model


class ProjectExplorerDock(QDockWidget):
    FILE_ITEM_ROLE = Qt.ItemDataRole.UserRole
    NODE_TYPE_ROLE = Qt.ItemDataRole.UserRole + 1
    selected_file_changed = Signal(object)
    selected_files_changed = Signal(object)

    def __init__(self, parent=None) -> None:
        super().__init__("Project Explorer", parent)
        self.tree_view = QTreeView(self)
        self.model = QStandardItemModel(self)
        self.tree_builder = ProjectExplorerTreeBuilder(
            self,
            file_item_role=self.FILE_ITEM_ROLE,
            node_type_role=self.NODE_TYPE_ROLE,
        )
        self.tree_view.setModel(self.model)
        self.tree_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tree_view.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tree_view.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setUniformRowHeights(True)
        self.setWidget(self.tree_view)

        self._items: list[ImportedFile] = []
        self._selection_model: QItemSelectionModel | None = None
        self._rebuild_tree()

    def set_imported_files(self, files: list[ImportedFile]) -> None:
        self._items = list(files)
        self._rebuild_tree()

    def _rebuild_tree(self) -> None:
        self.model = self.tree_builder.build(self._items)
        self.tree_view.setModel(self.model)
        self._reconnect_selection_model()
        root_item = self.model.item(0, 0)
        imported_files_item = root_item.child(0, 0) if root_item else None
        if root_item is not None:
            self.tree_view.expand(self.model.indexFromItem(root_item))
        if imported_files_item is not None:
            self.tree_view.expand(self.model.indexFromItem(imported_files_item))
        self.tree_view.resizeColumnToContents(0)

    def _reconnect_selection_model(self) -> None:
        if self._selection_model is not None:
            try:
                self._selection_model.currentChanged.disconnect(self._on_current_changed)
            except (RuntimeError, TypeError):
                pass
            try:
                self._selection_model.selectionChanged.disconnect(
                    self._on_selection_changed
                )
            except (RuntimeError, TypeError):
                pass

        self._selection_model = self.tree_view.selectionModel()
        if self._selection_model is None:
            return
        self._selection_model.currentChanged.connect(self._on_current_changed)
        self._selection_model.selectionChanged.connect(self._on_selection_changed)

    def _on_current_changed(
        self, current: QModelIndex, previous: QModelIndex
    ) -> None:
        _ = previous
        if self._selection_model is None:
            self.selected_file_changed.emit(None)
            return

        selected_file_count = 0
        for index in self._selection_model.selectedRows(0):
            if index.data(self.NODE_TYPE_ROLE) == "file" and isinstance(
                index.data(self.FILE_ITEM_ROLE), ImportedFile
            ):
                selected_file_count += 1

        node_type = current.data(self.NODE_TYPE_ROLE) if current.isValid() else None
        imported_file = current.data(self.FILE_ITEM_ROLE) if current.isValid() else None
        if (
            selected_file_count == 1
            and node_type == "file"
            and isinstance(imported_file, ImportedFile)
        ):
            # Single-file signal stays focused on current selection.
            self.selected_file_changed.emit(imported_file)
            return
        self.selected_file_changed.emit(None)

    def _on_selection_changed(self, *_args) -> None:
        selection_model = self._selection_model
        if selection_model is None:
            self.selected_files_changed.emit([])
            return

        selected_files: list[ImportedFile] = []
        for index in selection_model.selectedRows(0):
            node_type = index.data(self.NODE_TYPE_ROLE)
            imported_file = index.data(self.FILE_ITEM_ROLE)
            if node_type == "file" and isinstance(imported_file, ImportedFile):
                selected_files.append(imported_file)
        self.selected_files_changed.emit(selected_files)

"""Mock image viewer tab."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget


class ImageView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(self.view.renderHints())

        layout = QVBoxLayout(self)
        layout.addWidget(self.view)

        self._draw_mock_image()

    def _draw_mock_image(self) -> None:
        width = 360
        height = 240
        image = QImage(width, height, QImage.Format.Format_Grayscale8)

        for y in range(height):
            for x in range(width):
                value = int((x / max(width - 1, 1)) * 255)
                radial = abs((y - height / 2) / (height / 2))
                final = max(0, min(255, int(value * (1 - 0.35 * radial))))
                image.setPixel(x, y, final)

        pixmap = QPixmap.fromImage(image)
        self.scene.clear()
        self.scene.addPixmap(pixmap)
        self.scene.setSceneRect(pixmap.rect())
        self.view.fitInView(self.scene.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)

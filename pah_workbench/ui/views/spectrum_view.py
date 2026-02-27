"""Mock spectrum plot tab."""

from __future__ import annotations

import math

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide6.QtWidgets import QVBoxLayout, QWidget


class SpectrumView(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self._draw_mock_spectrum()

    def _draw_mock_spectrum(self) -> None:
        axis = self.figure.add_subplot(111)
        x_values = [3.0 + i * 0.05 for i in range(200)]
        y_values = [
            1.0 + 0.3 * math.sin(4.0 * x) + 0.12 * math.cos(11.0 * x) for x in x_values
        ]

        axis.plot(x_values, y_values, color="#1f77b4", linewidth=1.5)
        axis.set_title("Mock PAH Spectrum")
        axis.set_xlabel("Wavelength (um)")
        axis.set_ylabel("Flux (arb. units)")
        axis.grid(True, alpha=0.25)
        self.figure.tight_layout()
        self.canvas.draw_idle()

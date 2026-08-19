# Filename: gui_workbench.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt, QPointF

class ModularPatchbayCanvas(QWidget):
    """
    Interactive graphical modular patchbay canvas supporting click-and-drag
    patch cable routing between hardware modules and synth parameters.
    """
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setMinimumHeight(500)
        self.patches = []
        self.dragging_start = None
        self.current_mouse_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0d1117"))

        # Grid lines
        painter.setPen(QPen(QColor("#21262d"), 1, Qt.PenStyle.SolidLine))
        for x in range(0, self.width(), 40):
            painter.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 40):
            painter.drawLine(0, y, self.width(), y)

        # Draw module ports / jacks
        ports = [
            ("Oscillator Pitch (432Hz)", QPointF(150, 150)),
            ("Filter Cutoff Mod", QPointF(450, 150)),
            ("Capacitor Bank Trigger", QPointF(750, 150)),
            ("EQR Spatial Field (x,y,z)", QPointF(450, 350))
        ]

        for name, pos in ports:
            painter.setBrush(QBrush(QColor("#161b22")))
            painter.setPen(QPen(QColor("#00ffcc"), 2))
            painter.drawEllipse(pos, 10, 10)

            painter.setBrush(QBrush(QColor("#00ffcc")))
            painter.drawEllipse(pos, 3, 3)

            painter.setPen(QPen(QColor("#c9d1d9"), 1))
            painter.drawText(int(pos.x()) - 50, int(pos.y()) + 28, name)

        # Draw active patch cables
        painter.setPen(QPen(QColor("#00ffcc"), 2, Qt.PenStyle.SolidLine))
        for start, end in self.patches:
            painter.drawLine(start, end)

        # Draw active dragging cable
        if self.dragging_start and self.current_mouse_pos:
            painter.setPen(QPen(QColor("#f5d97d"), 1.5, Qt.PenStyle.DashLine))
            painter.drawLine(self.dragging_start, self.current_mouse_pos)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_start = event.position()
            self.current_mouse_pos = event.position()
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging_start:
            self.current_mouse_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.dragging_start and event.button() == Qt.MouseButton.LeftButton:
            self.patches.append((self.dragging_start, event.position()))
            self.dragging_start = None
            self.current_mouse_pos = None
            self.update()

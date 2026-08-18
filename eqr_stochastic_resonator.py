# Filename: eqr_stochastic_resonator.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from eqr_constants import EQR_CONSTANTS, MEUM, FREQUENCY_432HZ

class SkeuomorphicKnob(QWidget):
    """Skeuomorphic rotary knob with integrated patch jack port."""
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.setFixedSize(74, 96)
        self.dragging = False
        self.last_y = 0
        self.is_patched = False

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
        import math

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Label
        painter.setPen(QPen(QColor("#c9d1d9"), 1))
        painter.drawText(0, 12, self.width(), 16, Qt.AlignmentFlag.AlignCenter, self.label_text)

        # Knob Body
        center = Qt.QPointF(37, 54)
        radius = 20.0

        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#30363d"), 2))
        painter.drawEllipse(center, radius, radius)

        # Tick
        normalized = (self.value - self.min_val) / (self.max_val - self.min_val)
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 5) * math.sin(angle)
        tip_y = center.y() - (radius - 5) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, Qt.QPointF(tip_x, tip_y))

        # Wire Hole Jack
        jack_center = Qt.QPointF(37, 85)
        painter.setBrush(QBrush(QColor("#0d1117")))
        painter.setPen(QPen(QColor("#00ffcc") if self.is_patched else QColor("#484f58"), 1.5))
        painter.drawEllipse(jack_center, 6.0, 6.0)

        painter.setBrush(QBrush(QColor("#00ffcc" if self.is_patched else "#161b22")))
        painter.setPen(Qt.PenStyle.NoPin)
        painter.drawEllipse(jack_center, 2.0, 2.0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            jack_center = Qt.QPointF(37, 85)
            if (event.position() - jack_center).manhattanLength() < 10:
                self.is_patched = not self.is_patched
                self.update()
            else:
                self.dragging = True
                self.last_y = event.position().y()

    def mouseMoveEvent(self, event):
        if self.dragging:
            dy = self.last_y - event.position().y()
            self.last_y = event.position().y()
            span = self.max_val - self.min_val
            step = span * (dy / 150.0)
            self.value = max(self.min_val, min(self.max_val, self.value + step))
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        span = self.max_val - self.min_val
        step = span * (0.05 if delta > 0 else -0.05)
        self.value = max(self.min_val, min(self.max_val, self.value + step))
        self.update()


class StochasticResonatorPage(QWidget):
    """
    EQR Stochastic Resonator & Noise Modulation Matrix utilizing
    skeuomorphic hardware knobs, patch ports, and remaining structural constants.
    """
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        layout = QVBoxLayout()
        group = QGroupBox("EQR Stochastic Resonator & Noise Modulation Matrix")
        grid = QGridLayout()

        resonator_channels = [
            ("Stochastic Noise Density", 0.0, 100.0, 16.18),
            ("Brownian Drift Rate", 0.01, 5.0, 0.432),
            ("Copeland-Erdős Scale", 0.1, 2.0, EQR_CONSTANTS["COPELAND_ERDOS"]),
            ("Parabolic Uniformity", 0.1, 3.0, EQR_CONSTANTS["PARABOLIC_CON"]),
            ("Backhouse Constant Depth", 1.0, 2.5, EQR_CONSTANTS["BACKHOUSE_CONST"]),
            ("Porter-Constant Decay", 0.1, 2.0, EQR_CONSTANTS["PORTER_CONSTANT"]),
            ("Reciprocal Fibonacci Factor", 0.0, 1.0, EQR_CONSTANTS["RECIPROCAL_FIB"]),
            ("MEUM Stochastic Lock", 0.0, 2.0, MEUM)
        ]

        for idx, (label, min_v, max_v, def_v) in enumerate(resonator_channels):
            r = idx // 4
            c = idx % 4
            knob = SkeuomorphicKnob(label, min_v, max_v, def_v)
            grid.addWidget(knob, r, c)

        group.setLayout(grid)
        layout.addWidget(group)
        self.setLayout(layout)

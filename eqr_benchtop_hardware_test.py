# Filename: eqr_benchtop_hardware_test.py

import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from eqr_constants import EQR_CONSTANTS, MEUM, FREQUENCY_432HZ

class BenchtopTestKnob(QWidget):
    """Standalone skeuomorphic rotary knob designed for benchtop hardware calibration."""
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.setFixedSize(84, 106)
        self.dragging = False
        self.last_y = 0
        self.is_patched = True

    def paintEvent(self, event):
        from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
        import math

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Label
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(0, 10, self.width(), 16, Qt.AlignmentFlag.AlignCenter, self.label_text)

        # Value readout
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(0, 24, self.width(), 14, Qt.AlignmentFlag.AlignCenter, f"{self.value:.2f}")

        # Knob Body
        center = Qt.QPointF(42, 60)
        radius = 22.0

        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#30363d"), 2))
        painter.drawEllipse(center, radius, radius)

        # Rotation indicator tick
        normalized = (self.value - self.min_val) / (self.max_val - self.min_val)
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 5) * math.sin(angle)
        tip_y = center.y() - (radius - 5) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, Qt.QPointF(tip_x, tip_y))

        # Patch jack port at bottom
        jack_center = Qt.QPointF(42, 93)
        painter.setBrush(QBrush(QColor("#0d1117")))
        painter.setPen(QPen(QColor("#00ffcc") if self.is_patched else QColor("#484f58"), 1.5))
        painter.drawEllipse(jack_center, 6.0, 6.0)

        painter.setBrush(QBrush(QColor("#00ffcc" if self.is_patched else "#161b22")))
        painter.setPen(Qt.PenStyle.NoPin)
        painter.drawEllipse(jack_center, 2.0, 2.0)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            jack_center = Qt.QPointF(42, 93)
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


class EQRBenchtopCalibrationWindow(QWidget):
    """
    Dedicated benchtop diagnostic and calibration tool for real-time hardware testing,
    pulsed power monitoring, and constant verification.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EQR Benchtop Hardware Calibration & Diagnostics Suite")
        self.resize(850, 650)

        layout = QVBoxLayout()

        group = QGroupBox("Benchtop Diagnostics & Pulsed Power Calibration Matrix")
        grid = QGridLayout()

        benchtop_params = [
            ("Capacitor Bank Voltage", 0.0, 1500.0, 900.0),
            ("Capacitance Load", 10.0, 5000.0, 90.0),
            ("Z-Pinch Tuning Spectrum", 0.0, 100.0, 75.0),
            ("Nanoparticle Formic Ratio", 0.0, 100.0, 50.0),
            ("Resonant Charge Mode", 0.0, 1.0, 1.0),
            ("Meum Hardware Scaling", 0.0, 4.0, MEUM),
            ("Base Reference 432Hz", 20.0, 20000.0, FREQUENCY_432HZ),
            ("System Safety Interlock", 0.0, 1.0, 1.0)
        ]

        for idx, (label, min_v, max_v, def_v) in enumerate(benchtop_params):
            r = idx // 4
            c = idx % 4
            knob = BenchtopTestKnob(label, min_v, max_v, def_v)
            grid.addWidget(knob, r, c)

        group.setLayout(grid)
        layout.addWidget(group)

        # Test Trigger Button
        self.test_button = QPushButton("Execute Benchtop Calibration Diagnostics Pulse")
        self.test_button.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 10px;")
        layout.addWidget(self.test_button)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    benchtop_window = EQRBenchtopCalibrationWindow()
    benchtop_window.show()
    sys.exit(app.exec())

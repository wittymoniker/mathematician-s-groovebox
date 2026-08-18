# Filename: eqr_ultimate_extension_matrix.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette, QPainterPath

# ---------------------------------------------------------
# ULTIMATE EXTENSION KNOB WIDGET ($x, y, z$ Scalar Control)
# ---------------------------------------------------------
class UltimateExtensionKnob(QWidget):
    """
    Precision rotary controller for extended tensor dimensions and operator matrices.
    - Vertical Drag: Modulates continuous parameter scaling.
    - Jack Port Click: Toggles differential patch routing.
    - Scroll Wheel: High-resolution fine tuning.
    """
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, math_note="", parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.math_note = math_note
        self.setFixedSize(110, 130)
        self.dragging = False
        self.last_y = 0
        self.is_patched = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Label
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(0, 8, self.width(), 14, Qt.AlignmentFlag.AlignCenter, self.label_text)

        # Readout
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(0, 22, self.width(), 12, Qt.AlignmentFlag.AlignCenter, f"Val: {self.value:.3f}")

        # Knob Body
        center = QPointF(55, 62)
        radius = 20.0

        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#30363d"), 2))
        painter.drawEllipse(center, radius, radius)

        # Indicator Tick
        span_val = self.max_val - self.min_val if self.max_val != self.min_val else 1.0
        normalized = (self.value - self.min_val) / span_val
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 5) * math.sin(angle)
        tip_y = center.y() - (radius - 5) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, QPointF(tip_x, tip_y))

        # Patch Jack Port
        jack_center = QPointF(55, 96)
        painter.setBrush(QBrush(QColor("#0d1117")))
        painter.setPen(QPen(QColor("#00ffcc") if self.is_patched else QColor("#484f58"), 1.5))
        painter.drawEllipse(jack_center, 5.0, 5.0)

        # Mathematical Footer Note
        painter.setPen(QPen(QColor("#c9d1d9"), 1))
        painter.drawText(2, 108, self.width() - 4, 20, Qt.AlignmentFlag.AlignCenter, self.math_note)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            jack_center = QPointF(55, 96)
            if (event.position() - jack_center).manhattanLength() < 12:
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
        step = span * (0.02 if delta > 0 else -0.02)
        self.value = max(self.min_val, min(self.max_val, self.value + step))
        self.update()


# ---------------------------------------------------------
# ULTIMATE EXTENSION SUITE (Advanced Tensor & Field Modules)
# ---------------------------------------------------------
class EQRUltimateExtensionSuite(QMainWindow):
    """
    Final extension matrix integrating higher-order field tensors ($x, y, z$),
    differential operator selectors, and advanced frequency multiplexing lanes.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Ultimate Extension Matrix")
        self.resize(1700, 950)
        self.set_dark_palette()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Extension modules
        self.tabs.addTab(self.create_tensor_field_tab(), "1. Higher-Order Tensor Fields ($x, y, z$)")
        self.tabs.addTab(self.create_operator_matrix_tab(), "2. Differential Operator Matrix")
        self.tabs.addTab(self.create_multiplex_lane_tab(), "3. Frequency Multiplexing Lane")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("Ultimate Extension Active | Tensor Fields Synchronized | 432Hz Core Lock")

    def set_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#0d1117"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#161b22"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#21262d"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#1f6feb"))
        QApplication.setPalette(palette)

    def create_tensor_field_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Tensor Field Modulation Guide ($x, y, z$):</b><br>"
            "• Controls multi-dimensional tensor interactions and spatial curvature parameters.<br>"
            "• Drag knobs vertically; click patch ports to route individual differential lines."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        tensor_params = [
            ("X-Tensor Gradient", -20.0, 20.0, 1.0, "x spatial gradient"),
            ("Y-Tensor Curvature", -20.0, 20.0, 1.618, "y spatial curvature"),
            ("Z-Tensor Flux", -20.0, 20.0, 2.414, "z spatial flux"),
            ("Metric Tensor Scale", 0.1, 5.0, 1.0, "Metric scaling"),
            ("Affine Connection", -5.0, 5.0, 0.5, "Connection coefficient"),
            ("Ricci Scalar Gain", 0.0, 10.0, 2.0, "Scalar field gain"),
            ("Tensor Damping", 0.0, 1.0, 0.85, "Dissipation factor"),
            ("Field Coupling", 0.0, 2.0, 1.0, "Cross-coupling ratio")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(tensor_params):
            grid.addWidget(UltimateExtensionKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_operator_matrix_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Differential Operator Matrix:</b><br>"
            "Fine-tunes operator transformation rules derived from foundational math theory."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        operator_params = [
            ("Operator Alpha", 0.0, 10.0, 1.324, "Primary Operator"),
            ("Operator Beta", 0.0, 10.0, 2.414, "Secondary Operator"),
            ("Operator Gamma", 0.0, 10.0, 1.465, "Tertiary Operator"),
            ("Divergence Weight", 0.0, 5.0, 1.0, "Div vector"),
            ("Curl Magnitude", 0.0, 5.0, 0.75, "Curl vector"),
            ("Laplacian Density", 0.0, 5.0, 1.202, "Laplacian field"),
            ("Eigenvalue Shift", -10.0, 10.0, 0.0, "Eigen shift"),
            ("Phase Locking", 0.0, 1.0, 1.0, "Coherence lock")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(operator_params):
            grid.addWidget(UltimateExtensionKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_multiplex_lane_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Frequency Multiplexing Lane:</b><br>"
            "• Manages harmonic channel separation and frequency domain routing.<br>"
            "• Click the execution trigger to test multiplexer sync stability."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        mux_params = [
            ("Channel 1 Offset", 20.0, 2000.0, 432.0, "Base 432Hz"),
            ("Channel 2 Offset", 20.0, 4000.0, 864.0, "Harmonic 2"),
            ("Channel 3 Offset", 20.0, 8000.0, 1296.0, "Harmonic 3"),
            ("Channel 4 Offset", 20.0, 16000.0, 1728.0, "Harmonic 4"),
            ("Bandwidth Spread", 0.1, 10.0, 1.0, "Width control"),
            ("Modulation Depth", 0.0, 1.0, 0.5, "Depth scalar"),
            ("Carrier Suppression", 0.0, 1.0, 0.2, "Suppression factor"),
            ("Multiplex Interlock", 0.0, 1.0, 1.0, "Active State")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(mux_params):
            grid.addWidget(UltimateExtensionKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        action_btn = QPushButton("Execute Multiplex Channel Sync Pulse")
        action_btn.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 12px; border-radius: 6px;")
        layout.addWidget(action_btn)

        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRUltimateExtensionSuite()
    window.show()
    sys.exit(app.exec())

# Filename: eqr_singularity_matrix_final.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette, QPainterPath

# ---------------------------------------------------------
# SINGULARITY-GRADE MATHEMATICAL KNOB ($x, y, z$ Field Control)
# ---------------------------------------------------------
class SingularityMathKnob(QWidget):
    """
    Ultimate-tier rotary controller engineered for absolute singularity mapping.
    - Vertical Drag: Continuous parameter modulation across $x, y, z$ space.
    - Jack Port Click: Toggles hardware patch routing.
    - Scroll Wheel: High-precision logarithmic tuning.
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

        # Parameter Label
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
# SINGULARITY MATRIX SUITE (Final Comprehensive Hub)
# ---------------------------------------------------------
class EQRSingularityMatrixSuite(QMainWindow):
    """
    Absolute final synchronization suite unifying quantum field states,
    dimensional coordinate warping ($x, y, z$), and absolute master clocking.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Singularity Matrix Suite")
        self.resize(1750, 950)
        self.set_dark_palette()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Final modules
        self.tabs.addTab(self.create_singularity_coordinates_tab(), "1. Singularity Coordinates ($x, y, z$)")
        self.tabs.addTab(self.create_quantum_state_tab(), "2. Quantum State Modulator")
        self.tabs.addTab(self.create_master_sync_tab(), "3. Absolute Master Synchronization")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("Singularity Matrix Online | Zero-Point Lock Engaged | 432Hz Core Reference")

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

    def create_singularity_coordinates_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Singularity Coordinate Matrix ($x, y, z$):</b><br>"
            "• Direct vector warping across high-energy spatial boundaries.<br>"
            "• Drag vertically to adjust values; click jack ports to toggle patch paths."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        singularity_params = [
            ("X-Singularity Flux", -50.0, 50.0, 1.0, "x singularity vector"),
            ("Y-Singularity Harmonic", -50.0, 50.0, 1.618, "y singularity vector"),
            ("Z-Singularity Horizon", -50.0, 50.0, 2.414, "z horizon boundary"),
            ("Gravitational Scale", 0.0, 10.0, 1.0, "Metric gravity"),
            ("Event Horizon Width", 0.1, 5.0, 1.202, "Horizon width"),
            ("Hawking Radiation Gain", 0.0, 5.0, 0.5, "Thermal emission"),
            ("Singularity Damping", 0.0, 1.0, 0.9, "Stability damping"),
            ("Horizon Coupling", 0.0, 2.0, 1.0, "Cross-coupling")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(singularity_params):
            grid.addWidget(SingularityMathKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_quantum_state_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Quantum State Modulator:</b><br>"
            "Controls superposition weights and probabilistic wave collapse states."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        quantum_params = [
            ("Superposition Alpha", 0.0, 1.0, 0.707, "State 0 Amplitude"),
            ("Superposition Beta", 0.0, 1.0, 0.707, "State 1 Amplitude"),
            ("Phase Coherence", 0.0, 6.28, 0.0, "Phase angle"),
            ("Entanglement Factor", 0.0, 1.0, 1.0, "Correlator"),
            ("Decoherence Rate", 0.0, 1.0, 0.05, "Decay constant"),
            ("Tunneling Probability", 0.0, 1.0, 0.2, "Barrier pass"),
            ("Eigenstate Shift", -10.0, 10.0, 0.0, "Energy shift"),
            ("Zero-Point Lock", 0.0, 1.0, 1.0, "Vacuum state")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(quantum_params):
            grid.addWidget(SingularityMathKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_master_sync_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Absolute Master Synchronization:</b><br>"
            "• Final system-wide synchronization hub.<br>"
            "• Click the execution trigger to lock all matrices to the 432Hz core reference."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        sync_params = [
            ("Master Pitch Lock", 20.0, 20000.0, 432.0, "432Hz Reference"),
            ("Harmonic Multiplier", 0.1, 16.0, 1.0, "Integer ratio"),
            ("Clock Jitter Filter", 0.0, 1.0, 0.01, "Timing jitter"),
            ("Buffer Latency", 1.0, 64.0, 4.0, "Buffer frames"),
            ("Output Attenuation", 0.0, 1.0, 0.8, "Master gain"),
            ("Limiter Threshold", -24.0, 0.0, -0.1, "Peak ceiling"),
            ("System Interlock", 0.0, 1.0, 1.0, "Survival Mode"),
            ("Singularity Ready", 0.0, 1.0, 1.0, "Full Lock")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(sync_params):
            grid.addWidget(SingularityMathKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        action_btn = QPushButton("Execute Absolute Singularity Synchronization Pulse")
        action_btn.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 12px; border-radius: 6px;")
        layout.addWidget(action_btn)

        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRSingularityMatrixSuite()
    window.show()
    sys.exit(app.exec())

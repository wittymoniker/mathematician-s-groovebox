# Filename: eqr_complete_suite_master.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette, QPainterPath

# ---------------------------------------------------------
# ULTIMATE IDEALIZED KNOB & PATCH PORT WIDGET
# ---------------------------------------------------------
class IdealizedMathKnob(QWidget):
    """
    Skeuomorphic rotary controller designed for mathematical mapping ($x, y, z$ space).
    - Vertical Drag: Adjusts continuous value.
    - Jack Port Click: Toggles patch routing circuit (Cyan = Active, Grey = Bypassed).
    - Scroll Wheel: Micro-steps tuning.
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

        # Numerical Readout
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
# MASTER COMPREHENSIVE SUITE (All Modules Integrated)
# ---------------------------------------------------------
class EQRCompleteSuiteMaster(QMainWindow):
    """
    Final consolidated master application combining the Groovebox Sequencer,
    Spatial Coordinate Matrices ($x, y, z$), Transcendental Constants,
    and Benchtop Hardware Telemetry into a single unified workspace.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Ultimate Master Suite")
        self.resize(1650, 950)
        self.set_dark_palette()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Full module architecture integration
        self.tabs.addTab(self.create_spatial_matrix_tab(), "1. Spatial Matrix ($x, y, z$)")
        self.tabs.addTab(self.create_transcendental_tab(), "2. Transcendental Constants")
        self.tabs.addTab(self.create_hardware_bench_tab(), "3. Benchtop & Pulsed Power")
        self.tabs.addTab(self.create_groovebox_sequencer_tab(), "4. Groovebox Automation Hub")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("Ultimate Master Suite Online | 432Hz Reference | All Modules Fully Synchronized")

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

    def create_spatial_matrix_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Spatial Vector Space Guide ($x, y, z$):</b><br>"
            "• <b>Rotary Controls:</b> Drag vertically to scale variables across axes.<br>"
            "• <b>Jack Port:</b> Click to toggle patch routing state."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        channels = [
            ("X-Axis Variance", -10.0, 10.0, 1.0, "Mapped to x domain"),
            ("Y-Axis Harmonic", -10.0, 10.0, 1.618, "Mapped to y domain"),
            ("Z-Axis Depth Matrix", -10.0, 10.0, 2.414, "Mapped to z domain"),
            ("Core Spatial Scale", 0.0, 4.0, 1.618, "Ratio Scaling"),
            ("Master 432Hz Base", 20.0, 20000.0, 432.0, "Fundamental Tuning"),
            ("Golden Ratio Spread", -1.0, 1.0, 0.618, "Phi Phase Dispersion"),
            ("Resonance Feedback", 0.0, 1.0, 0.75, "Feedback Damping"),
            ("Analog Tube Saturation", 1.0, 10.0, 2.2, "Harmonic Overdrive")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(channels):
            grid.addWidget(IdealizedMathKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_transcendental_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Transcendental Constant Modulator:</b><br>"
            "Direct architectural control utilizing exact structural values."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        constants_list = [
            ("Plastic Number", 1.0, 2.0, 1.324, "ρ Constant"),
            ("Silver Ratio", 1.0, 3.0, 2.414, "δ_s Constant"),
            ("Supergolden", 1.0, 2.5, 1.465, "ψ Constant"),
            ("Apéry Constant", 1.0, 2.0, 1.202, "ζ(3) Vector"),
            ("Euler-Mascheroni", 0.0, 1.0, 0.577, "γ Constant"),
            ("Gauss Lemniscate", 1.0, 4.0, 2.622, "ϖ Constant"),
            ("Khinchin Constant", 1.0, 3.0, 2.685, "K_0 Vector"),
            ("Constant Lock", 0.0, 2.0, 1.618, "Primary Ratio")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(constants_list):
            grid.addWidget(IdealizedMathKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_hardware_bench_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Benchtop Hardware & Pulsed Power Matrix:</b><br>"
            "• Monitor parallel capacitor banks and diagnostic parameters."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        bench_params = [
            ("Capacitor Voltage", 0.0, 1500.0, 900.0, "900V Parallel Bank"),
            ("Capacitance Load", 10.0, 5000.0, 90.0, "90uF Storage"),
            ("Z-Pinch Tuning", 0.0, 100.0, 75.0, "Spectrum Offset"),
            ("Nanoparticle Formic", 0.0, 100.0, 50.0, "Composition Ratio"),
            ("Resonant Charge Mode", 0.0, 1.0, 1.0, "Parallel Active"),
            ("Hardware Scale", 0.0, 4.0, 1.618, "Hardware Ratio"),
            ("Base Reference", 20.0, 20000.0, 432.0, "Standard Hz"),
            ("System Interlock", 0.0, 1.0, 1.0, "Survival Mode")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(bench_params):
            grid.addWidget(IdealizedMathKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        action_btn = QPushButton("Execute Hardware Diagnostics & Calibration Pulse")
        action_btn.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 12px; border-radius: 6px;")
        layout.addWidget(action_btn)

        return widget

    def create_groovebox_sequencer_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Groovebox Automation Lane:</b><br>"
            "Integrated step and curve modulation routing matrix."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        matrix_group = QGroupBox("Master Groovebox Parameter Matrix ($x, y, z$)")
        matrix_grid = QGridLayout()
        params = [
            ("Harmonic Shift", 0.1, 16.0, 1.618, "x-domain scalar"),
            ("Sub-Bass Gain", 0.0, 2.0, 0.8, "y-domain gain"),
            ("Resonance Decay", 0.01, 5.0, 0.5, "z-domain decay"),
            ("Wave Folding", 0.0, 100.0, 25.0, "Non-linear fold")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(params):
            matrix_grid.addWidget(IdealizedMathKnob(lbl, min_v, max_v, def_v, note), 0, idx)
        matrix_group.setLayout(matrix_grid)
        container_layout.addWidget(matrix_group)

        container_layout.addStretch()
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRCompleteSuiteMaster()
    window.show()
    sys.exit(app.exec())

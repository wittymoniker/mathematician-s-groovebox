# Filename: eqr_groovebox_idealized.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette

# ---------------------------------------------------------
# MATHEMATICAL CONSTANTS & CONFIGURATION (The EQR Engine Core)
# ---------------------------------------------------------
MEUM = 1.618033988749895  # Proprietary scale constant
FREQUENCY_432HZ = 432.0

EQR_CONSTANTS = {
    "PHI": 1.618033, "SILVER_RATIO": 2.414213, "PLASTIC_NUMBER": 1.324717,
    "SUPERGOLDEN": 1.465571, "EULER_MASCHERONI": 0.577215, "APERY_CONSTANT": 1.202056,
    "GAUSS_LEMNISCATE": 2.622057, "KHINCHIN_CONST": 2.685452, "GLAISHER_KINKEL": 1.282427,
    "TWIN_PRIME": 0.660161, "BRUN_CONSTANT": 1.902160, "OMEGA_CONSTANT": 0.567143,
    "BACKHOUSE_CONST": 1.456074, "COPELAND_ERDOS": 0.233333, "PARABOLIC_CON": 1.229607,
    "PORTER_CONSTANT": 0.557014, "RECIPROCAL_FIB": 0.301502
}

# ---------------------------------------------------------
# SKEUOMORPHIC MATHEMATICAL KNOB WITH INLINE DOCUMENTATION
# ---------------------------------------------------------
class IdealizedMathKnob(QWidget):
    """
    Rotary controller representing a mathematical vector or constant transformation.
    - Drag Vertically: Adjusts parameter continuous value ($x, y, z$ scalar spaces).
    - Click Jack Port (Bottom): Toggles patch routing mode (closed/open circuit).
    - Scroll Wheel: Fine-tune micro-steps.
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
        painter.font().setPointSize(8)
        painter.drawText(0, 8, self.width(), 14, Qt.AlignmentFlag.AlignCenter, self.label_text)

        # Live Numerical Readout ($x, y, z$ mapping)
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(0, 22, self.width(), 12, Qt.AlignmentFlag.AlignCenter, f"Val: {self.value:.3f}")

        # Knob Body (Rotational Dial)
        center = QPointF(55, 62)
        radius = 20.0

        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#30363d"), 2))
        painter.drawEllipse(center, radius, radius)

        # Angle calculation (-130° to +130° arc)
        normalized = (self.value - self.min_val) / (self.max_val - self.min_val if self.max_val != self.min_val else 1.0)
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 5) * math.sin(angle)
        tip_y = center.y() - (radius - 5) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, QPointF(tip_x, tip_y))

        # Patch Jack Port (Bottom Control)
        jack_center = QPointF(55, 96)
        painter.setBrush(QBrush(QColor("#0d1117")))
        painter.setPen(QPen(QColor("#00ffcc") if self.is_patched else QColor("#484f58"), 1.5))
        painter.drawEllipse(jack_center, 5.0, 5.0)

        # Mathematical Operation Note Footer
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
# IDEALIZED GROOVEBOX MAIN APPLICATION WINDOW
# ---------------------------------------------------------
class EQRMathematicianGroovebox(QMainWindow):
    """
    Idealized Groovebox Architecture designed for mathematical synthesis.
    Unifies spatial coordinates (x, y, z), transcendental constants,
    and modular hardware workflows into an intuitive tabbed instrument.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Mathematician's Groovebox")
        self.resize(1500, 950)
        self.set_dark_palette()

        # Main Layout Container with Tabs
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Build Synthesizer Subsystem Modules
        self.tabs.addTab(self.create_space_matrix_tab(), "1. Coordinate Space (x, y, z)")
        self.tabs.addTab(self.create_transcendental_tab(), "2. Transcendental Constants")
        self.tabs.addTab(self.create_hardware_bench_tab(), "3. Benchtop & Pulsed Power")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("Groovebox Active | 432Hz Master Tuning | x,y,z Real-Time Vector Mapping Online")

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

    def create_space_matrix_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Documentation Banner
        doc_label = QLabel(
            "<b>User Guide & Button Workflow:</b><br>"
            "• <b>Rotary Knobs:</b> Click and drag vertically to scale variable metrics ($x, y, z$).<br>"
            "• <b>Bottom Jack Port:</b> Click the circular port to toggle signal patching (Cyan = Active Circuit, Grey = Bypassed).<br>"
            "• <b>Scroll Wheel:</b> Fine-tunes parameters dynamically."
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
            ("MEUM Spatial Scale", 0.0, 4.0, MEUM, "Core Ratio Scaling"),
            ("Master 432Hz Base", 20.0, 20000.0, FREQUENCY_432HZ, "Fundamental Tuning"),
            ("Golden Ratio Spread", -1.0, 1.0, 0.618, "Phi Phase Dispersion"),
            ("Resonance Feedback", 0.0, 1.0, 0.75, "Feedback Damping"),
            ("Analog Tube Saturation", 1.0, 10.0, 2.2, "Harmonic Overdrive")
        ]

        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(channels):
            knob = IdealizedMathKnob(lbl, min_v, max_v, def_v, note)
            grid.addWidget(knob, idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_transcendental_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Transcendental Constant Modulator:</b><br>"
            "Direct architectural synthesis control utilizing exact structural values from <i>Science Theories and Inventions</i>."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        constants_list = [
            ("Plastic Number", 1.0, 2.0, EQR_CONSTANTS["PLASTIC_NUMBER"], "ρ Constant"),
            ("Silver Ratio", 1.0, 3.0, EQR_CONSTANTS["SILVER_RATIO"], "δ_s Constant"),
            ("Supergolden", 1.0, 2.5, EQR_CONSTANTS["SUPERGOLDEN"], "ψ Constant"),
            ("Apéry Constant", 1.0, 2.0, EQR_CONSTANTS["APERY_CONSTANT"], "ζ(3) Vector"),
            ("Euler-Mascheroni", 0.0, 1.0, EQR_CONSTANTS["EULER_MASCHERONI"], "γ Constant"),
            ("Gauss Lemniscate", 1.0, 4.0, EQR_CONSTANTS["GAUSS_LEMNISCATE"], "ϖ Constant"),
            ("Khinchin Constant", 1.0, 3.0, EQR_CONSTANTS["KHINCHIN_CONST"], "K_0 Vector"),
            ("MEUM Transcendental Lock", 0.0, 2.0, MEUM, "Primary Ratio")
        ]

        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(constants_list):
            knob = IdealizedMathKnob(lbl, min_v, max_v, def_v, note)
            grid.addWidget(knob, idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_hardware_bench_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Benchtop Hardware & Pulsed Power Calibration Matrix:</b><br>"
            "• <b>Trigger Button:</b> Executes safe diagnostic sequence across parallel capacitor banks.<br>"
            "• Monitor real-time parameters for experimental hardware rigs."
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
            ("Meum Hardware Scale", 0.0, 4.0, MEUM, "Hardware Ratio"),
            ("Base Reference", 20.0, 20000.0, FREQUENCY_432HZ, "Standard Hz"),
            ("System Interlock", 0.0, 1.0, 1.0, "Survival Mode")
        ]

        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(bench_params):
            knob = IdealizedMathKnob(lbl, min_v, max_v, def_v, note)
            grid.addWidget(knob, idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        # Action Button
        action_btn = QPushButton("Execute Hardware Diagnostics & Calibration Pulse")
        action_btn.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 12px; border-radius: 6px;")
        layout.addWidget(action_btn)

        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRMathematicianGroovebox()
    window.show()
    sys.exit(app.exec())

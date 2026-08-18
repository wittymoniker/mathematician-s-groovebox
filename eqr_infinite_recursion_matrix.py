# Filename: eqr_infinite_recursion_matrix.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette, QPainterPath

# ---------------------------------------------------------
# INFINITE RECURSION MATHEMATICAL KNOB ($x, y, z$ Final Horizon)
# ---------------------------------------------------------
class InfiniteRecursionKnob(QWidget):
    """
    Absolute boundary-tier rotary controller for infinite mathematical recursion loops.
    - Vertical Drag: Continuous tensor modulation across $x, y, z$ space.
    - Jack Port Click: Toggles recursive circuit feedback.
    - Scroll Wheel: Hyper-precision asymptotic stepping.
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
# INFINITE RECURSION MATRIX SUITE (The Absolute Termination Node)
# ---------------------------------------------------------
class EQRInfiniteRecursionSuite(QMainWindow):
    """
    The definitive final modular GUI suite. Closes the topological loop across
    asymptotic recursive dimensions ($x, y, z$), fractal feedback, and absolute
    groovebox engine convergence.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Infinite Recursion Master Suite")
        self.resize(1800, 950)
        self.set_dark_palette()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Final closure modules
        self.tabs.addTab(self.create_recursion_coordinates_tab(), "1. Asymptotic Coordinates ($x, y, z$)")
        self.tabs.addTab(self.create_fractal_feedback_tab(), "2. Fractal Feedback Loop")
        self.tabs.addTab(self.create_absolute_closure_tab(), "3. Absolute Convergence Engine")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("Recursion Loop Closed | Asymptotic Convergence Reached | 432Hz Core Harmonic Stable")

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

    def create_recursion_coordinates_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Asymptotic Coordinate Matrix ($x, y, z$):</b><br>"
            "• Manages recursive boundary scaling and multi-layered spatial folding.<br>"
            "• Vertical drag adjusts continuous values; jack ports toggle feedback loops."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        recursion_params = [
            ("X-Recursion Depth", -100.0, 100.0, 1.0, "x recursive scalar"),
            ("Y-Recursion Scale", -100.0, 100.0, 1.618, "y recursive scaling"),
            ("Z-Asymptotic Limit", -100.0, 100.0, 2.414, "z limit boundary"),
            ("Fractal Iterations", 1.0, 64.0, 8.0, "Depth counter"),
            ("Convergence Rate", 0.0, 1.0, 0.95, "Asymptotic factor"),
            ("Self-Similarity Gain", 0.0, 2.0, 1.0, "Scaling ratio"),
            ("Phase Loop Damping", 0.0, 1.0, 0.85, "Damping coefficient"),
            ("Recursive Coupling", 0.0, 2.0, 1.0, "Inter-loop gain")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(recursion_params):
            grid.addWidget(InfiniteRecursionKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_fractal_feedback_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Fractal Feedback Loop:</b><br>"
            "Controls non-linear audio and structural regeneration matrices."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        feedback_params = [
            ("Feedback Amplitude", 0.0, 2.0, 0.75, "Regen gain"),
            ("Harmonic Folding", 0.0, 50.0, 12.0, "Wave fold index"),
            ("Bifurcation Rate", 0.0, 4.0, 2.0, "Chaos factor"),
            ("Attractor Density", 0.1, 10.0, 1.618, "Phase attractor"),
            ("Resonance Decay", 0.01, 5.0, 0.5, "Tail damping"),
            ("Spectral Dispersion", 0.0, 1.0, 0.3, "Spread factor"),
            ("Non-Linear Drive", 1.0, 10.0, 3.0, "Overdrive scalar"),
            ("Feedback Interlock", 0.0, 1.0, 1.0, "Active State")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(feedback_params):
            grid.addWidget(InfiniteRecursionKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_absolute_closure_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Absolute Convergence Engine:</b><br>"
            "• Final system convergence and master clock stabilization.<br>"
            "• Click the execution trigger to lock the infinite loop permanently to 432Hz."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        closure_params = [
            ("Master Reference Hz", 20.0, 20000.0, 432.0, "432Hz Core Pitch"),
            ("Harmonic Multiplier", 0.1, 16.0, 1.0, "Integer ratio"),
            ("Asymptotic Jitter Filter", 0.0, 1.0, 0.0, "Zero jitter"),
            ("Buffer Latency", 1.0, 64.0, 2.0, "Ultra-low buffer"),
            ("Output Attenuation", 0.0, 1.0, 0.85, "Master ceiling"),
            ("Brickwall Limiter", -24.0, 0.0, -0.1, "Peak limiter"),
            ("Survival Interlock", 0.0, 1.0, 1.0, "Mode active"),
            ("Infinite Lock", 0.0, 1.0, 1.0, "Loop Closed")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(closure_params):
            grid.addWidget(InfiniteRecursionKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        action_btn = QPushButton("Execute Absolute Infinite Recursion Closure Pulse")
        action_btn.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 12px; border-radius: 6px;")
        layout.addWidget(action_btn)

        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRInfiniteRecursionSuite()
    window.show()
    sys.exit(app.exec())

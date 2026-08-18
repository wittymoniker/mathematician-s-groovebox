# Filename: eqr_groovebox_complete_suite.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette

# ---------------------------------------------------------
# COMPLETE GROOVEBOX ROTARY CONTROLLER ($x, y, z$ Audio Space)
# ---------------------------------------------------------
class GrooveboxMasterKnob(QWidget):
    """
    Precision rotary controller for the complete groovebox workstation ($x, y, z$).
    - Vertical Drag: Modulates continuous parameter scaling.
    - Jack Port Click: Toggles audio routing / modulation patch state.
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

        # Footer Note
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
# COMPLETE GROOVEBOX MASTER SUITE (All Original Modules)
# ---------------------------------------------------------
class EQRGrooveboxCompleteSuite(QMainWindow):
    """
    Definitive, fully consolidated Groovebox Master Suite restoring all original
    modules: Spatial Coordinates ($x, y, z$), Transcendental Constants, Hardware
    Telemetry, Groovebox Sequencer, Synth Engines, and Infinite Recursion.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Complete Groovebox Master Suite")
        self.resize(1750, 950)
        self.set_dark_palette()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Full Restoration of All Architectural Tabs
        self.tabs.addTab(self.create_spatial_matrix_tab(), "1. Spatial Matrix ($x, y, z$)")
        self.tabs.addTab(self.create_transcendental_tab(), "2. Transcendental Constants")
        self.tabs.addTab(self.create_hardware_bench_tab(), "3. Benchtop & Pulsed Power")
        self.tabs.addTab(self.create_groovebox_sequencer_tab(), "4. Groovebox Automation Hub")
        self.tabs.addTab(self.create_synth_engine_tab(), "5. Synth Engine & Oscillators")
        self.tabs.addTab(self.create_recursion_closure_tab(), "6. Infinite Recursion Loop")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("Complete Groovebox Suite Online | All Modules Restored & Synchronized | 432Hz Core Active")

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
            grid.addWidget(GrooveboxMasterKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)
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
            grid.addWidget(GrooveboxMasterKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)
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
            grid.addWidget(GrooveboxMasterKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)
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
            "<b>Groovebox Automation Lane ($x, y, z$):</b><br>"
            "Integrated step and curve modulation routing matrix."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        seq_params = [
            ("X-Axis Step Scalar", -10.0, 10.0, 1.0, "x automation lane"),
            ("Y-Axis Velocity Gain", 0.0, 2.0, 1.0, "y velocity scale"),
            ("Z-Axis Gate Length", 0.05, 1.0, 0.5, "z gate duration"),
            ("Step Division", 1.0, 32.0, 16.0, "Steps per bar"),
            ("Swing Percentage", 0.0, 75.0, 0.0, "Shuffle timing"),
            ("Probability Gate", 0.0, 1.0, 1.0, "Trigger chance"),
            ("Micro-Timing Offset", -50.0, 50.0, 0.0, "Milliseconds shift"),
            ("Sequencer Lock", 0.0, 1.0, 1.0, "Active State")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(seq_params):
            grid.addWidget(GrooveboxMasterKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)
        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_synth_engine_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        doc_label = QLabel(
            "<b>Synth Engine & Waveform Modulator:</b><br>"
            "Controls core oscillator harmonics, wave folding, and filter resonance."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        synth_params = [
            ("Oscillator 1 Pitch", -24.0, 24.0, 0.0, "Semitones offset"),
            ("Oscillator 2 Detune", -100.0, 100.0, 7.0, "Cents spread"),
            ("Wave Folding Index", 0.0, 50.0, 12.0, "Non-linear fold"),
            ("Filter Cutoff Hz", 20.0, 20000.0, 2500.0, "Lowpass cutoff"),
            ("Filter Resonance", 0.0, 1.0, 0.65, "Feedback Q factor"),
            ("Amp Attack Time", 0.001, 2.0, 0.01, "Seconds attack"),
            ("Amp Decay Time", 0.01, 5.0, 0.8, "Seconds decay"),
            ("Engine Interlock", 0.0, 1.0, 1.0, "Active State")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(synth_params):
            grid.addWidget(GrooveboxMasterKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)
        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget

    def create_recursion_closure_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        doc_label = QLabel(
            "<b>Infinite Recursion & Absolute Convergence Engine:</b><br>"
            "• Final system convergence and master clock stabilization.<br>"
            "• Click execution trigger to lock the loop permanently to 432Hz."
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
            grid.addWidget(GrooveboxMasterKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)
        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)

        action_btn = QPushButton("Execute Absolute Groovebox Convergence & 432Hz Pipeline")
        action_btn.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 12px; border-radius: 6px;")
        layout.addWidget(action_btn)
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRGrooveboxCompleteSuite()
    window.show()
    sys.exit(app.exec())

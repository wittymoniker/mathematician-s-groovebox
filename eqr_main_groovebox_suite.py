# Filename: eqr_main_groovebox_suite.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette, QPainterPath

# ---------------------------------------------------------
# SHARED IDEALIZED KNOB & PATCH PORT WIDGET
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
# IDEALIZED SEQUENCER CANVAS (Wires & Nodes)
# ---------------------------------------------------------
class IdealizedSequencerCanvas(QWidget):
    """
    Modular step and curve routing canvas with realistic hanging patch wires
    and interactive control jacks.
    """
    def __init__(self, clone_id=1, parent=None):
        super().__init__(parent)
        self.clone_id = clone_id
        self.setMinimumHeight(280)
        self.nodes = [QPointF(60, 200), QPointF(340, 80), QPointF(680, 160), QPointF(960, 70)]
        self.wires = [(self.nodes[0], self.nodes[1]), (self.nodes[2], self.nodes[3])]
        self.active_node = None
        self.wiring_start = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        # Panel Background
        painter.fillRect(0, 0, w, h, QColor("#0a0e14"))

        # Grid lines
        painter.setPen(QPen(QColor("#161b22"), 1))
        for x in range(0, w, 40):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            painter.drawLine(0, y, w, y)

        # Hanging Patch Wires
        for p1, p2 in self.wires:
            ctrl = QPointF((p1.x() + p2.x()) / 2, max(p1.y(), p2.y()) + 60)
            path = QPainterPath()
            path.moveTo(p1)
            path.cubicTo(ctrl, ctrl, p2)

            # Shadow
            shadow_path = QPainterPath()
            shadow_path.moveTo(p1 + QPointF(0, 3))
            shadow_path.cubicTo(ctrl + QPointF(0, 3), ctrl + QPointF(0, 3), p2 + QPointF(0, 3))
            painter.setPen(QPen(QColor("#000000"), 3))
            painter.drawPath(shadow_path)

            # Neon Wire
            painter.setPen(QPen(QColor("#00ffcc"), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
            painter.drawPath(path)

        # Spline curve connecting nodes
        if len(self.nodes) >= 2:
            spline = QPainterPath()
            spline.moveTo(self.nodes[0])
            for i in range(len(self.nodes) - 1):
                pt1, pt2 = self.nodes[i], self.nodes[i+1]
                c1 = QPointF((pt1.x() + pt2.x()) / 2, pt1.y())
                c2 = QPointF((pt1.x() + pt2.x()) / 2, pt2.y())
                spline.cubicTo(c1, c2, pt2)
            painter.setPen(QPen(QColor("#f5d97d"), 2))
            painter.drawPath(spline)

        # Node Jacks
        for node in self.nodes:
            painter.setBrush(QBrush(QColor("#161b22")))
            painter.setPen(QPen(QColor("#00ffcc"), 2))
            painter.drawEllipse(node, 10, 10)
            painter.setBrush(QBrush(QColor("#00ffcc")))
            painter.setPen(Qt.PenStyle.NoPin)
            painter.drawEllipse(node, 3.5, 3.5)

        # Header note
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(16, 22, f"Clone #{self.clone_id} Vector Automaton | [Right-Click] Add Node | [Drag Jack to Jack] Patch Circuit")

    def mousePressEvent(self, event):
        pos = event.position()
        if event.button() == Qt.MouseButton.RightButton:
            self.nodes.append(QPointF(pos.x(), pos.y()))
            self.nodes.sort(key=lambda p: p.x())
            self.update()
        elif event.button() == Qt.MouseButton.LeftButton:
            for node in self.nodes:
                if (node - pos).manhattanLength() < 14:
                    self.wiring_start = node
                    return
            for idx, node in enumerate(self.nodes):
                if (node - pos).manhattanLength() < 22:
                    self.active_node = idx
                    break

    def mouseMoveEvent(self, event):
        if self.active_node is not None:
            new_pos = event.position()
            self.nodes[self.active_node] = QPointF(max(0, min(self.width(), new_pos.x())), max(0, min(self.height(), new_pos.y())))
            self.update()

    def mouseReleaseEvent(self, event):
        if self.wiring_start:
            pos = event.position()
            for node in self.nodes:
                if (node - pos).manhattanLength() < 18 and node != self.wiring_start:
                    self.wires.append((self.wiring_start, node))
                    break
            self.wiring_start = None
        self.active_node = None
        self.update()


# ---------------------------------------------------------
# COMPREHENSIVE MAIN GROOVEBOX SUITE WINDOW
# ---------------------------------------------------------
class EQRMainGrooveboxSuite(QMainWindow):
    """
    Fully unified EQR Groovebox Suite combining sequencer automation lanes,
    coordinate matrices ($x, y, z$), and transcendental constants into an ideal UI.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Master Groovebox Suite")
        self.resize(1550, 950)
        self.set_dark_palette()

        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)

        # Build System Tabs
        self.tabs.addTab(self.create_sequencer_tab(), "1. Sequencer & Automation Hub")
        self.tabs.addTab(self.create_constants_tab(), "2. 34-Constant Harmonic Matrix")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("Suite Online | 432Hz Master Reference | Meum Ratio Locked | All Systems Nominal")

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

    def create_sequencer_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Sequencer & Vector Automation Guide:</b><br>"
            "• <b>Canvas Nodes:</b> Drag nodes to shape automation curves; right-click to add nodes.<br>"
            "• <b>Patch Wires:</b> Click and drag from one node jack to another to create hardware-style modulation paths."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Add Canvas and Control Matrix
        self.lane = IdealizedSequencerCanvas(clone_id=1)
        container_layout.addWidget(self.lane)

        matrix_group = QGroupBox("Clone #1 Architectural Parameter Matrix ($x, y, z$)")
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

    def create_constants_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        doc_label = QLabel(
            "<b>Harmonic Constant Matrix:</b><br>"
            "Exact mathematical constants driving the groovebox synthesis engine without meum factors."
        )
        doc_label.setStyleSheet("background-color: #161b22; padding: 10px; border-radius: 6px; color: #8b949e;")
        layout.addWidget(doc_label)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)

        constants = [
            ("Plastic Number", 1.0, 2.0, 1.324, "ρ Constant"),
            ("Silver Ratio", 1.0, 3.0, 2.414, "δ_s Constant"),
            ("Supergolden", 1.0, 2.5, 1.465, "ψ Constant"),
            ("Apéry Constant", 1.0, 2.0, 1.202, "ζ(3) Vector"),
            ("Euler-Mascheroni", 0.0, 1.0, 0.577, "γ Constant"),
            ("Gauss Lemniscate", 1.0, 4.0, 2.622, "ϖ Constant"),
            ("Khinchin Constant", 1.0, 3.0, 2.685, "K_0 Vector"),
            ("MEUM Core Lock", 0.0, 2.0, 1.618, "Primary Ratio")
        ]
        for idx, (lbl, min_v, max_v, def_v, note) in enumerate(constants):
            grid.addWidget(IdealizedMathKnob(lbl, min_v, max_v, def_v, note), idx // 4, idx % 4)

        container.setLayout(grid)
        scroll.setWidget(container)
        layout.addWidget(scroll)
        return widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRMainGrooveboxSuite()
    window.show()
    sys.exit(app.exec())

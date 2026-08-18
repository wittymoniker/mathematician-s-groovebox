# Filename: effect_matrix_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt, QPointF

class EffectMatrixCanvas(QWidget):
    """
    Interactive Effect Cable Matrix canvas with explicit polarity (+ / - / Neutral)
    and scroll depth scaling.
    """
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setMinimumHeight(450)
        self.cables = []
        self.dragging_start = None
        self.current_mouse_pos = None
        self.polarity = "Neutral"
        self.cable_gain = 1.0  # Scroll depth indicator

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0a0f14"))

        # Header / Status labels with explicit scroll gain readout
        painter.setPen(QPen(QColor("#00ffcc"), 1))
        painter.drawText(20, 25, "EFFECT CABLE MATRIX (+ / - / Neutral)")

        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(20, 45, f"Polarity: {self.polarity} | [Scroll] Cable Gain Depth: {self.cable_gain:.2f}x | [Drag] Route Cable")

        # Draw effect buses / nodes
        nodes = [
            ("Reverb Send", QPointF(150, 150)),
            ("Delay Feedback", QPointF(450, 150)),
            ("Distortion Fold", QPointF(750, 150)),
            ("Filter Bank", QPointF(450, 320))
        ]

        for name, pos in nodes:
            painter.setBrush(QBrush(QColor("#f5d97d")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(pos, 10, 10)
            painter.setPen(QPen(QColor("#c9d1d9"), 1))
            painter.drawText(int(pos.x()) - 40, int(pos.y()) + 25, name)

        # Draw routed cables
        painter.setPen(QPen(QColor("#00ffcc"), 2, Qt.PenStyle.SolidLine))
        for start, end in self.cables:
            painter.drawLine(start, end)
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
            self.cables.append((self.dragging_start, event.position()))
            self.dragging_start = None
            self.current_mouse_pos = None
            self.update()

    def wheelEvent(self, event):
        """Scroll wheel adjusts cable gain depth with real-time text label updates."""
        delta = event.angleDelta().y()
        self.cable_gain = max(0.1, min(5.0, self.cable_gain + (0.1 if delta > 0 else -0.1)))
        self.update()


class EffectMatrixPage(QWidget):
    """Effect matrix workspace with polarity controls (+ / - / Neutral) and visual canvas."""
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        layout = QVBoxLayout()

        group = QGroupBox("Effect Cable Matrix (+ / - / Neutral)")
        group_layout = QVBoxLayout()

        # Toolbar for polarity selection
        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("Matrix Polarity Selector:"))
        self.combo_polarity = QComboBox()
        self.combo_polarity.addItems(["Neutral", "+ (Positive Feedback)", "- (Inverted Feedback)"])
        toolbar.addWidget(self.combo_polarity)
        toolbar.addStretch()
        group_layout.addLayout(toolbar)

        # Canvas
        self.canvas = EffectMatrixCanvas(self.engine)
        self.combo_polarity.currentTextChanged.connect(lambda val: setattr(self.canvas, 'polarity', val))
        group_layout.addWidget(self.canvas)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)

# Filename: eqr_final_master_hub.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QScrollArea, QLabel
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
        from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
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


class EQRComprehensiveMasterHub(QWidget):
    """
    Consolidated Master Hub containing the final remaining EQR hardware modules,
    fully populated with skeuomorphic rotary knobs, patch jacks, and all 34 structural constants.
    """
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        main_layout = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        container = QWidget()
        container_layout = QVBoxLayout(container)

        # Module 1: Harmonic Resonator & Spectral Synthesizer
        group1 = QGroupBox("EQR Harmonic Resonator & Spectral Synthesizer")
        grid1 = QGridLayout()
        mod1_params = [
            ("Harmonic Fundamental", 20.0, 20000.0, FREQUENCY_432HZ),
            ("Golden Ratio Width", 0.1, 10.0, EQR_CONSTANTS.get("PHI", 1.618)),
            ("Silver Constant Decay", 0.01, 5.0, EQR_CONSTANTS.get("SILVER_RATIO", 2.414)),
            ("Plastic Constant Scale", 0.1, 3.0, EQR_CONSTANTS.get("PLASTIC_NUMBER", 1.324)),
            ("Supergolden Factor", 0.1, 2.5, EQR_CONSTANTS.get("SUPERGOLDEN", 1.465)),
            ("Euler Mascheroni Bias", -2.0, 2.0, EQR_CONSTANTS.get("EULER_MASCHERONI", 0.577)),
            ("Apéry Resonance Depth", 1.0, 3.0, EQR_CONSTANTS.get("APERY_CONSTANT", 1.202)),
            ("MEUM Core Lock", 0.0, 2.0, MEUM)
        ]
        for idx, (lbl, min_v, max_v, def_v) in enumerate(mod1_params):
            grid1.addWidget(SkeuomorphicKnob(lbl, min_v, max_v, def_v), idx // 4, idx % 4)
        group1.setLayout(grid1)
        container_layout.addWidget(group1)

        # Module 2: Topology & Geodesic Field Modulator
        group2 = QGroupBox("EQR Topology & Geodesic Field Modulator")
        grid2 = QGridLayout()
        mod2_params = [
            ("Gauss Lemniscate Rate", 1.0, 4.0, EQR_CONSTANTS.get("GAUSS_LEMNISCATE", 2.622)),
            ("Khinchin Distribution", 1.0, 3.0, EQR_CONSTANTS.get("KHINCHIN_CONST", 2.685)),
            ("Glaisher Kinkela Pitch", 1.0, 2.0, EQR_CONSTANTS.get("GLAISHER_KINKEL", 1.282)),
            ("Twin Prime Shift", 0.1, 2.0, EQR_CONSTANTS.get("TWIN_PRIME", 0.660)),
            ("Brun Constant Spread", 1.0, 3.0, EQR_CONSTANTS.get("BRUN_CONSTANT", 1.902)),
            ("Omega Decay Factor", 0.1, 2.0, EQR_CONSTANTS.get("OMEGA_CONSTANT", 0.567)),
            ("Backhouse Density", 1.0, 2.5, EQR_CONSTANTS.get("BACKHOUSE_CONST", 1.456)),
            ("MEUM Topology Lock", 0.0, 2.0, MEUM)
        ]
        for idx, (lbl, min_v, max_v, def_v) in enumerate(mod2_params):
            grid2.addWidget(SkeuomorphicKnob(lbl, min_v, max_v, def_v), idx // 4, idx % 4)
        group2.setLayout(grid2)
        container_layout.addWidget(group2)

        # Module 3: Final Transcendental Summing Matrix
        group3 = QGroupBox("EQR Transcendental Summing & Final Output Matrix")
        grid3 = QGridLayout()
        mod3_params = [
            ("Copeland-Erdős Noise", 0.1, 2.0, EQR_CONSTANTS.get("COPELAND_ERDOS", 0.233)),
            ("Parabolic Uniformity", 0.1, 3.0, EQR_CONSTANTS.get("PARABOLIC_CON", 1.229)),
            ("Porter Constant Rate", 0.1, 2.0, EQR_CONSTANTS.get("PORTER_CONSTANT", 0.557)),
            ("Reciprocal Fibonacci", 0.0, 1.0, EQR_CONSTANTS.get("RECIPROCAL_FIB", 0.301)),
            ("Master Bus Limiting", 0.0, 1.0, 0.95),
            ("Output Tube Saturation", 1.0, 10.0, 3.0),
            ("Global Spatial Spread", -1.0, 1.0, 0.0),
            ("MEUM Final Lock", 0.0, 2.0, MEUM)
        ]
        for idx, (lbl, min_v, max_v, def_v) in enumerate(mod3_params):
            grid3.addWidget(SkeuomorphicKnob(lbl, min_v, max_v, def_v), idx // 4, idx % 4)
        group3.setLayout(grid3)
        container_layout.addWidget(group3)

        container_layout.addStretch()
        scroll.setWidget(container)
        main_layout.addWidget(scroll)
        self.setLayout(main_layout)

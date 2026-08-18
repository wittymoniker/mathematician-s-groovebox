# Filename: sequencer_automation_page.py

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QGroupBox, QHBoxLayout, QLabel,
    QComboBox, QScrollArea, QSlider, QPushButton, QGridLayout
)
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
from PyQt6.QtCore import Qt, QPointF

class CloneSequencerAutomationCanvas(QWidget):
    """
    Custom QPainter canvas allowing independent sequencing, spectral plotting,
    and multi-point automation curves for each cloned instrument rack layer.
    """
    def __init__(self, engine, clone_id=1, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.clone_id = clone_id
        self.setMinimumHeight(220)

        # Initial independent automation curve nodes for this specific clone
        self.nodes = [QPointF(50, 150), QPointF(450, 50), QPointF(850, 150)]
        self.active_node = None
        self.interaction_lines = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        # Background
        painter.fillRect(0, 0, width, height, QColor("#0d1117"))

        # Grid lines & sub-divisions
        painter.setPen(QPen(QColor("#21262d"), 1, Qt.PenStyle.SolidLine))
        for i in range(0, width, 40):
            painter.drawLine(i, 0, i, height)
        for j in range(0, height, 40):
            painter.drawLine(0, j, width, j)

        # Direct interaction wires
        painter.setPen(QPen(QColor("#00ffcc"), 1.2, Qt.PenStyle.DashLine))
        for start_pt, end_pt in self.interaction_lines:
            painter.drawLine(start_pt, end_pt)

        # Automation Curve (Cubic Bezier) for this Clone
        if len(self.nodes) >= 2:
            path = QPainterPath()
            path.moveTo(self.nodes[0])
            for i in range(len(self.nodes) - 1):
                p1 = self.nodes[i]
                p2 = self.nodes[i+1]
                ctrl1 = QPointF((p1.x() + p2.x()) / 2, p1.y())
                ctrl2 = QPointF((p1.x() + p2.x()) / 2, p2.y())
                path.cubicTo(ctrl1, ctrl2, p2)

            painter.setPen(QPen(QColor("#f5d97d"), 2, Qt.PenStyle.SolidLine))
            painter.drawPath(path)

        # Interactive Nodes
        painter.setBrush(QBrush(QColor("#00ffcc")))
        painter.setPen(Qt.PenStyle.NoPen)
        for node in self.nodes:
            painter.drawEllipse(node, 6, 6)

        # Label Overlay with complete coordinate indicators
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(15, 20, f"Clone #{self.clone_id} Automation Lane | Nodes: {len(self.nodes)} | [Right-Click] Add Node | [Scroll] Modify Value")

    def mousePressEvent(self, event):
        pos = event.position()
        if event.button() == Qt.MouseButton.RightButton:
            self.nodes.append(QPointF(pos.x(), pos.y()))
            self.nodes.sort(key=lambda p: p.x())
            self.update()
        elif event.button() == Qt.MouseButton.LeftButton:
            clicked_node = None
            for i, node in enumerate(self.nodes):
                if (node - pos).manhattanLength() < 14:
                    self.active_node = i
                    clicked_node = node
                    break
            if clicked_node is None:
                if not self.interaction_lines or len(self.interaction_lines[-1]) == 2:
                    self.interaction_lines.append((pos, pos))
                else:
                    start_pt = self.interaction_lines[-1][0]
                    self.interaction_lines[-1] = (start_pt, pos)
            self.update()

    def mouseMoveEvent(self, event):
        if self.active_node is not None:
            new_pos = event.position()
            x = max(0, min(self.width(), new_pos.x()))
            y = max(0, min(self.height(), new_pos.y()))
            self.nodes[self.active_node] = QPointF(x, y)
            self.update()

    def mouseReleaseEvent(self, event):
        self.active_node = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        step = 5.0 if delta > 0 else -5.0
        pos = event.position()
        for i, node in enumerate(self.nodes):
            if (node - pos).manhattanLength() < 30:
                new_y = max(0, min(self.height(), node.y() - step))
                self.nodes[i] = QPointF(node.x(), new_y)
                self.update()
                break


class CloneAutomationControlRack(QWidget):
    """
    An expansive control rack providing an exhaustive suite of knobs, sliders,
    and polarity selectors for every single clone channel.
    """
    def __init__(self, clone_id=1, parent=None):
        super().__init__(parent)
        self.clone_id = clone_id

        layout = QGridLayout()
        layout.setContentsMargins(4, 4, 4, 4)

        # Comprehensive set of extra knobs and configuration controls
        controls = [
            ("Step Gate Resolution", 1.0, 64.0, 16.0),
            ("Harmonic Skew Factor", 0.1, 10.0, 1.618),
            ("Quantize Divisor", 1.0, 32.0, 4.0),
            ("LFO Rate Mod", 0.05, 20.0, 1.0),
            ("Phase Offset Depth", -180.0, 180.0, 0.0),
            ("Resonance Feedback", 0.0, 1.0, 0.75),
            ("Jitter Probability", 0.0, 100.0, 5.0),
            ("Spectral Spread", 10.0, 8000.0, 432.0)
        ]

        for idx, (name, min_v, max_v, def_v) in enumerate(controls):
            row = idx // 4
            col = idx % 4

            box = QVBoxLayout()
            lbl = QLabel(f"{name} (#{clone_id}): {def_v:.2f}")
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setRange(int(min_v * 100), int(max_v * 100))
            slider.setValue(int(def_v * 100))

            # Connect lambda to update label dynamically
            slider.valueChanged.connect(lambda val, l=lbl, n=name: l.setText(f"{n} (#{self.clone_id}): {val/100.0:.2f}"))

            box.addWidget(lbl)
            box.addWidget(slider)

            # Additional Polarity / Mode selection combo box for granular routing
            combo = QComboBox()
            combo.addItems(["Neutral (+0)", "Positive (+1)", "Inverted (-1)", "Irrational Phi Scale", "Meum Locked"])
            box.addWidget(combo)

            layout.addLayout(box, row, col)

        self.setLayout(layout)


class PresequenceAutomationPage(QWidget):
    """
    Presequence & Automations workspace supporting stackable automation tracks
    and exhaustive control parameters for every individual instrument clone rack.
    """
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        main_layout = QVBoxLayout()

        group = QGroupBox("Clone-Specific Presequence Grid & Exhaustive Multi-Parameter Automations")
        group_layout = QVBoxLayout()

        # Scroll area for managing multiple clone automation lanes and control banks
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        self.lanes_layout = QVBoxLayout(scroll_widget)

        # Default Clone #1 Lane + Extensive Knob Rack
        self.initial_lane = CloneSequencerAutomationCanvas(self.engine, clone_id=1)
        self.initial_controls = CloneAutomationControlRack(clone_id=1)

        self.lanes_layout.addWidget(self.initial_lane)
        self.lanes_layout.addWidget(self.initial_controls)
        self.lanes_layout.addStretch()

        scroll_area.setWidget(scroll_widget)
        group_layout.addWidget(scroll_area)

        group.setLayout(group_layout)
        main_layout.addWidget(group)
        self.setLayout(main_layout)

    def add_clone_automation_lane(self, clone_id: int):
        """Dynamically adds an independent automation lane and exhaustive knob rack for a newly cloned instrument rack."""
        new_lane = CloneSequencerAutomationCanvas(self.engine, clone_id=clone_id)
        new_controls = CloneAutomationControlRack(clone_id=clone_id)

        # Insert before trailing stretch
        count = self.lanes_layout.count()
        self.lanes_layout.insertWidget(count - 1, new_lane)
        self.lanes_layout.insertWidget(count, new_controls)

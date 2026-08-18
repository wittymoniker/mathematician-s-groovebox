# Filename: cross_resonator_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel, QHBoxLayout, QSlider, QPushButton
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush
from PyQt6.QtCore import Qt, QPointF

class CrossResonatorCanvas(QWidget):
    """
    Interactive graphical cross-resonator network canvas.
    - [Right-Click]: Add resonator node.
    - [Left-Click & Drag]: Crosswire resonator feedback cables.
    - [Scroll Wheel]: Dynamically scale resonator depth / frequency modulation.
    """
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setMinimumHeight(450)
        self.nodes = [QPointF(200, 150), QPointF(500, 250), QPointF(800, 150)]
        self.cables = []
        self.dragging_start = None
        self.current_mouse_pos = None
        self.active_node = None
        self.modulation_depth = 50.0  # Scroll-controlled depth indicator

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0a0f14"))

        # Header / Status labels
        painter.setPen(QPen(QColor("#00ffcc"), 1))
        painter.drawText(20, 25, "CROSS-RESONATOR NETWORK MATRIX")

        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(20, 45, f"Controls: [Right-Click] Add Node | [Left-Click & Drag] Crosswire | [Scroll] Mod Depth: {self.modulation_depth:.1f}%")

        # Draw resonator feedback cables
        painter.setPen(QPen(QColor("#f5d97d"), 2, Qt.PenStyle.SolidLine))
        for start, end in self.cables:
            painter.drawLine(start, end)
        if self.dragging_start and self.current_mouse_pos:
            painter.setPen(QPen(QColor("#00ffcc"), 1.5, Qt.PenStyle.DashLine))
            painter.drawLine(self.dragging_start, self.current_mouse_pos)

        # Draw Nodes
        for i, node in enumerate(self.nodes):
            painter.setBrush(QBrush(QColor("#00ffcc") if i != self.active_node else QColor("#f5d97d")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(node, 12, 12)

            painter.setPen(QPen(QColor("#c9d1d9"), 1))
            painter.drawText(int(node.x()) - 35, int(node.y()) + 28, f"Resonator {i+1}")

    def mousePressEvent(self, event):
        pos = event.position()
        if event.button() == Qt.MouseButton.RightButton:
            self.nodes.append(QPointF(pos.x(), pos.y()))
            self.update()
        elif event.button() == Qt.MouseButton.LeftButton:
            clicked = False
            for i, node in enumerate(self.nodes):
                if (node - pos).manhattanLength() < 15:
                    self.dragging_start = node
                    self.active_node = i
                    clicked = True
                    break
            if not clicked:
                self.dragging_start = pos
            self.current_mouse_pos = pos
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
        """Scroll wheel alters the modulation depth amount with live UI indicator."""
        delta = event.angleDelta().y()
        self.modulation_depth = max(0.0, min(100.0, self.modulation_depth + (2.5 if delta > 0 else -2.5)))
        self.update()


class CrossResonatorPage(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        layout = QVBoxLayout()
        group = QGroupBox("Cross-Resonator Network (Graphical Canvas)")
        group_layout = QVBoxLayout()

        self.canvas = CrossResonatorCanvas(self.engine)
        group_layout.addWidget(self.canvas)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)

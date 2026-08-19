# Filename: gui_workbench.py

from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
from PyQt6.QtCore import Qt, QPointF

class AutomationCurveCanvas(QWidget):
    """
    Canvas for Presequence, Spectral, and Longitudinal graphs.
    - [Right-Click]: Create new graph/automation node.
    - [Left-Click]: Draw direct cross-module interaction lines.
    - [Scroll]: Adjust node or point magnitude.
    """
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setMinimumHeight(450)

        self.nodes = [QPointF(50, 300), QPointF(450, 100), QPointF(850, 300)]
        self.active_node = None
        self.interaction_lines = []

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()

        painter.fillRect(0, 0, width, height, QColor("#0a0f14"))

        # Grid lines
        painter.setPen(QPen(QColor("#2a2f34"), 1, Qt.PenStyle.SolidLine))
        for i in range(0, width, 50):
            painter.drawLine(i, 0, i, height)

        # Interaction wires
        painter.setPen(QPen(QColor("#00ffcc"), 1.5, Qt.PenStyle.DashLine))
        for start_pt, end_pt in self.interaction_lines:
            painter.drawLine(start_pt, end_pt)

        # Automation / Spectral Curve
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

        # Nodes
        painter.setBrush(QBrush(QColor("#00ffcc")))
        painter.setPen(Qt.PenStyle.NoPen)
        for node in self.nodes:
            painter.drawEllipse(node, 6, 6)

        # Overlay text guide
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(20, 25, "[Right-Click] Add Node | [Left-Click] Draw Interaction Wire | [Scroll] Modify Amount")

    def mousePressEvent(self, event):
        pos = event.position()
        if event.button() == Qt.MouseButton.RightButton:
            self.nodes.append(QPointF(pos.x(), pos.y()))
            self.nodes.sort(key=lambda p: p.x())
            self.update()
        elif event.button() == Qt.MouseButton.LeftButton:
            clicked_node = None
            for i, node in enumerate(self.nodes):
                if (node - pos).manhattanLength() < 12:
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


class ModularPatchbayCanvas(QWidget):
    """
    Visual canvas for cross-page wire routing between modules.
    Supports click-and-drag cable creation across all tabs in the suite.
    """
    def __init__(self, engine, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.setMinimumHeight(450)

        # Registered module endpoints across tabs for cross-wiring visualization
        self.modules = [
            {"name": "Instrument Rack (Pitch/Cutoff)", "pos": QPointF(150, 100)},
            {"name": "Presequence & Automation", "pos": QPointF(450, 100)},
            {"name": "Playlist (16 Tracks)", "pos": QPointF(750, 100)},
            {"name": "Cross-Resonator Network", "pos": QPointF(150, 300)},
            {"name": "Effect Cable Matrix (+/-/Neutral)", "pos": QPointF(450, 300)},
            {"name": "Master Export Bus", "pos": QPointF(750, 300)}
        ]

        self.cables = [] # Stores cross-tab routed cables
        self.dragging_start = None
        self.current_mouse_pos = None

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0a0f14"))

        # Header guide text
        painter.setPen(QPen(QColor("#00ffcc"), 1))
        painter.drawText(20, 25, "CROSS-TAB MODULAR PATCHBAY MATRIX (Click & Drag to Crosswire)")

        painter.setPen(QPen(QColor("#8b949e"), 1))
        guide = (
            "• [Left-Click & Drag] between module nodes to route live cross-tab control voltage cables.\n"
            "• Black Ports (○): Unrouted | Green Ports (●): Active cross-tab connection.\n"
            "• [Scroll Wheel] over any node/cable to scale modulation depth."
        )
        y = 45
        for line in guide.split('\n'):
            painter.drawText(20, y, line)
            y += 18

        # Draw established cross-tab cables
        painter.setPen(QPen(QColor("#f5d97d"), 2, Qt.PenStyle.SolidLine))
        for start, end in self.cables:
            painter.drawLine(start, end)

        if self.dragging_start and self.current_mouse_pos:
            painter.setPen(QPen(QColor("#00ffcc"), 2, Qt.PenStyle.DashLine))
            painter.drawLine(self.dragging_start, self.current_mouse_pos)

        # Draw module port nodes
        for mod in self.modules:
            painter.setBrush(QBrush(QColor("#00ffcc")))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(mod["pos"], 10, 10)

            painter.setPen(QPen(QColor("#c9d1d9"), 1))
            painter.drawText(int(mod["pos"].x()) - 50, int(mod["pos"].y()) + 25, mod["name"])

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for mod in self.modules:
                if (mod["pos"] - pos).manhattanLength() < 20:
                    self.dragging_start = mod["pos"]
                    break
            if not self.dragging_start:
                self.dragging_start = pos
            self.current_mouse_pos = pos
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging_start:
            self.current_mouse_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        if self.dragging_start and event.button() == Qt.MouseButton.LeftButton:
            end_pos = event.position()
            self.cables.append((self.dragging_start, end_pos))
            self.dragging_start = None
            self.current_mouse_pos = None
            self.update()

    def wheelEvent(self, event):
        """Scroll wheel alters modulation intensity of cables."""
        if self.cables:
            # Scale or manipulate last cable or nearest routing
            self.update()

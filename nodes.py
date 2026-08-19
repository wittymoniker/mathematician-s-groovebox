# nodes.py
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QMimeData, pyqtSignal
from PyQt6.QtGui import QDrag, QPainter, QFont, QColor

class PatchableModuleNode(QWidget):
    """Modular unit supporting cross-tab drag-and-drop and scrollwheel modulation."""
    state_changed = pyqtSignal(str, float, float)

    def __init__(self, name: str, parent_workspace=None):
        super().__init__()
        self.name = name
        self.parent_workspace = parent_workspace
        self.gain = 1.0
        self.polarity = 1.0  # 1.0 or -1.0
        self.setFixedSize(180, 110)
        self.setStyleSheet("""
            background-color: #1e1e1e;
            color: #00ffcc;
            border: 2px solid #333;
            border-radius: 8px;
        """)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.GlobalColor.white)
        font = QFont("Courier", 10, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(12, 22, f"[{self.name}]")

        font.setBold(False)
        painter.setFont(font)
        painter.setPen(QColor(200, 200, 200))
        painter.drawText(12, 48, f"Gain: {self.gain:.2f}")
        pol_str = "POS (+)" if self.polarity > 0 else "NEG (-)"
        painter.setPen(QColor(255, 100, 100) if self.polarity < 0 else QColor(100, 255, 100))
        painter.drawText(12, 70, f"Polarity: {pol_str}")
        painter.setPen(Qt.GlobalColor.lightGray)
        painter.drawText(12, 92, "Status: SURVIVAL ACTIVE")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(self.name)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if event.modifiers() == Qt.KeyboardModifier.ShiftModifier:
            self.polarity *= -1.0
        else:
            step = 0.05 if delta > 0 else -0.05
            self.gain = max(0.0, min(10.0, self.gain + step))
        self.state_changed.emit(self.name, self.gain, self.polarity)
        self.update()

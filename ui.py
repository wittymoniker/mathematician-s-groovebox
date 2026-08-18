# Filename: ui.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox, QGridLayout, QPushButton
from PyQt6.QtCore import Qt

class BaseModuleView(QWidget):
    """Base template view providing standardized layout frames for suite modules."""
    def __init__(self, title_text, description_text, engine):
        super().__init__()
        self.engine = engine

        layout = QVBoxLayout()
        group = QGroupBox(title_text)
        grid = QGridLayout()

        self.label = QLabel(description_text)
        grid.addWidget(self.label, 0, 0)

        group.setLayout(grid)
        layout.addWidget(group)
        self.setLayout(layout)

# Filename: playlist_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox

class PlaylistPage(QWidget):
    """Playlist and 16-track arrangement workspace."""
    def __init__(self, engine):
        super().__init__()
        self.engine = engine

        layout = QVBoxLayout()
        group = QGroupBox("Playlist (16 Tracks)")
        self.label = QLabel("Manage sequence blocks, automation painting, and arrangement arrangement across 16 tracks.")

        layout.addWidget(self.label)
        group.setLayout(layout)
        self.setLayout(layout)

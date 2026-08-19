# Filename: playlist_page.py

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QGridLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

class PlaylistPage(QWidget):
    """
    16-Track Playlist & Arranger Matrix workspace enabling pattern sequencing,
    bar layout management, and song structure arrangement.
    """
    def __init__(self, engine, max_tracks=16, max_bars=32):
        super().__init__()
        self.engine = engine
        self.max_tracks = max_tracks
        self.max_bars = max_bars

        layout = QVBoxLayout()
        group = QGroupBox(f"16-Track Playlist & Arranger Grid ({max_tracks} Tracks x {max_bars} Bars)")
        group_layout = QVBoxLayout()

        # Toolbar controls
        toolbar = QHBoxLayout()
        self.clear_btn = QPushButton("Clear Arrangement Grid")
        self.clear_btn.setStyleSheet("background-color: #21262d; color: #f85149; border: 1px solid #30363d; font-weight: bold; padding: 6px 12px;")
        self.clear_btn.clicked.connect(self._clear_grid)
        toolbar.addWidget(self.clear_btn)

        self.render_btn = QPushButton("Render Playlist Stems")
        self.render_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; border: 1px solid #00ffcc; font-weight: bold; padding: 6px 12px;")
        self.render_btn.clicked.connect(self._render_playlist)
        toolbar.addWidget(self.render_btn)

        toolbar.addStretch()
        group_layout.addLayout(toolbar)

        # Scrollable grid of track lanes and bar buttons
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        container = QWidget()
        grid = QGridLayout(container)
        grid.setContentsMargins(4, 4, 4, 4)
        grid.setSpacing(2)

        # Header labels for bars (every 4 bars highlighted)
        grid.addWidget(QLabel("Track \\ Bar"), 0, 0)
        for b in range(self.max_bars):
            lbl = QLabel(str(b + 1))
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #8b949e; font-size: 10px; font-weight: bold;")
            grid.addWidget(lbl, 0, b + 1)

        # Track rows & step/pattern toggles
        self.track_buttons = {}
        for t in range(self.max_tracks):
            track_lbl = QLabel(f"Trk {t+1:2d}")
            track_lbl.setStyleSheet("color: #c9d1d9; font-weight: bold; font-family: monospace; font-size: 11px;")
            grid.addWidget(track_lbl, t + 1, 0)

            for b in range(self.max_bars):
                btn = QPushButton(".")
                btn.setFixedSize(28, 28)
                btn.setCheckable(True)
                btn.setStyleSheet("""
                    QPushButton {
                        background-color: #161b22;
                        color: #484f58;
                        border: 1px solid #21262d;
                        font-family: monospace;
                        font-weight: bold;
                        font-size: 11px;
                        border-radius: 2px;
                    }
                    QPushButton:checked {
                        background-color: #00ffcc;
                        color: #0d1117;
                        border: 1px solid #ffffff;
                    }
                """)
                btn.clicked.connect(lambda checked, trk=t, bar=b: self._toggle_pattern(trk, bar))
                grid.addWidget(btn, t + 1, b + 1)
                self.track_buttons[(t, b)] = btn

        container.setLayout(grid)
        scroll_area.setWidget(container)
        group_layout.addWidget(scroll_area)

        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)

    def _toggle_pattern(self, track_idx, bar_idx):
        btn = self.track_buttons[(track_idx, bar_idx)]
        if btn.isChecked():
            btn.setText("1")
            self.engine.playlist_manager.assign_pattern(track_idx, bar_idx, 1)
        else:
            btn.setText(".")
            self.engine.playlist_manager.remove_pattern(track_idx, bar_idx)

    def _clear_grid(self):
        for (t, b), btn in self.track_buttons.items():
            btn.setChecked(False)
            btn.setText(".")
            self.engine.playlist_manager.remove_pattern(t, b)

    def _render_playlist(self):
        print("Rendering active 16-track playlist arrangement through EQR audio backend...")
        self.engine.playlist_manager.render_playlist_view()

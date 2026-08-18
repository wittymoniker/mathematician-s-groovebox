# Filename: main_gui.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget
from PyQt6.QtCore import QTimer

from synth_engine import ModularSynthEngine
from main import GeneratorPage, ModularPanePage
from sequencer_automation_page import PresequenceAutomationPage
from playlist_page import PlaylistPage
from cross_resonator_page import CrossResonatorPage
from effect_matrix_page import EffectMatrixPage
from master_export_page import MasterExportPage

class SuiteMainWindow(QMainWindow):
    """Main application window uniting all tabs and pages for the V9 Suite with full dark styling."""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ESKIBRUTUS & FRIENDS IN DEATH MAGIC: V9 SUITE")
        self.resize(1280, 800)

        # Apply Global Dark Theme Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0a0f14;
            }
            QTabWidget::pane {
                border: 1px solid #2a2f34;
                background-color: #0a0f14;
            }
            QTabBar::tab {
                background-color: #161b22;
                color: #8b949e;
                padding: 10px 15px;
                border: 1px solid #2a2f34;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #1f242c;
                color: #00ffcc;
                border-bottom-color: #1f242c;
            }
            QTabBar::tab:hover {
                background-color: #1f242c;
                color: #f5d97d;
            }
            QGroupBox {
                color: #f5d97d;
                font-weight: bold;
                border: 1px solid #30363d;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #0d1117;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QLabel {
                color: #c9d1d9;
            }
            QPushButton {
                background-color: #21262d;
                color: #c9d1d9;
                border: 1px solid #30363d;
                border-radius: 4px;
                padding: 6px 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #30363d;
                color: #00ffcc;
                border-color: #8b949e;
            }
        """)

        # Initialize Core Engine
        self.engine = ModularSynthEngine()

        # Central Tab Widget containing all suite pages
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        # Initialize and add all module tabs matching your suite layout
        self.generator_page = GeneratorPage(self.engine)
        self.presequence_page = PresequenceAutomationPage(self.engine)
        self.playlist_page = PlaylistPage(self.engine)
        self.modular_pane = ModularPanePage(self.engine)
        self.cross_resonator_page = CrossResonatorPage(self.engine)
        self.effect_matrix_page = EffectMatrixPage(self.engine)
        self.master_export_page = MasterExportPage(self.engine)

        self.tabs.addTab(self.generator_page, "Instrument Rack & Equations")
        self.tabs.addTab(self.presequence_page, "Presequence & Automations")
        self.tabs.addTab(self.playlist_page, "Playlist (16 Tracks)")
        self.tabs.addTab(self.modular_pane, "Modular Patchbay (Click & Drag)")
        self.tabs.addTab(self.cross_resonator_page, "Cross-Resonator Network (Graphical)")
        self.tabs.addTab(self.effect_matrix_page, "Effect Cable Matrix (+/-/Neutral)")
        self.tabs.addTab(self.master_export_page, "Master Export")

        # Real-time processing timer tick
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_engine_tick)
        self.timer.start(30)

    def update_engine_tick(self):
        x_val = self.generator_page.knob_pitch.current_val / 1000.0
        y_val = self.generator_page.knob_cutoff.current_val / 5000.0
        z_val = self.generator_page.knob_width.current_val

        self.engine.process_frame(x=x_val, y=y_val, z=z_val)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SuiteMainWindow()
    window.show()
    sys.exit(app.exec())

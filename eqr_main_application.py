# Filename: eqr_main_application.py

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QMessageBox
from PyQt6.QtGui import QIcon, QColor, QPalette
from PyQt6.QtCore import Qt

# Import all custom modular pages and hubs
from sequencer_automation_page import PresequenceAutomationPage
from master_sequencer_hub import EQRComprehensiveMasterHub
from eqr_audio_bus_mixer import MasterAudioBusMixerPage
from eqr_preset_morph_matrix import PresetMorphMatrixPage
from eqr_spectral_diffuser import SpectralDiffuserPage
from eqr_quantum_phase_shifter import QuantumPhaseShifterPage
from eqr_stochastic_resonator import StochasticResonatorPage

class EQRMainApplicationWindow(QMainWindow):
    """
    The central PyQt6 MainWindow for the Equation of Reality (EQR) modular synthesis ecosystem,
    unifying all sequencer lanes, patchable matrix hubs, and transcendental hardware modules.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Modular Synthesis & Hardware Hub")
        self.resize(1400, 900)

        # Apply dark architectural theme
        self.set_dark_palette()

        # Mock engine reference for parameter routing
        self.engine = {"status": "active", "sample_rate": 44100, "tuning": 432.0}

        # Central Tab Widget housing all subsystems
        self.tabs = QTabWidget()
        self.tabs.setTabPosition(QTabWidget.TabPosition.North)
        self.tabs.setDocumentMode(True)

        # Instantiate and add pages
        self.sequencer_page = PresequenceAutomationPage(self.engine)
        self.master_hub_page = EQRComprehensiveMasterHub(self.engine)
        self.audio_bus_page = MasterAudioBusMixerPage(self.engine)
        self.morph_matrix_page = PresetMorphMatrixPage(self.engine)
        self.spectral_diff_page = SpectralDiffuserPage(self.engine)
        self.quantum_phase_page = QuantumPhaseShifterPage(self.engine)
        self.stochastic_page = StochasticResonatorPage(self.engine)

        self.tabs.addTab(self.sequencer_page, "Sequencer & Automation")
        self.tabs.addTab(self.master_hub_page, "Master Hub (34 Constants)")
        self.tabs.addTab(self.audio_bus_page, "Audio Bus Mixer")
        self.tabs.addTab(self.morph_matrix_page, "Preset Morph Matrix")
        self.tabs.addTab(self.spectral_diff_page, "Spectral Diffuser")
        self.tabs.addTab(self.quantum_phase_page, "Quantum Phase Shifter")
        self.tabs.addTab(self.stochastic_page, "Stochastic Resonator")

        self.setCentralWidget(self.tabs)

        # Status Bar
        self.statusBar().showMessage("EQR Engine Online | 432Hz Reference | Meum Ratio Locked | All Systems Nominal")

    def set_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#0d1117"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#161b22"))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#0d1117"))
        palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#21262d"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.BrightText, QColor("#00ffcc"))
        palette.setColor(QPalette.ColorRole.Link, QColor("#58a6ff"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#1f6feb"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        QApplication.setPalette(palette)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EQRMainApplicationWindow()
    window.show()
    sys.exit(app.exec())

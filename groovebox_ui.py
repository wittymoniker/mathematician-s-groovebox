# groovebox_ui.py
import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTabWidget, QSplitter, QTextEdit,
    QGridLayout, QGroupBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from math_engine import EQRMathEngine
from nodes import PatchableModuleNode

class EQRGrooveboxCompleteSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("EQR Groovebox Engine - Updated Suite")
        self.resize(1600, 1000)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        self.build_top_toolbar()

        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.main_layout.addWidget(self.splitter)

        self.tabs = QTabWidget()
        self.splitter.addWidget(self.tabs)

        self.init_synthesizer_matrix_tab()
        self.init_eqr_processor_tab()
        self.init_timeline_playlist_tab()

        self.build_sidebar_inspector()
        self.build_control_deck()
        self.active_modules_count = 3

    def build_top_toolbar(self):
        toolbar_layout = QHBoxLayout()
        title = QLabel("<b>EQR GROOVEBOX ENGINE // RUNTIME</b>")
        title.setStyleSheet("color: #00ffcc; font-size: 14px;")
        toolbar_layout.addWidget(title)
        toolbar_layout.addStretch()

        self.sys_status = QLabel("Mode: Survival Active | Engine: Synchronized")
        self.sys_status.setStyleSheet("color: #88ff88; font-weight: bold;")
        toolbar_layout.addWidget(self.sys_status)
        self.main_layout.addLayout(toolbar_layout)

    def init_synthesizer_matrix_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        grid = QGridLayout()

        self.node_master = PatchableModuleNode("Master Oscillator", self)
        self.node_filter = PatchableModuleNode("Resonant Filter", self)

        grid.addWidget(self.node_master, 0, 0)
        grid.addWidget(self.node_filter, 0, 1)
        layout.addLayout(grid)
        layout.addStretch()
        self.tabs.addTab(tab, "Synthesizer Matrix")

    def init_eqr_processor_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)

        self.node_processor = PatchableModuleNode("EQR Flux Node", self)
        layout.addWidget(self.node_processor)

        coord_group = QGroupBox("Coordinate Vector Controls (x, y, z)")
        coord_layout = QGridLayout()

        self.spin_x = QDoubleSpinBox()
        self.spin_y = QDoubleSpinBox()
        self.spin_z = QDoubleSpinBox()

        for s in [self.spin_x, self.spin_y, self.spin_z]:
            s.setRange(-500.0, 500.0)
            s.setValue(1.0)
            s.setSingleStep(0.1)

        coord_layout.addWidget(QLabel("Variable X:"), 0, 0)
        coord_layout.addWidget(self.spin_x, 0, 1)
        coord_layout.addWidget(QLabel("Variable Y:"), 1, 0)
        coord_layout.addWidget(self.spin_y, 1, 1)
        coord_layout.addWidget(QLabel("Variable Z:"), 2, 0)
        coord_layout.addWidget(self.spin_z, 2, 1)

        coord_group.setLayout(coord_layout)
        layout.addWidget(coord_group)

        self.eval_btn = QPushButton("Evaluate Reality Tensor Matrix")
        self.eval_btn.clicked.connect(self.run_tensor_evaluation)
        layout.addWidget(self.eval_btn)

        layout.addStretch()
        self.tabs.addTab(tab, "EQR Processor")

    def init_timeline_playlist_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        self.timeline_log = QTextEdit()
        self.timeline_log.setReadOnly(True)
        self.timeline_log.setText("--- Infinite Playlist Timeline Initialized ---")
        layout.addWidget(self.timeline_log)
        self.tabs.addTab(tab, "Timeline & Playlist")

    def build_sidebar_inspector(self):
        sidebar = QWidget()
        layout = QVBoxLayout(sidebar)
        title = QLabel("<b>Telemetry Inspector</b>")
        layout.addWidget(title)

        self.inspector_text = QTextEdit()
        self.inspector_text.setReadOnly(True)
        self.inspector_text.setText("System telemetry active.")
        layout.addWidget(sidebar)
        self.splitter.addWidget(sidebar)

    def build_control_deck(self):
        deck_layout = QHBoxLayout()
        spawn_btn = QPushButton("Spawn Modular Unit")
        spawn_btn.clicked.connect(self.spawn_new_module)
        deck_layout.addWidget(spawn_btn)
        self.main_layout.addLayout(deck_layout)

    def spawn_new_module(self):
        self.active_modules_count += 1
        name = f"Dynamic Node {self.active_modules_count}"
        new_node = PatchableModuleNode(name, self)
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.addWidget(new_node)
        self.tabs.addTab(tab, f"Module {self.active_modules_count}")

    def run_tensor_evaluation(self):
        x = self.spin_x.value()
        y = self.spin_y.value()
        z = self.spin_z.value()
        result = EQRMathEngine.evaluate_coordinates(x, y, z)
        self.sys_status.setText(f"Tensor Evaluated: {result:.6f}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    suite = EQRGrooveboxCompleteSuite()
    suite.show()
    sys.exit(app.exec())

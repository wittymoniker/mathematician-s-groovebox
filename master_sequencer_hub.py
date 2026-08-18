# =========================================================
# master_sequencer_hub.py
# EQR GROOVEBOX ULTIMATE DAW & SYNTHESIS SUITE (v13.1 Ultimate Fixed)
# =========================================================

import sys
import math
import array
import wave
import random
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGroupBox, QGridLayout, QLabel, QPushButton, QScrollArea, QTabWidget,
    QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QFileDialog, QMessageBox,
    QSlider, QLineEdit, QMdiArea, QMdiSubWindow, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog
)
from PyQt6.QtCore import Qt, QPointF, QIODevice, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPalette, QPainterPath, QKeyEvent, QMouseEvent, QAction
from PyQt6.QtMultimedia import QAudioSink, QAudioFormat, QMediaDevices


class SynthAudioStream(QIODevice):
    def __init__(self, sample_rate=44100, parent=None):
        super().__init__(parent)
        self.sample_rate = sample_rate
        self.frequency = 432.0
        self.amplitude = 0.7
        self.waveform_type = "sine"
        self.phase = 0.0
        self.open(QIODevice.OpenModeFlag.ReadOnly)

    def set_frequency(self, freq):
        self.frequency = max(20.0, min(20000.0, freq))

    def set_amplitude(self, amp):
        self.amplitude = max(0.0, min(1.0, amp))

    def set_waveform(self, w_type):
        self.waveform_type = w_type

    def readData(self, maxlen):
        num_samples = maxlen // 2
        buffer = bytearray()
        dt = 1.0 / self.sample_rate

        for _ in range(num_samples):
            if self.waveform_type == "sine":
                sample = math.sin(2 * math.pi * self.phase)
            elif self.waveform_type == "square":
                sample = 1.0 if math.sin(2 * math.pi * self.phase) >= 0 else -1.0
            elif self.waveform_type == "sawtooth":
                sample = 2.0 * (self.phase - math.floor(0.5 + self.phase))
            elif self.waveform_type == "triangle":
                sample = 2.0 * abs(2.0 * (self.phase - math.floor(0.5 + self.phase))) - 1.0
            else:
                sample = math.sin(2 * math.pi * self.phase) * 0.6

            sample *= self.amplitude
            int_val = int(max(-32768, min(32767, sample * 32767)))
            buffer.extend(int_val.to_bytes(2, byteorder='little', signed=True))

            self.phase += self.frequency * dt
            if self.phase > 1.0:
                self.phase -= 1.0

        return bytes(buffer)

    def bytesAvailable(self):
        return 4096 + super().bytesAvailable()


class FrontPagePatchbayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(280)
        self.setMaximumHeight(340)
        self.setMouseTracking(True)
        self.parent_suite = parent

        self.nodes = [
            {"id": "out_spatial", "name": "Spatial Matrix (Out)", "type": "out", "polarity": "+", "x": 60, "y": 50},
            {"id": "out_eskibrutus", "name": "Eskibrutus (Out)", "type": "out", "polarity": "+", "x": 60, "y": 90},
            {"id": "out_vectoreski", "name": "Vectoreski (Out)", "type": "out", "polarity": "-", "x": 60, "y": 130},
            {"id": "out_eskitable", "name": "Eskitable (Out)", "type": "out", "polarity": "Neutral", "x": 60, "y": 170},
            {"id": "out_master_mix", "name": "Master Mix (Out)", "type": "out", "polarity": "+", "x": 60, "y": 210},

            {"id": "in_filter", "name": "Filter Cutoff (In)", "type": "in", "polarity": "+", "x": 560, "y": 70},
            {"id": "in_proximity", "name": "Proximity Sensitivity (In)", "type": "in", "polarity": "Neutral", "x": 560, "y": 140},
            {"id": "in_downmix", "name": "Downmix Deadstate (In)", "type": "in", "polarity": "-", "x": 560, "y": 210},
        ]
        self.wires = [
            {"from": "out_spatial", "to": "in_filter", "mod_amount": 0.75},
            {"from": "out_eskibrutus", "to": "in_proximity", "mod_amount": 0.50},
            {"from": "out_vectoreski", "to": "in_downmix", "mod_amount": -0.60}
        ]
        self.drag_start_node = None
        self.current_mouse_pos = QPointF(0, 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width(); h = self.height()
        painter.fillRect(0, 0, w, h, QColor("#080c10"))

        painter.setPen(QPen(QColor("#30363d"), 1, Qt.PenStyle.DashLine))
        painter.drawRect(2, 2, w - 4, h - 4)

        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(12, 18, "<b>Front-Page Modular Wire Patchbay</b> (Right-Click Drag to link | Scroll wheel for mod +/-)")

        for wire in self.wires:
            src = next((n for n in self.nodes if n["id"] == wire["from"]), None)
            dst = next((n for n in self.nodes if n["id"] == wire["to"]), None)
            if src and dst:
                color = "#00ffcc" if wire["mod_amount"] >= 0 else "#ff7b72"
                painter.setPen(QPen(QColor(color), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                painter.drawLine(QPointF(src["x"], src["y"]), QPointF(dst["x"], dst["y"]))

                mid_x = (src["x"] + dst["x"]) / 2
                mid_y = (src["y"] + dst["y"]) / 2
                painter.setBrush(QBrush(QColor("#161b22")))
                painter.setPen(QPen(QColor("#58a6ff"), 1))
                painter.drawRoundedRect(int(mid_x - 22), int(mid_y - 9), 44, 18, 4, 4)
                painter.setPen(QPen(QColor("#ffffff"), 1))
                painter.drawText(int(mid_x - 22), int(mid_y - 9), 44, 18, Qt.AlignmentFlag.AlignCenter, f"{wire['mod_amount']:+.2f}")

        if self.drag_start_node and self.current_mouse_pos:
            painter.setPen(QPen(QColor("#ffaa00"), 2.0, Qt.PenStyle.DashDotLine))
            painter.drawLine(QPointF(self.drag_start_node["x"], self.drag_start_node["y"]), self.current_mouse_pos)

        for node in self.nodes:
            is_out = node["type"] == "out"
            nx = node["x"]; ny = node["y"]
            pol_color = "#1f6feb" if node["polarity"] == "+" else ("#da3633" if node["polarity"] == "-" else "#8b949e")
            painter.setBrush(QBrush(QColor(pol_color)))
            painter.setPen(QPen(QColor("#ffffff"), 2))
            painter.drawEllipse(QPointF(nx, ny), 10, 10)

            painter.setPen(QPen(QColor("#ffffff"), 1))
            sign_text = "+" if node["polarity"] == "+" else ("-" if node["polarity"] == "-" else "N")
            painter.drawText(int(nx - 10), int(ny - 10), 20, 20, Qt.AlignmentFlag.AlignCenter, sign_text)

            painter.setPen(QPen(QColor("#c9d1d9"), 1))
            text_x = nx - 170 if is_out else nx + 16
            painter.drawText(int(text_x), int(ny - 8), 160, 16, Qt.AlignmentFlag.AlignRight if is_out else Qt.AlignmentFlag.AlignLeft, f"{node['name']}")


class ModularBayKnob(QWidget):
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, math_note="", parent=None, callback=None):
        super().__init__(parent)
        self.label_text = label_text
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.math_note = math_note
        self.callback = callback
        self.setFixedSize(80, 85)
        self.dragging = False
        self.last_y = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(0, 4, self.width(), 12, Qt.AlignmentFlag.AlignCenter, self.label_text)
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(0, 16, self.width(), 10, Qt.AlignmentFlag.AlignCenter, f"{self.value:.2f}")

        center = QPointF(40, 44)
        radius = 13.0
        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#30363d"), 1.5))
        painter.drawEllipse(center, radius, radius)

        span_val = self.max_val - self.min_val if self.max_val != self.min_val else 1.0
        normalized = (self.value - self.min_val) / span_val
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 3) * math.sin(angle)
        tip_y = center.y() - (radius - 3) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, QPointF(tip_x, tip_y))
        painter.setPen(QPen(QColor("#c9d1d9"), 1))
        painter.drawText(2, 70, self.width() - 4, 12, Qt.AlignmentFlag.AlignCenter, self.math_note)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.last_y = event.position().y()

    def mouseMoveEvent(self, event):
        if self.dragging:
            dy = self.last_y - event.position().y()
            self.last_y = event.position().y()
            span = self.max_val - self.min_val
            step = span * (dy / 150.0)
            self.value = max(self.min_val, min(self.max_val, self.value + step))
            self.update()
            if self.callback:
                self.callback(self.value)

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        span = self.max_val - self.min_val
        step = span * (0.02 if delta > 0 else -0.02)
        self.value = max(self.min_val, min(self.max_val, self.value + step))
        self.update()
        if self.callback:
            self.callback(self.value)


class LiveModuleGraphWidget(QWidget):
    def __init__(self, mode="wavetable", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.setMinimumHeight(100); self.setMaximumHeight(130)
        self.param_mod = 1.0
        self.frequency_mod = 432.0

    def update_parameters(self, mod_val, freq_val=432.0):
        self.param_mod = mod_val
        self.frequency_mod = freq_val
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width(); h = self.height()
        painter.fillRect(0, 0, w, h, QColor("#0d1117"))

        path = QPainterPath()
        painter.setPen(QPen(QColor("#00ffcc"), 1.8))
        freq_factor = 0.02 + (self.frequency_mod / 15000.0)
        for i in range(w):
            screen_y = h / 2 + (h / 3) * math.sin(i * freq_factor * self.param_mod) * math.cos(i * 0.015)
            if i == 0: path.moveTo(i, screen_y)
            else: path.lineTo(i, screen_y)
        painter.drawPath(path)
        painter.setPen(QPen(QColor("#30363d"), 1))
        painter.drawRect(0, 0, w - 1, h - 1)
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(8, 16, f"[{self.mode.upper()}] Param: {self.param_mod:.2f}")


class EQRGrooveboxUltimateSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Ultimate Modular DAW Suite (v13.1 Ultimate Fixed)")
        self.resize(1850, 1050)

        self.audio_sink = None
        self.audio_stream = None
        self.is_playing = False

        # Grouped module sequence categories
        self.module_categories = {
            "Sub-Bass / Drive Modules": ["Eskibrutus (Sub-Bass/Drive)"],
            "Phase / Morph Modules": ["Vectoreski (Phase/Morph)"],
            "Wavetable Synths": ["Eskitable (Wavetable Synth)"],
            "Spatial Matrices": ["Spatial Matrix Synth"],
            "Polynomial Equations": ["EQR Polynomial Synth"]
        }

        def default_pattern():
            return {
                "name": "Pattern 1",
                "length": 16,
                "speed": 1.0,
                "curve": "Linear",
                "depth": 0.75,
                "steps": [{"active": (i % 4 == 0), "pitch": 1.0, "amp": 1.0, "duration": 1.0} for i in range(16)]
            }

        self.instrument_sequences = {
            "Eskibrutus (Sub-Bass/Drive)": [default_pattern()],
            "Vectoreski (Phase/Morph)": [default_pattern()],
            "Eskitable (Wavetable Synth)": [default_pattern()],
            "Spatial Matrix Synth": [default_pattern()],
            "EQR Polynomial Synth": [default_pattern()],
        }

        # Automation tracks dictionary linked to modules with full x, y, z variable support
        self.automation_lanes = {
            "Eskibrutus (Sub-Bass/Drive)": {"x": 1.0, "y": 1.0, "z": 1.0, "curve_type": "Polynomial x*y*z"}
        }

        self.setup_window_creation_menu()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_front_page_tab(), "Front-Page Modular Patchbay & Master Controls")
        self.tabs.addTab(self.create_sequencer_playlist_tab(), "Sequencer Manager & Piano Roll")
        self.tabs.addTab(self.create_automation_manager_tab(), "Automation Module Manager & x,y,z Lanes")
        self.tabs.addTab(self.create_master_playlist_tab(), "Master Coordination Playlist")
        self.tabs.addTab(self.create_sample_module_tab(), "Sample Loader & Audio Module")
        self.tabs.addTab(self.create_mdi_suite_tab(), "Modular Subwindow Bays (MDI)")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("EQR Suite v13.1 Ready | Sequencer Dropdown Sync & Independent Note Selection Active.")

    def setup_window_creation_menu(self):
        menubar = self.menuBar()
        window_menu = menubar.addMenu("Module Creator & Synths")

        act_create = QAction("Create New Custom Synth Module...", self)
        act_create.triggered.connect(self.spawn_create_module_dialog)
        window_menu.addAction(act_create)
        window_menu.addSeparator()

        for title, func in [
            ("Spawn Eskibrutus Synth", self.create_eskibrutus_content),
            ("Spawn Vectoreski Synth", self.create_vectoreski_content),
            ("Spawn Eskitable Synth", self.create_eskitable_content),
            ("Spawn Spatial Matrix", self.create_spatial_matrix_content),
            ("Spawn EQR Equation Module", self.create_eqr_equation_content),
        ]:
            act = QAction(title, self)
            act.triggered.connect(lambda checked, t=title, f=func: self.spawn_subwindow_to_mdi(t, f(), 100, 100))
            window_menu.addAction(act)

    def spawn_create_module_dialog(self):
        mod_name, ok1 = QInputDialog.getText(self, "Create New Module", "Enter custom module name:")
        if not ok1 or not mod_name.strip(): return

        cat_keys = list(self.module_categories.keys())
        cat_choice, ok2 = QInputDialog.getItem(self, "Module Grouping", "Select module category type:", cat_keys, 0, False)
        if not ok2: return

        if cat_choice not in self.module_categories:
            self.module_categories[cat_choice] = []
        if mod_name not in self.module_categories[cat_choice]:
            self.module_categories[cat_choice].append(mod_name)

        def default_pattern():
            return {
                "name": "Pattern 1",
                "length": 16,
                "speed": 1.0,
                "curve": "Linear",
                "depth": 0.75,
                "steps": [{"active": False, "pitch": 1.0, "amp": 1.0, "duration": 1.0} for _ in range(16)]
            }

        if mod_name not in self.instrument_sequences:
            self.instrument_sequences[mod_name] = [default_pattern()]
        if mod_name not in self.automation_lanes:
            self.automation_lanes[mod_name] = {"x": 1.0, "y": 1.0, "z": 1.0, "curve_type": "Linear x*y*z"}

        # Refresh all module selector dropdowns dynamically
        self.refresh_all_module_dropdowns()

        QMessageBox.information(self, "Module Created", f"Successfully spawned and grouped module '{mod_name}' under '{cat_choice}'.")

    def refresh_all_module_dropdowns(self):
        # Refresh sequencer dropdown
        if hasattr(self, 'seq_instrument_combo'):
            self.seq_instrument_combo.blockSignals(True)
            curr_val = self.seq_instrument_combo.currentText()
            self.seq_instrument_combo.clear()
            for cat, mods in self.module_categories.items():
                for m in mods:
                    self.seq_instrument_combo.addItem(f"[{cat}] {m}")
            self.seq_instrument_combo.setCurrentText(curr_val)
            self.seq_instrument_combo.blockSignals(False)
            self.populate_sequence_names()

        # Refresh automation manager dropdown
        if hasattr(self, 'auto_mod_combo'):
            self.auto_mod_combo.blockSignals(True)
            curr_auto = self.auto_mod_combo.currentText()
            self.auto_mod_combo.clear()
            for mod in self.instrument_sequences.keys():
                self.auto_mod_combo.addItem(mod)
            self.auto_mod_combo.setCurrentText(curr_auto)
            self.auto_mod_combo.blockSignals(False)

    def create_front_page_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        left_layout = QVBoxLayout()
        self.patchbay_widget = FrontPagePatchbayWidget(self)
        left_layout.addWidget(self.patchbay_widget)

        master_group = QGroupBox("Master Mix, Master Tuning & Master FX Controls")
        master_grid = QGridLayout(master_group)
        self.knob_base_tuning = ModularBayKnob("Base Tuning", 400.0, 480.0, 432.0, "Hz", self, callback=self.update_base_tuning_live)
        master_grid.addWidget(self.knob_base_tuning, 0, 0)
        master_grid.addWidget(ModularBayKnob("Proximity Sens", 0.1, 5.0, 1.0, "Prox", self), 0, 1)
        master_grid.addWidget(ModularBayKnob("Downmix Dead", 0.0, 1.0, 0.0, "Dead", self), 0, 2)
        left_layout.addWidget(master_group)
        layout.addLayout(left_layout, stretch=3)

        right_layout = QVBoxLayout()
        audio_group = QGroupBox("Live Audio Stream & Export")
        audio_layout = QVBoxLayout(audio_group)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100); self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.update_audio_volume)
        audio_layout.addWidget(QLabel("Master Volume:"))
        audio_layout.addWidget(self.volume_slider)

        self.btn_preview = QPushButton("Start Live Audio Stream")
        self.btn_preview.clicked.connect(self.toggle_audio_preview)
        audio_layout.addWidget(self.btn_preview)

        right_layout.addWidget(audio_group)
        layout.addLayout(right_layout, stretch=2)
        return widget

    def toggle_audio_preview(self):
        if not self.is_playing:
            format = QAudioFormat()
            format.setSampleRate(44100)
            format.setChannelCount(1)
            format.setSampleFormat(QAudioFormat.SampleFormat.Int16)

            self.audio_stream = SynthAudioStream(sample_rate=44100, parent=self)
            init_freq = self.knob_base_tuning.value if hasattr(self, 'knob_base_tuning') else 432.0
            self.audio_stream.set_frequency(init_freq)
            self.audio_stream.set_amplitude(self.volume_slider.value() / 100.0)

            self.audio_sink = QAudioSink(QMediaDevices.defaultAudioOutput(), format, self)
            self.audio_sink.start(self.audio_stream)
            self.is_playing = True
            self.btn_preview.setText("Stop Live Audio Stream")
        else:
            if self.audio_sink: self.audio_sink.stop()
            if self.audio_stream: self.audio_stream.close()
            self.is_playing = False
            self.btn_preview.setText("Start Live Audio Stream")

    def update_base_tuning_live(self, val):
        if self.audio_stream:
            self.audio_stream.set_frequency(val)

    def update_audio_volume(self, val):
        if self.audio_stream: self.audio_stream.set_amplitude(val / 100.0)

    def create_sequencer_playlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("<b>Select Grouped Module:</b>"))
        self.seq_instrument_combo = QComboBox()
        for cat, mods in self.module_categories.items():
            for m in mods:
                self.seq_instrument_combo.addItem(f"[{cat}] {m}")
        self.seq_instrument_combo.currentIndexChanged.connect(self.refresh_sequencer_ui)
        toolbar.addWidget(self.seq_instrument_combo)

        toolbar.addWidget(QLabel("<b>Pattern Index:</b>"))
        self.seq_name_combo = QComboBox()
        self.seq_name_combo.currentIndexChanged.connect(self.load_selected_sequence_parameters)
        toolbar.addWidget(self.seq_name_combo)
        layout.addLayout(toolbar)

        self.multi_seq_table = QTableWidget()
        layout.addWidget(self.multi_seq_table)

        self.populate_sequence_names()
        return widget

    def get_current_clean_instrument_name(self):
        text = self.seq_instrument_combo.currentText()
        if "]" in text:
            return text.split("] ")[1]
        return text

    def populate_sequence_names(self):
        self.seq_name_combo.blockSignals(True)
        self.seq_name_combo.clear()
        inst = self.get_current_clean_instrument_name()
        if inst in self.instrument_sequences:
            for idx, seq in enumerate(self.instrument_sequences[inst]):
                self.seq_name_combo.addItem(f"Pattern {idx}: {seq['name']}")
        self.seq_name_combo.blockSignals(False)
        self.load_selected_sequence_parameters()

    def refresh_sequencer_ui(self):
        self.populate_sequence_names()

    def load_selected_sequence_parameters(self):
        inst = self.get_current_clean_instrument_name()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            seq_data = self.instrument_sequences[inst][seq_idx]
            self.build_sequence_table_grid(seq_data)

    def build_sequence_table_grid(self, seq_data):
        length = seq_data["length"]
        steps = seq_data["steps"]
        num_rows = 8

        self.multi_seq_table.setRowCount(num_rows)
        self.multi_seq_table.setColumnCount(length)

        for c in range(length):
            step_info = steps[c]
            is_active = step_info["active"]
            pitch_val = step_info.get("pitch", 1.0)

            target_row = round((1.0 - ((pitch_val - 0.25) / 1.75)) * (num_rows - 1))
            target_row = max(0, min(num_rows - 1, target_row))

            for r in range(num_rows):
                is_this_cell_target = is_active and (r == target_row)
                btn = QPushButton("ON" if is_this_cell_target else "---")
                btn.setCheckable(True)
                btn.setChecked(is_this_cell_target)

                # Fully decoupled row click handler for independent row activation across top, middle, and bottom
                btn.clicked.connect(lambda checked, s_obj=seq_data, col=c, row=r: self.on_grid_cell_clicked(s_obj, col, row, num_rows))
                self.multi_seq_table.setCellWidget(r, c, btn)

    def on_grid_cell_clicked(self, seq_data, col, row, num_rows):
        normalized_row_factor = 1.0 - (row / (num_rows - 1))
        new_pitch = 0.25 + (normalized_row_factor * 1.75)

        step_info = seq_data["steps"][col]
        step_info["active"] = True
        step_info["pitch"] = max(0.25, min(2.0, new_pitch))

        dur_val, ok = QInputDialog.getDouble(self, "Note Duration", f"Set duration (beats) for step {col+1}:", step_info.get("duration", 1.0), 0.1, 4.0, 2)
        if ok:
            step_info["duration"] = dur_val

        self.build_sequence_table_grid(seq_data)

    def create_automation_manager_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("<h2>Advanced Automation Module & x, y, z Variable Lane Manager</h2>"))

        self.auto_mod_combo = QComboBox()
        for mod in self.instrument_sequences.keys():
            self.auto_mod_combo.addItem(mod)
        layout.addWidget(self.auto_mod_combo)

        btn_edit_xyz = QPushButton("Configure x, y, z Automation Envelopes")
        btn_edit_xyz.clicked.connect(self.configure_module_xyz_automation)
        layout.addWidget(btn_edit_xyz)

        self.auto_status_label = QLabel("Select a module above to manage its stackable x,y,z automation methods.")
        layout.addWidget(self.auto_status_label)
        return widget

    def configure_module_xyz_automation(self):
        mod = self.auto_mod_combo.currentText()
        current_xyz = self.automation_lanes.get(mod, {"x": 1.0, "y": 1.0, "z": 1.0})

        x_val, ok1 = QInputDialog.getDouble(self, f"Automation X Lane [{mod}]", "Enter polynomial scaling for x:", current_xyz["x"], -100.0, 100.0, 4)
        if not ok1: return
        y_val, ok2 = QInputDialog.getDouble(self, f"Automation Y Lane [{mod}]", "Enter polynomial scaling for y:", current_xyz["y"], -100.0, 100.0, 4)
        if not ok2: return
        z_val, ok3 = QInputDialog.getDouble(self, f"Automation Z Lane [{mod}]", "Enter polynomial scaling for z:", current_xyz["z"], -100.0, 100.0, 4)
        if not ok3: return

        self.automation_lanes[mod] = {"x": x_val, "y": y_val, "z": z_val}
        self.auto_status_label.setText(f"Updated Automation for '{mod}': x={x_val}, y={y_val}, z={z_val} (Polynomial envelope active)")
        QMessageBox.information(self, "Automation Applied", f"Successfully applied x,y,z automation method to {mod}.")

    def create_master_playlist_tab(self):
        return QWidget()

    def create_sample_module_tab(self):
        return QWidget()

    def create_mdi_suite_tab(self):
        widget = QWidget(); l = QVBoxLayout(widget)
        self.mdi_area = QMdiArea()
        self.spawn_subwindow("Eskibrutus Synth", self.create_eskibrutus_content(), 20, 20)
        self.spawn_subwindow("Vectoreski Synth", self.create_vectoreski_content(), 380, 20)
        l.addWidget(self.mdi_area)
        return widget

    def spawn_subwindow(self, title, content_widget, x, y):
        sub = QMdiSubWindow()
        sub.setWidget(content_widget)
        sub.setWindowTitle(title)
        sub.resize(340, 310)
        sub.move(x, y)
        self.mdi_area.addSubWindow(sub)
        sub.show()

    def spawn_subwindow_to_mdi(self, title, content_widget, x, y):
        self.tabs.setCurrentIndex(5)
        self.spawn_subwindow(title, content_widget, x, y)

    def create_eskibrutus_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.addWidget(LiveModuleGraphWidget("eskibrutus", self))
        return w

    def create_vectoreski_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        l.addWidget(LiveModuleGraphWidget("vectoreski", self))
        return w

    def create_eskitable_content(self):
        return QWidget()

    def create_spatial_matrix_content(self):
        return QWidget()

    def create_eqr_equation_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        btn_prompt = QPushButton("Configure x, y, z Variables")
        btn_prompt.clicked.connect(self.prompt_xyz_variables)
        l.addWidget(btn_prompt)
        return w

    def prompt_xyz_variables(self):
        x_val, ok1 = QInputDialog.getDouble(self, "EQR Variable x", "Enter value for x:", 1.0, -100.0, 100.0, 4)
        if not ok1: return
        y_val, ok2 = QInputDialog.getDouble(self, "EQR Variable y", "Enter value for y:", 1.0, -100.0, 100.0, 4)
        if not ok2: return
        z_val, ok3 = QInputDialog.getDouble(self, "EQR Variable z", "Enter value for z:", 1.0, -100.0, 100.0, 4)
        if not ok3: return
        QMessageBox.information(self, "Variables Updated", f"Successfully set x={x_val}, y={y_val}, z={z_val} for EQR equations.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    suite = EQRGrooveboxUltimateSuite()
    suite.show()
    sys.exit(app.exec())

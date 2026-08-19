# =========================================================
# master_sequencer_hub.py
# EQR GROOVEBOX ULTIMATE DAW & SYNTHESIS SUITE (v13.9 High-End VST Architecture: 20 Randomized Instruments, Multi-Knob Arrays & Pattern Generation)
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


class SynthAudioStream(QIODevice):
    def __init__(self, sample_rate=44100, parent=None):
        super().__init__(parent)
        self.sample_rate = sample_rate
        self.frequency = 432.0
        self.amplitude = 0.7
        self.waveform_type = "sine"
        self.phase = 0.0
        self.custom_wavetable = [math.sin(2 * math.pi * i / 256.0) for i in range(256)]
        self.open(QIODevice.OpenModeFlag.ReadOnly)

    def set_frequency(self, freq):
        self.frequency = max(20.0, min(20000.0, freq))

    def set_amplitude(self, amp):
        self.amplitude = max(0.0, min(1.0, amp))

    def set_waveform(self, w_type):
        self.waveform_type = w_type

    def set_custom_wavetable(self, table):
        if table and len(table) > 0:
            self.custom_wavetable = list(table)

    def readData(self, maxlen):
        num_samples = maxlen // 2
        buffer = bytearray()
        dt = 1.0 / self.sample_rate
        table_len = len(self.custom_wavetable)

        for _ in range(num_samples):
            if self.waveform_type == "custom" and table_len > 0:
                idx = (self.phase * table_len) % table_len
                i0 = int(idx)
                i1 = (i0 + 1) % table_len
                frac = idx - i0
                sample = self.custom_wavetable[i0] * (1.0 - frac) + self.custom_wavetable[i1] * frac
            elif self.waveform_type == "sine":
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
        painter.drawText(12, 18, "<b>High-End VST Modular Wire Patchbay</b> (Multi-Knob Matrix Active)")

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
        self.setFixedSize(70, 75)
        self.dragging = False
        self.last_y = 0

    def set_value(self, val):
        self.value = max(self.min_val, min(self.max_val, val))
        self.update()
        if self.callback:
            self.callback(self.value)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(0, 3, self.width(), 11, Qt.AlignmentFlag.AlignCenter, self.label_text)
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(0, 14, self.width(), 10, Qt.AlignmentFlag.AlignCenter, f"{self.value:.2f}")

        center = QPointF(35, 40)
        radius = 11.0
        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#30363d"), 1.5))
        painter.drawEllipse(center, radius, radius)

        span_val = self.max_val - self.min_val if self.max_val != self.min_val else 1.0
        normalized = (self.value - self.min_val) / span_val
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 2) * math.sin(angle)
        tip_y = center.y() - (radius - 2) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, QPointF(tip_x, tip_y))
        painter.setPen(QPen(QColor("#c9d1d9"), 1))
        painter.drawText(2, 60, self.width() - 4, 11, Qt.AlignmentFlag.AlignCenter, self.math_note)

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


class LiveDrawableWavetableWidget(QWidget):
    def __init__(self, mode="wavetable", parent=None):
        super().__init__(parent)
        self.mode = mode
        self.setMinimumHeight(130)
        self.setMaximumHeight(160)
        self.setMouseTracking(True)
        self.parent_suite = parent
        self.table_size = 256
        self.raw_wavetable = [math.sin(2 * math.pi * i / self.table_size) for i in range(self.table_size)]
        self.wavetable = list(self.raw_wavetable)

        # Randomized or default algebraic / polynomial / ISN parameters
        self.poly_expression = random.choice(["x*y*z", "isn", "inverse_isn", "x**2 + y**2 - z", "sin(x)*cos(y)*z", "x*y - z**2"])
        self.influence_factor = random.uniform(0.1, 0.9)
        self.x_var = random.uniform(0.5, 3.5)
        self.y_var = random.uniform(0.5, 3.5)
        self.z_var = random.uniform(0.5, 3.5)

        self.is_drawing = False
        self.bound_knobs = []
        self.recalculate_waveform()

    def register_bound_knob(self, knob_widget):
        if knob_widget not in self.bound_knobs:
            self.bound_knobs.append(knob_widget)

    def set_poly_parameters(self, expr, inf, x_v, y_v, z_v):
        self.poly_expression = expr
        self.influence_factor = inf
        self.x_var = x_v
        self.y_var = y_v
        self.z_var = z_v
        self.recalculate_waveform()

    def recalculate_waveform(self):
        self.wavetable = []
        table_len = len(self.raw_wavetable)
        for i in range(table_len):
            base_val = self.raw_wavetable[i]
            phase_norm = i / table_len

            poly_val = self.evaluate_polynomial_formula(phase_norm, self.x_var, self.y_var, self.z_var)
            blended = base_val * (1.0 - self.influence_factor) + (base_val * poly_val * self.influence_factor)
            self.wavetable.append(max(-1.0, min(1.0, blended)))

        self.update()
        self.update_bound_knobs_from_wavetable()

    def evaluate_polynomial_formula(self, t, x, y, z):
        expr = self.poly_expression.lower().replace(" ", "")
        try:
            if "inverse_isn" in expr or "inv_isn" in expr:
                denom = (x * t + y * t**2 + z * t**3)
                return 1.0 / (denom if abs(denom) > 1e-5 else 1e-5)
            elif "isn" in expr:
                return math.sin(x * t) * math.cos(y * t) * (z * t + 1.0)
            else:
                local_env = {"x": x, "y": y, "z": z, "t": t, "math": math}
                res = eval(expr, {"__builtins__": None}, local_env)
                return float(res)
        except Exception:
            return x * y * z * t

    def update_bound_knobs_from_wavetable(self):
        if not self.bound_knobs or not self.wavetable: return
        rms = math.sqrt(sum(v*v for v in self.wavetable) / len(self.wavetable))
        peak = max(abs(v) for v in self.wavetable)
        asymmetry = sum(self.wavetable) / len(self.wavetable)

        for i, knob in enumerate(self.bound_knobs):
            span = knob.max_val - knob.min_val
            norm_val = (rms + peak + asymmetry) / 3.0
            new_val = knob.min_val + ((i * 0.33 + norm_val) % 1.0) * span
            knob.set_value(new_val)

        if self.parent_suite and hasattr(self.parent_suite, 'audio_stream') and self.parent_suite.audio_stream:
            self.parent_suite.audio_stream.set_custom_wavetable(self.wavetable)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_drawing = True
            self.modify_table_at_pos(event.position())

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.is_drawing:
            self.modify_table_at_pos(event.position())

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_drawing = False
            self.recalculate_waveform()

    def modify_table_at_pos(self, pos: QPointF):
        w = self.width(); h = self.height()
        if w <= 0 or h <= 0: return
        x_frac = max(0.0, min(1.0, pos.x() / w))
        y_frac = max(0.0, min(1.0, pos.y() / h))
        val = 1.0 - (2.0 * y_frac)

        idx = int(x_frac * (self.table_size - 1))
        radius = 5
        for i in range(max(0, idx - radius), min(self.table_size, idx + radius + 1)):
            dist_factor = 1.0 - (abs(i - idx) / (radius + 1))
            self.raw_wavetable[i] = self.raw_wavetable[i] * (1.0 - dist_factor) + val * dist_factor

        self.recalculate_waveform()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width(); h = self.height()
        painter.fillRect(0, 0, w, h, QColor("#0d1117"))

        painter.setPen(QPen(QColor("#21262d"), 1, Qt.PenStyle.DashLine))
        painter.drawLine(0, h // 2, w, h // 2)
        painter.drawLine(w // 2, 0, w // 2, h)

        path = QPainterPath()
        painter.setPen(QPen(QColor("#00ffcc"), 2.0))
        table_len = len(self.wavetable)
        for i in range(w):
            t_idx = int((i / w) * (table_len - 1))
            val = self.wavetable[t_idx]
            screen_y = (h / 2) - (val * (h / 2.2))
            if i == 0: path.moveTo(i, screen_y)
            else: path.lineTo(i, screen_y)
        painter.drawPath(path)

        painter.setPen(QPen(QColor("#30363d"), 1))
        painter.drawRect(0, 0, w - 1, h - 1)
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(8, 16, f"[{self.mode.upper()}] Poly: {self.poly_expression} | Inf: {self.influence_factor:.2f}")


class EQRGrooveboxUltimateSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Ultimate Modular DAW Suite (v13.9 High-End VST 20-Instrument Randomized Suite)")
        self.resize(1900, 1050)

        self.audio_sink = None
        self.audio_stream = None
        self.is_playing = False

        # Generate up to 20 random high-end VST instruments with randomized properties
        self.module_categories = {
            "High-End VST Synths": [f"VST_Engine_{i+1:02d}" for i in range(20)]
        }

        def default_pattern(p_name):
            # Up to 16 patterns for each instrument, random lengths and parameters
            length = random.choice([16, 32, 64])
            return {
                "name": p_name,
                "length": length,
                "speed": random.choice([0.5, 1.0, 2.0]),
                "scale_increment": random.randint(1, 4),
                "curve": random.choice(["Linear", "Exponential", "Polynomial", "ISN-Morph"]),
                "depth": random.uniform(0.5, 1.0),
                "steps": [{"active": random.choice([True, False, True]), "tonal_shift": random.randint(-12, 12), "amp": random.uniform(0.4, 1.0), "duration": 1.0} for _ in range(length)]
            }

        self.instrument_sequences = {}
        for cat, mods in self.module_categories.items():
            for mod in mods:
                # Exactly 16 patterns per instrument
                self.instrument_sequences[mod] = [default_pattern(f"Pattern {p+1}") for p in range(16)]

        # Master playlist with implementation constraint: no more than four times per pattern block
        self.master_playlist_tracks = []
        for mod in self.module_categories["High-End VST Synths"][:8]: # Assign tracks to first 8 instruments
            blocks = {}
            # Ensure no pattern is implemented more than 4 times across the track timeline
            assigned_counts = {p_idx: 0 for p_idx in range(16)}
            for col in range(32):
                p_idx = random.randint(0, 15)
                if assigned_counts[p_idx] < 4:
                    blocks[col] = p_idx
                    assigned_counts[p_idx] += 1
            self.master_playlist_tracks.append({"instrument": mod, "pattern_idx": 0, "blocks": blocks})

        self.automation_lanes = {
            mod: {"x": random.uniform(0.1, 5.0), "y": random.uniform(0.1, 5.0), "z": random.uniform(0.1, 5.0), "curve_type": "High-End VST x*y*z"}
            for mods in self.module_categories.values() for mod in mods
        }

        self.setup_window_creation_menu()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_front_page_tab(), "Front-Page Modular Patchbay & Master Controls")
        self.tabs.addTab(self.create_sequencer_playlist_tab(), "Sequencer Manager & Step Grid (16 Patterns)")
        self.tabs.addTab(self.create_automation_manager_tab(), "Automation Module Manager & x,y,z Lanes")
        self.tabs.addTab(self.create_master_playlist_tab(), "Master Coordination Playlist (Max 4x Limit)")
        self.tabs.addTab(self.create_sample_module_tab(), "Sample Loader & Audio Module")
        self.tabs.addTab(self.create_mdi_suite_tab(), "Modular Subwindow Bays (MDI)")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("EQR Suite v13.9 Active | 20 Randomized High-End VST Instruments & Multi-Knob Architecture Loaded.")

    def setup_window_creation_menu(self):
        menubar = self.menuBar()
        window_menu = menubar.addMenu("VST Engine Creator")

        act_create = QAction("Create New VST Instrument...", self)
        act_create.triggered.connect(self.spawn_create_module_dialog)
        window_menu.addAction(act_create)

    def spawn_create_module_dialog(self):
        mod_name, ok1 = QInputDialog.getText(self, "Create VST Engine", "Enter VST instrument name:")
        if not ok1 or not mod_name.strip(): return

        if "High-End VST Synths" not in self.module_categories:
            self.module_categories["High-End VST Synths"] = []
        if mod_name not in self.module_categories["High-End VST Synths"]:
            self.module_categories["High-End VST Synths"].append(mod_name)

        self.instrument_sequences[mod_name] = [{"name": f"Pattern {p+1}", "length": 16, "speed": 1.0, "scale_increment": 1, "curve": "Linear", "depth": 0.75, "steps": [{"active": False, "tonal_shift": 0, "amp": 1.0, "duration": 1.0} for _ in range(16)]} for p in range(16)]
        self.automation_lanes[mod_name] = {"x": 1.0, "y": 1.0, "z": 1.0, "curve_type": "VST x*y*z"}

        self.refresh_all_module_dropdowns()
        QMessageBox.information(self, "VST Created", f"Successfully spawned VST engine '{mod_name}' with 16 default patterns.")

    def refresh_all_module_dropdowns(self):
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

        if hasattr(self, 'auto_mod_combo'):
            self.auto_mod_combo.blockSignals(True)
            curr_auto = self.auto_mod_combo.currentText()
            self.auto_mod_combo.clear()
            for mod in self.instrument_sequences.keys():
                self.auto_mod_combo.addItem(mod)
            self.auto_mod_combo.setCurrentText(curr_auto)
            self.auto_mod_combo.blockSignals(False)

        if hasattr(self, 'playlist_instrument_combo'):
            self.playlist_instrument_combo.blockSignals(True)
            curr_p = self.playlist_instrument_combo.currentText()
            self.playlist_instrument_combo.clear()
            for mod in self.instrument_sequences.keys():
                self.playlist_instrument_combo.addItem(mod)
            self.playlist_instrument_combo.setCurrentText(curr_p)
            self.playlist_instrument_combo.blockSignals(False)
            self.populate_playlist_pattern_combo()

    def create_front_page_tab(self):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        left_layout = QVBoxLayout()
        self.patchbay_widget = FrontPagePatchbayWidget(self)
        left_layout.addWidget(self.patchbay_widget)

        master_group = QGroupBox("Master Mix, High-End VST Tuning & Extended Macro Controls")
        master_grid = QGridLayout(master_group)
        self.knob_base_tuning = ModularBayKnob("Base Tuning", 400.0, 480.0, 432.0, "Hz", self, callback=self.update_base_tuning_live)
        master_grid.addWidget(self.knob_base_tuning, 0, 0)
        master_grid.addWidget(ModularBayKnob("Macro Filter", 100.0, 10000.0, 2500.0, "Cut", self), 0, 1)
        master_grid.addWidget(ModularBayKnob("Resonance Q", 0.1, 10.0, 2.0, "Res", self), 0, 2)
        master_grid.addWidget(ModularBayKnob("Unison Detune", 0.0, 1.0, 0.15, "Det", self), 0, 3)
        master_grid.addWidget(ModularBayKnob("Stereo Width", 0.0, 2.0, 1.2, "Wdt", self), 0, 4)
        left_layout.addWidget(master_group)
        layout.addLayout(left_layout, stretch=3)

        right_layout = QVBoxLayout()
        audio_group = QGroupBox("Live Audio Stream & VST Export")
        audio_layout = QVBoxLayout(audio_group)

        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100); self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.update_audio_volume)
        audio_layout.addWidget(QLabel("Master VST Volume:"))
        audio_layout.addWidget(self.volume_slider)

        self.btn_preview = QPushButton("Start Live VST Audio Stream")
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
            self.audio_stream.set_waveform("custom")

            self.audio_sink = QAudioSink(QMediaDevices.defaultAudioOutput(), format, self)
            self.audio_sink.start(self.audio_stream)
            self.is_playing = True
            self.btn_preview.setText("Stop Live VST Audio Stream")
        else:
            if self.audio_sink: self.audio_sink.stop()
            if self.audio_stream: self.audio_stream.close()
            self.is_playing = False
            self.btn_preview.setText("Start Live VST Audio Stream")

    def update_base_tuning_live(self, val):
        if self.audio_stream:
            self.audio_stream.set_frequency(val)

    def update_audio_volume(self, val):
        if self.audio_stream: self.audio_stream.set_amplitude(val / 100.0)

    def create_sequencer_playlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("<b>Select VST Instrument:</b>"))
        self.seq_instrument_combo = QComboBox()
        for cat, mods in self.module_categories.items():
            for m in mods:
                self.seq_instrument_combo.addItem(f"[{cat}] {m}")
        self.seq_instrument_combo.currentIndexChanged.connect(self.refresh_sequencer_ui)
        toolbar.addWidget(self.seq_instrument_combo)

        toolbar.addWidget(QLabel("<b>Pattern Index (16 Max):</b>"))
        self.seq_name_combo = QComboBox()
        self.seq_name_combo.currentIndexChanged.connect(self.load_selected_sequence_parameters)
        toolbar.addWidget(self.seq_name_combo)

        btn_scale_cfg = QPushButton("Set Scale Increment...")
        btn_scale_cfg.clicked.connect(self.prompt_scale_increment)
        toolbar.addWidget(btn_scale_cfg)

        layout.addLayout(toolbar)

        self.scale_info_label = QLabel("<b>Scale Increment:</b> 1 semitone multiplier (Up to 16 Patterns Active per Instrument)")
        self.scale_info_label.setStyleSheet("color: #58a6ff;")
        layout.addWidget(self.scale_info_label)

        self.single_seq_table = QTableWidget()
        self.single_seq_table.cellClicked.connect(self.on_sequencer_cell_clicked)
        layout.addWidget(self.single_seq_table)

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
                self.seq_name_combo.addItem(f"Pattern {idx+1}: {seq['name']}")
        self.seq_name_combo.blockSignals(False)
        self.load_selected_sequence_parameters()

    def refresh_sequencer_ui(self):
        self.populate_sequence_names()

    def prompt_scale_increment(self):
        inst = self.get_current_clean_instrument_name()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst not in self.instrument_sequences or seq_idx < 0: return
        seq_data = self.instrument_sequences[inst][seq_idx]

        curr_inc = seq_data.get("scale_increment", 1)
        new_inc, ok = QInputDialog.getInt(self, "Scale Increment Multiplier", "Enter scale increment unit:", curr_inc, 1, 12, 1)
        if ok:
            seq_data["scale_increment"] = new_inc
            self.scale_info_label.setText(f"<b>Scale Increment:</b> {new_inc}")

    def load_selected_sequence_parameters(self):
        inst = self.get_current_clean_instrument_name()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            seq_data = self.instrument_sequences[inst][seq_idx]
            inc = seq_data.get("scale_increment", 1)
            self.scale_info_label.setText(f"<b>Scale Increment:</b> {inc} (Pattern Length: {seq_data['length']})")
            self.build_single_sequencer_grid(seq_data)

    def build_single_sequencer_grid(self, seq_data):
        length = seq_data["length"]
        steps = seq_data["steps"]
        scale_inc = seq_data.get("scale_increment", 1)

        self.single_seq_table.blockSignals(True)
        self.single_seq_table.setRowCount(1)
        self.single_seq_table.setColumnCount(length)
        self.single_seq_table.setVerticalHeaderLabels(["Steps"])

        for c in range(length):
            step_info = steps[c]
            is_active = step_info.get("active", False)
            t_shift = step_info.get("tonal_shift", 0)
            shift_str = f"{t_shift * scale_inc:+d}"

            item = QTableWidgetItem(f"[{shift_str}] ON" if is_active else "---")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            if is_active:
                item.setBackground(QColor("#1f6feb"))
                item.setForeground(QColor("#ffffff"))
            else:
                item.setBackground(QColor("#161b22"))
                item.setForeground(QColor("#8b949e"))
            self.single_seq_table.setItem(0, c, item)

        self.single_seq_table.blockSignals(False)

    def on_sequencer_cell_clicked(self, row, col):
        inst = self.get_current_clean_instrument_name()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst not in self.instrument_sequences or seq_idx < 0: return

        seq_data = self.instrument_sequences[inst][seq_idx]
        step_info = seq_data["steps"][col]
        step_info["active"] = not step_info.get("active", False)
        self.build_single_sequencer_grid(seq_data)

    def create_automation_manager_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        layout.addWidget(QLabel("<h2>High-End VST Automation & x, y, z Variable Envelopes</h2>"))

        self.auto_mod_combo = QComboBox()
        for mod in self.instrument_sequences.keys():
            self.auto_mod_combo.addItem(mod)
        layout.addWidget(self.auto_mod_combo)

        btn_edit_xyz = QPushButton("Configure x, y, z VST Automation Envelopes")
        btn_edit_xyz.clicked.connect(self.configure_module_xyz_automation)
        layout.addWidget(btn_edit_xyz)

        self.auto_status_label = QLabel("Select a VST instrument above to manage its polynomial x,y,z automation.")
        layout.addWidget(self.auto_status_label)
        return widget

    def configure_module_xyz_automation(self):
        mod = self.auto_mod_combo.currentText()
        current_xyz = self.automation_lanes.get(mod, {"x": 1.0, "y": 1.0, "z": 1.0})

        x_val, ok1 = QInputDialog.getDouble(self, f"Automation X [{mod}]", "Enter x scale:", current_xyz["x"], -100.0, 100.0, 4)
        if not ok1: return
        y_val, ok2 = QInputDialog.getDouble(self, f"Automation Y [{mod}]", "Enter y scale:", current_xyz["y"], -100.0, 100.0, 4)
        if not ok2: return
        z_val, ok3 = QInputDialog.getDouble(self, f"Automation Z [{mod}]", "Enter z scale:", current_xyz["z"], -100.0, 100.0, 4)
        if not ok3: return

        self.automation_lanes[mod] = {"x": x_val, "y": y_val, "z": z_val}
        self.auto_status_label.setText(f"Updated VST Automation for '{mod}': x={x_val}, y={y_val}, z={z_val}")
        QMessageBox.information(self, "VST Automation Applied", f"Successfully applied x,y,z automation to {mod}.")

    def create_master_playlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("<b>Paint VST Instrument:</b>"))
        self.playlist_instrument_combo = QComboBox()
        for mod in self.instrument_sequences.keys():
            self.playlist_instrument_combo.addItem(mod)
        self.playlist_instrument_combo.currentIndexChanged.connect(self.populate_playlist_pattern_combo)
        toolbar.addWidget(self.playlist_instrument_combo)

        toolbar.addWidget(QLabel("<b>Pattern (1-16):</b>"))
        self.playlist_pattern_combo = QComboBox()
        toolbar.addWidget(self.playlist_pattern_combo)

        btn_add_track = QPushButton("Add Arrangement Track")
        btn_add_track.clicked.connect(self.add_master_playlist_track)
        toolbar.addWidget(btn_add_track)

        layout.addLayout(toolbar)

        info_label = QLabel("<b>Master Playlist Arranger:</b> Strict limit enforced—each pattern implementation is restricted to <b>no more than four times</b> per track timeline.")
        info_label.setStyleSheet("color: #00ffcc;")
        layout.addWidget(info_label)

        self.playlist_table = QTableWidget()
        self.playlist_table.cellClicked.connect(self.on_playlist_cell_clicked)
        layout.addWidget(self.playlist_table)

        self.rebuild_master_playlist_grid()
        return widget

    def populate_playlist_pattern_combo(self):
        self.playlist_pattern_combo.blockSignals(True)
        self.playlist_pattern_combo.clear()
        inst = self.playlist_instrument_combo.currentText()
        if inst in self.instrument_sequences:
            for idx, seq in enumerate(self.instrument_sequences[inst]):
                self.playlist_pattern_combo.addItem(f"Pattern {idx+1}: {seq['name']}", idx)
        self.playlist_pattern_combo.blockSignals(False)

    def add_master_playlist_track(self):
        inst = self.playlist_instrument_combo.currentText()
        pat_idx = self.playlist_pattern_combo.currentData()
        if pat_idx is None: pat_idx = 0
        self.master_playlist_tracks.append({"instrument": inst, "pattern_idx": pat_idx, "blocks": {}})
        self.rebuild_master_playlist_grid()

    def rebuild_master_playlist_grid(self):
        num_tracks = len(self.master_playlist_tracks)
        timeline_cols = 32

        self.playlist_table.blockSignals(True)
        self.playlist_table.setRowCount(num_tracks)
        self.playlist_table.setColumnCount(timeline_cols)

        row_labels = []
        for r, track in enumerate(self.master_playlist_tracks):
            row_labels.append(f"{track['instrument']} [Pat {track['pattern_idx']+1}]")
            for c in range(timeline_cols):
                is_painted = c in track["blocks"]
                p_val = track["blocks"].get(c, 0)
                item = QTableWidgetItem(f"P{p_val+1}" if is_painted else "---")
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if is_painted:
                    item.setBackground(QColor("#238636"))
                    item.setForeground(QColor("#ffffff"))
                else:
                    item.setBackground(QColor("#161b22"))
                    item.setForeground(QColor("#8b949e"))
                self.playlist_table.setItem(r, c, item)

        self.playlist_table.setVerticalHeaderLabels(row_labels)
        self.playlist_table.blockSignals(False)

    def on_playlist_cell_clicked(self, row, col):
        if row < 0 or row >= len(self.master_playlist_tracks): return
        track = self.master_playlist_tracks[row]

        curr_pat_idx = self.playlist_pattern_combo.currentData()
        if curr_pat_idx is None: curr_pat_idx = 0

        # Check constraint: no more than four times per pattern
        pattern_counts = list(track["blocks"].values()).count(curr_pat_idx)
        if col in track["blocks"]:
            del track["blocks"][col]
        else:
            if pattern_counts >= 4:
                QMessageBox.warning(self, "Constraint Enforcement", "Cannot implement this pattern more than 4 times on this track timeline.")
                return
            track["blocks"][col] = curr_pat_idx

        self.rebuild_master_playlist_grid()

    def create_sample_module_tab(self):
        return QWidget()

    def create_mdi_suite_tab(self):
        widget = QWidget(); l = QVBoxLayout(widget)
        self.mdi_area = QMdiArea()
        self.spawn_subwindow("VST Engine 01", self.create_vst_engine_content("VST_Engine_01"), 20, 20)
        self.spawn_subwindow("VST Engine 02", self.create_vst_engine_content("VST_Engine_02"), 440, 20)
        l.addWidget(self.mdi_area)
        return widget

    def spawn_subwindow(self, title, content_widget, x, y):
        sub = QMdiSubWindow()
        sub.setWidget(content_widget)
        sub.setWindowTitle(title)
        sub.resize(430, 420)
        sub.move(x, y)
        self.mdi_area.addSubWindow(sub)
        sub.show()

    def prompt_poly_expression_settings(self, wavetable_widget):
        expr, ok1 = QInputDialog.getText(
            self, "Algebraic / Polynomial / ISN Prompt",
            "Enter polynomial, ISN, or Inverse ISN expression using x, y, z, t:",
            QLineEdit.EchoMode.Normal, wavetable_widget.poly_expression
        )
        if not ok1: return

        inf, ok2 = QInputDialog.getDouble(self, "Influence Knob", "Enter multiplication influence factor (0.0 to 1.0):", wavetable_widget.influence_factor, 0.0, 1.0, 3)
        if not ok2: return

        x_v, ok3 = QInputDialog.getDouble(self, "Variable x", "Enter value for x:", wavetable_widget.x_var, -100.0, 100.0, 3)
        if not ok3: return

        y_v, ok4 = QInputDialog.getDouble(self, "Variable y", "Enter value for y:", wavetable_widget.y_var, -100.0, 100.0, 3)
        if not ok4: return

        z_v, ok5 = QInputDialog.getDouble(self, "Variable z", "Enter value for z:", wavetable_widget.z_var, -100.0, 100.0, 3)
        if not ok5: return

        wavetable_widget.set_poly_parameters(expr, inf, x_v, y_v, z_v)

    def create_vst_engine_content(self, engine_name):
        w = QWidget(); l = QVBoxLayout(w)
        wavetable_widget = LiveDrawableWavetableWidget(engine_name, self)
        l.addWidget(wavetable_widget)

        btn_poly = QPushButton("Algebraic / ISN / Polynomial Prompt...")
        btn_poly.clicked.connect(lambda: self.prompt_poly_expression_settings(wavetable_widget))
        l.addWidget(btn_poly)

        # Extended high-end VST macro knobs
        knobs_layout1 = QHBoxLayout()
        k1 = ModularBayKnob("Osc Drive", 0.0, 10.0, random.uniform(1.0, 5.0), "Drv", self)
        k2 = ModularBayKnob("Wavetable", 0.0, 1.0, random.uniform(0.2, 0.8), "Wav", self)
        k3 = ModularBayKnob("Vector Skew", -1.0, 1.0, random.uniform(-0.5, 0.5), "Skw", self)
        wavetable_widget.register_bound_knob(k1)
        wavetable_widget.register_bound_knob(k2)
        wavetable_widget.register_bound_knob(k3)
        knobs_layout1.addWidget(k1); knobs_layout1.addWidget(k2); knobs_layout1.addWidget(k3)
        l.addLayout(knobs_layout1)

        knobs_layout2 = QHBoxLayout()
        k4 = ModularBayKnob("Filter Cut", 200.0, 8000.0, 2000.0, "Cut", self)
        k5 = ModularBayKnob("Resonance", 0.1, 8.0, 1.5, "Res", self)
        k6 = ModularBayKnob("Unison Amt", 0.0, 1.0, 0.3, "Uni", self)
        knobs_layout2.addWidget(k4); knobs_layout2.addWidget(k5); knobs_layout2.addWidget(k6)
        l.addLayout(knobs_layout2)

        return w


if __name__ == "__main__":
    app = QApplication(sys.argv)
    suite = EQRGrooveboxUltimateSuite()
    suite.show()
    sys.exit(app.exec())

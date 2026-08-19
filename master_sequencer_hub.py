# =========================================================
# master_sequencer_hub.py
# EQR GROOVEBOX ULTIMATE DAW & SYNTHESIS SUITE (v14.1 Clean Single-Row Chord Prompt & Large Green MDI Spawn)
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
    QSlider, QLineEdit, QMdiArea, QMdiSubWindow, QTableWidget, QTableWidgetItem, QHeaderView, QInputDialog, QMenu
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


class UnquantizedPlaylistCanvas(QWidget):
    """
    Unquantized continuous timeline canvas allowing free placement of pattern audio clips,
    complete with per-instance timestretch, pitch offsets, amplitude scaling, and
    scrollwheel-adjustable +/- modulation lines.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(450)
        self.setMouseTracking(True)
        self.parent_suite = parent
        self.clips = []
        self.scrollwheel_mod_amount = 0.10
        self.dragging_clip = None
        self.drag_offset_x = 0.0

    def add_clip(self, inst, pat, x=50.0, y=50.0, duration=120.0, pitch=0.0, amp=1.0, stretch=1.0):
        self.clips.append({
            "inst": inst, "pat": pat, "x": x, "y": y,
            "duration": duration, "pitch": pitch, "amp": amp, "stretch": stretch
        })
        self.update()

    def randomize_unique_playlist(self, available_instruments, available_patterns_dict):
        self.clips.clear()
        if not available_instruments: return

        num_clips = random.randint(12, 28)
        current_x = 40.0

        for _ in range(num_clips):
            inst = random.choice(available_instruments)
            pat_list = available_patterns_dict.get(inst, [])
            pat_idx = random.randint(0, len(pat_list) - 1) if pat_list else 0

            x_pos = current_x + random.uniform(5.0, 45.0)
            y_pos = float(random.randint(0, 5) * 65 + 40)
            duration = random.uniform(60.0, 180.0)
            pitch = float(random.randint(-12, 12))
            amp = random.uniform(0.3, 1.0)
            stretch = random.uniform(0.5, 2.0)

            self.clips.append({
                "inst": inst, "pat": pat_idx, "x": x_pos, "y": y_pos,
                "duration": duration, "pitch": pitch, "amp": amp, "stretch": stretch
            })
            current_x = x_pos + duration

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width(); h = self.height()
        painter.fillRect(0, 0, w, h, QColor("#080c10"))

        painter.setPen(QPen(QColor("#21262d"), 1, Qt.PenStyle.DashLine))
        for x_line in range(0, w, 80):
            painter.drawLine(x_line, 0, x_line, h)

        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(12, 22, f"<b>Unquantized Audio Timeline Canvas</b> | Scroll Mod Amount: {self.scrollwheel_mod_amount:+.2f} (Scroll wheel on clips adjusts modulation/stretch)")

        for clip in self.clips:
            cx = clip["x"]; cy = clip["y"]; cwidth = clip["duration"]
            painter.setBrush(QBrush(QColor("#1f6feb")))
            painter.setPen(QPen(QColor("#00ffcc"), 1.5))
            painter.drawRoundedRect(int(cx), int(cy), int(cwidth), 50, 6, 6)

            painter.setPen(QPen(QColor("#ffffff"), 1))
            label = f"{clip['inst']} | P{clip['pat']+1} | Pitch:{clip['pitch']:+.0f} | Stretch:{clip['stretch']:.2f}x | Amp:{clip['amp']:.2f}"
            painter.drawText(int(cx + 8), int(cy + 30), int(cwidth - 16), 20, Qt.AlignmentFlag.AlignLeft, label)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            for clip in self.clips:
                if clip["x"] <= pos.x() <= clip["x"] + clip["duration"] and clip["y"] <= pos.y() <= clip["y"] + 50:
                    self.dragging_clip = clip
                    self.drag_offset_x = pos.x() - clip["x"]
                    break

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging_clip:
            self.dragging_clip["x"] = max(0.0, event.position().x() - self.drag_offset_x)
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        self.dragging_clip = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        step = 0.01 if delta > 0 else -0.01
        self.scrollwheel_mod_amount = max(-5.0, min(5.0, self.scrollwheel_mod_amount + step))

        pos = event.position()
        for clip in self.clips:
            if clip["x"] <= pos.x() <= clip["x"] + clip["duration"] and clip["y"] <= pos.y() <= clip["y"] + 50:
                clip["stretch"] = max(0.1, min(4.0, clip["stretch"] + step))
                clip["amp"] = max(0.0, min(1.0, clip["amp"] + (step * 0.5)))
                break

        self.update()


class ModularBayKnob(QWidget):
    """
    High-End VST Knob supporting +/- scrollwheel-adjustable modulation lines and right-click patching.
    """
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, math_note="", parent=None, callback=None):
        super().__init__(parent)
        self.label_text = label_text
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.math_note = math_note
        self.callback = callback
        self.setFixedSize(75, 80)
        self.dragging = False
        self.last_y = 0
        self.modulation_depth = 0.25
        self.patched_in = True
        self.patched_out = True

    def set_value(self, val):
        self.value = max(self.min_val, min(self.max_val, val))
        self.update()
        if self.callback:
            self.callback(self.value)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw patch status color indicator on borders
        border_color = "#00ffcc" if (self.patched_in and self.patched_out) else "#8b949e"

        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(0, 2, self.width(), 11, Qt.AlignmentFlag.AlignCenter, self.label_text)
        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(0, 13, self.width(), 10, Qt.AlignmentFlag.AlignCenter, f"{self.value:.2f}")

        center = QPointF(37, 42)
        radius = 11.0
        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor(border_color), 1.5))
        painter.drawEllipse(center, radius, radius)

        span_val = self.max_val - self.min_val if self.max_val != self.min_val else 1.0
        normalized = (self.value - self.min_val) / span_val
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 2) * math.sin(angle)
        tip_y = center.y() - (radius - 2) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, QPointF(tip_x, tip_y))

        mod_color = "#3fb950" if self.modulation_depth >= 0 else "#f85149"
        painter.setPen(QPen(QColor(mod_color), 1.5, Qt.PenStyle.DashLine))
        painter.drawArc(int(center.x() - radius - 4), int(center.y() - radius - 4), int((radius + 4) * 2), int((radius + 4) * 2), 30 * 16, int(self.modulation_depth * 120 * 16))

        painter.setPen(QPen(QColor("#c9d1d9"), 1))
        patch_status = "[IN/OUT]" if (self.patched_in and self.patched_out) else "[UNPATCHED]"
        painter.drawText(2, 65, self.width() - 4, 11, Qt.AlignmentFlag.AlignCenter, f"{patch_status}")

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        act_in = menu.addAction(f"Toggle Wire Patch IN (Current: {'Connected' if self.patched_in else 'Disconnected'})")
        act_out = menu.addAction(f"Toggle Wire Patch OUT (Current: {'Connected' if self.patched_out else 'Disconnected'})")
        act_mod = menu.addAction("Reset Scrollwheel Modulation Line")

        action = menu.exec(event.globalPos())
        if action == act_in:
            self.patched_in = not self.patched_in
            self.update()
        elif action == act_out:
            self.patched_out = not self.patched_out
            self.update()
        elif action == act_mod:
            self.modulation_depth = 0.0
            self.update()

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
        step = 0.05 if delta > 0 else -0.05
        self.modulation_depth = max(-2.0, min(2.0, self.modulation_depth + step))
        self.update()


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

        self.poly_expression = random.choice(["x*y*z", "isn", "inverse_isn", "x**2 + y**2 - z"])
        self.influence_factor = random.uniform(0.1, 0.9)
        self.x_var = random.uniform(0.5, 3.5)
        self.y_var = random.uniform(0.5, 3.5)
        self.z_var = random.uniform(0.5, 3.5)
        self.modulation_amount = 0.5
        self.patched_in = True
        self.patched_out = True

        self.is_drawing = False
        self.recalculate_waveform()

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
            blended = base_val * (1.0 - (self.influence_factor * self.modulation_amount)) + (base_val * poly_val * self.influence_factor)
            self.wavetable.append(max(-1.0, min(1.0, blended)))
        self.update()

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
                return float(eval(expr, {"__builtins__": None}, local_env))
        except Exception:
            return x * y * z * t

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        act_in = menu.addAction(f"Toggle Waveform Wire Patch IN (Current: {'Connected' if self.patched_in else 'Disconnected'})")
        act_out = menu.addAction(f"Toggle Waveform Wire Patch OUT (Current: {'Connected' if self.patched_out else 'Disconnected'})")
        act_mod = menu.addAction("Reset Wavetable Modulation Line")

        action = menu.exec(event.globalPos())
        if action == act_in:
            self.patched_in = not self.patched_in
            self.update()
        elif action == act_out:
            self.patched_out = not self.patched_out
            self.update()
        elif action == act_mod:
            self.modulation_amount = 0.0
            self.recalculate_waveform()

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        step = 0.05 if delta > 0 else -0.05
        self.modulation_amount = max(-2.0, min(2.0, self.modulation_amount + step))
        self.recalculate_waveform()

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

        border_color = "#00ffcc" if (self.patched_in and self.patched_out) else "#30363d"
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

        painter.setPen(QPen(QColor(border_color), 1.5))
        painter.drawRect(0, 0, w - 1, h - 1)
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        patch_tag = "[IN/OUT]" if (self.patched_in and self.patched_out) else "[UNPATCHED]"
        painter.drawText(8, 16, f"[{self.mode.upper()}] {patch_tag} Poly: {self.poly_expression} | Mod: {self.modulation_amount:+.2f}")


class EQRGrooveboxUltimateSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Ultimate Modular DAW Suite (v14.1 Clean Single-Row Chord Prompt & Large Green MDI Spawn)")
        self.resize(1900, 1050)

        self.audio_sink = None
        self.audio_stream = None
        self.is_playing = False

        self.module_categories = {
            "High-End VST Synths": [f"VST_Engine_{i+1:02d}" for i in range(20)]
        }

        def default_pattern(p_name):
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
                self.instrument_sequences[mod] = [default_pattern(f"Pattern {p+1}") for p in range(16)]

        self.setup_window_creation_menu()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_front_page_tab(), "Front-Page Modular Patchbay & Master Controls")
        self.tabs.addTab(self.create_sequencer_playlist_tab(), "Sequencer Manager & Single Step Row")
        self.tabs.addTab(self.create_automation_manager_tab(), "Automation Module Manager")
        self.tabs.addTab(self.create_master_playlist_tab(), "Unquantized Master Playlist & Timestretch")
        self.tabs.addTab(self.create_mdi_suite_tab(), "Modular Subwindow Bays (MDI)")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("EQR Suite v14.1 Active | Single-Row Piano Grid, Chord Prompt Input, & Large Green MDI Spawn Ready.")

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
        self.refresh_all_module_dropdowns()
        QMessageBox.information(self, "VST Created", f"Successfully spawned VST engine '{mod_name}' with 16 patterns.")

    def refresh_all_module_dropdowns(self):
        if hasattr(self, 'seq_instrument_combo'):
            self.seq_instrument_combo.blockSignals(True)
            curr_val = self.seq_instrument_combo.currentText()
            self.seq_instrument_combo.clear()
            for cat, mods in self.module_categories.items():
                for m in mods: self.seq_instrument_combo.addItem(f"[{cat}] {m}")
            self.seq_instrument_combo.setCurrentText(curr_val)
            self.seq_instrument_combo.blockSignals(False)
            self.populate_sequence_names()

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

        master_group = QGroupBox("Master Mix, High-End VST Tuning & Scrollwheel Mod Knobs (Right-Click for Wire Patches)")
        master_grid = QGridLayout(master_group)
        self.knob_base_tuning = ModularBayKnob("Base Tuning", 400.0, 480.0, 432.0, "Hz", self)
        master_grid.addWidget(self.knob_base_tuning, 0, 0)
        master_grid.addWidget(ModularBayKnob("Macro Filter", 100.0, 10000.0, 2500.0, "Cut", self), 0, 1)
        master_grid.addWidget(ModularBayKnob("Resonance Q", 0.1, 10.0, 2.0, "Res", self), 0, 2)
        master_grid.addWidget(ModularBayKnob("Unison Detune", 0.0, 1.0, 0.15, "Det", self), 0, 3)
        layout.addWidget(master_group, stretch=3)
        return widget

    def create_sequencer_playlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("<b>Select VST Instrument:</b>"))
        self.seq_instrument_combo = QComboBox()
        for cat, mods in self.module_categories.items():
            for m in mods: self.seq_instrument_combo.addItem(f"[{cat}] {m}")
        self.seq_instrument_combo.currentIndexChanged.connect(self.refresh_sequencer_ui)
        toolbar.addWidget(self.seq_instrument_combo)

        toolbar.addWidget(QLabel("<b>Pattern Index:</b>"))
        self.seq_name_combo = QComboBox()
        self.seq_name_combo.currentIndexChanged.connect(self.load_selected_sequence_parameters)
        toolbar.addWidget(self.seq_name_combo)
        layout.addLayout(toolbar)

        # Chord Prompt Input Pane directly integrated with the single piano roll row
        chord_prompt_layout = QHBoxLayout()
        chord_prompt_layout.addWidget(QLabel("<b>Chord Prompt Input Pane:</b>"))
        self.chord_input_field = QLineEdit()
        self.chord_input_field.setPlaceholderText("Enter chord shorthand (e.g. Cmaj7, Am9, F#m, G7) to populate active sequence row...")
        chord_prompt_layout.addWidget(self.chord_input_field)

        btn_apply_chord = QPushButton("Apply Chord to Row")
        btn_apply_chord.clicked.connect(self.apply_chord_prompt_to_sequence)
        btn_apply_chord.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold;")
        chord_prompt_layout.addWidget(btn_apply_chord)
        layout.addLayout(chord_prompt_layout)

        self.scale_info_label = QLabel("<b>Scale Increment:</b> Single unified row with tonal offsets and chord prompt mapping.")
        layout.addWidget(self.scale_info_label)

        # Exactly 1 single row table as explicitly requested
        self.single_seq_table = QTableWidget()
        self.single_seq_table.setMaximumHeight(90)
        self.single_seq_table.cellClicked.connect(self.on_sequencer_cell_clicked)
        layout.addWidget(self.single_seq_table)

        self.populate_sequence_names()
        return widget

    def get_current_clean_instrument_name(self):
        text = self.seq_instrument_combo.currentText()
        if "]" in text: return text.split("] ")[1]
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

    def load_selected_sequence_parameters(self):
        inst = self.get_current_clean_instrument_name()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            seq_data = self.instrument_sequences[inst][seq_idx]
            self.build_single_sequencer_grid(seq_data)

    def build_single_sequencer_grid(self, seq_data):
        length = seq_data["length"]
        steps = seq_data["steps"]
        scale_inc = seq_data.get("scale_increment", 1)

        self.single_seq_table.blockSignals(True)
        self.single_seq_table.setRowCount(1)  # Strictly 1 single row
        self.single_seq_table.setColumnCount(length)
        for c in range(length):
            step_info = steps[c]
            is_active = step_info.get("active", False)
            t_shift = step_info.get("tonal_shift", 0)
            shift_str = f"{t_shift * scale_inc:+d}"
            item = QTableWidgetItem(f"[{shift_str}] ON" if is_active else "---")
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setBackground(QColor("#1f6feb") if is_active else QColor("#161b22"))
            item.setForeground(QColor("#ffffff") if is_active else QColor("#8b949e"))
            self.single_seq_table.setItem(0, c, item)
        self.single_seq_table.blockSignals(False)

    def on_sequencer_cell_clicked(self, row, col):
        inst = self.get_current_clean_instrument_name()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst not in self.instrument_sequences or seq_idx < 0: return
        seq_data = self.instrument_sequences[inst][seq_idx]
        seq_data["steps"][col]["active"] = not seq_data["steps"][col].get("active", False)
        self.build_single_sequencer_grid(seq_data)

    def apply_chord_prompt_to_sequence(self):
        chord_text = self.chord_input_field.text().strip().upper()
        if not chord_text: return
        inst = self.get_current_clean_instrument_name()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst not in self.instrument_sequences or seq_idx < 0: return
        seq_data = self.instrument_sequences[inst][seq_idx]

        # Simple interval mapping based on chord text
        offsets = [0, 4, 7, 11] if "7" in chord_text else [0, 4, 7]
        if "M" in chord_text or "MAJ" in chord_text: offsets = [0, 4, 7, 11]
        elif "M" not in chord_text and ("M" in chord_text or "MIN" in chord_text or "M" in chord_text): offsets = [0, 3, 7]

        for idx, step in enumerate(seq_data["steps"]):
            step["active"] = True
            step["tonal_shift"] = offsets[idx % len(offsets)]

        self.build_single_sequencer_grid(seq_data)
        QMessageBox.information(self, "Chord Applied", f"Successfully applied chord '{chord_text}' intervals across the single sequence row.")

    def create_automation_manager_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("<h2>High-End VST Automation & x, y, z Variable Envelopes</h2>"))
        return widget

    def create_master_playlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("<b>VST Instrument:</b>"))
        self.playlist_instrument_combo = QComboBox()
        for mod in self.instrument_sequences.keys():
            self.playlist_instrument_combo.addItem(mod)
        self.playlist_instrument_combo.currentIndexChanged.connect(self.populate_playlist_pattern_combo)
        toolbar.addWidget(self.playlist_instrument_combo)

        toolbar.addWidget(QLabel("<b>Pattern:</b>"))
        self.playlist_pattern_combo = QComboBox()
        toolbar.addWidget(self.playlist_pattern_combo)

        btn_add_clip = QPushButton("Add Clip to Unquantized Timeline")
        btn_add_clip.clicked.connect(self.add_unquantized_clip)
        toolbar.addWidget(btn_add_clip)

        btn_randomize = QPushButton("Randomize Unique Unquantized Playlist")
        btn_randomize.clicked.connect(self.trigger_unique_playlist_randomization)
        btn_randomize.setStyleSheet("background-color: #238636; color: white; font-weight: bold;")
        toolbar.addWidget(btn_randomize)

        layout.addLayout(toolbar)

        info_label = QLabel("<b>Unquantized Timeline Controls:</b> Drag clips freely across time. Scrollwheel over a clip adjusts its timestretch & amplitude. Bypasses all grid quantization and heuristic limits.")
        info_label.setStyleSheet("color: #00ffcc;")
        layout.addWidget(info_label)

        self.unquantized_canvas = UnquantizedPlaylistCanvas(self)
        layout.addWidget(self.unquantized_canvas)

        self.populate_playlist_pattern_combo()
        return widget

    def populate_playlist_pattern_combo(self):
        self.playlist_pattern_combo.blockSignals(True)
        self.playlist_pattern_combo.clear()
        inst = self.playlist_instrument_combo.currentText()
        if inst in self.instrument_sequences:
            for idx, seq in enumerate(self.instrument_sequences[inst]):
                self.playlist_pattern_combo.addItem(f"Pattern {idx+1}: {seq['name']}", idx)
        self.playlist_pattern_combo.blockSignals(False)

    def add_unquantized_clip(self):
        inst = self.playlist_instrument_combo.currentText()
        pat_idx = self.playlist_pattern_combo.currentData()
        if pat_idx is None: pat_idx = 0
        self.unquantized_canvas.add_clip(inst, pat_idx, x=50.0, y=float(random.randint(0, 3) * 65 + 40))

    def trigger_unique_playlist_randomization(self):
        inst_list = list(self.instrument_sequences.keys())
        self.unquantized_canvas.randomize_unique_playlist(inst_list, self.instrument_sequences)
        QMessageBox.information(self, "Playlist Randomized", "Successfully generated a unique unquantized playlist with randomized timestretch, pitch, and amplitude per instance.")

    def create_mdi_suite_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        self.mdi_area = QMdiArea()
        self.spawn_subwindow("VST Engine 01", self.create_vst_engine_content("VST_Engine_01"), 20, 20)
        self.spawn_subwindow("VST Engine 02", self.create_vst_engine_content("VST_Engine_02"), 440, 20)
        layout.addWidget(self.mdi_area)

        # Large and Green Spawn Button at the bottom of the MDI tab as requested
        btn_spawn_large_green = QPushButton("SPAWN NEW VST MODULE ENGINE")
        btn_spawn_large_green.setMinimumHeight(65)
        btn_spawn_large_green.setStyleSheet("background-color: #238636; color: white; font-size: 18px; font-weight: bold; border-radius: 8px;")
        btn_spawn_large_green.clicked.connect(self.spawn_additional_mdi_engine)
        layout.addWidget(btn_spawn_large_green)

        return widget

    def spawn_additional_mdi_engine(self):
        mod_name, ok = QInputDialog.getText(self, "Spawn MDI VST Engine", "Enter new MDI engine name:")
        if not ok or not mod_name.strip(): return
        self.spawn_subwindow(mod_name, self.create_vst_engine_content(mod_name), random.randint(30, 150), random.randint(30, 150))

    def spawn_subwindow(self, title, content_widget, x, y):
        sub = QMdiSubWindow()
        sub.setWidget(content_widget)
        sub.setWindowTitle(title)
        sub.resize(430, 440)
        sub.move(x, y)
        self.mdi_area.addSubWindow(sub)
        sub.show()

    def create_vst_engine_content(self, engine_name):
        w = QWidget(); l = QVBoxLayout(w)
        wavetable_widget = LiveDrawableWavetableWidget(engine_name, self)
        l.addWidget(wavetable_widget)

        knobs_layout1 = QHBoxLayout()
        k1 = ModularBayKnob("Osc Drive", 0.0, 10.0, random.uniform(1.0, 5.0), "Drv", self)
        k2 = ModularBayKnob("Wavetable", 0.0, 1.0, random.uniform(0.2, 0.8), "Wav", self)
        k3 = ModularBayKnob("Vector Skew", -1.0, 1.0, random.uniform(-0.5, 0.5), "Skw", self)
        knobs_layout1.addWidget(k1); knobs_layout1.addWidget(k2); knobs_layout1.addWidget(k3)
        l.addLayout(knobs_layout1)

        return w


if __name__ == "__main__":
    app = QApplication(sys.argv)
    suite = EQRGrooveboxUltimateSuite()
    suite.show()
    sys.exit(app.exec())

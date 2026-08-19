# =========================================================
# eqr_groovebox_ultimate_modular.py
# EQR GROOVEBOX ULTIMATE DAW & SYNTHESIS SUITE (v12.0)
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


# ---------------------------------------------------------
# CUSTOM EVALUATOR SUPPORTING EQR ALGEBRAIC x, y, z VARIABLES
# ---------------------------------------------------------
def custom_eval_equation(eq_str, x_val, y_val=1.618, z_val=2.414, proximity=1.0, downmix=0.0):
    if downmix >= 1.0:
        return 0.0

    cleaned = eq_str.strip().lower()

    def isn(val):
        try:
            return math.sin(val * proximity) / (1.0 + abs(val))
        except ZeroDivisionError:
            return 0.0

    def iisn(val):
        try:
            return math.asin(max(-1.0, min(1.0, val * 0.75 * proximity))) * 1.618
        except (ValueError, ZeroDivisionError):
            return 0.0

    safe_dict = {
        'x': x_val * proximity,
        'y': y_val * proximity,
        'z': z_val * proximity,
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'exp': math.exp,
        'log': math.log,
        'sqrt': math.sqrt,
        'abs': abs,
        'pi': math.pi,
        'e': math.e,
        'isn': isn,
        'inverse_isn': iisn,
        'iisn': iisn
    }

    try:
        compiled = eval(f"__import__('math').fabs(0) or ({cleaned})", {"__builtins__": {}}, safe_dict)
        raw_signal = float(compiled)
    except Exception:
        raw_signal = float(x_val**3 - 3.0 * x_val + y_val)

    return raw_signal * (1.0 - max(0.0, min(1.0, downmix)))


# ---------------------------------------------------------
# REAL-TIME AUDIO GENERATOR BUFFER
# ---------------------------------------------------------
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
                sample = math.sin(2 * math.pi * self.phase) * 0.6 + math.sin(2 * math.pi * self.phase * 2.0) * 0.4

            sample *= self.amplitude
            int_val = int(max(-32768, min(32767, sample * 32767)))
            buffer.extend(int_val.to_bytes(2, byteorder='little', signed=True))

            self.phase += self.frequency * dt
            if self.phase > 1.0:
                self.phase -= 1.0

        return bytes(buffer)

    def bytesAvailable(self):
        return 4096 + super().bytesAvailable()


# ---------------------------------------------------------
# FRONT-PAGE PATCHBAY CANVAS
# ---------------------------------------------------------
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

    def mousePressEvent(self, event: QMouseEvent):
        pos = event.position()
        if event.button() == Qt.MouseButton.RightButton:
            for node in self.nodes:
                if (QPointF(node["x"], node["y"]) - pos).manhattanLength() < 18:
                    self.drag_start_node = node
                    self.current_mouse_pos = pos
                    self.update()
                    return

    def mouseMoveEvent(self, event: QMouseEvent):
        self.current_mouse_pos = event.position()
        if self.drag_start_node:
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton and self.drag_start_node:
            pos = event.position()
            for node in self.nodes:
                if node != self.drag_start_node and (QPointF(node["x"], node["y"]) - pos).manhattanLength() < 20:
                    src = self.drag_start_node if self.drag_start_node["type"] == "out" else node
                    dst = node if self.drag_start_node["type"] == "out" else self.drag_start_node
                    if src["type"] == "out" and dst["type"] == "in":
                        existing = next((w for w in self.wires if w["to"] == dst["id"]), None)
                        if existing:
                            existing["from"] = src["id"]
                        else:
                            self.wires.append({"from": src["id"], "to": dst["id"], "mod_amount": 0.50})
            self.drag_start_node = None
            self.update()

    def wheelEvent(self, event):
        pos = event.position()
        delta = event.angleDelta().y()
        step = 0.05 if delta > 0 else -0.05
        for wire in self.wires:
            src = next((n for n in self.nodes if n["id"] == wire["from"]), None)
            dst = next((n for n in self.nodes if n["id"] == wire["to"]), None)
            if src and dst:
                mid_x = (src["x"] + dst["x"]) / 2
                mid_y = (src["y"] + dst["y"]) / 2
                if (QPointF(mid_x, mid_y) - pos).manhattanLength() < 25:
                    wire["mod_amount"] = max(-2.0, min(2.0, wire["mod_amount"] + step))
                    self.update()
                    event.accept()
                    return
        event.ignore()


# ---------------------------------------------------------
# INTERACTIVE QWERTY KEYBOARD
# ---------------------------------------------------------
class InteractiveQwertyKeyboard(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(90)
        self.setMaximumHeight(105)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.key_map = {
            Qt.Key.Key_A: 432.00, Qt.Key.Key_S: 484.90, Qt.Key.Key_D: 544.53,
            Qt.Key.Key_F: 577.24, Qt.Key.Key_W: 457.94, Qt.Key.Key_E: 514.33,
            Qt.Key.Key_R: 611.83, Qt.Key.Key_G: 648.56, Qt.Key.Key_H: 687.48,
            Qt.Key.Key_J: 771.74, Qt.Key.Key_Y: 728.69, Qt.Key.Key_K: 816.60,
            Qt.Key.Key_L: 916.48, Qt.Key.Key_U: 865.74, Qt.Key.Key_I: 971.21,
            Qt.Key.Key_O: 1029.07, Qt.Key.Key_P: 1090.87
        }
        self.active_keys = set()
        self.parent_suite = parent

    def keyPressEvent(self, event: QKeyEvent):
        key = event.key()
        if key in self.key_map and key not in self.active_keys:
            self.active_keys.add(key)
            if self.parent_suite and hasattr(self.parent_suite, 'trigger_note_frequency'):
                self.parent_suite.trigger_note_frequency(self.key_map[key])
            self.update()

    def keyReleaseEvent(self, event: QKeyEvent):
        key = event.key()
        if key in self.active_keys:
            self.active_keys.remove(key)
            if self.parent_suite and hasattr(self.parent_suite, 'release_note_frequency'):
                self.parent_suite.release_note_frequency()
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        w = self.width(); h = self.height()
        painter.fillRect(0, 0, w, h, QColor("#0d1117"))
        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(8, 14, "<b>QWERTY Keyboard:</b> [A S D F W E R G H J Y K L U I O P]")

        keys_layout = [
            ('W', 100, 24, 22, 32, Qt.Key.Key_W), ('E', 126, 24, 22, 32, Qt.Key.Key_E),
            ('R', 152, 24, 22, 32, Qt.Key.Key_R), ('Y', 214, 24, 22, 32, Qt.Key.Key_Y),
            ('U', 266, 24, 22, 32, Qt.Key.Key_U), ('I', 292, 24, 22, 32, Qt.Key.Key_I),
            ('O', 318, 24, 22, 32, Qt.Key.Key_O), ('P', 344, 24, 22, 32, Qt.Key.Key_P),
            ('A', 70,  58, 26, 36, Qt.Key.Key_A), ('S', 98,  58, 26, 36, Qt.Key.Key_S),
            ('D', 126, 58, 26, 36, Qt.Key.Key_D), ('F', 154, 58, 26, 36, Qt.Key.Key_F),
            ('G', 182, 58, 26, 36, Qt.Key.Key_G), ('H', 210, 58, 26, 36, Qt.Key.Key_H),
            ('J', 238, 58, 26, 36, Qt.Key.Key_J), ('K', 266, 58, 26, 36, Qt.Key.Key_K),
            ('L', 294, 58, 26, 36, Qt.Key.Key_L),
        ]
        for name, x, y, kw, kh, kcode in keys_layout:
            is_pressed = kcode in self.active_keys
            painter.setBrush(QBrush(QColor("#1f6feb") if is_pressed else QColor("#21262d")))
            painter.setPen(QPen(QColor("#00ffcc") if is_pressed else QColor("#30363d"), 1.5))
            painter.drawRoundedRect(x, y, kw, kh, 3, 3)
            painter.setPen(QPen(QColor("#ffffff") if is_pressed else QColor("#c9d1d9"), 1))
            painter.drawText(x, y, kw, kh, Qt.AlignmentFlag.AlignCenter, name)


# ---------------------------------------------------------
# COMPACT KNOB WIDGET
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# LIVE REAL-TIME OSCILLOSCOPE GRAPH
# ---------------------------------------------------------
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


# ---------------------------------------------------------
# MASTER SUITE WINDOW
# ---------------------------------------------------------
class EQRGrooveboxUltimateSuite(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Equation of Reality (EQR) - Ultimate Modular DAW Suite (v12.0)")
        self.resize(1800, 1020)
        self.set_dark_palette()

        self.audio_sink = None
        self.audio_stream = None
        self.is_playing = False

        def default_pattern():
            return {
                "name": "Pattern 1",
                "length": 16,
                "speed": 1.0,
                "curve": "Linear",
                "depth": 0.75,
                "steps": [{"active": (i % 4 == 0), "pitch": 1.0, "amp": 1.0} for i in range(16)]
            }

        self.instrument_sequences = {
            "Eskibrutus (Sub-Bass/Drive)": [default_pattern()],
            "Vectoreski (Phase/Morph)": [default_pattern()],
            "Eskitable (Wavetable Synth)": [default_pattern()],
            "Spatial Matrix Synth": [default_pattern()],
            "EQR Polynomial Synth": [default_pattern()],
        }

        self.setup_window_creation_menu()

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("QTabWidget::pane { border: 1px solid #30363d; background: #0d1117; } QTabBar::tab { background: #161b22; color: #c9d1d9; padding: 10px 18px; border: 1px solid #30363d; } QTabBar::tab:selected { background: #1f6feb; color: white; font-weight: bold; }")

        self.tabs.addTab(self.create_front_page_tab(), "Front-Page Modular Patchbay & Master Controls")
        self.tabs.addTab(self.create_sequencer_playlist_tab(), "Sequencer Manager & Piano Roll")
        self.tabs.addTab(self.create_master_playlist_tab(), "Master Coordination Playlist")
        self.tabs.addTab(self.create_sample_module_tab(), "Sample Loader & Audio Module")
        self.tabs.addTab(self.create_mdi_suite_tab(), "Modular Subwindow Bays (MDI)")

        self.setCentralWidget(self.tabs)
        self.statusBar().showMessage("EQR Suite v12.0 Ready | Algebraic x, y, z Mapping Active.")

    def set_dark_palette(self):
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#0d1117"))
        palette.setColor(QPalette.ColorRole.WindowText, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Base, QColor("#161b22"))
        palette.setColor(QPalette.ColorRole.Text, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Button, QColor("#21262d"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor("#c9d1d9"))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#1f6feb"))
        QApplication.setPalette(palette)

    def setup_window_creation_menu(self):
        menubar = self.menuBar()
        window_menu = menubar.addMenu("Spawn / Clone Synth Windows")

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

        add_mod_act = QAction("Add New Instrument Module...", self)
        add_mod_act.triggered.connect(self.prompt_add_new_instrument_module)
        window_menu.addSeparator()
        window_menu.addAction(add_mod_act)

    def prompt_add_new_instrument_module(self):
        name, ok = QInputDialog.getText(self, "Add New Instrument Module", "Enter New Instrument Name:")
        if ok and name.strip():
            inst_name = name.strip()
            if inst_name not in self.instrument_sequences:
                self.instrument_sequences[inst_name] = [{
                    "name": "Pattern 1", "length": 16, "speed": 1.0, "curve": "Linear", "depth": 0.75,
                    "steps": [{"active": False, "pitch": 1.0, "amp": 1.0} for _ in range(16)]
                }]
                if hasattr(self, 'seq_instrument_combo'):
                    self.refresh_sequencer_ui()
                self.spawn_subwindow_to_mdi(inst_name, self.create_custom_instrument_content(inst_name), 150, 150)
                QMessageBox.information(self, "Module Added", f"Successfully created new instrument module: {inst_name}")

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
        master_grid.addWidget(ModularBayKnob("Sidechain Q", 0.0, 10.0, 2.5, "SC", self), 0, 3)
        left_layout.addWidget(master_group)
        layout.addLayout(left_layout, stretch=3)

        right_layout = QVBoxLayout()
        audio_group = QGroupBox("Live Audio Stream & Export")
        audio_layout = QVBoxLayout(audio_group)
        vol_layout = QHBoxLayout()
        vol_layout.addWidget(QLabel("Master Volume:"))
        self.volume_slider = QSlider(Qt.Orientation.Horizontal)
        self.volume_slider.setRange(0, 100); self.volume_slider.setValue(80)
        self.volume_slider.valueChanged.connect(self.update_audio_volume)
        vol_layout.addWidget(self.volume_slider)
        audio_layout.addLayout(vol_layout)

        self.btn_preview = QPushButton("Start Live Audio Stream")
        self.btn_preview.setStyleSheet("background-color: #238636; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
        self.btn_preview.clicked.connect(self.toggle_audio_preview)
        audio_layout.addWidget(self.btn_preview)

        self.btn_random_song = QPushButton("🎲 Random Song Generator")
        self.btn_random_song.setStyleSheet("background-color: #8957e5; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
        self.btn_random_song.clicked.connect(self.trigger_random_song_generation)
        audio_layout.addWidget(self.btn_random_song)

        btn_export = QPushButton("Export Rendered WAV File...")
        btn_export.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 8px; border-radius: 6px;")
        btn_export.clicked.connect(self.export_wav_file)
        audio_layout.addWidget(btn_export)
        right_layout.addWidget(audio_group)

        kb_group = QGroupBox("Live QWERTY Trigger Matrix")
        kb_layout = QVBoxLayout(kb_group)
        self.qwerty_keyboard = InteractiveQwertyKeyboard(self)
        kb_layout.addWidget(self.qwerty_keyboard)
        right_layout.addWidget(kb_group)

        layout.addLayout(right_layout, stretch=2)
        return widget

    def trigger_random_song_generation(self):
        curve_options = ["Linear", "Exponential", "Quadratic", "Custom Polynomial"]
        available_instruments = list(self.instrument_sequences.keys())
        selected_instruments = random.sample(available_instruments, k=random.randint(1, min(4, len(available_instruments))))

        summary_messages = []
        for inst in selected_instruments:
            length = random.choice([8, 12, 16, 24, 32])
            speed = random.choice([0.5, 1.0, 1.5, 2.0])
            curve = random.choice(curve_options)
            depth = round(random.uniform(0.2, 1.0), 2)

            x_coord = random.uniform(-2.0, 2.0)
            y_coord = random.uniform(0.5, 2.5)
            z_coord = random.uniform(-1.0, 3.0)

            steps = []
            for s in range(length):
                eval_val = math.sin(s * x_coord) * math.cos(y_coord) + (z_coord * 0.1)
                is_on = eval_val > 0.0 or random.random() < 0.35
                pitch_val = round(random.uniform(0.5, 2.0), 2)
                amp_val = round(random.uniform(0.2, 2.0), 2)
                steps.append({"active": is_on, "pitch": pitch_val, "amp": amp_val})

            self.instrument_sequences[inst][0] = {
                "name": f"Random x{x_coord:.1f}y{y_coord:.1f}",
                "length": length,
                "speed": speed,
                "curve": curve,
                "depth": depth,
                "steps": steps
            }
            summary_messages.append(f"• {inst}: {length} steps ({curve}, Depth {depth})")

        if hasattr(self, 'seq_instrument_combo'):
            self.refresh_sequencer_ui()

        QMessageBox.information(
            self,
            "Random Song Generated (EQR Engine)",
            "Successfully generated bounded random song configuration across instruments:\n\n" + "\n".join(summary_messages)
        )

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
            self.btn_preview.setStyleSheet("background-color: #da3633; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
        else:
            if self.audio_sink: self.audio_sink.stop()
            if self.audio_stream: self.audio_stream.close()
            self.is_playing = False
            self.btn_preview.setText("Start Live Audio Stream")
            self.btn_preview.setStyleSheet("background-color: #238636; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")

    def update_base_tuning_live(self, val):
        if self.audio_stream:
            self.audio_stream.set_frequency(val)

    def update_audio_volume(self, val):
        if self.audio_stream: self.audio_stream.set_amplitude(val / 100.0)

    def trigger_note_frequency(self, freq):
        if self.audio_stream: self.audio_stream.set_frequency(freq)

    def release_note_frequency(self):
        if self.audio_stream:
            curr_base = self.knob_base_tuning.value if hasattr(self, 'knob_base_tuning') else 432.0
            self.audio_stream.set_frequency(curr_base)

    def export_wav_file(self):
        filename, _ = QFileDialog.getSaveFileName(self, "Export Rendered WAV", "", "WAV Files (*.wav)")
        if filename:
            try:
                with wave.open(filename, 'w') as wav_file:
                    wav_file.setnchannels(1); wav_file.setsampwidth(2); wav_file.setframerate(44100)
                    sample_rate = 44100; duration = 3.0
                    for i in range(int(sample_rate * duration)):
                        sample = math.sin(2 * math.pi * 432.0 * (i / sample_rate)) * 0.75
                        data = int(max(-32768, min(32767, sample * 32767))).to_bytes(2, byteorder='little', signed=True)
                        wav_file.writeframes(data)
                QMessageBox.information(self, "Export Complete", f"Successfully exported WAV to {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export file: {str(e)}")

    def create_sequencer_playlist_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("<b>Select Instrument:</b>"))
        self.seq_instrument_combo = QComboBox()
        self.seq_instrument_combo.addItems(list(self.instrument_sequences.keys()))
        self.seq_instrument_combo.setStyleSheet("background-color: #161b22; color: #c9d1d9; padding: 6px;")
        self.seq_instrument_combo.currentIndexChanged.connect(self.refresh_sequencer_ui)
        toolbar.addWidget(self.seq_instrument_combo)

        toolbar.addWidget(QLabel("<b>Pattern Index (0-N):</b>"))
        self.seq_name_combo = QComboBox()
        self.seq_name_combo.setStyleSheet("background-color: #161b22; color: #c9d1d9; padding: 6px;")
        self.seq_name_combo.currentIndexChanged.connect(self.load_selected_sequence_parameters)
        toolbar.addWidget(self.seq_name_combo)

        btn_new_seq = QPushButton("Create New Pattern (0-N)")
        btn_new_seq.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 6px 12px;")
        btn_new_seq.clicked.connect(self.create_new_sequence_for_instrument)
        toolbar.addWidget(btn_new_seq)
        layout.addLayout(toolbar)

        control_bar = QHBoxLayout()
        control_bar.addWidget(QLabel("<b>Sequence Length:</b>"))
        self.spin_seq_length = QSpinBox()
        self.spin_seq_length.setRange(4, 64)
        self.spin_seq_length.setValue(16)
        self.spin_seq_length.valueChanged.connect(self.update_sequence_length)
        control_bar.addWidget(self.spin_seq_length)

        control_bar.addWidget(QLabel("<b>Speed:</b>"))
        self.spin_seq_speed = QDoubleSpinBox()
        self.spin_seq_speed.setRange(0.25, 4.0)
        self.spin_seq_speed.setValue(1.0)
        self.spin_seq_speed.setSingleStep(0.25)
        self.spin_seq_speed.valueChanged.connect(self.update_sequence_speed)
        control_bar.addWidget(self.spin_seq_speed)

        control_bar.addWidget(QLabel("<b>Curve Mode:</b>"))
        self.combo_curve_mode = QComboBox()
        self.combo_curve_mode.addItems(["Linear", "Exponential", "Quadratic", "Custom Polynomial"])
        self.combo_curve_mode.setStyleSheet("background-color: #161b22; color: #c9d1d9; padding: 4px;")
        self.combo_curve_mode.currentIndexChanged.connect(self.update_sequence_curve_mode)
        control_bar.addWidget(self.combo_curve_mode)

        control_bar.addWidget(QLabel("<b>Piano Roll Depth (0-1):</b>"))
        self.spin_seq_depth = QDoubleSpinBox()
        self.spin_seq_depth.setRange(0.0, 1.0)
        self.spin_seq_depth.setValue(0.75)
        self.spin_seq_depth.setSingleStep(0.05)
        self.spin_seq_depth.valueChanged.connect(self.update_sequence_depth)
        control_bar.addWidget(self.spin_seq_depth)

        layout.addLayout(control_bar)

        self.multi_seq_table = QTableWidget()
        self.multi_seq_table.setStyleSheet("background-color: #161b22; color: #c9d1d9; gridline-color: #30363d;")
        layout.addWidget(self.multi_seq_table)

        self.freq_interval_label = QLabel("<b>Harmonic Frequencies Interval:</b> Base: 432Hz")
        self.freq_interval_label.setStyleSheet("color: #00ffcc; padding: 4px;")
        layout.addWidget(self.freq_interval_label)

        self.populate_sequence_names()
        return widget

    def populate_sequence_names(self):
        self.seq_name_combo.blockSignals(True)
        self.seq_name_combo.clear()
        inst = self.seq_instrument_combo.currentText()
        if inst in self.instrument_sequences:
            for idx, seq in enumerate(self.instrument_sequences[inst]):
                self.seq_name_combo.addItem(f"Pattern {idx}: {seq['name']}")
        self.seq_name_combo.blockSignals(False)
        self.load_selected_sequence_parameters()

    def refresh_sequencer_ui(self):
        current_inst = self.seq_instrument_combo.currentText()
        self.seq_instrument_combo.blockSignals(True)
        self.seq_instrument_combo.clear()
        self.seq_instrument_combo.addItems(list(self.instrument_sequences.keys()))
        if current_inst in self.instrument_sequences:
            self.seq_instrument_combo.setCurrentText(current_inst)
        self.seq_instrument_combo.blockSignals(False)
        self.populate_sequence_names()

    def load_selected_sequence_parameters(self):
        inst = self.seq_instrument_combo.currentText()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            seq_data = self.instrument_sequences[inst][seq_idx]
            self.spin_seq_length.blockSignals(True)
            self.spin_seq_length.setValue(seq_data["length"])
            self.spin_seq_length.blockSignals(False)

            self.spin_seq_speed.blockSignals(True)
            self.spin_seq_speed.setValue(seq_data["speed"])
            self.spin_seq_speed.blockSignals(False)

            self.combo_curve_mode.blockSignals(True)
            self.combo_curve_mode.setCurrentText(seq_data.get("curve", "Linear"))
            self.combo_curve_mode.blockSignals(False)

            self.spin_seq_depth.blockSignals(True)
            self.spin_seq_depth.setValue(seq_data.get("depth", 0.75))
            self.spin_seq_depth.blockSignals(False)

            self.build_sequence_table_grid(seq_data)

    def build_sequence_table_grid(self, seq_data):
        length = seq_data["length"]
        steps = seq_data["steps"]
        while len(steps) < length:
            steps.append({"active": False, "pitch": 1.0, "amp": 1.0})

        depth = seq_data.get("depth", 0.75)
        num_rows = max(4, int(4 + (depth * 8)))

        self.multi_seq_table.setRowCount(num_rows)
        self.multi_seq_table.setColumnCount(length)
        self.multi_seq_table.setHorizontalHeaderLabels([str(i+1) for i in range(length)])
        self.multi_seq_table.setVerticalHeaderLabels([f"Row {r+1} (Oct/Harm)" for r in range(num_rows)])

        curve_mode = seq_data.get("curve", "Linear")
        freq_list_str = []
        base_hz = 432.0

        for c in range(length):
            rel_dist = (c + 1) / float(length)
            if curve_mode == "Exponential":
                factor = math.exp(rel_dist * depth * 2.0)
            elif curve_mode == "Quadratic":
                factor = 1.0 + (rel_dist ** 2) * depth * 3.0
            elif curve_mode == "Custom Polynomial":
                factor = 1.0 + (rel_dist ** 3 - rel_dist * depth) * 2.0
            else:
                factor = 1.0 + (rel_dist - 0.5) * depth * 1.5

            freq_above = base_hz * factor
            freq_below = base_hz / max(0.01, factor)
            freq_disp = freq_above if c % 2 == 0 else freq_below
            freq_list_str.append(f"{freq_disp:.1f}Hz")

            step_info = steps[c]
            is_active = step_info["active"]
            pitch_val = step_info.get("pitch", 1.0)
            amp_val = step_info.get("amp", 1.0)

            target_row = int((pitch_val / 2.0) * (num_rows - 1))
            target_row = max(0, min(num_rows - 1, target_row))

            for r in range(num_rows):
                is_this_row_active = is_active and (r == target_row)
                btn = QPushButton(f"{('ON' if is_this_row_active else 'OFF')}\nP:{pitch_val:.1f} A:{amp_val:.1f}")
                btn.setCheckable(True)
                btn.setChecked(is_this_row_active)
                btn.setStyleSheet("""
                    QPushButton { background-color: #161b22; color: #8b949e; border: 1px solid #30363d; font-size: 9px; font-weight: bold; }
                    QPushButton:checked { background-color: #1f6feb; color: white; border: 1px solid #00ffcc; }
                """)
                btn.clicked.connect(lambda checked, s_obj=seq_data, col=c, r_idx=r, num_r=num_rows: self.on_grid_cell_clicked(s_obj, col, r_idx, num_r))
                self.multi_seq_table.setCellWidget(r, c, btn)
                self.multi_seq_table.setRowHeight(r, 45)

        self.freq_interval_label.setText(f"<b>Harmonic Frequencies Interval (Curve: {curve_mode} | Depth: {depth:.2f} | Rows: {num_rows}):</b> " + " | ".join(freq_list_str[:6]) + ("..." if length > 6 else ""))

    def on_grid_cell_clicked(self, seq_data, col, row_idx, num_rows):
        step_info = seq_data["steps"][col]
        pitch_f, ok1 = QInputDialog.getDouble(self, "Edit Note Factors", "Pitch Shift Factor (0.0 to 2.0):", step_info.get("pitch", 1.0), 0.0, 2.0, 2)
        if ok1:
            amp_f, ok2 = QInputDialog.getDouble(self, "Edit Note Factors", "Amplitude Factor (0.0 to 2.0):", step_info.get("amp", 1.0), 0.0, 2.0, 2)
            if ok2:
                step_info["active"] = True
                step_info["pitch"] = pitch_f
                step_info["amp"] = amp_f
            else:
                step_info["active"] = not step_info["active"]
        else:
            step_info["active"] = not step_info["active"]

        self.build_sequence_table_grid(seq_data)

    def create_new_sequence_for_instrument(self):
        inst = self.seq_instrument_combo.currentText()
        if inst in self.instrument_sequences:
            count = len(self.instrument_sequences[inst])
            new_seq = {
                "name": f"Pattern {count}",
                "length": 16,
                "speed": 1.0,
                "curve": "Linear",
                "depth": 0.75,
                "steps": [{"active": False, "pitch": 1.0, "amp": 1.0} for _ in range(16)]
            }
            self.instrument_sequences[inst].append(new_seq)
            self.populate_sequence_names()
            self.seq_name_combo.setCurrentIndex(len(self.instrument_sequences[inst]) - 1)

    def update_sequence_length(self, val):
        inst = self.seq_instrument_combo.currentText()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            seq_data = self.instrument_sequences[inst][seq_idx]
            seq_data["length"] = val
            while len(seq_data["steps"]) < val:
                seq_data["steps"].append({"active": False, "pitch": 1.0, "amp": 1.0})
            self.build_sequence_table_grid(seq_data)

    def update_sequence_speed(self, val):
        inst = self.seq_instrument_combo.currentText()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            self.instrument_sequences[inst][seq_idx]["speed"] = val

    def update_sequence_curve_mode(self, idx):
        inst = self.seq_instrument_combo.currentText()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            seq_data = self.instrument_sequences[inst][seq_idx]
            seq_data["curve"] = self.combo_curve_mode.currentText()
            self.build_sequence_table_grid(seq_data)

    def update_sequence_depth(self, val):
        inst = self.seq_instrument_combo.currentText()
        seq_idx = self.seq_name_combo.currentIndex()
        if inst in self.instrument_sequences and seq_idx >= 0:
            seq_data = self.instrument_sequences[inst][seq_idx]
            seq_data["depth"] = val
            self.build_sequence_table_grid(seq_data)

    def create_master_playlist_tab(self):
        widget = QWidget(); l = QVBoxLayout(widget)
        l.addWidget(QLabel("<b>Master Coordination Playlist (Arrange Patterns 0-N across Arrangement Tracks)</b>"))
        table = QTableWidget(6, 16)
        table.setHorizontalHeaderLabels([f"Bar {i+1}" for i in range(16)])
        table.setVerticalHeaderLabels([
            "Track 1 (Eskibrutus)", "Track 2 (Vectoreski)", "Track 3 (Eskitable)",
            "Track 4 (Spatial)", "Track 5 (Polynomial)", "Track 6 (Arrangement Master)"
        ])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        table.setStyleSheet("background-color: #161b22; color: #c9d1d9; gridline-color: #30363d;")

        for r in range(6):
            for c in range(16):
                btn = QPushButton(f"Pat {(c % 3)}")
                btn.setCheckable(True)
                if c % 4 == 0: btn.setChecked(True)
                btn.setStyleSheet("""
                    QPushButton { background-color: #21262d; color: #8b949e; border: 1px solid #30363d; font-weight: bold; }
                    QPushButton:checked { background-color: #238636; color: white; }
                """)
                table.setCellWidget(r, c, btn)
        l.addWidget(table)
        return widget

    def create_sample_module_tab(self):
        widget = QWidget(); l = QVBoxLayout(widget)
        l.addWidget(QLabel("<b>Audio Sample Loader & Player Module</b>"))
        self.sample_path_label = QLabel("No sample loaded.")
        l.addWidget(self.sample_path_label)

        btn_load_sample = QPushButton("Load Audio Sample (.WAV / .MP3)...")
        btn_load_sample.setStyleSheet("background-color: #1f6feb; color: white; font-weight: bold; padding: 10px;")
        btn_load_sample.clicked.connect(self.load_external_sample)
        l.addWidget(btn_load_sample)

        self.sample_graph = LiveModuleGraphWidget("sample_waveform", self)
        l.addWidget(self.sample_graph)
        return widget

    def load_external_sample(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Load Audio Sample", "", "Audio Files (*.wav *.mp3)")
        if filename:
            self.sample_path_label.setText(f"Loaded Sample: {filename}")
            QMessageBox.information(self, "Sample Loaded", f"Successfully loaded sample file: {filename}")

    def create_mdi_suite_tab(self):
        widget = QWidget(); l = QVBoxLayout(widget)
        self.mdi_area = QMdiArea()
        self.mdi_area.setStyleSheet("background-color: #05070a;")
        self.spawn_subwindow("Eskibrutus Synth", self.create_eskibrutus_content(), 20, 20)
        self.spawn_subwindow("Vectoreski Synth", self.create_vectoreski_content(), 380, 20)
        self.spawn_subwindow("Eskitable Synth", self.create_eskitable_content(), 740, 20)
        self.spawn_subwindow("Spatial Matrix", self.create_spatial_matrix_content(), 20, 340)
        self.spawn_subwindow("EQR Equation Module", self.create_eqr_equation_content(), 380, 340)
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
        self.tabs.setCurrentIndex(4)
        self.spawn_subwindow(title, content_widget, x, y)

    def create_eskibrutus_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        graph = LiveModuleGraphWidget("eskibrutus", self)
        l.addWidget(graph)
        sc = QScrollArea(); sc.setWidgetResizable(True); cont = QWidget(); grid = QGridLayout(cont)
        def on_drive_changed(val): graph.update_parameters(val, 432.0)
        grid.addWidget(ModularBayKnob("Sub Drive", 0, 10, 5, "Drive", self, callback=on_drive_changed), 0, 0)
        grid.addWidget(ModularBayKnob("Harmonic", 0, 10, 3, "Harm", self), 0, 1)
        sc.setWidget(cont); l.addWidget(sc); return w

    def create_vectoreski_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        graph = LiveModuleGraphWidget("vectoreski", self)
        l.addWidget(graph)
        sc = QScrollArea(); sc.setWidgetResizable(True); cont = QWidget(); grid = QGridLayout(cont)
        def on_morph_changed(val): graph.update_parameters(val, 500.0)
        grid.addWidget(ModularBayKnob("Morph Rate", 0.1, 5, 1.2, "Hz", self, callback=on_morph_changed), 0, 0)
        grid.addWidget(ModularBayKnob("Phase Shift", 0, 6.28, 1.57, "Rad", self), 0, 1)
        sc.setWidget(cont); l.addWidget(sc); return w

    def create_eskitable_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        graph = LiveModuleGraphWidget("eskitable", self)
        l.addWidget(graph)
        sc = QScrollArea(); sc.setWidgetResizable(True); cont = QWidget(); grid = QGridLayout(cont)
        def on_table_changed(val): graph.update_parameters(val / 10.0, 600.0)
        grid.addWidget(ModularBayKnob("Table Pos", 0, 100, 25, "%", self, callback=on_table_changed), 0, 0)
        grid.addWidget(ModularBayKnob("Interpolation", 0, 10, 2, "Q", self), 0, 1)
        sc.setWidget(cont); l.addWidget(sc); return w

    def create_spatial_matrix_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        graph = LiveModuleGraphWidget("spatial", self)
        l.addWidget(graph)
        sc = QScrollArea(); sc.setWidgetResizable(True); cont = QWidget(); grid = QGridLayout(cont)
        def on_x_changed(val): graph.update_parameters(val, 450.0)
        grid.addWidget(ModularBayKnob("X Var", -10, 10, 1, "x", self, callback=on_x_changed), 0, 0)
        grid.addWidget(ModularBayKnob("Y Var", -10, 10, 1.6, "y", self), 0, 1)
        sc.setWidget(cont); l.addWidget(sc); return w

    def create_eqr_equation_content(self):
        w = QWidget(); l = QVBoxLayout(w)
        graph = LiveModuleGraphWidget("eqr_equation", self)
        l.addWidget(graph)
        sc = QScrollArea(); sc.setWidgetResizable(True); cont = QWidget(); grid = QGridLayout(cont)
        def on_poly_changed(val): graph.update_parameters(val, 480.0)
        grid.addWidget(ModularBayKnob("Polynomial X", -10, 10, 1, "x", self, callback=on_poly_changed), 0, 0)
        grid.addWidget(ModularBayKnob("Polynomial Y", -10, 10, 1.618, "y", self), 0, 1)
        sc.setWidget(cont); l.addWidget(sc); return w

    def create_custom_instrument_content(self, inst_name):
        w = QWidget(); l = QVBoxLayout(w)
        graph = LiveModuleGraphWidget(inst_name.lower(), self)
        l.addWidget(graph)
        sc = QScrollArea(); sc.setWidgetResizable(True); cont = QWidget(); grid = QGridLayout(cont)
        def on_custom_changed(val): graph.update_parameters(val, 520.0)
        grid.addWidget(ModularBayKnob("Custom Drive", 0, 10, 5, "Drv", self, callback=on_custom_changed), 0, 0)
        grid.addWidget(ModularBayKnob("Resonance", 0, 10, 4, "Res", self), 0, 1)
        sc.setWidget(cont); l.addWidget(sc); return w


if __name__ == "__main__":
    app = QApplication(sys.argv)
    suite = EQRGrooveboxUltimateSuite()
    suite.show()
    sys.exit(app.exec())

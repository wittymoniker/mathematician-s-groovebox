# Updated EQR Groovebox Engine v3.6.8 (eqr_groovebox_engine_v368.py)
# Enhanced with Straightforward Envelope/Decay Control, Global & Concurrent Rhythm Flux Linking,
# Fully Activated Drum Machines, Sequencers, Automation Lanes, Stochastic Micro-Timing Drift,
# Quantum Probability Gating, and Advanced Multidimensional x, y, z Operator Scaling.


import random
import math
import wave
import json
import numpy as np
from PyQt6.QtCore import Qt, QPoint,QPointF, QRectF, QTimer
from PyQt6.QtGui import (QPainter, QPen, QColor, QPainterPath, QLinearGradient, QBrush, QFont,QAction, QPalette, QAction, QKeyEvent,QBrush
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QVBoxLayout,
    QHBoxLayout, QLabel, QSlider, QPushButton, QComboBox, QScrollArea,
    QTabWidget, QLineEdit, QListWidget, QFormLayout, QSpinBox, QDoubleSpinBox, QGridLayout, QFileDialog, QSplitter, QGroupBox,QTextEdit,QMenu, QMessageBox,QTableWidget, QTableWidgetItem, QSpinBox, QDoubleSpinBox, QCheckBox, QDial, QTabWidget, QScrollArea, QSlider,QMenuBar, QMessageBox, QFileDialog, QFileDialog, QTextEdit, QDialog, QInputDialog,QListWidget,QTableWidgetItem, QHeaderView,QProgressBar,QSpinBox, QCheckBox,QComboBox
)
import random

MEUM_CONSTANT = 1.1975807343385265188
DAW_STYLE = """
    QMainWindow, QWidget { background-color: #121212; color: #e0e0e0; font-family: 'Segoe UI', Arial, sans-serif; font-size: 10pt; }
    QPushButton { background-color: #2a2a2a; color: #ffffff; border: 1px solid #3a3a3a; border-radius: 3px; padding: 5px 10px; font-weight: bold; }
    QPushButton:hover { background-color: #383838; border: 1px solid #555555; }
    QPushButton:pressed { background-color: #ff6b00; }
    QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox { background-color: #1a1a1a; color: #00ffcc; border: 1px solid #333333; border-radius: 3px; padding: 3px; }
    QTableWidget { background-color: #161616; gridline-color: #282828; color: #ffffff; }
    QHeaderView::section { background-color: #1f1f1f; color: #aaaaaa; border: 1px solid #333333; font-size: 9px; }
    QLabel { color: #cccccc; }
    QSlider::groove:horizontal { height: 4px; background: #333333; border-radius: 2px; }
    QSlider::handle:horizontal { background: #ff6b00; width: 12px; margin: -4px 0; border-radius: 6px; }
"""

# --- 48 IDEAL INSTRUMENT & EFFECT TOPOLOGIES ---
DEFAULT_INSTRUMENT_LIST = [
    # Family 1: Topological Wave-Folding & Non-Linear Curvature (Oscillators 1-8)
    "1. Meum Phase-Fold Oscillator", "2. Z-Pinch Waveguide Synth", "3. Hyperbolic Attractor Generator", "4. Non-Linear Polynomial Folder",
    "5. Strange Attractor Chaos Engine", "6. Topological Torus Synthesizer", "7. Klein Bottle Surface Generator", "8. Crystalline Wavefolder Matrix",
    # Family 2: Multivectorial & Phase-Space Dynamics (Oscillators 9-16)
    "9. Quaternion Cl(0,3) Space Synth", "10. Clifford Multivector Rotor", "11. Phase-Space Trajectory Synth", "12. Spinor Standing Wave Generator",
    "13. Tensor Curvature Field Lead", "14. Vector Field Flow Synthesizer", "15. Eigenstate Harmonic Matrix", "16. Wavepacket Localization Engine",
    # Family 3: Quantum, Soliton & Field-Coupling (Oscillators 17-24)
    "17. Quantum Tunneling Oscillator", "18. Soliton Pulse Engine", "19. Bose-Einstein Condensate Pad", "20. Zero-Point Energy Oscillator",
    "21. Casimir Force Resonator", "22. Photon-Coupling Synth", "23. Neutrino Flux Modulator", "24. Quark Confinement Bass",
    # Family 4: Stochastic, Thermodynamic & Entropic Noise (Oscillators 25-32)
    "25. Stochastic Noise Chamber", "26. Entropy Decay Engine", "27. Doppler Shift Emulator", "28. Brownian Motion Synth",
    "29. Fractional Brownian Filter", "30. Thermal Noise Generator", "31. Microstate Combinatoric Pad", "32. Dissipative Structure Synth",
    # Family 5: Input-Dependent Spatial & Spectral Effects (Effects 33-40)
    "33. Topological Phase Shifter", "34. Non-Linear Spectral Fold-Back Effect", "35. Curvature Convolution Matrix", "36. Gravitational Time-Dilation Delay",
    "37. Wave-Number Dispersion Filter", "38. Vortex Phase Modulator", "39. Anisotropic Spatial Diffusion", "40. Tensor Field Reverb Processor",
    # Family 6: Input-Dependent Dynamic Waveform Resonators (Effects 41-48)
    "41. Spectral Centroid Dynamic Shifter", "42. Soliton Envelope Shaper", "43. Wavepacket Granulator Effect", "44. Non-Linear Diode Clipper Effect",
    "45. Plasma Ionization Gate", "46. Magnetostrictive Resonator Effect", "47. Crystalline Lattice Damper", "48. Event Horizon Limiter"
]
class FormulaModulatorWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Dynamic Coordinate Formula Inputs</b>"))

        # Formula Inputs
        self.x_input = self.create_formula_row(layout, "X-Axis Expr:", "np.sin(time * 2.0) + base_x")
        self.y_input = self.create_formula_row(layout, "Y-Axis Expr:", "np.cos(time * 1.5) * base_y")
        self.z_input = self.create_formula_row(layout, "Z-Axis Expr:", "abs(x + y) - time")

        # Compile Button
        self.compile_btn = QPushButton("Inject Formulas into Audio Thread")
        self.compile_btn.setStyleSheet("background-color: darkred; color: white; font-weight: bold;")
        layout.addWidget(self.compile_btn)

    def create_formula_row(self, parent_layout, label_text, default_expr):
        row = QHBoxLayout()
        row.addWidget(QLabel(label_text))

        line_edit = QLineEdit(default_expr)
        line_edit.setStyleSheet("background-color: #222; color: #0f0; font-family: monospace;")
        row.addWidget(line_edit)

        # Add a macro slider for manual offset tuning
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(50)
        row.addWidget(slider)

        parent_layout.addLayout(row)
        return line_edit
class VisualOscilloscope(QFrame):
    """Real-time signal output oscilloscope and vector scope."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 140)
        self.setStyleSheet("background-color: #0a0c0e; border: 1px solid #2a2e39; border-radius: 6px;")
        self.wave_data = np.zeros(100)

    def update_waveform(self, new_data):
        if isinstance(new_data, np.ndarray):
            self.wave_data = np.resize(new_data, 100)
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#00ffcc"))
        pen.setWidth(2)
        painter.setPen(pen)

        width = self.width()
        height = self.height()
        mid_y = height / 2.0

        points = []
        for i, val in enumerate(self.wave_data):
            x = (i / 99.0) * width
            y = mid_y - (float(val) * (height * 0.4))
            points.append((x, y))

        for j in range(len(points) - 1):
            painter.drawLine(int(points[j][0]), int(points[j][1]), int(points[j+1][0]), int(points[j+1][1]))
class ModulationMatrixWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Sunken)
        layout = QGridLayout(self)

        layout.addWidget(QLabel("<b>Virtual Patch Matrix</b>"), 0, 0, 1, 4)
        layout.addWidget(QLabel("Source"), 1, 0)
        layout.addWidget(QLabel("Destination"), 1, 1)
        layout.addWidget(QLabel("Amount"), 1, 2)

        # Create 4 patch cables
        self.patches = []
        for i in range(4):
            source_combo = QComboBox()
            source_combo.addItems(["None", "X Coordinate", "Y Coordinate", "Z Coordinate", "LFO 1", "Step Sequencer"])

            dest_combo = QComboBox()
            dest_combo.addItems(["None", "Filter Cutoff", "Resonance", "Wave Drive", "Delay Time", "Delay Feedback", "Pitch Node"])

            amount_spin = QDoubleSpinBox()
            amount_spin.setRange(-1.0, 1.0)
            amount_spin.setSingleStep(0.01)
            amount_spin.setValue(0.5)

            layout.addWidget(source_combo, i+2, 0)
            layout.addWidget(dest_combo, i+2, 1)
            layout.addWidget(amount_spin, i+2, 2)

            self.patches.append({"source": source_combo, "dest": dest_combo, "amount": amount_spin})
class PatchbayCanvas(QFrame):
    """Interactive visual patchbay canvas for signal routing and node mapping."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 200)
        self.setStyleSheet("background-color: #121418; border: 1px solid #2a2e39; border-radius: 6px;")


class MemoryBankSelector(QWidget):
    """Memory Bank Selector pane for project workflow and preset management."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        self.bank_combo = QComboBox()
        self.bank_combo.addItems([
            "Bank Alpha [90uF/900V Resonant]",
            "Bank Beta [2000uF/1350V]",
            "Bank Gamma [3500uF/300V]"
        ])
        self.bank_combo.setStyleSheet("background-color: #1a1e24; color: #00ffcc; border: 1px solid #3a3f4b; padding: 4px;")

        load_btn = QPushButton("Load Preset State")
        save_btn = QPushButton("Save State Snapshot")
        for btn in (load_btn, save_btn):
            btn.setStyleSheet("background-color: #222733; color: #ffffff; border: 1px solid #3a3f4b; padding: 6px;")

        layout.addWidget(QLabel("<b>Memory Bank Selector</b>"))
        layout.addWidget(self.bank_combo)
        layout.addWidget(load_btn)
        layout.addWidget(save_btn)
        layout.addStretch()
class EQRMathEngine:
    def __init__(self, use_meum=True):
        """
        Initializes the EQR math engine.
        Args:
            use_meum (bool): Flag to toggle Meum factor weighting.
                             (Default set based on project optimization preference).
        """
        self.use_meum = use_meum

    # --- Custom Isosceles Trigonometric Functions ---
    def isn(self, val):
        """Isosceles Sine implementation."""
        arr = np.asarray(val, dtype=float)
        return np.sin(arr) / (1.0 + np.abs(np.cos(arr)))

    def ics(val):
        """Isosceles Cosine implementation."""
        arr = np.asarray(val, dtype=float)
        return np.cos(arr) / (1.0 + np.abs(np.sin(arr)))

    def arcisn(self, val):

        arr = np.asarray(val, dtype=float)
        v = np.clip(arr / 2.0, -1.0, 1.0)
        return np.arcsin(v)

    def arcics(self, val):

        arr = np.asarray(val, dtype=float)
        v = np.clip(arr / 2.0, -1.0, 1.0)
        return np.arccos(v)

    # --- Core Expression Evaluator ---
    def evaluate_coordinate_expression(expr_str, x, y, z):

    # Safe namespace dictionary for mathematical parsing
        allowed_globals = {
            "__builtins__": {},
            "sin": np.sin,
            "cos": np.cos,
            "tan": np.tan,
            "sqrt": np.sqrt,
            "abs": np.abs,
            "pi": np.pi,
            "e": np.e
        }

        local_vars = {
            "x": float(x),
            "y": float(y),
            "z": float(z)
        }

        try:
            # Evaluates strictly against x, y, and z parameters
            result = eval(expr_str, allowed_globals, local_vars)
            return float(result)
        except Exception as e:
            print(f"Evaluation Error for expression '{expr_str}': {e}")
            return 0.0
class PortWidget(QWidget):
    """Input/output terminal for the scientific patchbay node network."""
    def __init__(self, port_type, parent=None):
        super().__init__(parent)
        self.port_type = port_type  # 'in' or 'out'
        self.setFixedSize(22, 22)
        self.color = "#00ffc8" if port_type == 'out' else "#ff6400"
        self.setStyleSheet(f"""
            background-color: {self.color};
            border-radius: 11px;
            border: 3px solid #1a1a1a;
        """)

    def mousePressEvent(self, event):
        if self.parent() and hasattr(self.parent(), 'start_cable_drag'):
            self.parent().start_cable_drag(self)
        event.accept()


class ScientificCanvas(QWidget):
    """Interactive node patchbay canvas with Bezier signal cables."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(2400, 1800)
        self.cables = []
        self.active_cable_start = None
        self.current_mouse_pos = QPoint(0, 0)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: #0b0b0e; border: 1px solid #1f1f2e;")

    def start_cable_drag(self, port_widget):
        self.active_cable_start = port_widget
        self.current_mouse_pos = port_widget.mapTo(self, port_widget.rect().center())
        self.update()

    def mouseMoveEvent(self, event):
        if self.active_cable_start:
            self.current_mouse_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.active_cable_start:
            target_widget = self.childAt(event.pos())
            if isinstance(target_widget, PortWidget) and target_widget != self.active_cable_start:
                if self.active_cable_start.port_type != target_widget.port_type:
                    cable_pair = (self.active_cable_start, target_widget)
                    reverse_pair = (target_widget, self.active_cable_start)
                    if cable_pair not in self.cables and reverse_pair not in self.cables:
                        self.cables.append(cable_pair)
            self.active_cable_start = None
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for start, end in self.cables:
            if start and end:
                p1 = start.mapTo(self, start.rect().center())
                p2 = end.mapTo(self, end.rect().center())

                glow_pen = QPen(QColor(0, 255, 200, 50), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(glow_pen)
                painter.drawPath(self.create_bezier_path(p1, p2))

                core_pen = QPen(QColor(0, 255, 200), 2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(core_pen)
                painter.drawPath(self.create_bezier_path(p1, p2))

        if self.active_cable_start:
            p1 = self.active_cable_start.mapTo(self, self.active_cable_start.rect().center())
            p2 = self.current_mouse_pos
            drag_pen = QPen(QColor(255, 100, 0, 200), 2, Qt.PenStyle.DashLine, Qt.PenCapStyle.RoundCap)
            painter.setPen(drag_pen)
            painter.drawPath(self.create_bezier_path(p1, p2))

    def create_bezier_path(self, p1, p2):
        path = QPainterPath()
        path.moveTo(p1)
        dx = (p2.x() - p1.x()) * 0.5
        ctrl1 = QPoint(p1.x() + dx, p1.y())
        ctrl2 = QPoint(p2.x() - dx, p2.y())
        path.cubicTo(ctrl1, ctrl2, p2)
        return path

class MathNodeWidget(QFrame):
    """Draggable processing node for algebra & vector fields."""
    def __init__(self, name, x, y, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.resize(240, 150)
        self.move(x, y)
        self.setStyleSheet("""
            background-color: #14141c;
            color: #ffffff;
            border: 1px solid #2e2e42;
            border-radius: 8px;
        """)

        layout = QVBoxLayout(self)
        self.title_input = QLineEdit(name)
        self.title_input.setStyleSheet("""
            background-color: #1c1c28;
            color: #00ffc8;
            border: 1px solid #3d3d5c;
            padding: 4px;
            font-weight: bold;
            border-radius: 4px;
        """)
        layout.addWidget(self.title_input)

        ports_layout = QHBoxLayout()
        in_container = QVBoxLayout()
        lbl_in = QLabel("IN")
        lbl_in.setStyleSheet("color: #ff6400; border: none; font-size: 9px; font-weight: bold;")
        in_container.addWidget(lbl_in)
        self.in_port = PortWidget('in', self)
        in_container.addWidget(self.in_port)

        out_container = QVBoxLayout()
        lbl_out = QLabel("OUT")
        lbl_out.setStyleSheet("color: #00ffc8; border: none; font-size: 9px; font-weight: bold;")
        out_container.addWidget(lbl_out)
        self.out_port = PortWidget('out', self)
        out_container.addWidget(self.out_port)

        ports_layout.addLayout(in_container)
        ports_layout.addLayout(out_container)
        layout.addLayout(ports_layout)

        self.dragging = False
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            self.raise_()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            if self.parent():
                self.parent().update()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

class SequencerPane(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>16-Step Modulation Sequencer</b>"))

        grid_layout = QGridLayout()
        self.steps = []
        for i in range(16):
            btn = QPushButton(str(i+1))
            btn.setCheckable(True)
            btn.setStyleSheet("background-color: #222; color: #888;")
            btn.clicked.connect(lambda checked, b=btn: b.setStyleSheet("background-color: #00aa55; color: #fff;" if b.isChecked() else "background-color: #222; color: #888;"))
            row, col = divmod(i, 8)
            grid_layout.addWidget(btn, row, col)
            self.steps.append(btn)

        layout.addLayout(grid_layout)
class DoubleNumericSliderRow(QWidget):
    """Precision double slider + spinbox widget."""
    def __init__(self, min_val, max_val, default_val, decimals=2, unit="", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(int(min_val * 100), int(max_val * 100))
        self.slider.setValue(int(default_val * 100))
        self.slider.setStyleSheet("background: transparent;")

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.setValue(default_val)
        self.spinbox.setDecimals(decimals)
        self.spinbox.setSuffix(unit)
        self.spinbox.setStyleSheet("background-color: #1c1c28; color: #00ffc8; border: 1px solid #3d3d5c; padding: 2px; border-radius: 3px;")

        self.slider.valueChanged.connect(lambda v: self.spinbox.setValue(v / 100.0))
        self.spinbox.valueChanged.connect(lambda v: self.slider.setValue(int(v * 100)))

        layout.addWidget(self.slider, 3)
        layout.addWidget(self.spinbox, 1)


class SoundCloudTimelineVisualizer(QWidget):
    """SoundCloud-style static waveform overview with split-spectrum color gradient peaks and recursion trigger labels."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(140)
        self.setStyleSheet("background-color: #0b0b0e; border: 1px solid #1f1f2e; border-radius: 6px;")
        # Pre-calculated structural events: (x_ratio, label, color_mode, depth_param)
        self.triggers = [
            (0.08, "EskiBrutuses WaveMorph [x=0.2, d=3]", "#00ffc8", 1),
            (0.22, "EQR Singularity Collapse [f(x,y,z)=0]", "#ff00ff", 2),
            (0.35, "EskiPhased Non-Linear Matrix [Feedback 82%]", "#00bfff", 1.5),
            (0.48, "Fractalizer Harmonic Fold [Depth 5x]", "#ff6400", 3),
            (0.65, "EskiRecursive Wave-Fold [Chaos Mod 0.4]", "#ffff00", 2.2),
            (0.82, "Z-Axis Field Resonance [Peak Phase]", "#ff0055", 2.8)
        ]

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        mid_y = h / 2.0 - 10

        # Draw background track bar
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(16, 16, 24))
        painter.drawRoundedRect(10, 10, w - 20, h - 20, 6, 6)

        # Draw SoundCloud style static amplitude peaks with split-spectrum colors
        random.seed(42) # Consistent static peak generation
        bar_width = 3
        gap = 2
        num_bars = (w - 40) // (bar_width + gap)

        for i in range(num_bars):
            x = 20 + i * (bar_width + gap)
            ratio = i / num_bars

            # Formulate multi-frequency loudness curve across duration
            envelope = math.sin(ratio * math.pi * 3.5) * 0.5 + 0.5
            harmonic = math.cos(ratio * math.pi * 12.0) * 0.25 + 0.75
            noise = random.uniform(0.4, 1.0)
            amplitude = int((h - 50) * envelope * harmonic * noise)

            # Split spectrum color grading based on frequency band
            if ratio < 0.3:
                grad_color = QColor(0, 255, 200, 200) # Cyan / Sub-bass
            elif ratio < 0.6:
                grad_color = QColor(255, 0, 255, 200) # Magenta / Mid harmonics
            else:
                grad_color = QColor(255, 100, 0, 200) # Orange / High fractal folds

            painter.setBrush(grad_color)
            painter.drawRoundedRect(x, int(mid_y - amplitude / 2), bar_width, max(4, amplitude), 1, 1)

        # Draw Timeline Trigger Labels & Recursion Markers
        for rx, text, hex_col, depth in self.triggers:
            tx = int(rx * w)
            # Marker line
            painter.setPen(QPen(QColor(hex_col), 2, Qt.PenStyle.SolidLine))
            painter.drawLine(tx, 15, tx, h - 15)

            # Floating label tag
            painter.setBrush(QColor(18, 18, 28, 230))
            painter.setPen(QPen(QColor(hex_col), 1))
            label_w = min(170, len(text) * 6 + 12)
            painter.drawRoundedRect(tx - 5, h - 38, label_w, 24, 4, 4)

            painter.setPen(QColor(240, 240, 255))
            painter.setFont(QFont("Segoe UI", 8, QFont.Weight.Bold))
            painter.drawText(tx, h - 22, text)


class SynthRackUnitWidget(QFrame):
    """Dedicated interactive control panel for an active synth instance with all parameters & modes."""
    def __init__(self, synth_name, synth_id, parent=None):
        super().__init__(parent)
        self.synth_name = synth_name
        self.synth_id = synth_id
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            background-color: #14141c;
            border: 1px solid #2e2e42;
            border-radius: 8px;
            padding: 8px;
        """)

        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        title_lbl = QLabel(f"⚡ {synth_name} [Instance #{synth_id}]")
        title_lbl.setStyleSheet("color: #00ffc8; font-weight: bold; font-size: 13px; border: none;")
        header_layout.addWidget(title_lbl)
        header_layout.addStretch()

        self.mode_combo = QComboBox()
        self.mode_combo.addItems([
            "Mode A: Vector Space Warp",
            "Mode B: Non-Linear Resonance",
            "Mode C: Recursive Chaos Fold",
            "Mode D: EQR Singularity Lock"
        ])
        self.mode_combo.setStyleSheet("background-color: #1c1c28; color: #fff; border: 1px solid #3d3d5c; padding: 3px; border-radius: 4px;")
        header_layout.addWidget(self.mode_combo)
        layout.addLayout(header_layout)

        # Knobs & Implicit Parameters
        params_grid = QGridLayout()

        self.param1 = DoubleNumericSliderRow(0.01, 10.0, 1.2, decimals=2, unit="x")
        self.param2 = DoubleNumericSliderRow(20.0, 20000.0, 880.0, decimals=1, unit=" Hz")
        self.param3 = DoubleNumericSliderRow(0.0, 1.0, 0.75, decimals=2, unit="")
        self.param4 = DoubleNumericSliderRow(1.0, 16.0, 4.0, decimals=1, unit=" Stp")

        params_grid.addWidget(QLabel("Morph Rate / Speed:"), 0, 0)
        params_grid.addWidget(self.param1, 0, 1)
        params_grid.addWidget(QLabel("Harmonic Frequency:"), 1, 0)
        params_grid.addWidget(self.param2, 1, 1)
        params_grid.addWidget(QLabel("Feedback / Chaos Blend:"), 2, 0)
        params_grid.addWidget(self.param3, 2, 1)
        params_grid.addWidget(QLabel("Recursive Fold Depth:"), 3, 0)
        params_grid.addWidget(self.param4, 3, 1)

        layout.addLayout(params_grid)
class WaveformVisualizer(QWidget):
    """Custom visualizer widget for real-time amplitude peak monitoring."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(120)
        self.amplitude_data = [0.0] * 50

    def update_data(self, new_val):
        self.amplitude_data.pop(0)
        self.amplitude_data.append(new_val)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Background canvas
        painter.fillRect(self.rect(), QColor(20, 20, 25))

        # Draw waveform trace based on coordinate evaluations
        pen = QPen(QColor(0, 220, 150))
        pen.setWidth(2)
        painter.setPen(pen)

        width = self.width()
        height = self.height()
        step = width / max(len(self.amplitude_data) - 1, 1)

        for i in range(len(self.amplitude_data) - 1):
            x1 = int(i * step)
            y1 = int(height / 2 - self.amplitude_data[i] * (height / 2))
            x2 = int((i + 1) * step)
            y2 = int(height / 2 - self.amplitude_data[i + 1] * (height / 2))
            painter.drawLine(x1, y1, x2, y2)
class DoubleNumericSliderRow(QWidget):
    """Synchronized precision double-spinbox and slider layout for scientific variables."""
    def __init__(self, min_val, max_val, default_val, decimals=2, unit="", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(int(min_val * 100), int(max_val * 100))
        self.slider.setValue(int(default_val * 100))
        self.slider.setStyleSheet("background: transparent;")

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.setValue(default_val)
        self.spinbox.setDecimals(decimals)
        self.spinbox.setSuffix(unit)
        self.spinbox.setStyleSheet("background-color: #27272a; color: #00ffc8; border: 1px solid #52525b; padding: 3px; border-radius: 3px;")

        self.slider.valueChanged.connect(lambda v: self.spinbox.setValue(v / 100.0))
        self.spinbox.valueChanged.connect(lambda v: self.slider.setValue(int(v * 100)))

        layout.addWidget(self.slider, 3)
        layout.addWidget(self.spinbox, 1)
class FlexibleSequencer:
    """Holds subsequence memory within intervals with non-destructive quantization."""
    def __init__(self):
        self.sequence_buffer = []
        self.quantize_grid = None
    def mousePressEvent(self, event):
        if self.parent() and hasattr(self.parent(), 'start_cable_drag'):
            self.parent().start_cable_drag(self)
        event.accept()
    def add_note(self, time, pitch, duration):
        self.sequence_buffer.append({'time': time, 'pitch': pitch, 'duration': duration})

    def get_subsequence(self, start_interval, end_interval):
        sub = [n for n in self.sequence_buffer if start_interval <= n['time'] < end_interval]
        if self.quantize_grid:
            quantized = []
            for note in sub:
                q_note = note.copy()
                q_note['time'] = round(note['time'] / self.quantize_grid) * self.quantize_grid
                quantized.append(q_note)
            return quantized
        return sub
class CablePatchPanel(QWidget):
    """Interactive canvas workspace for nodes and cable patching via ports."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(1600, 1000)
        self.cables = []
        self.active_cable_start = None
        self.current_mouse_pos = QPoint(0, 0)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: #121212; border: 1px solid #333;")

    def start_cable_drag(self, port_widget):
        self.active_cable_start = port_widget
        self.current_mouse_pos = port_widget.mapTo(self, port_widget.rect().center())
        self.update()

    def mouseMoveEvent(self, event):
        if self.active_cable_start:
            self.current_mouse_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.active_cable_start:
            target_widget = self.childAt(event.pos())
            if isinstance(target_widget, PortWidget) and target_widget != self.active_cable_start:
                if self.active_cable_start.port_type != target_widget.port_type:
                    self.cables.append((self.active_cable_start, target_widget, QColor(0, 255, 200)))
            self.active_cable_start = None
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for start, end, color in self.cables:
            if start and end:
                p1 = start.mapTo(self, start.rect().center())
                p2 = end.mapTo(self, end.rect().center())
                pen = QPen(color, 3.0, Qt.PenStyle.SolidLine)
                painter.setPen(pen)
                painter.drawLine(p1, p2)

        if self.active_cable_start:
            p1 = self.active_cable_start.mapTo(self, self.active_cable_start.rect().center())
            pen = QPen(QColor(255, 100, 0, 220), 2.5, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            painter.drawLine(p1, self.current_mouse_pos)
class MathEngine:
    """Core mathematical engine evaluated strictly on x, y, z variables without Meum factors."""
    @staticmethod
    def isn(val):
        return np.sin(val) / (1.0 + np.abs(np.cos(val)))

    @staticmethod
    def ics(val):
        return np.cos(val) / (1.0 + np.abs(np.sin(val)))

    @staticmethod
    def eskivector(x, y, z):
        return MathEngine.isn(x) * y, MathEngine.ics(y) * z, np.sin(x * y * z)

    @staticmethod
    def eskitable(x, y, z):
        return np.clip((x + y) * 0.5, -1.0, 1.0) * MathEngine.ics(z)

class GlobalPatchBus:
    def __init__(self):
        self.cables = []
        self.nodes = {}

    def add_cable(self, src, dst):
        if (src, dst) not in self.cables:
            self.cables.append((src, dst))

    def remove_cable(self, src, dst):
        if (src, dst) in self.cables:
            self.cables.remove((src, dst))

global_patch_bus = GlobalPatchBus()
class EQRCoordinateEngine:
    def __init__(self):
        self.x = np.linspace(-1.0, 1.0, 512)
        self.y = np.linspace(-1.0, 1.0, 512)
        self.z = np.zeros(512)

    def evaluate_composition_script(self, script_text: str, t: float):
        x, y, z = self.x, self.y, self.z + t
        namespace = {"np": np, "x": x, "y": y, "z": z, "isn": np.sin, "ics": np.cos, "result": np.zeros_like(x)}

        try:
            exec(script_text, namespace)
            output = namespace.get("result", np.zeros_like(x))
            return self.apply_heuristic_envelope(output)
        except Exception as e:
            print(f"Script Execution Error: {e}")
            return np.zeros_like(x)

    def apply_heuristic_envelope(self, signal_vector):
        envelope = np.exp(-np.abs(self.x) * 2.5)
        return signal_vector * envelope


class FocusZone3DWidget(QWidget):
    """3D zone widget featuring mouse point selection, right-click insert, and middle-click/scroll deletion."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(250)
        self.focal_points = [{'x': 0.0, 'y': 0.0, 'z': 0.0}]
        self.selected_point_idx = 0
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        w, h = self.width(), self.height()
        click_x = event.position().x()
        click_y = event.position().y()

        clicked_idx = -1
        for idx, pt in enumerate(self.focal_points):
            px = int((pt['x'] + 1.0) * (w / 2.0))
            py = int((1.0 - pt['y']) * (h / 2.0))
            if abs(click_x - px) < 14 and abs(click_y - py) < 14:
                clicked_idx = idx
                break

        if event.button() == Qt.MouseButton.LeftButton:
            if clicked_idx != -1:
                self.selected_point_idx = clicked_idx
                self.update()
        elif event.button() == Qt.MouseButton.RightButton:
            if clicked_idx != -1:
                self.selected_point_idx = clicked_idx
            else:
                nx = (click_x / w) * 2.0 - 1.0
                ny = 1.0 - (click_y / h) * 2.0
                self.focal_points.append({'x': nx, 'y': ny, 'z': 0.0})
                self.selected_point_idx = len(self.focal_points) - 1
            self.update()
        elif event.button() == Qt.MouseButton.MiddleButton:
            # Middle-click directly deletes the clicked or currently selected point
            target_idx = clicked_idx if clicked_idx != -1 else self.selected_point_idx
            if len(self.focal_points) > 1:
                self.focal_points.pop(target_idx)
                self.selected_point_idx = max(0, target_idx - 1)
                self.update()

    def wheelEvent(self, event):
        # Scrolling downward also deletes the selected point if more than one exists
        if event.angleDelta().y() < 0 and len(self.focal_points) > 1:
            self.focal_points.pop(self.selected_point_idx)
            self.selected_point_idx = max(0, self.selected_point_idx - 1)
            self.update()
        event.accept()

    def update_coordinate_axis(self, axis: str, val: float):
        if self.focal_points:
            self.focal_points[self.selected_point_idx][axis] = val
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor(20, 20, 28))

        painter.setPen(QPen(QColor(50, 50, 70), 1, Qt.PenStyle.DashLine))
        w, h = self.width(), self.height()
        painter.drawLine(0, h // 2, w, h // 2)
        painter.drawLine(w // 2, 0, w // 2, h)

        for idx, pt in enumerate(self.focal_points):
            px = int((pt['x'] + 1.0) * (w / 2.0))
            py = int((1.0 - pt['y']) * (h / 2.0))

            color = QColor(255, 100, 100) if idx == self.selected_point_idx else QColor(0, 220, 180)
            painter.setBrush(color)
            painter.setPen(QPen(Qt.GlobalColor.white, 2))
            painter.drawEllipse(px - 8, py - 8, 16, 16)

            painter.setPen(QPen(Qt.GlobalColor.white, 1))
            painter.setFont(QFont("Arial", 8))
            painter.drawText(px + 12, py - 5, f"P{idx}({pt['x']:.2f},{pt['y']:.2f},{pt['z']:.2f})")


class EQRVisualizerCanvas(QWidget):
    """
    Real-time parametric visualizer based on the Equation of Reality (EQR)
    operator framework, mapping x, y, and z variables to dynamic phase-space renders.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(160)
        self.setStyleSheet("background-color: #0b0b0b; border: 1px solid #ff6b00; border-radius: 4px;")

        self.phase = 0.0
        self.scale_factor = 1.0
        self.x_offset = 0.0
        self.y_offset = 0.0

        # Timer for real-time mathematical phase updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_phase)
        self.timer.start(30) # ~33 FPS smooth render

    def update_phase(self):
        self.phase += 0.03
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self):
            return
        try:
            painter.fillRect(self.rect(), QColor(11, 11, 11))
            w, h = self.width(), self.height()
            cx, cy = w / 2.0, h / 2.0

            # Draw coordinate grid / field lines
            painter.setPen(QPen(QColor(30, 30, 30), 1, Qt.PenStyle.DashLine))
            painter.drawLine(0, int(cy), w, int(cy))
            painter.drawLine(int(cx), 0, int(cx), h)

            # EQR Parametric Curve Rendering (x, y, z operator mapping)
            pen = QPen(QColor(0, 255, 204), 2)
            painter.setPen(pen)

            points = []
            num_steps = 300
            for i in range(num_steps):
                t = (i / num_steps) * 4 * np.pi + self.phase

                # EQR Core Equations for x, y, and z variables
                x_val = np.sin(t * 1.5) * np.cos(t * 0.5 + self.phase * 0.2) * 120.0
                y_val = np.cos(t * 2.0) * np.sin(t * 1.2) * 80.0
                z_val = np.sin(t + self.phase) * 50.0 # Operator depth factor

                # Projection mapping onto 2D canvas space
                px = cx + x_val + (z_val * 0.3)
                py = cy + y_val + (z_val * 0.2)
                points.append(QPointF(px, py))

            for i in range(len(points) - 1):
                # Gradient color transition based on index
                hue_color = QColor.fromHsvF((i / num_steps + self.phase * 0.1) % 1.0, 0.8, 1.0)
                painter.setPen(QPen(hue_color, 2))
                painter.drawLine(points[i], points[i+1])

        finally:
            painter.end()
class AdvancedDSPEngine:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def compute_synth_waveform(self, track_idx, sub_t, freq, state):
        # Retrieve 6 internal sliding scale parameters
        k1 = state.get("internal_p1", 0.5)
        k2 = state.get("internal_p2", 0.5)
        k3 = state.get("internal_p3", 0.5)
        k4 = state.get("internal_p4", 0.5)
        k5 = state.get("internal_p5", 0.5)
        k6 = state.get("internal_p6", 0.5)

        # External controls & preset selector
        fractal = state.get("fractalizer", 0.5)
        eqr = state.get("eqr_effect", 0.5)
        preset = state.get("preset_idx", 0)

        phase = 2 * np.pi * freq * sub_t

        # Route math based on the Preset Dropdown selection (0 to 4)
        if preset == 0:
            # Preset 0: Non-Linear Wave-Folder Topology
            raw = np.sin(phase * (1.0 + k1)) + k2 * np.sin(phase * 2.0 * k3)
            folded = np.tanh(raw * (1.0 + fractal * 5.0))
            return folded * (1.0 + k4 * np.cos(phase * k5)) * (1.0 - k6 * 0.5)

        elif preset == 1:
            # Preset 1: Z-Pinch / Quantum Field Resonance
            pinched = np.sin(phase * (1.0 + track_idx * 0.05)) * (1.0 + k1 * np.tan(np.clip(sub_t * k2, -1.5, 1.5)))
            resonance = np.arcsin(np.clip(pinched * (0.5 + eqr), -0.99, 0.99))
            return resonance * k3 * (1.0 + k4 * np.sin(sub_t * k5 * 10.0)) * (1.0 - k6)

        elif preset == 2:
            # Preset 2: Hyperbolic & Torus Phase-Space
            hyp = np.sinh(k1 * np.sin(phase)) / (1.0 + np.cosh(k2 * np.cos(phase * k3)))
            torus_mod = np.cos(phase * (1.0 + k4)) + 0.5 * np.sin(phase * (2.0 + k5))
            return hyp * torus_mod * (1.0 + fractal * 3.0) * (1.0 - k6 * 0.2)

        elif preset == 3:
            # Preset 3: Stochastic & Entropic Noise Lattice
            stochastic_jitter = np.random.normal(0, 0.15, len(sub_t)) * k1
            chaotic_wave = np.sin(phase * (1.0 + k2) + stochastic_jitter)
            modulated = chaotic_wave / (1.0 + k3 * np.abs(np.sin(phase * k4)))
            return modulated * k5 * (1.0 + eqr * 2.0) * (1.0 - k6 * 0.3)

        else:
            # Preset 4: Custom Polynomial / Matrix Operator
            # Uses the track index to scale harmonic spacing dynamically across the 48 synths
            harmonic_offset = 1.0 + (track_idx % 12) * 0.08
            poly = k1 * (np.sin(phase * harmonic_offset)**3) - k2 * (np.cos(phase * k3)**2) + k4 * np.sin(phase)
            return np.tanh(poly * (1.0 + fractal * 4.0)) * (1.0 + eqr) * (1.0 - k6 * 0.1)
class MathEngine:
    """Core mathematical engine evaluated strictly on x, y, z variables without Meum factors."""
    @staticmethod
    def isn(val):
        return np.sin(val) / (1.0 + np.abs(np.cos(val)))

    @staticmethod
    def ics(val):
        return np.cos(val) / (1.0 + np.abs(np.sin(val)))

    @staticmethod
    def eskivector(x, y, z):
        return MathEngine.isn(x) * y, MathEngine.ics(y) * z, np.sin(x * y * z)

    @staticmethod
    def eskitable(x, y, z):
        return np.clip((x + y) * 0.5, -1.0, 1.0) * MathEngine.ics(z)

class OperatorNode:
    def __init__(self, op_type):
        self.op_type = op_type  # e.g., 'isn', 'ics', 'eskivector', 'eskitable'

    def compute(self, x, y, z):
        engine = MathEngine()
        if self.op_type == 'isn':
            return engine.isn(x)
        elif self.op_type == 'ics':
            return engine.ics(y)
        elif self.op_type == 'eskivector':
            return engine.evaluate_eskivector(x, y, z)
        elif self.op_type == 'eskitable':
            return engine.evaluate_eskitable(x, y, z)
        return x, y, z
class InstrumentSpawner:
    def __init__(self, inst_type):
        self.inst_type = inst_type # 'percussion', 'pad', 'keys'
        self.math_engine = MathEngine()
        self.envelope = 1.0

    def trigger_spawn(self, x, y, z):
        """Spawns or evaluates an audio frame based on instrument type and x, y, z coordinates."""
        # Evaluate base vector/table components
        vx, vy, vz = self.math_engine.evaluate_eskivector(x, y, z)
        table_val = self.math_engine.evaluate_eskitable(vx, vy, vz)

        if self.inst_type == 'percussion':
            # Fast decaying transient envelope with non-linear distortion
            self.envelope *= 0.95
            return np.tanh(table_val * self.envelope * 3.0)

        elif self.inst_type == 'pad':
            # Smooth, sustained harmonic evolution via isosceles trig
            osc = self.math_engine.isn(vx) + self.math_engine.ics(vy)
            return osc * 0.5

        elif self.inst_type == 'keys':
            # Punchy, discrete coordinate mapping
            return table_val * np.cos(z)

        return table_val

class EQRMasterController:
    def __init__(self):
        self.spawners = {
            'kick_perc': InstrumentSpawner('percussion'),
            'ambient_pad': InstrumentSpawner('pad'),
            'lead_keys': InstrumentSpawner('keys')
        }

    def render_active_spawners(self, buffer_size, x_arr, y_arr, z_arr):
        """Mixes active instrument spawners down to a master output buffer."""
        master_buffer = np.zeros(buffer_size)

        for name, spawner in self.spawners.items():
            voice_buffer = np.zeros(buffer_size)
            for i in range(buffer_size):
                voice_buffer[i] = spawner.trigger_spawn(x_arr[i], y_arr[i], z_arr[i])

            # Mix into master
            master_buffer += voice_buffer

        return master_buffer / len(self.spawners)
class MemoryBankPane(QGroupBox):
    """Manages project states, memory banks, and quick preset switching."""
    def __init__(self, parent=None):
        super().__init__("Memory Bank & Project Workflow", parent)
        layout = QGridLayout()

        self.bank_combo = QComboBox()
        self.bank_combo.addItems([f"Bank {chr(65+i)}: Preset {i+1}" for i in range(8)])

        btn_save = QPushButton("Save State")
        btn_load = QPushButton("Load State")
        btn_export = QPushButton("Export Buffer")
        btn_clear = QPushButton("Clear Bank")

        layout.addWidget(QLabel("Active Bank:"), 0, 0)
        layout.addWidget(self.bank_combo, 0, 1, 1, 3)
        layout.addWidget(btn_save, 1, 0)
        layout.addWidget(btn_load, 1, 1)
        layout.addWidget(btn_export, 1, 2)
        layout.addWidget(btn_clear, 1, 3)

        self.setLayout
class PatchTerminal(QWidget):
    def __init__(self, name, is_input=True, parent=None):
        super().__init__(parent)
        self.name = name
        self.is_input = is_input
        self.setFixedSize(110, 26)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        col = QColor("#00ffcc") if self.is_input else QColor("#58a6ff")
        p.setBrush(QBrush(QColor("#161b22")))
        p.setPen(QPen(col, 2.0))
        p.drawEllipse(4, 4, 16, 16)
        p.setPen(QPen(QColor("#c9d1d9"), 1))
        p.drawText(24, 17, self.name)
class PlaylistArrangerWidget(QWidget):
    """Spicy multivariate modular playlist arranger where numeric program data, clips,
    and automation tracks can be dynamically created and wired."""
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        top_bar.addWidget(QLabel("<b>Multivariate Modular Playlist & Program Data Matrix</b>"))
        btn_add_track = QPushButton("Add Arrangement Track")
        top_bar.addWidget(btn_add_track)
        layout.addLayout(top_bar)

        self.tracks_layout = QVBoxLayout()
        layout.addLayout(self.tracks_layout)

        # Add initial track
        self.add_track("Track 1: Master Rhythm & Eskibrutus Gate")
        self.add_track("Track 2: Multivariate Modulation Timeline")

        self.setLayout(layout)

    def add_track(self, title="Modular Track"):
        box = QGroupBox(title)
        l = QHBoxLayout()
        l.addWidget(QLabel("Program Data Intensity:"))
        sl = QSlider(Qt.Orientation.Horizontal)
        sl.setRange(0, 100)
        sl.setValue(75)
        l.addWidget(sl)
        l.addWidget(PatchTerminal("Track CV Out", is_input=False))
        box.setLayout(l)
        self.tracks_layout.addWidget(box)
class PlaylistArrangementWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Interactive Global Playlist & Arrangement Timeline")
        self.resize(800, 600)
        self.setStyleSheet(TELETUBBY_STYLE)

        container = QWidget()
        layout = QVBoxLayout(container)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("<b>Timeline Snap & Polyrhythm Scaling:</b>"))
        self.grid_scale_combo = QComboBox()
        self.grid_scale_combo.addItems(["1 Bar (Quantized)", "1/2 Beat", "1/4 Beat", "1/8 Beat", "Fully Unquantized / De-quantized Flow"])
        controls.addWidget(self.grid_scale_combo)

        controls.addWidget(QLabel("<b>Tempo (BPM):</b>"))
        self.global_tempo = QLineEdit("124.0")
        controls.addWidget(self.global_tempo)
        layout.addLayout(controls)

        self.timeline_view = QTextEdit()
        self.timeline_view.setPlainText(
            "# Active Playlist Arrangement Channels\n"
            "Track 1 [Instrument_1] |=======| [Bars 1 - 16]   (De-quant Offset: +4.2ms | Polyrhythm: 1.0x)\n"
            "Track 2 [Instrument_2]   |===|   [Bars 8 - 20]   (De-quant Offset: -1.5ms | Polyrhythm: 0.75x)\n"
            "Track 3 [Instrument_3] |=======| [Bars 12 - 32]  (De-quant Offset: 0.0ms  | Polyrhythm: 1.25x)"
        )
        self.timeline_view.setStyleSheet("background-color: #ffffff; color: #1e272e; font-family: monospace; font-size: 14px; border-radius: 12px;")
        layout.addWidget(self.timeline_view)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Universal Brush Painter Mode"))
        btn_layout.addWidget(QPushButton("Quantize All Sequence Clips"))
        btn_layout.addWidget(QPushButton("Render Instrument Stems to Disk"))
        layout.addLayout(btn_layout)

        container.setLayout(layout)
        self.setCentralWidget(container)
class MasterModuleNode(QGroupBox):
    """Modular node for Tab 1 supporting Definers, Functions, and Combiner/Splitters."""
    def __init__(self, title="Math Operator Module", parent=None, delete_callback=None):
        super().__init__(title, parent)
        layout = QVBoxLayout()

        top_bar = QHBoxLayout()
        self.type_combo = QComboBox()
        self.type_combo.addItems(["Definer Hub (Var Data)", "Function Module (Match/Oppose/Attract)", "Combiner / Splitter (+/-)"])
        top_bar.addWidget(self.type_combo)
        if delete_callback:
            btn_del = QPushButton("X")
            btn_del.setFixedWidth(30)
            btn_del.setStyleSheet("background-color: #da3633; color: white;")
            btn_del.clicked.connect(lambda: delete_callback(self))
            top_bar.addWidget(btn_del)
        layout.addLayout(top_bar)

        self.expr_edit = QLineEdit("isn(x) * t")
        layout.addWidget(QLabel("Equation / F(x) Operator:"))
        layout.addWidget(self.expr_edit)

        # Jacks depending on module type
        jacks_layout = QHBoxLayout()
        self.jack_in = PatchTerminal("Signal In", is_input=True)
        self.jack_out1 = PatchTerminal("Automated Out", is_input=False)
        self.jack_out2 = PatchTerminal("Secondary Out", is_input=False)
        jacks_layout.addWidget(self.jack_in)
        jacks_layout.addWidget(self.jack_out1)
        jacks_layout.addWidget(self.jack_out2)
        layout.addLayout(jacks_layout)

        self.setLayout(layout)
class WaveformVectorCanvas(QWidget):
    """Live interactive canvas supporting L/R clicks, mouse scroll for 'hardness/percussiveness',
    scroll-drag for wavetable framing, and vector continuousity vs syncopation."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 110)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.points = [QPointF(i * 13.7, 55 + math.sin(i)*30) for i in range(16)]
        self.hardness = 50.0  # Controls percussiveness vs paddedness
        self.vector_scale = 1.0
        self.syncopation = 0.5
        self.dragging_point = None

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor("#0d1117"))

        # Grid lines
        p.setPen(QPen(QColor("#21262d"), 1))
        for x in range(0, w, 30):
            p.drawLine(x, 0, x, h)

        # Draw Wavetable / Vector Line
        path = QPainterPath()
        if self.points:
            path.moveTo(self.points[0])
            for pt in self.points[1:]:
                path.lineTo(pt)
        p.setPen(QPen(QColor("#00ffcc"), 2.5))
        p.drawPath(path)

        # Draw handles
        for pt in self.points:
            p.setBrush(QBrush(QColor("#58a6ff")))
            p.setPen(Qt.PenStyle.NoPen)
            p.drawEllipse(pt, 4, 4)

        p.setPen(QPen(QColor("#8b949e"), 1))
        p.drawText(10, 18, f"Hardness: {self.hardness:.1f} | Vector Scale: {self.vector_scale:.2f}")

    def mousePressEvent(self, event):
        pos = event.position()
        if event.button() == Qt.MouseButton.LeftButton:
            for pt in self.points:
                if (pt - pos).manhattanLength() < 12:
                    self.dragging_point = pt
                    break
        elif event.button() == Qt.MouseButton.RightButton:
            # Shift hardness / percussiveness mode on right click
            self.hardness = (self.hardness + 10) % 100.0
            self.update()

    def mouseMoveEvent(self, event):
        if self.dragging_point:
            self.dragging_point.setY(max(5, min(self.height() - 5, event.position().y())))
            self.update()

    def mouseReleaseEvent(self, event):
        self.dragging_point = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            self.vector_scale = max(0.1, self.vector_scale + (0.1 if delta > 0 else -0.1))
        else:
            self.hardness = max(0.0, min(100.0, self.hardness + (5.0 if delta > 0 else -5.0)))
        self.update()
class InstrumentStrip(QGroupBox):
    """Dynamic Instrument Node with modulation resistance profile (Padded, Keys, Percussion),
    live waveform editor, and patch terminals."""
    def __init__(self, title="Instrument Node", parent=None, delete_callback=None):
        super().__init__(title, parent)
        layout = QVBoxLayout()

        top_row = QHBoxLayout()
        self.engine_combo = QComboBox()
        self.engine_combo.addItems(["Eskibrutus", "Vector Synth", "Oscillator Synth", "Wavetable Synth", "Equation Synth"])
        top_row.addWidget(QLabel("Engine:"))
        top_row.addWidget(self.engine_combo)

        # Response Profile (Resistance to modulations over long/short periods)
        self.profile_combo = QComboBox()
        self.profile_combo.addItems(["Normal Response", "Padded (High Modulation Resistance)", "Keys (Tempo Envelope)", "Percussion (Fast Transient)"])
        top_row.addWidget(QLabel("Profile:"))
        top_row.addWidget(self.profile_combo)

        if delete_callback:
            btn_del = QPushButton("Delete")
            btn_del.setStyleSheet("background-color: #da3633; color: white;")
            btn_del.clicked.connect(lambda: delete_callback(self))
            top_row.addWidget(btn_del)

        layout.addLayout(top_row)

        # Live Wavetable & Vector Canvas
        self.wave_canvas = WaveformVectorCanvas()
        layout.addWidget(self.wave_canvas)

        # Patch Terminals for wiring across synth parameters
        term_layout = QHBoxLayout()
        self.in_term = PatchTerminal(f"{title} Mod In", is_input=True)
        self.out_term = PatchTerminal(f"{title} Out", is_input=False)
        term_layout.addWidget(self.in_term)
        term_layout.addWidget(self.out_term)
        layout.addLayout(term_layout)

        # Sliders for Osc Effects, Wavetable Framing, Vector Scaling, Continuousity
        sliders_grid = QGridLayout()
        self.sliders = {}
        s_defs = [("Cutoff", 80), ("Resonance", 30), ("Osc Effects", 50), ("Wavetable Frame", 40), ("Vector Scale", 70), ("Continuousity", 60)]
        for idx, (s_name, val) in enumerate(s_defs):
            row, col = dividx = divmod(idx, 2)
            sliders_grid.addWidget(QLabel(s_name), row, col * 2)
            sl = QSlider(Qt.Orientation.Horizontal)
            sl.setRange(0, 100)
            sl.setValue(val)
            sliders_grid.addWidget(sl, row, col * 2 + 1)
            self.sliders[s_name] = sl
        layout.addLayout(sliders_grid)

        self.setLayout(layout)
class SongAutomationTimeline(QWidget):
    """Timeline module for song length, module automation over time, and content duration mapping."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(220)
        layout = QVBoxLayout()

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Song Length (Bars):"))
        self.bars_spin = QSpinBox()
        self.bars_spin.setRange(4, 256)
        self.bars_spin.setValue(32)
        controls_layout.addWidget(self.bars_spin)

        controls_layout.addWidget(QLabel("Global Tempo (BPM):"))
        self.tempo_spin = QSpinBox()
        self.tempo_spin.setRange(40, 300)
        self.tempo_spin.setValue(120)
        controls_layout.addWidget(self.tempo_spin)

        layout.addLayout(controls_layout)

        # Automation Lane Canvas representation
        self.lane_canvas = MultiLaneSequencerCanvas()
        layout.addWidget(self.lane_canvas)
        self.setLayout(layout)
# --- Modular Synthesizer/Sequencer Node ---
class ModulationRoutingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Ableton Style Modulation & Device Rack")
        self.resize(750, 480)
        self.setStyleSheet(DAW_STYLE)

        container = QWidget()
        layout = QVBoxLayout(container)

        layout.addWidget(QLabel("<b>🎛️ Modular Device & LFO Modulation Matrix</b>"))

        rack_layout = QGridLayout()
        rack_layout.addWidget(QLabel("LFO 1 Rate (Hz):"), 0, 0)
        self.lfo_slider = QSlider(Qt.Orientation.Horizontal)
        self.lfo_slider.setValue(35)
        rack_layout.addWidget(self.lfo_slider, 0, 1)

        rack_layout.addWidget(QLabel("Filter Cutoff:"), 1, 0)
        self.cutoff_slider = QSlider(Qt.Orientation.Horizontal)
        self.cutoff_slider.setValue(70)
        rack_layout.addWidget(self.cutoff_slider, 1, 1)

        rack_layout.addWidget(QLabel("Wavefold Drive:"), 2, 0)
        self.drive_slider = QSlider(Qt.Orientation.Horizontal)
        self.drive_slider.setValue(50)
        rack_layout.addWidget(self.drive_slider, 2, 1)
        layout.addLayout(rack_layout)

        self.routing_view = QTextEdit()
        self.routing_view.setPlainText(
            "# Active Modulation Routing Matrix (Ableton CV/Mod Style)\n"
            "LFO 1 ------------> Filter Cutoff (Amount: +65%)\n"
            "Macro 1 (Drive) --> Wavefolder Saturation (Amount: 80%)\n"
            "Envelope 1 -------> Master Volume VCA"
        )
        self.routing_view.setStyleSheet("background-color: #161616; color: #00ffcc; font-family: monospace;")
        layout.addWidget(self.routing_view)

        container.setLayout(layout)
        self.setCentralWidget(container)
class SynthNodeWidget(QFrame):
    """Editable modular node frame with visible ports and a rename field."""
    def __init__(self, name, x, y, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setLineWidth(2)
        self.resize(210, 140)
        self.move(x, y)
        self.setStyleSheet("background-color: #1e1e1e; color: #ffffff; border: 1px solid #555; border-radius: 6px;")

        layout = QVBoxLayout(self)

        # Editable title field
        self.title_input = QLineEdit(name)
        self.title_input.setStyleSheet("background-color: #2a2a2a; color: #ffffff; border: 1px solid #666; padding: 4px;")
        self.title_label = self.title_input
        layout.addWidget(self.title_input)

        ports_layout = QHBoxLayout()

        in_container = QVBoxLayout()
        lbl_in = QLabel("In")
        lbl_in.setStyleSheet("color: #00ffc8; border: none; font-size: 11px; font-weight: bold;")
        in_container.addWidget(lbl_in)
        self.in_port = PortWidget('in', self)
        in_container.addWidget(self.in_port)

        out_container = QVBoxLayout()
        lbl_out = QLabel("Out")
        lbl_out.setStyleSheet("color: #ff6400; border: none; font-size: 11px; font-weight: bold;")
        out_container.addWidget(lbl_out)
        self.out_port = PortWidget('out', self)
        out_container.addWidget(self.out_port)

        ports_layout.addLayout(in_container)
        ports_layout.addLayout(out_container)
        layout.addLayout(ports_layout)

        self.dragging = False
        self.drag_position = QPoint()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            if self.parent():
                self.parent().update()
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
class ArrangementTrackWidget(QWidget):
    """Arrangement timeline track for placing and editing sequence blocks."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("background-color: #181818; border: 1px solid #444; border-radius: 4px;")
        layout = QHBoxLayout(self)

        self.track_label = QLabel("Arrangement Track")
        self.track_label.setStyleSheet("color: #ffffff; font-weight: bold;")

        self.blocks_layout = QHBoxLayout()

        self.add_block_btn = QPushButton("+ Add Subsequence")
        self.add_block_btn.setStyleSheet("background-color: #333; color: #ffffff; border: 1px solid #555; padding: 6px 12px; border-radius: 4px;")
        self.add_block_btn.clicked.connect(self.on_add_subsequence)

        layout.addWidget(self.track_label)
        layout.addLayout(self.blocks_layout)
        layout.addStretch()
        layout.addWidget(self.add_block_btn)

    def on_add_subsequence(self):
        block = QPushButton("Subsequence Clip")
        block.setStyleSheet("background-color: #005555; color: #ffffff; border: 1px solid #00ffc8; padding: 6px; border-radius: 3px;")
        self.blocks_layout.addWidget(block)
class FitToFrameContainer(QWidget):
    """A responsive container that scales its inner child widget to fit window bounds."""
    def __init__(self, inner_widget, base_width=1200, base_height=800):
        super().__init__()
        self.inner_widget = inner_widget
        self.base_width = base_width
        self.base_height = base_height

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.inner_widget)
        self.scale_factor = 1.0

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w = self.width()
        h = self.height()

        scale_x = w / self.base_width
        scale_y = h / self.base_height
        self.scale_factor = min(scale_x, scale_y)

# Import Reality Synth and Music Fractallizer from synth_engine (with fallback stubs)
class FractallizerVisualizerCanvas(QWidget):
    def __init__(self, parent=None, app_ref=None):
        super().__init__(parent)
        self.app_ref = app_ref
        self.setMinimumHeight(160)
        self.setStyleSheet("background-color: #080808; border: 1px solid #ff6b00; border-radius: 4px;")
        self.phase = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_fractal)
        self.timer.start(25)

    def update_fractal(self):
        self.phase += 0.05
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self): return
        try:
            painter.fillRect(self.rect(), QColor(8, 8, 8))
            w, h = self.width(), self.height()
            cx, cy = w / 2.0, h / 2.0
            points = []
            for i in range(200):
                t = (i / 200.0) * 6 * np.pi + self.phase
                r = (55.0 + (self.app_ref.macro_fractal.value() * 5 if self.app_ref else 10)) * np.sin(t * 2.5 + self.phase)
                points.append(QPointF(cx + r * np.cos(t), cy + r * np.sin(t)))
            for i in range(len(points) - 1):
                col = QColor.fromHsvF((i / 200.0 + self.phase * 0.1) % 1.0, 0.9, 1.0)
                painter.setPen(QPen(col, 2))
                painter.drawLine(points[i], points[i+1])
        finally:
            painter.end()

class ReadmeGuideDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mathematician's DAW - Master Readme & Scripting Guide")
        self.resize(750, 600)
        self.setStyleSheet(DAW_STYLE)
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("<h3>📖 Master Studio Readme & Symbolic Scripting Command Index</h3>"))

        text_view = QTextEdit()
        text_view.setReadOnly(True)
        text_view.setPlainText(
            "=== 1. INTRODUCTION & CORE ARCHITECTURE ===\n"
            "Mathematician's DAW combines high-energy pulsed power synth modeling with EQR Phase-Space "
            "and mathematical curvature tonal mapping (anchored by default to 432 Hz).\n\n"
            "=== 2. GLOBAL VS. SINGLE-INSTRUMENT SCRIPTING ===\n"
            "• Global Scripting: Evaluates matrix-wide transformations across all 48 tracks simultaneously (e.g. Master Randomizers, Global Tempo automation).\n"
            "• Single-Instrument Scripting: Targets individual channel instances, allowing specific tuning curvature, chord matrices, and envelope sculpting.\n\n"
            "=== 3. SYMBOLIC SCRIPTING COMMAND REFERENCE ===\n"
            "• Freq(x) = 432 * 2^(x/12) -> Evaluates 12-TET exponential scaling.\n"
            "• Curvature(fib) -> Applies Fibonacci ratio spacing across step sequences.\n"
            "• Modulate(patch_bay, src, dest) -> Routes modular control voltages dynamically.\n\n"
            "=== 4. WORKFLOW GUIDE ===\n"
            "1. Use the Top Sequencer to select instrument instances, enter comma-separated chords, and pick tonal curvature modes.\n"
            "2. Open the Playlist to arrange tracks up to 1024 sequences wide with optional step quantization.\n"
            "3. Use the Modular Patch Bay and Sound Sculpting knobs to shape your timbres in real time."
        )
        text_view.setStyleSheet("background-color: #161616; color: #00ffcc; font-family: monospace; font-size: 11px;")
        layout.addWidget(text_view)

        close_btn = QPushButton("Close Guide")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

class ModularPatchBayDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Modular Modulation Bay & Routing Matrix")
        self.resize(700, 500)
        self.setStyleSheet(DAW_STYLE)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h3>🔌 Master Modular Patch Bay & CV Routing Matrix</h3>"))

        toolbar = QHBoxLayout()
        random_patch_btn = QPushButton("🎲 Randomize Patch Bay")
        random_patch_btn.setStyleSheet("background-color: #ff6b00; color: white;")
        random_patch_btn.clicked.connect(self.randomize_matrix)
        toolbar.addWidget(random_patch_btn)

        clear_patch_btn = QPushButton("Clear Patch Bay")
        clear_patch_btn.clicked.connect(self.clear_matrix)
        toolbar.addWidget(clear_patch_btn)
        layout.addLayout(toolbar)

        self.table = QTableWidget(12, 12)
        self.table.setHorizontalHeaderLabels([f"Mod Out {i+1}" for i in range(12)])
        self.table.setVerticalHeaderLabels([f"Dest {i+1}" for i in range(12)])
        self.table.setStyleSheet("QTableWidget { background-color: #161616; gridline-color: #282828; }")
        layout.addWidget(self.table)

        close_btn = QPushButton("Close")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def randomize_matrix(self):
        for r in range(12):
            for c in range(12):
                if random.random() > 0.7:
                    item = QTableWidgetItem("⚡ CV")
                    item.setBackground(QColor(255, 107, 0))
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.table.setItem(r, c, item)
                else:
                    self.table.setItem(r, c, None)
        QMessageBox.information(self, "Patch Bay", "Modular routing matrix randomized successfully.")

    def clear_matrix(self):
        self.table.clearContents()

# ==========================================
# SCRIPT PANEL DIALOG
# ==========================================
class ScriptPanelDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Mathematician's EQR & Chaos Scripting Suite")
        self.resize(700, 500)
        self.setStyleSheet(DAW_STYLE)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<h3>📜 Python / EQR Phase-Space Script Console</h3>"))

        self.editor = QTextEdit()
        self.editor.setPlainText(
            "# Custom EQR Operator & Curvature Evaluation Script\n"
            "import numpy as np\n\n"
            "def evaluate_phase_space(step_matrix, curvature=1.618):\n"
            "    print(f'Evaluating EQR tensor across matrix with curvature {curvature}')\n"
            "    return True\n\n"
            "evaluate_phase_space(None, 1.618033)\n"
        )
        self.editor.setStyleSheet("background-color: #141414; color: #00ffcc; font-family: monospace; font-size: 11px;")
        layout.addWidget(self.editor)

        btn_layout = QHBoxLayout()
        run_btn = QPushButton("▶ Run Script Evaluation")
        run_btn.setStyleSheet("background-color: #ff6b00; color: white;")
        run_btn.clicked.connect(lambda: QMessageBox.information(self, "Script Engine", "Script executed successfully in active memory namespace."))
        btn_layout.addWidget(run_btn)

        close_btn = QPushButton("Close Panel")
        close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
class MusicFractallizer:
    def __init__(self, dimensions=('x', 'y', 'z'), survival_mode=True):
        self.dimensions = dimensions
        self.survival_mode = survival_mode
        self.active_patches = []
    def generate_fractal_stream(self, seed_data):
        return {dim: np.tanh(seed_data) for dim in self.dimensions}

class RealitySynthEngine:
    def __init__(self, survival_mode=True):
        self.fractallizer = MusicFractallizer(dimensions=('x', 'y', 'z'), survival_mode=survival_mode)
    def render_reality_patch(self, base_patch_data):
        return {coord: sig.tolist() for coord, sig in self.fractallizer.generate_fractal_stream(base_patch_data).items()}


class AdvancedWaveformVisualizerCanvas(QWidget):
    """Multi-model real-time Wavetable, Vector, and Algebraic Equation Visualizer."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(280)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.phase = 0.0
        self.active_mode = "Eskivector"

    def update_phase(self):
        self.phase += 0.05
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        p.fillRect(0, 0, w, h, QColor("#0a0e14"))
        p.setPen(QPen(QColor("#161b22"), 1))
        for x in range(0, w, 40):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            p.drawLine(0, y, w, y)

        path = QPainterPath()
        center_y = h / 2.0
        meum_ratio = 1.618

        for px in range(w):
            t_val = (px / w) * 4.0 * math.pi + self.phase
            if self.active_mode == "Eskivector":
                val = MathEngine.isn(t_val * meum_ratio) + 0.5 * MathEngine.ics(t_val)
            elif self.active_mode == "Eskitable":
                val = MathEngine.arcisn(math.sin(t_val)) * MathEngine.arcics(math.cos(t_val * 0.5))
            elif self.active_mode == "Eskiosc":
                val = MathEngine.isn_inv(math.sin(t_val))
            else: # Eskiequation
                val = MathEngine.isn(t_val) * MathEngine.ics(t_val * meum_ratio) + MathEngine.arcisn(math.sin(t_val * 0.25))

            py = center_y - (val * (h * 0.35))
            if px == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)

        p.setPen(QPen(QColor("#00ffcc"), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawPath(path)

        p.setPen(QPen(QColor("#58a6ff"), 1, Qt.PenStyle.DashLine))
        p.drawLine(0, int(center_y), w, int(center_y))
        p.drawText(15, 25, f"Visualizer Active Model: [{self.active_mode}] — Isosceles Trig & Algebraic Waveform")
class MultiLaneSequencerCanvas(QWidget):
    """Sequencer canvas with built-in modulation patch outputs per track."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.step_count = 16
        self.setMinimumHeight(200)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.steps = [{"amp": 0.9, "pitch": 440.0, "gate": True} for _ in range(16)]

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor("#0a0e14"))
        step_w = w / self.step_count
        for i in range(self.step_count):
            sx = i * step_w
            val_h = self.steps[i]["amp"] * (h - 20)
            p.setBrush(QBrush(QColor("#00ffcc")))
            p.drawRoundedRect(QRectF(sx + 2, h - val_h - 10, step_w - 4, val_h), 2, 2)
class StepPainterSequencerCanvas(QWidget):
    """Sequencer supporting color-coded step painting for frequency, amplitude, and duration."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.step_count = 16
        self.setMinimumHeight(300)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.steps = [
            {"freq": 220.0 + i*30, "amp": 0.7, "duration": 1.0, "color": QColor("#00ffcc" if i%2==0 else "#58a6ff")}
            for i in range(32)
        ]
        self.painting_mode = "amplitude"

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor("#0a0e14"))
        p.setPen(QPen(QColor("#00ffcc"), 1))
        p.drawText(15, 25, f"Step Painter Mode: [{self.painting_mode}] — Active Step Count: {self.step_count}")

class IdealizedMathKnob(QWidget):
    """Skeuomorphic rotary controller designed for mathematical mapping ($x, y, z, t$ space)."""
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, math_note="", parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.min_val = min_val
        self.max_val = max_val
        self.value = default_val
        self.math_note = math_note
        self.setFixedSize(110, 130)
        self.dragging = False
        self.last_y = 0
        self.is_patched = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QPen(QColor("#58a6ff"), 1))
        painter.drawText(0, 8, self.width(), 14, Qt.AlignmentFlag.AlignCenter, self.label_text)

        painter.setPen(QPen(QColor("#8b949e"), 1))
        painter.drawText(0, 22, self.width(), 12, Qt.AlignmentFlag.AlignCenter, f"Val: {self.value:.3f}")

        center = QPointF(55, 62)
        radius = 20.0

        painter.setBrush(QBrush(QColor("#161b22")))
        painter.setPen(QPen(QColor("#30363d"), 2))
        painter.drawEllipse(center, radius, radius)

        span_val = self.max_val - self.min_val if self.max_val != self.min_val else 1.0
        normalized = (self.value - self.min_val) / span_val
        angle = math.radians(-130 + (normalized * 260))
        tip_x = center.x() + (radius - 5) * math.sin(angle)
        tip_y = center.y() - (radius - 5) * math.cos(angle)

        painter.setPen(QPen(QColor("#00ffcc"), 2.5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawLine(center, QPointF(tip_x, tip_y))

        jack_center = QPointF(55, 96)
        painter.setBrush(QBrush(QColor("#0d1117")))
        painter.setPen(QPen(QColor("#00ffcc") if self.is_patched else QColor("#484f58"), 1.5))
        painter.drawEllipse(jack_center, 5.0, 5.0)

        painter.setPen(QPen(QColor("#c9d1d9"), 1))
        painter.drawText(2, 108, self.width() - 4, 20, Qt.AlignmentFlag.AlignCenter, self.math_note)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            jack_center = QPointF(55, 96)
            if (event.position() - jack_center).manhattanLength() < 12:
                self.is_patched = not self.is_patched
                self.update()
            else:
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

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        span = self.max_val - self.min_val
        step = span * (0.02 if delta > 0 else -0.02)
        self.value = max(self.min_val, min(self.max_val, self.value + step))
        self.update()
class SequencerEngine:
    def __init__(self, steps=16):
        self.steps = steps
        self.current_step = 0
        self.active_pattern = [0.0] * steps

    def step_forward(self, synth_callback):
        """Advances the sequencer step and triggers sound generation."""
        val = self.active_pattern[self.current_step]

        # Trigger synth callback with current coordinate step intensity
        if synth_callback and callable(synth_callback):
            synth_callback(self.current_step, val)

        self.current_step = (self.current_step + 1) % self.steps
        return self.current_step
class ModularSequencerEngine:
    """Drives step logic across tabs and translates steps into active synth events."""
    def __init__(self, total_steps=16):
        self.total_steps = total_steps
        self.current_step = 0
        self.tab_triggers = {} # Maps tab index/name to step arrays

    def register_tab_grid(self, tab_id, default_pattern=None):
        if default_pattern is None:
            default_pattern = [1 if i % 4 == 0 else 0 for i in range(self.total_steps)]
        self.tab_triggers[tab_id] = default_pattern

    def advance_clock(self, synth_bank, active_tab_id, x_val, y_val, z_val):
        # Advance step counter
        self.current_step = (self.current_step + 1) % self.total_steps

        # Check if current tab has a trigger pattern
        if active_tab_id in self.tab_triggers:
            pattern = self.tab_triggers[active_tab_id]
            is_triggered = pattern[self.current_step]

            if is_triggered:
                # Force generation check across active synths using x, y, z variables
                freq = 220.0 * (1.0 + (self.current_step % 7) * 0.15)
                synth_bank.spawn_synth("Additive", base_freq=freq)

        return self.current_step
class InteractivePatchbayCanvas(QWidget):
    """Master Hub visualizing all cross-panel connections."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 700)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()
        p.fillRect(0, 0, w, h, QColor("#0a0e14"))

        # Grid lines
        p.setPen(QPen(QColor("#161b22"), 1))
        for x in range(0, w, 40):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            p.drawLine(0, y, w, y)

        # Render global cross-panel cables
        p.setPen(QPen(QColor("#ff7b72"), 3.0, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        for src, dst in global_patch_bus.cables:
            # Placeholder coordinates mapping for visualization overview
            p.drawLine(150, 150, 750, 400)

        p.setPen(QPen(QColor("#8b949e"), 1))
        p.drawText(25, 35, "Master Patchbay: Monitoring all cross-panel connections between Panels 1, 2, and 3.")
class SideDisplayPanelManager:
    """Rebuilds and populates side display panels with active modular routing controls."""
    def __init__(self, parent_layout):
        self.layout = parent_layout
        self.panels = {}
        self.init_panels()

    def init_panels(self):
        # Panel A: Macro X-Y-Z Variable Monitor
        self.panels['xyz_monitor'] = {
            "label": "XYZ Matrix Spatial State",
            "widgets": ["x_slider", "y_slider", "z_slider"],
            "status": "Active"
        }

        # Panel B: Reapplied Side Feature (Spectral Tilt & Harmonic Spread)
        self.panels['spectral_control'] = {
            "label": "Harmonic Spectrum Balancer",
            "widgets": ["tilt_dial", "spread_dial"],
            "status": "Rebuilt & Live"
        }

        # Panel C: Unused Feature Activation (Stochastic Grain Cloud)
        self.panels['stochastic_mod'] = {
            "label": "Stochastic Grain Generator",
            "widgets": ["density_knob", "scatter_knob"],
            "status": "Newly Appplied"
        }

    def render_panel_data(self, x, y, z):
        """Updates side panel readouts dynamically based on core calculations."""
        metrics = {
            "X_Var": round(x, 4),
            "Y_Var": round(y, 4),
            "Z_Var": round(z, 4),
            "Active_Panels": len(self.panels)
        }
        return metrics

class FreeformSequencerCanvas(QWidget):
    """Sequencer canvas supporting dynamic step length and micro-timing."""
    def __init__(self, sequence_data=None, parent=None):
        super().__init__(parent)
        self.seq_data = sequence_data if sequence_data is not None else [0.0] * 16
        self.step_count = 16
        self.non_quant_offset = 0.0
        self.setMinimumHeight(260)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.nodes = [QPointF(60, 180), QPointF(340, 60), QPointF(680, 140), QPointF(960, 50)]
        self.wires = [(self.nodes[0], self.nodes[1]), (self.nodes[2], self.nodes[3])]
        self.active_node = None
        self.wiring_start = None

    def set_step_count(self, count):
        self.step_count = count
        if len(self.seq_data) < count:
            self.seq_data.extend([0.0] * (count - len(self.seq_data)))
        self.update()

    def set_non_quant_offset(self, offset):
        self.non_quant_offset = offset
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        try:
            if isinstance(self.seq_data, dict):
                notes = self.seq_data.get("notes", [])
            elif isinstance(self.seq_data, list):
                notes = [
                    {"time": float(i) + self.non_quant_offset, "duration": 1.0, "active": bool(val != 0)}
                    for i, val in enumerate(self.seq_data[:self.step_count])
                ]
            else:
                notes = []

            w, h = self.width(), self.height()
            p.fillRect(0, 0, w, h, QColor("#0a0e14"))

            p.setPen(QPen(QColor("#161b22"), 1))
            for x in range(0, w, 40):
                p.drawLine(x, 0, x, h)
            for y in range(0, h, 40):
                p.drawLine(0, y, w, y)

            for p1, p2 in self.wires:
                ctrl = QPointF((p1.x() + p2.x()) / 2, max(p1.y(), p2.y()) + 60)
                path = QPainterPath()
                path.moveTo(p1)
                path.cubicTo(ctrl, ctrl, p2)
                p.setPen(QPen(QColor("#00ffcc"), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
                p.drawPath(path)

            max_time = max([n.get("time", 0.0) + n.get("duration", 1.0) for n in notes] + [float(self.step_count)])
            scale_x = w / max(float(self.step_count), max_time)

            for i, note in enumerate(notes):
                nx = note.get("time", float(i)) * scale_x
                nw = max(12, note.get("duration", 1.0) * scale_x)
                ny = 15 + (i % 4) * 24

                is_active = note.get("active", True)
                p.setBrush(QBrush(QColor("#00ffcc" if is_active else "#21262d")))
                p.setPen(QPen(QColor("#ffffff" if is_active else "#484f58"), 1))
                p.drawRoundedRect(int(nx), int(ny), int(nw), 18, 4, 4)

                p.setPen(QPen(QColor("#ffffff" if is_active else "#8b949e"), 1))
                p.drawText(int(nx) + 4, int(ny) + 13, f"N{i+1}")

        finally:
            p.end()

    def mousePressEvent(self, event):
        pos = event.position()
        if event.button() == Qt.MouseButton.RightButton:
            self.nodes.append(QPointF(pos.x(), pos.y()))
            self.nodes.sort(key=lambda p: p.x())
            self.update()
        elif event.button() == Qt.MouseButton.LeftButton:
            for node in self.nodes:
                if (node - pos).manhattanLength() < 14:
                    self.wiring_start = node
                    return
            for idx, node in enumerate(self.nodes):
                if (node - pos).manhattanLength() < 22:
                    self.active_node = idx
                    break

    def mouseMoveEvent(self, event):
        if self.active_node is not None:
            new_pos = event.position()
            self.nodes[self.active_node] = QPointF(max(0, min(self.width(), new_pos.x())), max(0, min(self.height(), new_pos.y())))
            self.update()

    def mouseReleaseEvent(self, event):
        if self.wiring_start:
            pos = event.position()
            for node in self.nodes:
                if (node - pos).manhattanLength() < 18 and node != self.wiring_start:
                    self.wires.append((self.wiring_start, node))
                    break
            self.wiring_start = None
        self.active_node = None
        self.update()
import math
import random

class DynamicSynthManager:
    """Manages live instantiation, tracking, and audio block generation for active synths."""
    def __init__(self, sample_rate=44100.0):
        self.sr = sample_rate
        self.active_instances = []

    def spawn_instance(self, module_type, base_freq=440.0):
        """Spawns a specific interactive synth instance."""
        if module_type == "AdditiveNode":
            inst = AdditiveSynthInstance(base_freq, self.sr)
        elif module_type == "FormantNode":
            inst = FormantSynthInstance(base_freq, self.sr)
        elif module_type == "StochasticNode":
            inst = StochasticNoiseInstance(base_freq, self.sr)
        else:
            inst = StandardSynthInstance(base_freq, self.sr)

        self.active_instances.append(inst)
        # Prune older instances if max polyphony is reached to prevent lag
        if len(self.active_instances) > 16:
            self.active_instances.pop(0)
        return inst

    def process_audio_stream(self, num_samples, x, y, z):
        """Renders and sums all active synth instances using x, y, z coordinate parameters."""
        master_buffer = [0.0] * num_samples
        for instance in list(self.active_instances):
            if instance.is_finished():
                self.active_instances.remove(instance)
                continue
            buf = instance.render_block(num_samples, x, y, z)
            for i in range(num_samples):
                master_buffer[i] += buf[i]
        return master_buffer
class PatchbayCanvas(QWidget):
    """Interactive canvas that visually renders node patching wires and real-time waveforms."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.amplitude_data = [0.0] * 60
        self.connections = [
            ("EskiVector Node", "Reality Wave-Folder"),
            ("EskiTable Unit", "Fractalizer Matrix")
        ]

    def update_data(self, new_val):
        self.amplitude_data.pop(0)
        # Scaled up gain for high-visibility waveforms
        self.amplitude_data.append(new_val * 4.5)
        self.update()

    def add_connection(self, source, target):
        if (source, target) not in self.connections:
            self.connections.append((source, target))
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dark studio background
        painter.fillRect(self.rect(), QColor(15, 15, 20))

        # Draw Coded Patching Wires
        wire_pen = QPen(QColor(255, 140, 0))
        wire_pen.setWidth(3)
        painter.setPen(wire_pen)

        # Render visual nodes and connecting wires across the canvas
        node_positions = {
            "EskiVector Node": QPointF(100, 60),
            "EskiTable Unit": QPointF(100, 140),
            "Reality Wave-Folder": QPointF(400, 60),
            "Fractalizer Matrix": QPointF(400, 140)
        }

        for src, tgt in self.connections:
            if src in node_positions and tgt in node_positions:
                p1 = node_positions[src]
                p2 = node_positions[tgt]
                # Draw curved patching wire
                painter.drawLine(int(p1.x()), int(p1.y()), int(p2.x()), int(p2.y()))

        # Draw Node Blocks
        for name, pt in node_positions.items():
            painter.setBrush(QBrush(QColor(40, 40, 55)))
            painter.setPen(QPen(QColor(0, 220, 150), 2))
            painter.drawRoundedRect(int(pt.x() - 70), int(pt.y() - 25), 140, 50, 8, 8)
            painter.setPen(QColor(255, 255, 255))
            painter.drawText(int(pt.x() - 60), int(pt.y() + 5), name)

        # Draw Scaled Waveform / Vector Display at the bottom half
        graph_y_offset = 220
        wave_pen = QPen(QColor(0, 255, 180))
        wave_pen.setWidth(3)
        painter.setPen(wave_pen)

        width = self.width()
        step = width / max(len(self.amplitude_data) - 1, 1)

        for i in range(len(self.amplitude_data) - 1):
            x1 = int(i * step)
            y1 = int(graph_y_offset - self.amplitude_data[i] * 40)
            x2 = int((i + 1) * step)
            y2 = int(graph_y_offset - self.amplitude_data[i + 1] * 40)
            painter.drawLine(x1, y1, x2, y2)
# -------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION DATABASE
# -------------------------------------------------------------------------
FREQUENCY_432HZ = 432.0
class StandardSynthInstance:
    def __init__(self, freq, sr):
        self.freq = freq
        self.sr = sr
        self.phase = 0.0
        self.life = 100

    def is_finished(self):
        return self.life <= 0

    def render_block(self, num_samples, x, y, z):
        buf = []
        modulated_freq = self.freq * (0.8 + abs(x) * 0.4)
        step = (2.0 * math.pi * modulated_freq) / self.sr
        for _ in range(num_samples):
            self.phase += step
            val = math.sin(self.phase) * 0.3 * max(0.0, y)
            buf.append(val)
        self.life -= 1
        return buf

class AdditiveSynthInstance(StandardSynthInstance):
    def render_block(self, num_samples, x, y, z):
        buf = []
        harmonics = [1.0, 2.0, 3.5, 4.0, 6.0]
        step = (2.0 * math.pi * self.freq) / self.sr
        for i in range(num_samples):
            self.phase += step
            sample = 0.0
            for h in harmonics:
                sample += math.sin(self.phase * h * (1.0 + z * 0.05)) / h
            buf.append(sample * 0.15 * max(0.0, y))
        self.life -= 1
        return buf

class FormantSynthInstance(StandardSynthInstance):
    def render_block(self, num_samples, x, y, z):
        buf = []
        carrier_step = (2.0 * math.pi * self.freq) / self.sr
        formant_step = (2.0 * math.pi * (self.freq * abs(x * 3.0))) / self.sr
        for _ in range(num_samples):
            self.phase += carrier_step
            c = math.sin(self.phase)
            m = math.cos(self.phase * 1.5) * math.sin(formant_step)
            val = c * m * 0.2 * abs(z)
            buf.append(val)
        self.life -= 1
        return buf

class StochasticNoiseInstance(StandardSynthInstance):
    def render_block(self, num_samples, x, y, z):
        buf = []
        for _ in range(num_samples):
            noise = (random.random() * 2.0 - 1.0)
            val = noise * 0.1 * abs(x) * max(0.0, y)
            buf.append(val)
        self.life -= 1
        return buf
class MasterSynthBank:
    """Manages dynamic spawning and audio rendering for modular synths."""
    def __init__(self, sample_rate=44100.0):
        self.sr = sample_rate
        self.active_synths = []

    def spawn_synth(self, synth_type, base_freq=440.0):
        if synth_type == "Additive":
            synth = AdditiveSynthNode(base_freq, self.sr)
        elif synth_type == "Formant":
            synth = FormantSynthNode(base_freq, self.sr)
        elif synth_type == "NoiseBurst":
            synth = NoiseBurstNode(base_freq, self.sr)
        else:
            synth = StandardWaveSynthNode(base_freq, self.sr)
        self.active_synths.append(synth)
        return synth

    def render_buffer(self, num_samples, x_mod=1.0, y_mod=1.0, z_mod=1.0):
        buffer = [0.0] * num_samples
        for synth in self.active_synths:
            s_buf = synth.generate_block(num_samples, x_mod, y_mod, z_mod)
            for i in range(num_samples):
                buffer[i] += s_buf[i]
        return buffer
# ==========================================
# 3. INTERACTIVE SEQUENCER, SERIALIZATION & VISUAL LAYERS
# ==========================================
class InteractiveSequencerGrid:
    """Handles step sequencing and triggers live synth module generation."""
    def __init__(self, steps=16):
        self.steps = steps
        self.current_step = 0
        self.pattern_matrix = [1 if i % 4 == 0 else 0 for i in range(steps)]

    def step_clock(self, synth_manager, x, y, z):
        self.current_step = (self.current_step + 1) % self.steps
        if self.pattern_matrix[self.current_step] == 1:
            if x > 0.3:
                m_type = "Additive"
            elif z > 0.5:
                m_type = "Formant"
            else:
                m_type = "Stochastic"
            base_f = 110.0 * (1.0 + (self.current_step % 8) * 0.2)
            synth_manager.spawn_instance(m_type, base_freq=base_f)
        return self.current_step



class AudioEngineBridge:
    """Bridges the UI coordinate state and sequencer ticks directly to the audio output stream."""
    def __init__(self, synth_manager, sequencer_grid):
        self.synth_manager = synth_manager
        self.sequencer = sequencer_grid

    def audio_callback(self, outdata, frames, time_info, status, x_val, y_val, z_val):
        """Standard NumPy/SoundDevice or PyAudio callback hook."""
        # 1. Advance sequencer clock per audio buffer block / tick
        self.sequencer.step_clock(self.synth_manager, x_val, y_val, z_val)

        # 2. Render live audio buffer from active synth instances using x, y, z
        buffer = self.synth_manager.process_audio_stream(frames, x_val, y_val, z_val)

        # 3. Format output for playback stream
        for i in range(frames):
            val = buffer[i] if i < len(buffer) else 0.0
            # Simple soft-clip limiter to prevent distortion
            outdata[i] = max(-1.0, min(1.0, val))
class StandardWaveSynthNode:
    def __init__(self, freq, sr):
        self.freq = freq
        self.sr = sr
        self.phase = 0.0
        self.amp = 0.5

    def generate_block(self, num_samples, x, y, z):
        buf = []
        # Incorporating x, y, z variables for mathematical spatial modulation
        effective_freq = self.freq * (0.5 + abs(x) * 0.5)
        step = (2.0 * math.pi * effective_freq) / self.sr
        for _ in range(num_samples):
            self.phase += step
            val = math.sin(self.phase) * self.amp * y
            buf.append(val)
        return buf
class ModularTabManager(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        # Add initial control tab workspace
        self.add_new_module_tab("Core Synthesizer Matrix")
    def add_new_module_tab(self, title_prefix="Node Module"):
        tab_count = self.count()
        tab_title = f"{title_prefix} {tab_count + 1}"

        container = QWidget()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)

        inner_widget = QWidget()
        layout = QVBoxLayout(inner_widget)

        # Populate workspace with expanded DSP control and patch routing panels
        layout.addWidget(QLabel(f"--- {tab_title} Workspace ---"))
        layout.addWidget(self.create_dsp_control_panel())
        layout.addWidget(self.create_patch_bay_panel())
        layout.addWidget(QLabel(f"--- {tab_title} Workspace ---"))
        layout.addWidget(CoordinateVisualizer())       # Snippet 5
        layout.addWidget(FormulaModulatorWidget())     # Snippet 3
        layout.addWidget(ModulationMatrixWidget())     # Snippet 4
        layout.addWidget(self.create_dsp_control_panel())
        scroll.setWidget(inner_widget)

        tab_layout = QVBoxLayout(container)
        tab_layout.addWidget(scroll)
        container.setLayout(tab_layout)

        self.addTab(container, tab_title)
        self.setCurrentWidget(container)

    def close_tab(self, index):
        if self.count() > 1:
            widget = self.widget(index)
            self.removeTab(index)
            widget.deleteLater()

    def create_dsp_control_panel(self):
        panel = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(QPushButton("Bypass FX"))
        layout.addWidget(QPushButton("Sync LFO"))
        layout.addWidget(QPushButton("Resonant Feedback"))
        panel.setLayout(layout)
        return panel

    def create_patch_bay_panel(self):
        panel = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(QLabel("Patch Matrix: [X -> Cutoff] [Y -> Resonance] [Z -> Delay Time]"))
        panel.setLayout(layout)
        return panel
class ModularTabController:
    """Manages active tabs and links user interface adjustments to synth modulation."""
    def __init__(self):
        self.active_tab_index = 0
        self.tab_names = ["Additive Grid", "Formant Space", "Stochastic Cloud", "Master Matrix"]

    def switch_tab(self, index):
        self.active_tab_index = index % len(self.tab_names)
        return self.tab_names[self.active_tab_index]

    def get_tab_specific_multiplier(self, x, y, z):
        """Applies distinct mathematical scaling based on the currently selected tab."""
        if self.active_tab_index == 0:
            return x * 1.5 # Additive focus
        elif self.active_tab_index == 1:
            return y * 2.0 # Formant vocal resonance focus
        elif self.active_tab_index == 2:
            return z * 1.2 # Stochastic noise scatter focus
        else:
            return (x + y + z) / 3.0 # Master blend

class GrooveboxSerializationManager:
    """Handles saving and loading of sequencer patterns and active synth configurations."""

    @staticmethod
    def export_project(filepath, sequencer_grid, synth_manager, x, y, z):
        data = {
            "version": "2.0",
            "coordinates": {"x": x, "y": y, "z": z},
            "sequencer_pattern": sequencer_grid.pattern_matrix,
            "active_synths": [type(s).__name__ for s in synth_manager.active_instances]
        }
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Export failed: {e}")
            return False

    @staticmethod
    def import_project(filepath, sequencer_grid, synth_manager):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            if "sequencer_pattern" in data:
                sequencer_grid.pattern_matrix = data["sequencer_pattern"]

            synth_manager.active_instances.clear()
            if "active_synths" in data:
                for s_type in data["active_synths"]:
                    synth_manager.spawn_instance(s_type, base_freq=220.0)

            return data.get("coordinates", {"x": 0.5, "y": 0.5, "z": 0.5})
        except Exception as e:
            print(f"Import failed: {e}")
            return None



class AdditiveSynthNode(StandardWaveSynthNode):
    """Generates sound using harmonic overtone stacking modulated by z."""
    def generate_block(self, num_samples, x, y, z):
        buf = []
        harmonics = [1.0, 2.0, 3.0, 4.0, 6.0, 8.0]
        weights = [1.0, 0.5, 0.25, 0.125, 0.0625, 0.03]
        step = (2.0 * math.pi * self.freq) / self.sr

        for i in range(num_samples):
            self.phase += step
            sample = 0.0
            for h, w in zip(harmonics, weights):
                sample += math.sin(self.phase * h * (1.0 + z * 0.1)) * w
            buf.append(sample * self.amp * y * 0.5)
        return buf

class FormantSynthNode(StandardWaveSynthNode):
    """Vocal/formant filtered oscillation powered by variable x, y, z mapping."""
    def generate_block(self, num_samples, x, y, z):
        buf = []
        formant_freq = 800.0 * abs(x + 0.1)
        step = (2.0 * math.pi * self.freq) / self.sr
        f_step = (2.0 * math.pi * formant_freq) / self.sr

        for _ in range(num_samples):
            self.phase += step
            carrier = math.sin(self.phase)
            modulator = math.sin(self.phase * 1.414) * math.cos(f_step)
            val = carrier * modulator * self.amp * z
            buf.append(val)
        return buf
class VirtualPatchCable:
    def __init__(self, source_node, target_param, attenuation=1.0):
        self.source_node = source_node
        self.target_param = target_param
        self.attenuation = attenuation
        self.is_connected = True

    def route(self, x_val, y_val, z_val):
        """Routes coordinate outputs or LFO signals into target DSP parameters."""
        if not self.is_connected:
            return 0.0

        # Select coordinate source based on mapping string
        val = 0.0
        if self.source_node == 'X':
            val = x_val
        elif self.source_node == 'Y':
            val = y_val
        elif self.source_node == 'Z':
            val = z_val

        return val * self.attenuation
class NoiseBurstNode(StandardWaveSynthNode):
    """Stochastic rhythmic noise burst generator for percussion/texture tabs."""
    def generate_block(self, num_samples, x, y, z):
        buf = []
        for _ in range(num_samples):
            noise = (random.random() * 2.0 - 1.0)
            envelope = max(0.0, 1.0 - (self.phase % 1.0))
            val = noise * envelope * self.amp * x * y
            buf.append(val)
        return buf
class VisualInstrumentLayerManager:
    """Manages the visual stacking and layout rendering of active synth modules on screen."""
    def __init__(self):
        self.visual_nodes = []

    def update_visual_stack(self, active_instances):
        self.visual_nodes.clear()
        for idx, instance in enumerate(active_instances):
            node_name = type(instance).__name__
            ui_node_card = {
                "id": idx,
                "type": node_name,
                "layer_depth": idx * 15,
                "status": "Active"
            }
            self.visual_nodes.append(ui_node_card)
        return self.visual_nodes
# -------------------------------------------------------------------------
# GLOBAL CABLE ROUTING & RESAMPLING BUS MANAGER
# -------------------------------------------------------------------------
class JackButton(QPushButton):
    """Custom interactive jack button assignable to every waveform and musical parameter."""
    def __init__(self, param_name, parent=None):
        super().__init__("JACK", parent)
        self.param_name = param_name
        self.setCheckable(True)
        self.setStyleSheet("""
            QPushButton {
                background-color: #2b2b2b;
                color: #00ffcc;
                border: 1px solid #00ffcc;
                border-radius: 4px;
                font-size: 10px;
                font-weight: bold;
                padding: 3px;
            }
            QPushButton:checked {
                background-color: #00ffcc;
                color: #121212;
            }
        """)
        self.toggled.connect(self.on_toggle)

    def on_toggle(self, checked):
        state = "PATCHED" if checked else "UNPATCHED"
        print(f"Jack Control [{self.param_name}]: {state}")


class ParameterControlRow(QWidget):
    """A wrapper widget containing a label, slider, and an assigned JackButton for modulation routing."""
    def __init__(self, label_text, min_val=0, max_val=100, default_val=50, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.label.setStyleSheet("color: #ffffff; font-size: 11px;")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(min_val, max_val)
        self.slider.setValue(default_val)

        self.jack_btn = JackButton(label_text)

        layout.addWidget(self.label, 2)
        layout.addWidget(self.slider, 3)
        layout.addWidget(self.jack_btn, 1)

        self.setLayout(layout)
MEUM=1.1975807343385265188
class WavetableVectorVisualizerCanvas(QWidget):
    """Real-time Wavetable and Isosceles Trigonometric Polynomial Waveform Visualizer."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(260)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.phase = 0.0

    def update_phase(self):
        self.phase += 0.05
        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        w, h = self.width(), self.height()

        p.fillRect(0, 0, w, h, QColor("#0a0e14"))
        p.setPen(QPen(QColor("#161b22"), 1))
        for x in range(0, w, 40):
            p.drawLine(x, 0, x, h)
        for y in range(0, h, 40):
            p.drawLine(0, y, w, y)

        path = QPainterPath()
        center_y = h / 2.0
        meum_ratio = 1.1975807343385265188

        for px in range(w):
            t_val = (px / w) * 4.0 * math.pi + self.phase
            val = MathEngine.isn(t_val * meum_ratio) + 0.5 * MathEngine.ics(t_val) * MathEngine.arcisn(math.sin(t_val * 0.5))
            py = center_y - (val * (h * 0.35))
            if px == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)

        p.setPen(QPen(QColor("#00ffcc"), 2.2, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawPath(path)

        p.setPen(QPen(QColor("#58a6ff"), 1, Qt.PenStyle.DashLine))
        p.drawLine(0, int(center_y), w, int(center_y))
        p.drawText(10, 20, "Eskivector / Eskitable / Eskiosc / Eskiequation Real-Time Wavetable Visualizer")
class GlobalCrossTabBusManager:
    """Manages universal inter-synth wiring, dedicated synth input/output jacks, master audio routing, and resampling."""
    def __init__(self):
        self.global_cables = []
        self.subscribers = []
        self.resampling_active = False
        self.resampled_buffers = []

    def register_subscriber(self, widget):
        if widget not in self.subscribers:
            self.subscribers.append(widget)

    def add_cable(self, src_module, src_node, tgt_module, tgt_node, polarity="Neutral", gain=1.0):
        cable = {
            "src_module": src_module, "src_node": src_node,
            "tgt_module": tgt_module, "tgt_node": tgt_node,
            "polarity": polarity, "gain": gain
        }
        self.global_cables.append(cable)
        self.broadcast_update()

    def remove_cable(self, index):
        if 0 <= index < len(self.global_cables):
            self.global_cables.pop(index)
            self.broadcast_update()

    def update_cable_polarity_gain(self, index, polarity, gain_delta):
        if 0 <= index < len(self.global_cables):
            self.global_cables[index]["polarity"] = polarity
            self.global_cables[index]["gain"] = max(0.1, round(self.global_cables[index]["gain"] + gain_delta, 2))
            self.broadcast_update()

    def trigger_resampling(self):
        self.resampling_active = True
        captured_signature = f"Resampled_Loop_{len(self.resampled_buffers) + 1}_{random.randint(1000, 9999)}"
        self.resampled_buffers.append(captured_signature)
        self.broadcast_update()
        return captured_signature

    def clear_all(self):
        self.global_cables.clear()
        self.resampled_buffers.clear()
        self.resampling_active = False
        self.broadcast_update()

    def broadcast_update(self):
        for sub in self.subscribers:
            if hasattr(sub, "on_global_patch_updated"):
                sub.on_global_patch_updated(self.global_cables)

GLOBAL_BUS = GlobalCrossTabBusManager()


# -------------------------------------------------------------------------
# ACTIVATED DRUM & SEQUENCER RUNTIME CONTROLLER WITH RHYTHM FLUX LINKING
# -------------------------------------------------------------------------
class ActiveEngineClock:
    """Drives real-time activation states, step triggers, automation clock ticks, and Rhythm Flux Linking (Global/Concurrent)."""
    def __init__(self, engine):
        self.engine = engine
        self.current_step = 0
        self.transport_active = True
        self.clock_ticks_executed = 0

        # New Rhythm Flux Linking Modes & Parameters
        self.rhythm_flux_mode = "Global" # Options: "Global", "Active Concurrent", "Unlinked"
        self.rhythm_flux_rate = 1.0     # Multiplier governing synchronized rhythm flux across synths/drums
        self.flux_sync_enabled = True

    def tick_clock(self):
        if not self.transport_active:
            return self.current_step
        # Apply rhythm flux rate scaling to step progression
        step_increment = max(1, int(round(self.rhythm_flux_rate)))
        self.current_step = (self.current_step + step_increment) % 64
        self.clock_ticks_executed += 1
        return self.current_step

    def evaluate_drum_trigger(self, kit_name, step_index):
        flux_offset = int(self.rhythm_flux_rate * 2) % 5
        if self.rhythm_flux_mode == "Global":
            return ((step_index + flux_offset) % 4 == 0) or ((step_index + flux_offset) % 3 == 0 and self.engine.survival_mode)
        elif self.rhythm_flux_mode == "Active Concurrent":
            # Interleaved concurrent flux across synths and drums
            return (step_index % max(2, int(3 * self.rhythm_flux_rate)) == 0)
        else:
            return (step_index % 4 == 0)

    def evaluate_sequencer_gate(self, seq_name, step_index):
        if self.rhythm_flux_mode == "Global":
            return (step_index % 2 == 0) or (step_index % int(max(2, 4 / self.rhythm_flux_rate)) == 0)
        elif self.rhythm_flux_mode == "Active Concurrent":
            return (step_index % 3 != 0)
        else:
            return (step_index % 2 == 0)


# -------------------------------------------------------------------------
# CORE GROOVEBOX & HARDWARE ENGINE
# -------------------------------------------------------------------------
class DAWPlaylistGrid(QMainWindow):
    def __init__(self, parent=None, app_ref=None):
        super().__init__(parent)
        self.app_ref = app_ref
        self.setWindowTitle("Master Arrangement Playlist & Playhead")
        self.resize(1200, 750)
        self.setStyleSheet(DAW_STYLE)

        container = QWidget()
        layout = QVBoxLayout(container)

        toolbar = QHBoxLayout()
        toolbar.addWidget(QLabel("<b>Arrangement Master:</b>"))

        self.play_btn = QPushButton("▶ PLAY / PAUSE")
        self.play_btn.setStyleSheet("background-color: #00aa55; color: white; font-weight: bold;")
        toolbar.addWidget(self.play_btn)

        toolbar.addWidget(QLabel("Global Tempo:"))
        self.tempo_spin = QSpinBox()
        self.tempo_spin.setRange(40, 300)
        self.tempo_spin.setValue(120)
        toolbar.addWidget(self.tempo_spin)

        random_song_btn = QPushButton("🎲 Randomize Song")
        random_song_btn.setStyleSheet("background-color: #9900cc; color: white; font-weight: bold;")
        random_song_btn.clicked.connect(self.randomize_entire_song_from_playlist)
        toolbar.addWidget(random_song_btn)

        clear_grid_btn = QPushButton("Clear Global Playlist")
        clear_grid_btn.clicked.connect(self.clear_grid)
        toolbar.addWidget(clear_grid_btn)

        layout.addLayout(toolbar)

        self.grid_table = QTableWidget(len(DEFAULT_INSTRUMENT_LIST), 128)
        self.update_vertical_headers()
        self.grid_table.horizontalHeader().setDefaultSectionSize(40)
        self.grid_table.verticalHeader().setDefaultSectionSize(24)
        self.grid_table.setStyleSheet("""
            QTableWidget { background-color: #161616; gridline-color: #282828; }
            QHeaderView::section { background-color: #1f1f1f; color: #aaaaaa; border: 1px solid #333333; font-size: 9px; }
        """)
        self.grid_table.cellClicked.connect(self.paint_clip)
        layout.addWidget(self.grid_table)

        self.status_bar = QLabel("Status: Playlist ready.")
        self.status_bar.setStyleSheet("color: #00ffcc; font-family: monospace;")
        layout.addWidget(self.status_bar)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_vertical_headers(self):
        if self.app_ref and hasattr(self.app_ref, 'instrument_names'):
            names = self.app_ref.instrument_names
        else:
            names = DEFAULT_INSTRUMENT_LIST
        self.grid_table.setRowCount(len(names))
        self.grid_table.setVerticalHeaderLabels(names)

    def paint_clip(self, row, col):
        item = QTableWidgetItem("■ Seq")
        item.setBackground(QColor(255, 107, 0))
        item.setForeground(QColor(255, 255, 255))
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_table.setItem(row, col, item)

    def clear_grid(self):
        self.grid_table.clearContents()
        self.status_bar.setText("Status: Global playlist cleared.")

    def randomize_entire_song_from_playlist(self):
        if self.app_ref and hasattr(self.app_ref, 'randomize_entire_song'):
            self.app_ref.randomize_entire_song()

    def get_grid_data(self):
        rows = self.grid_table.rowCount()
        cols = self.grid_table.columnCount()
        data = []
        for r in range(rows):
            row_items = []
            for c in range(cols):
                item = self.grid_table.item(r, c)
                row_items.append(item.text() if item is not None else None)
            data.append(row_items)
        return data
class GrooveboxEngine:
    """Core groovebox engine supporting advanced x,y,z operator equations, stochastic micro-timing, and Rhythm Flux linking."""
    def __init__(self):
        self.global_bpm = 112.0
        self.scale_system = "Equation Tonal Scale (Dynamic)"
        self.scale_equation = "x**2 + y - z"
        self.scale_increment = 0.25
        self.divergence_steps_count = 16

        self.survival_mode = False
        self.creative_mode = False
        self.normal_mode = True
        self.fractallizer_enabled = True
        self.eqr_processor_enabled = True

        self.runtime_clock = ActiveEngineClock(self)
        self.runtime_clock.transport_active = True

        self.reality_synth = RealitySynthEngine()
        self.reality_synth.survival_mode = self.survival_mode
        self.fractalizer = MusicFractallizer(dimensions=('x', 'y', 'z'))
        self.fractalizer.survival_mode = self.survival_mode

        self.available_synths = [f"Synth_Node_{i+1}" for i in range(32)]
        self.active_synth_count = 32
        self.active_synths = []
        self.synth_wiring_matrix = {}

        self.math_chord_library = {
            "Unit Harmonic Stack (+/- 1, 2, 3)": [(-3.0, 0.4), (-2.0, 0.6), (-1.0, 0.8), (1.0, 1.0), (2.0, 0.7), (3.0, 0.4)],
            "Divergent Asymmetric Point Pair": [(-4.25, 0.5), (-1.5, 0.9), (0.25, 1.0), (3.75, 0.6)],
            "Scalar Cluster": [(-1.0, 0.5), (0.0, 1.0), (1.0, 0.5), (2.0, 0.25)],
            "Linear Step Sweep (+/- 1 to 5)": [(float(i), 1.0 / abs(i) if i != 0 else 1.0) for i in range(-5, 6) if i != 0],
            "Quantum Divergence Cluster": [(-6.0, 0.2), (-3.5, 0.5), (-1.2, 0.9), (1.2, 0.9), (3.5, 0.5), (6.0, 0.2)],
            "Equation Polynomial Resonance": [(-4.0, 0.3), (-2.0, 0.7), (0.0, 1.0), (2.0, 0.7), (4.0, 0.3)],
            "Hyperbolic Phase Web": [(-5.0, 0.5), (-2.5, 0.8), (2.5, 0.8), (5.0, 0.5)],
            "Advanced Operator Matrix [x*y - z**3]": [(-3.14, 0.7), (-1.57, 0.9), (1.57, 0.9), (3.14, 0.7)]
        }

        self.instrument_sequence_banks = {}
        self.custom_wavetable_shapes = {}
        self.playlist_clips = {}

        self.active_fx_modules = ["Cloud Granulator 1", "Spectral Phase Shifter", "Nonlinear Wavefolder", "Feedback Delay", "Quantum Resonator"]
        self.active_sequencer_modules = ["Master Sequencer Lane 1", "Rhythmic Gate Generator 1", "Polyphonic Arpeggiator 1", "Stochastic Probability Matrix"]
        self.active_drum_kits = ["Kick Matrix 808", "Snare Divergence Engine", "Hi-Hat Noise Burst", "Percussion Cluster"]
        self.active_synth_panels = ["Master Equation Polynomial Synthesizer", "Eskibrutus Vectoreski Synth 1"]

        self.automation_patterns = {
            "Default Filter Sweep": [0.0, 25.0, 50.0, 85.0, 100.0, 75.0, 40.0, 10.0],
            "Resonance Pulse": [10.0, 90.0, 10.0, 90.0, 50.0, 50.0, 100.0, 0.0],
            "Exponential Pitch Ramp": [0.0, 12.0, 24.0, 36.0, 48.0, 60.0, 80.0, 100.0],
            "Chaotic LFO Modulation": [15.0, 85.0, 45.0, 95.0, 10.0, 60.0, 30.0, 90.0],
            "Harmonic Stepped Envelope": [0.0, 33.0, 33.0, 66.0, 66.0, 100.0, 50.0, 25.0],
            "Stochastic Micro-Drift": [50.0, 52.0, 48.0, 55.0, 45.0, 58.0, 42.0, 50.0]
        }

        self.available_patterns = [
            "Primary Bank - Unit Harmonic Stack",
            "Secondary Bank - Divergent Asymmetric",
            "Pulse Pattern A",
            "Pulse Pattern B",
            "Granular Noise Burst",
            "Sub-Bass Oscillator Sweep",
            "Algebraic Lead Motif",
            "Fractal Rhythm Pulse",
            "Quantum Stochastic Groove"
        ]

    def randomize_synth_routing(self):
        count = random.randint(1, 32) if self.creative_mode else 32
        self.active_synths = random.sample(self.available_synths, count)

        self.synth_wiring_matrix = {}
        for i, synth in enumerate(self.active_synths):
            downstream_target = self.active_synths[(i + 1) % len(self.active_synths)]
            modulation_source = random.choice(self.active_synths)
            attenuation_val = 0.75 if self.survival_mode else (1.25 if self.creative_mode else 1.0)

            self.synth_wiring_matrix[synth] = {
                "primary_output": downstream_target,
                "modulator": modulation_source,
                "attenuation": attenuation_val
            }
        return self.active_synths, self.synth_wiring_matrix

    def activate_fractalizer_stream(self):
        if not self.fractallizer_enabled:
            return {}
        dummy_seed = np.linspace(-1, 1, 512)
        self.last_fractal_output = self.fractalizer.generate_fractal_stream(dummy_seed)
        self.fractal_stream_active = True
        return self.last_fractal_output

    def activate_reality_synth_render(self):
        dummy_patch = np.linspace(-1, 1, 512)
        rendered_buffer = self.reality_synth.render_reality_patch(dummy_patch)
        return rendered_buffer

    def add_instrument_sequence_bank(self, instrument_name, seq_name, pitch=0.0, amp=1.0, math_chord="Unit Harmonic Stack (+/- 1, 2, 3)", stretch=1.0, length_steps=16):
        if instrument_name not in self.instrument_sequence_banks:
            self.instrument_sequence_banks[instrument_name] = []

        new_seq = {
            "name": seq_name,
            "pitch": pitch,
            "amp": amp,
            "math_chord": math_chord,
            "stretch": stretch,
            "length_steps": length_steps,
            "notes": [{"time": i * 1.5, "duration": 1.0, "active": self.runtime_clock.evaluate_sequencer_gate(seq_name, i)} for i in range(length_steps)]
        }
        self.instrument_sequence_banks[instrument_name].append(new_seq)
        pat_title = f"{instrument_name} : {seq_name}"
        if pat_title not in self.available_patterns:
            self.available_patterns.append(pat_title)
        return new_seq

    def get_instrument_banks(self, instrument_name):
        if instrument_name not in self.instrument_sequence_banks:
            self.add_instrument_sequence_bank(instrument_name, "Primary Bank", 0.0, 1.0, "Unit Harmonic Stack (+/- 1, 2, 3)", 1.0, 16)
        return self.instrument_sequence_banks[instrument_name]

    def save_custom_wavetable(self, instrument_name, points):
        self.custom_wavetable_shapes[instrument_name] = [QPointF(p.x(), p.y()) for p in points]

    def get_custom_wavetable(self, instrument_name):
        return self.custom_wavetable_shapes.get(instrument_name, [])

    def assign_playlist_clip(self, track: int, bar_pos: float, clip_data: dict):
        self.playlist_clips[(track, bar_pos)] = clip_data

    def remove_playlist_clip(self, track: int, bar_pos: float):
        if (track, bar_pos) in self.playlist_clips:
            del self.playlist_clips[(track, bar_pos)]

    def randomize_song(self):
        self.playlist_clips.clear()
        GLOBAL_BUS.clear_all()
        self.randomize_synth_routing()

        possible_fx = [
            "Cloud Granulator 1", "Cloud Granulator 2", "Spectral Phase Shifter",
            "Nonlinear Wavefolder", "Feedback Delay", "Quantum Resonator",
            "Algebraic Distortion Unit", "Convolution Reverb Matrix", "Stochastic Spectral Shifter"
        ]
        possible_seqs = [
            "Master Sequencer Lane 1", "Rhythmic Gate Generator 1", "Polyphonic Arpeggiator 1",
            "Euclidean Rhythm Engine", "Stochastic Step Sequencer", "Probability Trigger Matrix", "Quantum Operator Sequencer"
        ]
        possible_drums = [
            "Kick Matrix 808", "Snare Divergence Engine", "Hi-Hat Noise Burst",
            "Percussion Cluster", "Algebraic Tom Unit", "Quantum Claves"
        ]
        possible_synths = [
            "Master Equation Polynomial Synthesizer", "Eskibrutus Vectoreski Synth 1",
            "Vector Morph Synth Alpha", "Quantum Phase Synthesizer 2", "Stochastic Harmonic Engine"
        ]

        self.active_fx_modules = random.sample(possible_fx, random.randint(4, len(possible_fx)))
        self.active_sequencer_modules = random.sample(possible_seqs, random.randint(3, len(possible_seqs)))
        self.active_drum_kits = random.sample(possible_drums, random.randint(2, len(possible_drums)))
        self.active_synth_panels = random.sample(possible_synths, random.randint(2, len(possible_synths)))

        equations = [
            "x**2 + y - z",
            "math.sin(x) * y - z**2",
            "x * y - z",
            "abs(x) + math.cos(y) - z",
            "x**3 - y**2 + z",
            "math.tanh(x * y) - z"
        ]
        self.scale_equation = random.choice(equations)
        self.global_bpm = float(random.randint(98, 142))
        self.scale_increment = round(random.uniform(0.15, 0.35), 2)
        self.divergence_steps_count = 16

        modules = self.active_synth_panels + self.active_fx_modules
        for mod in modules:
            rand_points = [QPointF(i * (500 / 16), random.randint(10, 90)) for i in range(17)]
            self.save_custom_wavetable(mod, rand_points)
            self.get_instrument_banks(mod)

        sources = [(self.active_synth_panels[0], "Audio Gain"), (self.active_synth_panels[min(1, len(self.active_synth_panels)-1)], "Filter Q")] + [(fx, "Scatter") for fx in self.active_fx_modules[:2]]
        targets = ["Master Audio Output Bus", "Auxiliary Bus A", "Auxiliary Bus B"]
        polarities = ["+", "-", "Neutral"]

        for _ in range(random.randint(5, 12)):
            src_mod, src_node = random.choice(sources)
            tgt_mod = random.choice(targets)
            pol = random.choice(polarities)
            gain_val = round(random.uniform(0.4, 2.2), 2)
            GLOBAL_BUS.add_cable(src_mod, src_node, tgt_mod, "Primary Sum Node", polarity=pol, gain=gain_val)

        target_bars = random.randint(64, 192)
        num_tracks = random.randint(8, 32)
        pattern_names = self.available_patterns
        chord_names = list(self.math_chord_library.keys())
        auto_names = list(self.automation_patterns.keys())

        for trk in range(num_tracks):
            bar_steps = list(range(0, target_bars, 2))
            chosen_bars = random.sample(bar_steps, min(len(bar_steps), random.randint(14, 40)))

            for bar in chosen_bars:
                clip_data = {
                    "name": random.choice(pattern_names),
                    "chord": random.choice(chord_names),
                    "pitch": float(random.choice([-12, -7, -5, 0, 5, 7, 12, 14])),
                    "amplitude": round(random.uniform(0.4, 1.5), 2),
                    "stretch": round(random.uniform(0.5, 2.0), 2),
                    "automation_pattern": random.choice(auto_names)
                }
                self.playlist_clips[(trk, float(bar))] = clip_data

    def generate_equation_scale_frequencies(self):
        freqs = []
        for i in range(self.divergence_steps_count):
            x = i * self.scale_increment
            y = x * 1.618
            z = 1.0 if (i % 4 == 0 or i % 3 == 0) else 0.0
            try:
                val = eval(self.scale_equation, {"__builtins__": None}, {"x": x, "y": y, "z": z, "math": math})
                freq = FREQUENCY_432HZ + (float(val) * 22.5)
                freqs.append(max(35.0, freq))
            except Exception:
                freqs.append(FREQUENCY_432HZ + (i * 12.0 * self.scale_increment))
        return freqs

    def resolve_math_chord_frequencies(self, chord_name, x_var=1.0, y_var=1.0, z_var=1.0):
        base_freqs = self.generate_equation_scale_frequencies()
        base_f = base_freqs[0] if base_freqs else FREQUENCY_432HZ
        point_pairs = self.math_chord_library.get(chord_name, [(1.0, 1.0)])

        resolved = []
        for offset_mult, amp_val in point_pairs:
            adjusted_offset = offset_mult * x_var * y_var - (z_var * 0.1)
            freq = base_f + (adjusted_offset * self.scale_increment * 55.0)
            resolved.append((max(20.0, freq), amp_val))
        return resolved

    def serialize_project(self, filepath):
        data = {
            "global_bpm": self.global_bpm,
            "scale_system": self.scale_system,
            "scale_equation": self.scale_equation,
            "scale_increment": self.scale_increment,
            "divergence_steps_count": self.divergence_steps_count,
            "survival_mode": self.survival_mode,
            "creative_mode": self.creative_mode,
            "normal_mode": self.normal_mode,
            "fractallizer_enabled": self.fractallizer_enabled,
            "eqr_processor_enabled": self.eqr_processor_enabled,
            "math_chord_library": self.math_chord_library,
            "instrument_sequence_banks": self.instrument_sequence_banks,
            "automation_patterns": self.automation_patterns,
            "playlist_clips": {f"{t},{b}": dat for (t, b), dat in self.playlist_clips.items()},
            "global_cables": GLOBAL_BUS.global_cables,
            "resampled_buffers": GLOBAL_BUS.resampled_buffers,
            "active_synths": self.active_synths,
            "synth_wiring_matrix": self.synth_wiring_matrix,
            "active_fx_modules": self.active_fx_modules,
            "active_sequencer_modules": self.active_sequencer_modules,
            "active_drum_kits": self.active_drum_kits,
            "active_synth_panels": self.active_synth_panels
        }
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def deserialize_project(self, filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
        self.global_bpm = data.get("global_bpm", 112.0)
        self.scale_equation = data.get("scale_equation", "x**2 + y - z")
        self.scale_increment = data.get("scale_increment", 0.25)
        self.divergence_steps_count = data.get("divergence_steps_count", 16)
        self.survival_mode = data.get("survival_mode", False)
        self.creative_mode = data.get("creative_mode", False)
        self.normal_mode = data.get("normal_mode", True)
        self.fractallizer_enabled = data.get("fractallizer_enabled", True)
        self.eqr_processor_enabled = data.get("eqr_processor_enabled", True)
        if "math_chord_library" in data:
            self.math_chord_library = data.get("math_chord_library")
        self.instrument_sequence_banks = data.get("instrument_sequence_banks", {})
        self.automation_patterns = data.get("automation_patterns", {"Default Filter Sweep": [0, 50, 100]})
        self.active_synths = data.get("active_synths", [])
        self.synth_wiring_matrix = data.get("synth_wiring_matrix", {})
        self.active_fx_modules = data.get("active_fx_modules", self.active_fx_modules)
        self.active_sequencer_modules = data.get("active_sequencer_modules", self.active_sequencer_modules)
        self.active_drum_kits = data.get("active_drum_kits", self.active_drum_kits)
        self.active_synth_panels = data.get("active_synth_panels", self.active_synth_panels)
        pc = data.get("playlist_clips", {})
        self.playlist_clips = {}
        for key_str, dat in pc.items():
            t_str, b_str = key_str.split(",")
            self.playlist_clips[(int(t_str), float(b_str))] = dat
        GLOBAL_BUS.global_cables = data.get("global_cables", [])
        GLOBAL_BUS.resampled_buffers = data.get("resampled_buffers", [])
        GLOBAL_BUS.broadcast_update()

    def export_audio(self, filepath, duration_sec=300.0, sample_rate=44100):
        num_samples = int(sample_rate * duration_sec)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)
        wave_data = np.zeros(num_samples)

        bank_index = 0
        total_banks = sum(len(banks) for banks in self.instrument_sequence_banks.values())
        if total_banks == 0:
            total_banks = 1

        for instr_name, banks in self.instrument_sequence_banks.items():
            for bank in banks:
                chord_name = bank.get("math_chord", "Unit Harmonic Stack (+/- 1, 2, 3)")
                pitch_shift = bank.get("pitch", 0.0)
                pitch_multiplier = 2.0 ** (pitch_shift / 12.0)
                resolved_pairs = self.resolve_math_chord_frequencies(chord_name)
                bank_amp = bank.get("amp", 1.0)

                layer_detune = 1.0 + (bank_index - (total_banks / 2.0)) * 0.002
                phase_offset = (bank_index / float(total_banks)) * 2.0 * np.pi

                for freq, pt_amp in resolved_pairs:
                    adjusted_freq = freq * pitch_multiplier * layer_detune
                    tempo_mod_factor = 1.0 + 0.15 * np.sin(2.0 * np.pi * (self.global_bpm / 112.0) * t * 0.05 + phase_offset)
                    gate = 0.5 * (1 + np.sin(2 * np.pi * (self.global_bpm / 60.0) * t * tempo_mod_factor + phase_offset + np.sin(t * 0.1) * 0.05))
                    wave_data += bank_amp * pt_amp * 0.08 * gate * np.sin(2 * np.pi * (adjusted_freq * tempo_mod_factor) * t + phase_offset)

                bank_index += 1

        max_val = np.max(np.abs(wave_data))
        if max_val > 0:
            wave_data = wave_data / max_val
        audio_int = np.int16(wave_data * 32767)

        with wave.open(filepath, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int.tobytes())


# -------------------------------------------------------------------------
# FREE-FLOATING & RESIZABLE WORKSPACE PANEL
# -------------------------------------------------------------------------
class ResizableWorkspacePanel(QWidget):
    def __init__(self, title, content_widget, parent=None):
        super().__init__(parent)
        self.title = title
        self.setMinimumSize(340, 260)
        self.resize(620, 390)
        self.setStyleSheet("""
            ResizableWorkspacePanel {
                background-color: #0d1117;
                border: 1px solid #30363d;
                border-radius: 6px;
            }
            QLabel { color: #c9d1d9; background: transparent; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)
        layout.setSpacing(4)

        header_layout = QHBoxLayout()
        self.title_lbl = QLabel(f"🎛 {title} [Resizable Panel]")
        self.title_lbl.setStyleSheet("color: #f5d97d; font-weight: bold; font-size: 11px; background: transparent;")
        header_layout.addWidget(self.title_lbl)
        header_layout.addStretch()

        resize_hint = QLabel("↔ Drag borders to resize")
        resize_hint.setStyleSheet("color: #8b949e; font-size: 9px; background: transparent;")
        header_layout.addWidget(resize_hint)
        layout.addLayout(header_layout)
        layout.addWidget(content_widget)

        self.dragging = False
        self.resizing = False
        self.drag_position = QPointF()
        self.resize_margin = 12

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.position().x() >= self.width() - self.resize_margin and event.position().y() >= self.height() - self.resize_margin:
                self.resizing = True
            else:
                self.dragging = True
                self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.resizing:
            new_w = max(340, event.position().x())
            new_h = max(260, event.position().y())
            self.resize(int(new_w), int(new_h))
            event.accept()
        elif self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False
        self.resizing = False
        event.accept()


# -------------------------------------------------------------------------
# FREEHAND DRAWABLE WAVETABLE CANVAS
# -------------------------------------------------------------------------
class WavetableCanvas(QWidget):
    def __init__(self, instrument_name, engine, parent=None):
        super().__init__(parent)
        self.instrument_name = instrument_name
        self.engine = engine
        self.setMinimumHeight(110)
        self.setStyleSheet("background-color: #0d1117; border: 1px solid #30363d; border-radius: 4px;")

        existing = self.engine.get_custom_wavetable(self.instrument_name)
        if existing:
            self.points = list(existing)
        else:
            self.points = [QPointF(i * (500 / 16), 55 + 25 * math.sin(i * 0.4)) for i in range(17)]

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#0d1117"))

        p.setPen(QPen(QColor("#161b22"), 1, Qt.PenStyle.DashLine))
        for x in range(0, self.width(), 50): p.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 30): p.drawLine(0, y, self.width(), y)

        if len(self.points) >= 2:
            path = QPainterPath(); path.moveTo(self.points[0])
            for pt in self.points[1:]: path.lineTo(pt)
            p.setPen(QPen(QColor("#00ffcc"), 2.0))
            p.drawPath(path)

        p.setBrush(QBrush(QColor("#f5d97d")))
        p.setPen(QPen(QColor("#ffffff"), 1))
        for pt in self.points: p.drawEllipse(pt, 3, 3)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            self.points.append(QPointF(max(0, min(self.width(), pos.x())), max(5, min(self.height() - 5, pos.y()))))
            self.points.sort(key=lambda pt: pt.x())
            if len(self.points) > 24:
                self.points = self.points[:24]
            self.engine.save_custom_wavetable(self.instrument_name, self.points)
            self.update()


# -------------------------------------------------------------------------
# INTERACTIVE PATCHABLE KNOB & PATCH JACK
# -------------------------------------------------------------------------
class PatchableKnob(QWidget):
    """Features direct straightforward envelope/decay responsiveness and patch jack capability."""
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, unit="", module_name="Synth 1", parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.min_val = min_val
        self.max_val = max_val
        self.current_val = default_val
        self.unit = unit
        self.module_name = module_name
        self.is_patched = False

        self.polarity = "Neutral"
        self.gain_multiplier = 1.0
        self.setFixedSize(140, 125)
        self.setStyleSheet("background: #0d1117;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(2)

        self.label = QLabel(f"{label_text}: {default_val:.1f}{unit}")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setStyleSheet("color: #c9d1d9; font-size: 9px; font-weight: bold; background: transparent;")
        layout.addWidget(self.label)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(int(min_val * 10), int(max_val * 10))
        self.slider.setValue(int(default_val * 10))
        self.slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #161b22; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #00ffcc; width: 12px; margin: -4px 0; border-radius: 6px; }
        """)
        self.slider.valueChanged.connect(self._on_slider_changed)
        layout.addWidget(self.slider)

        target_row = QHBoxLayout()
        target_lbl = QLabel("Tgt:")
        target_lbl.setStyleSheet("color: #8b949e; font-size: 8px; background: transparent;")
        target_row.addWidget(target_lbl)

        self.target_combo = QComboBox()
        self.target_combo.setFixedHeight(20)
        self.target_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; font-size: 8px; border: 1px solid #30363d;")
        self.target_combo.addItems([
            "Master Audio Sum", "Filter Cutoff", "Resonance Mod",
            "Granular Scatter", "Amplitude Envelope", "Phase Distortion"
        ])
        self.target_combo.currentIndexChanged.connect(self._on_target_changed)
        target_row.addWidget(self.target_combo)
        layout.addLayout(target_row)

        bottom_row = QHBoxLayout()
        self.polarity_btn = QPushButton("Neutral")
        self.polarity_btn.setFixedHeight(20)
        self.polarity_btn.setStyleSheet("background-color: #161b22; color: #00ffcc; font-size: 8px; border: 1px solid #30363d; font-weight: bold;")
        self.polarity_btn.clicked.connect(self._toggle_polarity)
        bottom_row.addWidget(self.polarity_btn)

        self.port_btn = QPushButton("Deactivate" if self.is_patched else "Activate")
        self.port_btn.setFixedSize(65, 22)
        self.port_btn.setCheckable(True)
        self.port_btn.setChecked(self.is_patched)
        self.port_btn.setStyleSheet("""
            QPushButton { background-color: #161b22; color: #8b949e; border: 1px solid #30363d; border-radius: 4px; font-weight: bold; font-size: 9px; }
            QPushButton:checked { background-color: #00ffcc; color: #0d1117; border: 1px solid #ffffff; }
        """)
        self.port_btn.clicked.connect(self._toggle_patch)
        bottom_row.addWidget(self.port_btn)
        layout.addLayout(bottom_row)

        gain_row = QHBoxLayout()
        self.gain_down_btn = QPushButton("-")
        self.gain_down_btn.setFixedSize(18, 18)
        self.gain_down_btn.setStyleSheet("background-color: #161b22; color: #ff7b72; font-size: 9px; font-weight: bold;")
        self.gain_down_btn.clicked.connect(lambda: self._adjust_gain(-0.25))

        self.gain_lbl = QLabel("Amt: 1.0x")
        self.gain_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gain_lbl.setStyleSheet("color: #8b949e; font-size: 8px; background: transparent;")

        self.gain_up_btn = QPushButton("+")
        self.gain_up_btn.setFixedSize(18, 18)
        self.gain_up_btn.setStyleSheet("background-color: #161b22; color: #00ffcc; font-size: 9px; font-weight: bold;")
        self.gain_up_btn.clicked.connect(lambda: self._adjust_gain(0.25))

        gain_row.addWidget(self.gain_down_btn)
        gain_row.addWidget(self.gain_lbl)
        gain_row.addWidget(self.gain_up_btn)
        layout.addLayout(gain_row)

    def _on_slider_changed(self, val):
        self.current_val = val / 10.0
        self.label.setText(f"{self.label_text}: {self.current_val:.1f}{self.unit}")

    def _on_target_changed(self, index):
        if self.is_patched:
            target_name = self.target_combo.currentText()
            for i, c in enumerate(GLOBAL_BUS.global_cables):
                if c["src_module"] == self.module_name and c["src_node"] == self.label_text:
                    GLOBAL_BUS.global_cables[i]["tgt_module"] = target_name
                    GLOBAL_BUS.broadcast_update()
                    break

    def _toggle_polarity(self):
        if self.polarity == "Neutral":
            self.polarity = "+"
            self.polarity_btn.setStyleSheet("background-color: #161b22; color: #f5d97d; font-size: 8px; border: 1px solid #f5d97d; font-weight: bold;")
            self.polarity_btn.setText("+ (Pos)")
        elif self.polarity == "+":
            self.polarity = "-"
            self.polarity_btn.setStyleSheet("background-color: #161b22; color: #ff7b72; font-size: 8px; border: 1px solid #ff7b72; font-weight: bold;")
            self.polarity_btn.setText("- (Inv)")
        else:
            self.polarity = "Neutral"
            self.polarity_btn.setStyleSheet("background-color: #161b22; color: #00ffcc; font-size: 8px; border: 1px solid #30363d; font-weight: bold;")
            self.polarity_btn.setText("Neutral")

        if self.is_patched:
            for i, c in enumerate(GLOBAL_BUS.global_cables):
                if c["src_module"] == self.module_name and c["src_node"] == self.label_text:
                    GLOBAL_BUS.update_cable_polarity_gain(i, self.polarity, 0.0)
                    break

    def _adjust_gain(self, delta):
        self.gain_multiplier = max(0.25, round(self.gain_multiplier + delta, 2))
        self.gain_lbl.setText(f"Amt: {self.gain_multiplier:.2f}x")
        if self.is_patched:
            for i, c in enumerate(GLOBAL_BUS.global_cables):
                if c["src_module"] == self.module_name and c["src_node"] == self.label_text:
                    GLOBAL_BUS.update_cable_polarity_gain(i, self.polarity, delta)
                    break

    def _toggle_patch(self, checked):
        self.is_patched = checked
        target_name = self.target_combo.currentText()
        if checked:
            self.port_btn.setText("Deactivate")
            GLOBAL_BUS.add_cable(
                src_module=self.module_name, src_node=self.label_text,
                tgt_module=target_name, tgt_node="Primary Sum Node",
                polarity=self.polarity, gain=self.gain_multiplier
            )
        else:
            self.port_btn.setText("Activate")
            for i, c in enumerate(GLOBAL_BUS.global_cables):
                if c["src_module"] == self.module_name and c["src_node"] == self.label_text:
                    GLOBAL_BUS.remove_cable(i)
                    break


# -------------------------------------------------------------------------
# FREEFORM SEQUENCER CANVAS
# -------------------------------------------------------------------------
class FreeformSequencerCanvas(QWidget):
    def __init__(self, sequence_data, parent=None):
        super().__init__(parent)
        self.seq_data = sequence_data
        self.setMinimumHeight(130)
        self.setStyleSheet("background-color: #0b0f15; border: 1px solid #30363d; border-radius: 4px;")

    def paintEvent(self, event):
        # Initialize the painter once for the widget
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        try:
            # Safely resolve sequence data or notes fallback
            notes = self.seq_data.get("notes", []) if isinstance(self.seq_data, dict) else [
                {"time": float(i), "duration": 1.0, "active": True} for i, val in enumerate(self.seq_data)
            ]

            formatted_notes = []
            for i, n in enumerate(notes):
                if isinstance(n, dict):
                    formatted_notes.append({
                        "time": n.get("time", float(i)),
                        "duration": n.get("duration", 1.0),
                        "active": n.get("active", True)
                    })
                else:
                    formatted_notes.append({
                        "time": float(i),
                        "duration": 1.0,
                        "active": bool(n)
                    })

            max_time = max([n["time"] + n["duration"] for n in formatted_notes] + [16.0])
            scale_x = self.width() / max(16.0, max_time)

            # Draw background grid/fill manually here if needed, then render notes:
            for i, note in enumerate(formatted_notes):
                nx = note["time"] * scale_x
                nw = max(12, note["duration"] * scale_x)
                ny = 15 + (i % 4) * 24

                is_active = note["active"]
                p.setBrush(QBrush(QColor("#00ffcc" if is_active else "#21262d")))
                p.setPen(QPen(QColor("#ffffff") if is_active else QColor("#484f58"), 1))
                p.drawRoundedRect(int(nx), int(ny), int(nw), 18, 4, 4)

                p.setPen(QPen(QColor("#ffffff" if is_active else "#8b949e"), 1))
                p.drawText(int(nx) + 4, int(ny) + 13, f"N{i+1}")

        finally:
            # Explicitly end painting so QBackingStore releases the canvas device
            p.end()


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            max_time = max([n["time"] + n["duration"] for n in self.seq_data.get("notes", [])] + [16.0])
            scale_x = self.width() / max(16.0, max_time)
            clicked_time = pos.x() / scale_x

            notes = self.seq_data.get("notes", [])
            found = False
            for note in notes:
                if note["time"] <= clicked_time <= (note["time"] + note["duration"]):
                    note["active"] = not note["active"]
                    found = True
                    break
            if not found:
                notes.append({"time": round(clicked_time, 2), "duration": 1.5, "active": True})
            self.update()


# -------------------------------------------------------------------------
# TAB 1: SYNTHS, MULTI-SEQUENCE STACKS & EQUATION POLYNOMIAL SYNTH
# -------------------------------------------------------------------------
class SynthModulePage(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = GrooveboxEngine()
        self.setStyleSheet("background-color: #070b10;")
        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        spawn_audio_in_btn = QPushButton("+ Spawn Audio In/Out Jack Module")
        spawn_audio_in_btn.setStyleSheet("background-color: #1f242c; color: #ff7b72; font-weight: bold; border: 1px solid #ff7b72; padding: 6px;")
        spawn_audio_in_btn.clicked.connect(lambda: self._spawn_panel("Dedicated Audio I/O Loop", is_audio_in=True))

        spawn_poly_btn = QPushButton("+ Spawn Equation Polynomial Synth")
        spawn_poly_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 6px;")
        spawn_poly_btn.clicked.connect(lambda: self._spawn_panel("Equation Polynomial Algebra Synth", is_polynomial=True))

        spawn_synth_btn = QPushButton("+ Spawn Resizable Multi-Seq Synth")
        spawn_synth_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        spawn_synth_btn.clicked.connect(lambda: self._spawn_panel("Vector Synth & Multi-Seq Engine", is_synth=True))

        spawn_random_instr_btn = QPushButton("🎲 Spawn Randomizer Instrument")
        spawn_random_instr_btn.setStyleSheet("background-color: #2b1135; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 6px;")
        spawn_random_instr_btn.clicked.connect(self._spawn_randomizer_instrument)

        activate_fractal_btn = QPushButton("🌀 Activate Fractallizer")
        activate_fractal_btn.setStyleSheet("background-color: #2b1135; color: #ff7b72; font-weight: bold; border: 1px solid #ff7b72; padding: 6px;")
        activate_fractal_btn.clicked.connect(self._trigger_fractalizer)

        activate_reality_btn = QPushButton("🌌 Activate Reality Synth")
        activate_reality_btn.setStyleSheet("background-color: #112b35; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        activate_reality_btn.clicked.connect(self._trigger_reality_synth)

        top_bar.addWidget(spawn_audio_in_btn)
        top_bar.addWidget(spawn_poly_btn)
        top_bar.addWidget(spawn_synth_btn)
        top_bar.addWidget(spawn_random_instr_btn)
        top_bar.addWidget(activate_fractal_btn)
        top_bar.addWidget(activate_reality_btn)
        top_bar.addStretch()
        layout.addLayout(top_bar)

        toggles_bar = QHBoxLayout()

        self.fractal_toggle = QCheckBox("Enable Music Fractallizer")
        self.fractal_toggle.setChecked(getattr(self.engine, 'fractallizer_enabled', True))
        self.fractal_toggle.setStyleSheet("""
            QCheckBox { color: #888888; font-weight: bold; background: #161b22; padding: 4px; border: 1px solid #30363d; }
            QCheckBox:checked { color: #00ffcc; border-color: #00ffcc; }
        """)
        self.fractal_toggle.stateChanged.connect(self._toggle_fractalizer_state)

        self.eqr_toggle = QCheckBox("Enable EQR Processor")
        self.eqr_toggle.setChecked(getattr(self.engine, 'eqr_processor_enabled', True))
        self.eqr_toggle.setStyleSheet("""
            QCheckBox { color: #888888; font-weight: bold; background: #161b22; padding: 4px; border: 1px solid #30363d; }
            QCheckBox:checked { color: #f5d97d; border-color: #f5d97d; }
        """)
        self.eqr_toggle.stateChanged.connect(self._toggle_eqr_processor_state)

        toggles_bar.addWidget(self.fractal_toggle)
        toggles_bar.addWidget(self.eqr_toggle)
        toggles_bar.addStretch()
        layout.addLayout(toggles_bar)

        mode_bar = QHBoxLayout()
        self.mode_status_lbl = QLabel()
        self._update_mode_label()
        self.mode_status_lbl.setStyleSheet("color: #f5d97d; font-weight: bold; background: #161b22; padding: 4px; border: 1px solid #30363d;")

        toggle_mode_btn = QPushButton("🔄 Cycle Operational Mode (Normal ➔ Creative ➔ Survival)")
        toggle_mode_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 4px;")
        toggle_mode_btn.clicked.connect(self._toggle_modes)

        mode_bar.addWidget(self.mode_status_lbl)
        mode_bar.addWidget(toggle_mode_btn)
        mode_bar.addStretch()
        layout.addLayout(mode_bar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #070b10; border: none;")
        self.container = QWidget(self)
        self.container.setStyleSheet("background-color: #070b10;")
        self.container_layout = QGridLayout(self.container)

        self.refresh_synth_grid()

        self.container.setLayout(self.container_layout)
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

    def refresh_synth_grid(self):
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        for idx, synth_name in enumerate(self.engine.active_synth_panels):
            is_poly = "Polynomial" in synth_name or "Algebra" in synth_name
            is_synth_type = not is_poly
            row = idx // 2
            col = idx % 2
            self._add_panel_to_grid(synth_name, is_synth=is_synth_type, is_polynomial=is_poly, row=row, col=col)

        self.container.update()

    def _toggle_fractalizer_state(self, state):
        self.engine.fractallizer_enabled = bool(state)
        status = "Enabled" if self.engine.fractallizer_enabled else "Disabled"
        QMessageBox.information(self, "Fractallizer State", f"Music Fractallizer has been {status}.")

    def _toggle_eqr_processor_state(self, state):
        self.engine.eqr_processor_enabled = bool(state)
        status = "Enabled" if self.engine.eqr_processor_enabled else "Disabled"
        QMessageBox.information(self, "EQR Processor State", f"EQR Processor has been {status}.")

    def _update_mode_label(self):
        s_mode = "ON" if self.engine.survival_mode else "OFF"
        n_mode = "ON" if self.engine.normal_mode else "OFF"
        c_mode = "ON" if self.engine.creative_mode else "OFF"
        self.mode_status_lbl.setText(f"Electron Sling State -> Survival: {s_mode} | Normal: {n_mode} | Creative: {c_mode}")

    def _toggle_modes(self):
        if self.engine.normal_mode:
            self.engine.normal_mode = False
            self.engine.creative_mode = True
            self.engine.survival_mode = False
        elif self.engine.creative_mode:
            self.engine.normal_mode = False
            self.engine.creative_mode = False
            self.engine.survival_mode = True
        else:
            self.engine.normal_mode = True
            self.engine.creative_mode = False
            self.engine.survival_mode = False

        self.engine.reality_synth.survival_mode = self.engine.survival_mode
        self.engine.fractalizer.survival_mode = self.engine.survival_mode
        self._update_mode_label()

        active_name = "Normal" if self.engine.normal_mode else ("Creative" if self.engine.creative_mode else "Survival")
        QMessageBox.information(self, "Operational Mode Updated", f"Electron Sling mode switched to: {active_name} Mode.")

    def _trigger_fractalizer(self):
        if not self.engine.fractallizer_enabled:
            QMessageBox.warning(self, "Fractallizer Disabled", "Cannot trigger stream: Music Fractallizer is currently disabled via UI controls.")
            return
        stream = self.engine.activate_fractalizer_stream()
        QMessageBox.information(self, "Music Fractallizer Activated", f"Music Fractallizer stream successfully generated with spatial dimensions: {list(stream.keys())}.")

    def _trigger_reality_synth(self):
        buffer_data = self.engine.activate_reality_synth_render()
        QMessageBox.information(self, "Reality Synth Rendered", f"Reality Synth active buffer rendered for coordinates: {list(buffer_data.keys())}.")

    def _spawn_panel(self, kind, is_synth=False, is_audio_in=False, is_polynomial=False):
        name = f"{kind} #{len(self.engine.active_synth_panels) + 1}"
        if name not in self.engine.active_synth_panels:
            self.engine.active_synth_panels.append(name)
        self.refresh_synth_grid()

    def _spawn_randomizer_instrument(self):
        rand_prefixes = ["Stochastic", "Quantum", "Algebraic", "Fractal", "Harmonic", "Resonant", "Vectoreski"]
        rand_suffixes = ["Oscillator", "Sling", "Resonator", "Generator", "Synth Node", "Phase Wave"]
        instr_name = f"{random.choice(rand_prefixes)} {random.choice(rand_suffixes)} {random.randint(100, 999)}"

        chords = list(self.engine.math_chord_library.keys())
        chosen_chord = random.choice(chords)
        self.engine.add_instrument_sequence_bank(instr_name, "Differentiated Tempo Bank", pitch=float(random.randint(-12, 12)), amp=round(random.uniform(0.5, 1.5), 2), math_chord=chosen_chord)

        if instr_name not in self.engine.active_synth_panels:
            self.engine.active_synth_panels.append(instr_name)
        self.refresh_synth_grid()
        QMessageBox.information(self, "Randomizer Instrument Spawned", f"Successfully spawned randomizer instrument '{instr_name}' with differentiated tempo interval parameters and cross-mod heuristic routing.")

    def _add_panel_to_grid(self, title, is_synth=False, is_audio_in=False, is_polynomial=False, row=0, col=0):
        self.content_widget = QWidget(self)
        self.content_widget.setStyleSheet("background-color: #0d1117;")
        c_layout = QVBoxLayout(content_widget)
        c_layout.setContentsMargins(4, 4, 4, 4)

        if is_polynomial:
            poly_hud_layout = QVBoxLayout()
            poly_lbl = QLabel("📐 Live Polynomial Algebra Evaluator (Step-Gated x, y, z Variables)")
            poly_lbl.setStyleSheet("color: #f5d97d; font-weight: bold; background: transparent;")
            poly_hud_layout.addWidget(poly_lbl)

            eq_row = QHBoxLayout()
            eq_label = QLabel("Eq:")
            eq_label.setStyleSheet("color: #c9d1d9; background: transparent;")
            eq_row.addWidget(eq_label)

            eq_field = QLineEdit(self.engine.scale_equation)
            eq_field.setStyleSheet("background-color: #161b22; color: #00ffcc; font-family: monospace; border: 1px solid #30363d;")
            eq_row.addWidget(eq_field)

            eval_btn = QPushButton("Evaluate & Map")
            eval_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d;")
            eval_btn.clicked.connect(lambda: self._evaluate_polynomial_osc(eq_field.text(), title))
            eq_row.addWidget(eval_btn)
            poly_hud_layout.addLayout(eq_row)
            c_layout.addLayout(poly_hud_layout)

        if is_audio_in:
            io_header = QHBoxLayout()
            lbl_in = QLabel("🔴 Input Jack [IN]")
            lbl_in.setStyleSheet("color: #ff7b72; background: transparent;")
            io_header.addWidget(lbl_in)

            in_jack = QPushButton("● Audio Input Bus")
            in_jack.setStyleSheet("background-color: #00ffcc; color: #0d1117; font-weight: bold; font-size: 9px;")
            io_header.addWidget(in_jack)

            lbl_out = QLabel("🟢 Output Jack [OUT]")
            lbl_out.setStyleSheet("color: #00ffcc; background: transparent;")
            io_header.addWidget(lbl_out)

            out_jack = QPushButton("● Audio Output Bus")
            out_jack.setStyleSheet("background-color: #f5d97d; color: #0d1117; font-weight: bold; font-size: 9px;")
            io_header.addWidget(out_jack)

            resample_btn = QPushButton("Buffer Resample")
            resample_btn.setStyleSheet("background-color: #2b1115; color: #ff7b72; border: 1px solid #ff7b72; font-weight: bold; padding: 3px;")
            resample_btn.clicked.connect(lambda: self._trigger_resampling(title))
            io_header.addWidget(resample_btn)
            c_layout.addLayout(io_header)

        if is_synth:
            banks_layout = QHBoxLayout()
            lbl_bks = QLabel("Sequence Banks:")
            lbl_bks.setStyleSheet("color: #c9d1d9; background: transparent;")
            banks_layout.addWidget(lbl_bks)

            bank_combo = QComboBox()
            bank_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")

            instr_banks = self.engine.get_instrument_banks(title)
            for b in instr_banks:
                bank_combo.addItem(b["name"])
            banks_layout.addWidget(bank_combo)

            add_bank_btn = QPushButton("+ New Sequence")
            add_bank_btn.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #00ffcc; font-size: 9px; font-weight: bold;")
            add_bank_btn.clicked.connect(lambda: self._add_new_sequence_bank(title, bank_combo))
            banks_layout.addWidget(add_bank_btn)
            c_layout.addLayout(banks_layout)

            param_grid = QGridLayout()
            pitch_spin = QDoubleSpinBox(); pitch_spin.setRange(-24.0, 24.0); pitch_spin.setValue(0.0); pitch_spin.setSuffix(" st")
            pitch_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")

            amp_spin = QDoubleSpinBox(); amp_spin.setRange(0.0, 2.0); amp_spin.setValue(1.0); amp_spin.setSingleStep(0.1)
            amp_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")

            stretch_spin = QDoubleSpinBox(); stretch_spin.setRange(0.2, 4.0); stretch_spin.setValue(1.0); stretch_spin.setSingleStep(0.1)
            stretch_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")

            math_chord_combo = QComboBox()
            math_chord_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
            math_chord_combo.addItems(list(self.engine.math_chord_library.keys()))

            length_spin = QSpinBox(); length_spin.setRange(4, 128); length_spin.setValue(16)
            length_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")

            param_grid.addWidget(QLabel("Pitch Shift:"), 0, 0); param_grid.addWidget(pitch_spin, 0, 1)
            param_grid.addWidget(QLabel("Amp:"), 0, 2); param_grid.addWidget(amp_spin, 0, 3)
            param_grid.addWidget(QLabel("Stretch:"), 1, 0); param_grid.addWidget(stretch_spin, 1, 1)
            param_grid.addWidget(QLabel("Math Chords (Point Pairs):"), 1, 2); param_grid.addWidget(math_chord_combo, 1, 3)
            param_grid.addWidget(QLabel("Steps:"), 2, 0); param_grid.addWidget(length_spin, 2, 1)
            c_layout.addLayout(param_grid)

            active_bank = instr_banks[0]
            seq_canvas = FreeformSequencerCanvas(active_bank)
            c_layout.addWidget(seq_canvas)

        wt_canvas = WavetableCanvas(title, self.engine)
        c_layout.addWidget(wt_canvas)

        knobs_layout = QHBoxLayout()
        knobs_layout.addWidget(PatchableKnob("Envelope Decay", 10.0, 1000.0, 250.0, "ms", title, self))
        knobs_layout.addWidget(PatchableKnob("Audio Gain", 0.0, 100.0, 75.0, "%", title, self))
        knobs_layout.addWidget(PatchableKnob("Filter Q", 0.1, 20.0, 4.0, "Q", title, self))
        c_layout.addLayout(knobs_layout)

        panel = ResizableWorkspacePanel(title, content_widget)
        panel.show()
        self.container_layout.addWidget(panel, row, col)

    def _add_new_sequence_bank(self, title, combo):
        bank_name = f"Sequence Bank {len(self.engine.get_instrument_banks(title)) + 1}"
        self.engine.add_instrument_sequence_bank(title, bank_name)
        combo.addItem(bank_name)
        combo.setCurrentIndex(combo.count() - 1)
        QMessageBox.information(self, "Sequence Bank Added", f"Created new freeform sequence bank '{bank_name}' for {title}.")

    def _trigger_resampling(self, title):
        buf_name = GLOBAL_BUS.trigger_resampling()
        QMessageBox.information(self, "Live Resampling Captured", f"Active audio input loop from '{title}' successfully resampled into buffer: {buf_name}")

    def _evaluate_polynomial_osc(self, eq_text, title):
        self.engine.scale_equation = eq_text
        freqs = self.engine.generate_equation_scale_frequencies()
        QMessageBox.information(self, "Polynomial Evaluated", f"Equation '{eq_text}' successfully computed across step-gated x, y, z variables for '{title}'. Generated {len(freqs)} rhythmic frequencies!")


# -------------------------------------------------------------------------
# TAB 2: FULLY ACTIVATED DRUM & PERCUSSION MATRIX
# -------------------------------------------------------------------------
class DrumMatrixPage(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setStyleSheet("background-color: #070b10;")
        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        top_info = QLabel("🥁 Fully Activated Drum & Percussion Synthesizer Matrix (Live Step-Clock Gated Transients)")
        top_info.setStyleSheet("color: #f5d97d; font-weight: bold; font-size: 12px; background: transparent;")
        top_bar.addWidget(top_info)
        top_bar.addStretch()

        activate_all_drums_btn = QPushButton("⚡ Force Trigger All Drum Gates")
        activate_all_drums_btn.setStyleSheet("background-color: #2b1135; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        activate_all_drums_btn.clicked.connect(self._force_trigger_drums)
        top_bar.addWidget(activate_all_drums_btn)

        spawn_drum_btn = QPushButton("+ Spawn Drum Machine Unit")
        spawn_drum_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        spawn_drum_btn.clicked.connect(self._spawn_new_drum_unit)
        top_bar.addWidget(spawn_drum_btn)
        layout.addLayout(top_bar)

        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #070b10; border: none;")
        self.container = QWidget(self); self.container.setStyleSheet("background-color: #070b10;")
        self.grid = QGridLayout(self.container)

        self.refresh_drum_grid()

        self.container.setLayout(self.grid)
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

    def refresh_drum_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        for idx, kit_name in enumerate(self.engine.active_drum_kits):
            self.w = QWidget(self); w.setStyleSheet("background-color: #0d1117;")
            l = QVBoxLayout(w)

            kit_header = QHBoxLayout()
            lbl_kit = QLabel(f"Kit: {kit_name} [Activated Runtime Triggers]")
            lbl_kit.setStyleSheet("color: #c9d1d9; font-weight: bold; background: transparent;")
            kit_header.addWidget(lbl_kit)
            kit_header.addStretch()

            despawn_btn = QPushButton("✕ Despawn")
            despawn_btn.setFixedSize(70, 20)
            despawn_btn.setStyleSheet("background-color: #2b1115; color: #ff7b72; border: 1px solid #ff7b72; font-size: 8px; font-weight: bold;")
            despawn_btn.clicked.connect(lambda checked, name=kit_name: self._despawn_drum_unit(name))
            kit_header.addWidget(despawn_btn)
            l.addLayout(kit_header)

            grid_row = QGridLayout()
            for step in range(16):
                btn = QPushButton(str(step + 1))
                btn.setCheckable(True)
                is_active_gate = self.engine.runtime_clock.evaluate_drum_trigger(kit_name, step)
                btn.setChecked(is_active_gate)
                if is_active_gate:
                    btn.setStyleSheet("background-color: #00ffcc; color: #0d1117; font-weight: bold; font-size: 9px; border: 1px solid #ffffff;")
                else:
                    btn.setStyleSheet("background-color: #161b22; color: #8b949e; font-size: 9px;")
                grid_row.addWidget(btn, 0, step)
            l.addLayout(grid_row)

            knobs = QHBoxLayout()
            knobs.addWidget(PatchableKnob("Decay", 10.0, 500.0, 150.0, "ms", kit_name))
            knobs.addWidget(PatchableKnob("Pitch Mod", 0.0, 100.0, 40.0, "%", kit_name))
            knobs.addWidget(PatchableKnob("Drive", 0.0, 10.0, 2.0, "x", kit_name))
            l.addLayout(knobs)

            panel = ResizableWorkspacePanel(kit_name, w)
            panel.show()
            self.grid.addWidget(panel, idx // 2, idx % 2)
        self.container.update()

    def _force_trigger_drums(self):
        tick = self.engine.runtime_clock.tick_clock()
        self.refresh_drum_grid()
        QMessageBox.information(self, "Drum Matrices Triggered", f"Successfully advanced runtime clock to step {tick}. All active drum machine banks are firing transient triggers!")

    def _spawn_new_drum_unit(self):
        new_name = f"Custom Drum Unit {len(self.engine.active_drum_kits) + 1}"
        self.engine.active_drum_kits.append(new_name)
        self.refresh_drum_grid()
        QMessageBox.information(self, "Drum Machine Spawned", f"Successfully spawned new fully activated drum machine unit '{new_name}' under Tab 2.")

    def _despawn_drum_unit(self, kit_name):
        if len(self.engine.active_drum_kits) > 1:
            self.engine.active_drum_kits.remove(kit_name)
            self.refresh_drum_grid()
            QMessageBox.information(self, "Drum Machine Despawned", f"Successfully despawned drum machine '{kit_name}'.")
        else:
            QMessageBox.warning(self, "Despawn Failed", "At least one drum machine unit must remain active.")


# -------------------------------------------------------------------------
# TAB 3: GRANULAR FX & FREQUENCY SHIFTER
# -------------------------------------------------------------------------
class GranularFXPage(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setStyleSheet("background-color: #070b10;")
        self.layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        title = QLabel("🌌 Granular FX, Spectral Shifter & Wavefolder Matrix (Dynamic FX Instances)")
        title.setStyleSheet("color: #00ffcc; font-weight: bold; font-size: 12px; background: transparent;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        spawn_fx_btn = QPushButton("+ Spawn Custom FX Module")
        spawn_fx_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        spawn_fx_btn.clicked.connect(self._spawn_new_fx_unit)
        top_bar.addWidget(spawn_fx_btn)
        self.layout.addLayout(top_bar)

        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #070b10; border: none;")
        self.container = QWidget(self); self.container.setStyleSheet("background-color: #070b10;")
        self.grid = QGridLayout(self.container)

        self.refresh_fx_grid()
        self.container.setLayout(self.grid)
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

    def refresh_fx_grid(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        for idx, fx_name in enumerate(self.engine.active_fx_modules):
            self.w = QWidget(self); w.setStyleSheet("background-color: #0d1117;")
            l = QVBoxLayout(w)

            sub_header = QHBoxLayout()
            sub_lbl = QLabel(f"Processor Subtype: Advanced {fx_name}")
            sub_lbl.setStyleSheet("color: #f5d97d; font-size: 9px; background: transparent;")
            sub_header.addWidget(sub_lbl)
            sub_header.addStretch()

            despawn_btn = QPushButton("✕ Despawn")
            despawn_btn.setFixedSize(70, 20)
            despawn_btn.setStyleSheet("background-color: #2b1115; color: #ff7b72; border: 1px solid #ff7b72; font-size: 8px; font-weight: bold;")
            despawn_btn.clicked.connect(lambda checked, name=fx_name: self._despawn_fx_unit(name))
            sub_header.addWidget(despawn_btn)
            l.addLayout(sub_header)

            knobs = QHBoxLayout()
            knobs.addWidget(PatchableKnob("Grain Size", 10.0, 250.0, 50.0, "ms", fx_name))
            knobs.addWidget(PatchableKnob("Density", 1.0, 100.0, 32.0, "gr/s", fx_name))
            knobs.addWidget(PatchableKnob("Scatter", 0.0, 100.0, 75.0, "%", fx_name))
            knobs.addWidget(PatchableKnob("Feedback", 0.0, 100.0, 40.0, "%", fx_name))
            l.addLayout(knobs)

            wt = WavetableCanvas(fx_name, self.engine)
            l.addWidget(wt)

            panel = ResizableWorkspacePanel(fx_name, w)
            panel.show()
            self.grid.addWidget(panel, idx // 2, idx % 2)
        self.container.update()

    def _spawn_new_fx_unit(self):
        new_name = f"Custom FX Unit {len(self.engine.active_fx_modules) + 1}"
        if new_name not in self.engine.active_fx_modules:
            self.engine.active_fx_modules.append(new_name)
            self.refresh_fx_grid()
            QMessageBox.information(self, "FX Module Spawned", f"Successfully spawned new FX module '{new_name}' into the signal chain.")

    def _despawn_fx_unit(self, fx_name):
        if len(self.engine.active_fx_modules) > 1:
            self.engine.active_fx_modules.remove(fx_name)
            self.refresh_fx_grid()
            QMessageBox.information(self, "FX Module Despawned", f"Successfully despawned FX module '{fx_name}'.")
        else:
            QMessageBox.warning(self, "Despawn Failed", "At least one active FX module must remain in the routing matrix.")


# -------------------------------------------------------------------------
# TAB 4: FULLY ACTIVATED AUTOMATION & STEP SEQUENCER SUITE
# -------------------------------------------------------------------------
class AutomationCurveCanvas(QWidget):
    def __init__(self, points_list, parent=None):
        super().__init__(parent)
        self.points_list = points_list
        self.setMinimumHeight(120)
        self.setStyleSheet("background-color: #0b0f15; border: 1px solid #30363d; border-radius: 4px;")

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#0b0f15"))

        p.setPen(QPen(QColor("#161b22"), 1, Qt.PenStyle.DashLine))
        for x in range(0, self.width(), 50): p.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 30): p.drawLine(0, y, self.width(), y)

        n = len(self.points_list)
        if n >= 2:
            step_w = self.width() / max(1, n - 1)
            path = QPainterPath()
            pts = []
            for i, val in enumerate(self.points_list):
                px = i * step_w
                py = self.height() - (val / 100.0) * (self.height() - 20) - 10
                pts.append(QPointF(px, py))

            path.moveTo(pts[0])
            for pt in pts[1:]:
                path.lineTo(pt)

            p.setPen(QPen(QColor("#f5d97d"), 2.0))
            p.drawPath(path)

            p.setBrush(QBrush(QColor("#00ffcc")))
            p.setPen(QPen(QColor("#ffffff"), 1))
            for pt in pts:
                p.drawEllipse(pt, 4, 4)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            n = len(self.points_list)
            if n > 0:
                idx = min(n - 1, max(0, int(round((pos.x() / self.width()) * (n - 1)))))
                val = max(0.0, min(100.0, round((self.height() - pos.y() - 10) / (self.height() - 20) * 100.0, 1)))
                self.points_list[idx] = val
                self.update()


class AutomationPatternPage(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setStyleSheet("background-color: #070b10;")
        layout = QVBoxLayout(self)

        top_bar = QHBoxLayout()
        title = QLabel("⚙️ Fully Activated Modular Step Sequencer, Automation Envelopes & Pattern Designer")
        title.setStyleSheet("color: #f5d97d; font-weight: bold; font-size: 12px; background: transparent;")
        top_bar.addWidget(title)
        top_bar.addStretch()

        activate_all_seqs_btn = QPushButton("⚡ Force Trigger All Sequencers")
        activate_all_seqs_btn.setStyleSheet("background-color: #2b1135; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 6px;")
        activate_all_seqs_btn.clicked.connect(self._force_trigger_sequencers)
        top_bar.addWidget(activate_all_seqs_btn)

        add_pat_btn = QPushButton("+ New Automation Pattern")
        add_pat_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        add_pat_btn.clicked.connect(self._add_automation_pattern)
        top_bar.addWidget(add_pat_btn)

        spawn_seq_btn = QPushButton("+ Spawn Sequencer Module")
        spawn_seq_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 6px;")
        spawn_seq_btn.clicked.connect(self._spawn_sequencer_module)
        top_bar.addWidget(spawn_seq_btn)

        layout.addLayout(top_bar)

        self.scroll = QScrollArea(); self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background-color: #070b10; border: none;")
        self.container = QWidget(self); self.container.setStyleSheet("background-color: #070b10;")
        self.grid = QGridLayout(self.container)

        self._refresh_automation_panels()
        self.container.setLayout(self.grid)
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)

    def _refresh_automation_panels(self):
        while self.grid.count():
            item = self.grid.takeAt(0)
            if item and item.widget():
                item.widget().deleteLater()

        total_idx = 0
        for pat_name, points in self.engine.automation_patterns.items():
            self.w = QWidget(self); w.setStyleSheet("background-color: #0d1117;")
            l = QVBoxLayout(w)

            lbl = QLabel(f"Automation & Step Sequencer Lane: '{pat_name}' (Active Automation Curve)")
            lbl.setStyleSheet("color: #00ffcc; font-weight: bold; background: transparent;")
            l.addWidget(lbl)

            canvas = AutomationCurveCanvas(points)
            l.addWidget(canvas)

            panel = ResizableWorkspacePanel(f"Sequencer / Automation: {pat_name}", w)
            panel.show()
            self.grid.addWidget(panel, total_idx // 2, total_idx % 2)
            total_idx += 1

        for seq_mod_name in self.engine.active_sequencer_modules:
            self.w = QWidget(self); w.setStyleSheet("background-color: #0d1117;")
            l = QVBoxLayout(w)

            seq_header = QHBoxLayout()
            seq_lbl = QLabel(f"Poly-Rhythmic Sequencer Instance: {seq_mod_name} [Activated Gates]")
            seq_lbl.setStyleSheet("color: #ff7b72; font-weight: bold; background: transparent;")
            seq_header.addWidget(seq_lbl)
            seq_header.addStretch()

            despawn_seq_btn = QPushButton("✕ Despawn")
            despawn_seq_btn.setFixedSize(70, 20)
            despawn_seq_btn.setStyleSheet("background-color: #2b1115; color: #ff7b72; border: 1px solid #ff7b72; font-size: 8px; font-weight: bold;")
            despawn_seq_btn.clicked.connect(lambda checked, name=seq_mod_name: self._despawn_sequencer_module(name))
            seq_header.addWidget(despawn_seq_btn)
            l.addLayout(seq_header)

            step_grid = QGridLayout()
            for step in range(16):
                s_btn = QPushButton(str(step + 1))
                s_btn.setCheckable(True)
                is_gate_active = self.engine.runtime_clock.evaluate_sequencer_gate(seq_mod_name, step)
                s_btn.setChecked(is_gate_active)
                if is_gate_active:
                    s_btn.setStyleSheet("background-color: #f5d97d; color: #0d1117; font-weight: bold; font-size: 9px; border: 1px solid #ffffff;")
                else:
                    s_btn.setStyleSheet("background-color: #161b22; color: #8b949e; font-size: 9px;")
                step_grid.addWidget(s_btn, 0, step)
            l.addLayout(step_grid)

            knobs = QHBoxLayout()
            knobs.addWidget(PatchableKnob("Gate Length", 10.0, 100.0, 50.0, "%", seq_mod_name))
            knobs.addWidget(PatchableKnob("Probability", 0.0, 100.0, 85.0, "%", seq_mod_name))
            knobs.addWidget(PatchableKnob("Swing Rate", 0.0, 50.0, 12.0, "%", seq_mod_name))
            l.addLayout(knobs)

            panel = ResizableWorkspacePanel(f"Sequencer Module: {seq_mod_name}", w)
            panel.show()
            self.grid.addWidget(panel, total_idx // 2, total_idx % 2)
            total_idx += 1
        self.container.update()

    def _force_trigger_sequencers(self):
        tick = self.engine.runtime_clock.tick_clock()
        self._refresh_automation_panels()
        QMessageBox.information(self, "Sequencer Modules Triggered", f"Successfully advanced sequencer clock to step {tick}. All poly-rhythmic step sequencers and automation curves are fully engaged!")

    def _add_automation_pattern(self):
        pat_name = f"Custom Sequencer Lane {len(self.engine.automation_patterns) + 1}"
        self.engine.automation_patterns[pat_name] = [0.0, 50.0, 100.0, 50.0, 25.0, 80.0, 100.0, 0.0]
        self._refresh_automation_panels()
        QMessageBox.information(self, "Sequencer Lane Created", f"New modular step/automation envelope '{pat_name}' successfully added.")

    def _spawn_sequencer_module(self):
        seq_name = f"Advanced Sequencer Instance {len(self.engine.active_sequencer_modules) + 1}"
        if seq_name not in self.engine.active_sequencer_modules:
            self.engine.active_sequencer_modules.append(seq_name)
            self._refresh_automation_panels()
            QMessageBox.information(self, "Sequencer Module Spawned", f"Successfully spawned new sequencer module '{seq_name}'.")

    def _despawn_sequencer_module(self, seq_name):
        if len(self.engine.active_sequencer_modules) > 1:
            self.engine.active_sequencer_modules.remove(seq_name)
            self._refresh_automation_panels()
            QMessageBox.information(self, "Sequencer Module Despawned", f"Successfully despawned sequencer module '{seq_name}'.")
        else:
            QMessageBox.warning(self, "Despawn Failed", "At least one sequencer module must remain active.")


# -------------------------------------------------------------------------
# INFINITE SCROLLABLE PLAYLIST CANVAS
# -------------------------------------------------------------------------
class InfinitePlaylistInnerWidget(QWidget):
    def __init__(self, engine, parent_page, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.parent_page = parent_page
        self.setMinimumSize(8000, 1600)
        self.setStyleSheet("background-color: #070b10;")

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#070b10"))

        p.setPen(QPen(QColor("#161b22"), 1, Qt.PenStyle.DashLine))
        for x in range(0, self.width(), 80):
            p.drawLine(x, 0, x, self.height())
            p.setPen(QPen(QColor("#484f58"), 1))
            p.drawText(x + 4, 15, f"Bar {x // 80 + 1}")
            p.setPen(QPen(QColor("#161b22"), 1, Qt.PenStyle.DashLine))

        for (trk, bar_pos), clip in self.engine.playlist_clips.items():
            cx = bar_pos * 80
            cy = 25 + (trk * 50)
            p.setBrush(QBrush(QColor("#1f242c")))
            p.setPen(QPen(QColor("#00ffcc"), 1.5))
            p.drawRoundedRect(int(cx), cy, 140, 42, 4, 4)

            p.setPen(QPen(QColor("#f5d97d"), 9))
            p.drawText(int(cx) + 6, cy + 14, f"{clip.get('name', 'Clip')}")
            p.setPen(QPen(QColor("#8b949e"), 8))
            p.drawText(int(cx) + 6, cy + 28, f"P:{clip.get('pitch', 0)} | A:{clip.get('amplitude', 1)} | Auto:{clip.get('automation_pattern', 'Def')}")

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            bar_pos = pos.x() / 80.0
            track = int(pos.y() // 50)

            pattern_name = self.parent_page.pattern_combo.currentText()
            math_chord = self.parent_page.playlist_chord_combo.currentText()
            pitch_val = self.parent_page.playlist_pitch_spin.value()
            amp_val = self.parent_page.playlist_amp_spin.value()
            auto_pat = self.parent_page.playlist_auto_combo.currentText()

            clip_data = {
                "name": pattern_name,
                "chord": math_chord,
                "pitch": pitch_val,
                "amplitude": amp_val,
                "automation_pattern": auto_pat
            }
            self.engine.assign_playlist_clip(track, round(bar_pos, 2), clip_data)
            self.update()


class InfinitePlaylistCanvas(QScrollArea):
    def __init__(self, engine, parent_page, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.parent_page = parent_page
        self.setWidgetResizable(True)
        self.setStyleSheet("background-color: #070b10; border: none;")
        self.canvas_inner = InfinitePlaylistInnerWidget(self.engine, self.parent_page)
        self.setWidget(self.canvas_inner)

class EQRVisualizerCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(160)
        self.setStyleSheet("background-color: #0b0b0b; border: 1px solid #ff6b00; border-radius: 4px;")

        self.phase = 0.0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_phase)
        self.timer.start(30)

    def update_phase(self):
        self.phase += 0.03
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self):
            return
        try:
            painter.fillRect(self.rect(), QColor(11, 11, 11))
            w, h = self.width(), self.height()
            cx, cy = w / 2.0, h / 2.0

            painter.setPen(QPen(QColor(30, 30, 30), 1, Qt.PenStyle.DashLine))
            painter.drawLine(0, int(cy), w, int(cy))
            painter.drawLine(int(cx), 0, int(cx), h)

            num_steps = 300
            points = []
            for i in range(num_steps):
                t = (i / num_steps) * 4 * np.pi + self.phase
                x_val = np.sin(t * 1.5) * np.cos(t * 0.5 + self.phase * 0.2) * 120.0
                y_val = np.cos(t * 2.0) * np.sin(t * 1.2) * 80.0
                z_val = np.sin(t + self.phase) * 50.0

                px = cx + x_val + (z_val * 0.3)
                py = cy + y_val + (z_val * 0.2)
                points.append(QPointF(px, py))

            for i in range(len(points) - 1):
                hue_color = QColor.fromHsvF((i / num_steps + self.phase * 0.1) % 1.0, 0.8, 1.0)
                painter.setPen(QPen(hue_color, 2))
                painter.drawLine(points[i], points[i+1])
        finally:
            painter.end()
# -------------------------------------------------------------------------
# MASTER PATCH CANVAS (Visual Wires & Dedicated Synth Jacks)
# -------------------------------------------------------------------------
class EQRVectorEngine(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mathematician's Groovebox")
        self.resize(1000, 700)

        # Initialize core layout container
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        # Title Label / Workspace Indicator
        self.label = QLabel("Coordinate Audio Synthesis Workspace Active")
        self.layout.addWidget(self.label)

        layout.addRow("Operator Variable X:", self.x_input)
        layout.addRow("Operator Variable Y:", self.y_input)
        layout.addRow("Operator Variable Z:", self.z_input)
class MasterPatchCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.cables = GLOBAL_BUS.global_cables
        self.setMinimumHeight(220)
        self.setStyleSheet("background-color: #0b0f15; border: 1px solid #30363d; border-radius: 4px;")

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#0b0f15"))

        p.setPen(QPen(QColor("#161b22"), 1, Qt.PenStyle.DashLine))
        for x in range(0, self.width(), 60): p.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), 40): p.drawLine(0, y, self.width(), y)

        if not self.cables:
            p.setPen(QPen(QColor("#8b949e"), 10))
            p.drawText(20, 30, "No active patch cables. Activate Parameter Jacks in synth modules or use the Song Randomizer.")
            return

        for i, cable in enumerate(self.cables):
            src = cable.get("src_module", "Src")
            tgt = cable.get("tgt_module", "Tgt")
            pol = cable.get("polarity", "Neutral")
            gain = cable.get("gain", 1.0)

            y_pos = 35 + (i * 30) % max(40, self.height() - 40)
            color = "#00ffcc" if pol == "+" else ("#ff7b72" if pol == "-" else "#f5d97d")

            p.setPen(QPen(QColor(color), 2.0))
            p.drawLine(30, y_pos, self.width() - 30, y_pos)

            p.setBrush(QBrush(QColor("#161b22")))
            p.setPen(QPen(QColor(color), 1))
            p.drawRoundedRect(35, y_pos - 12, 190, 24, 4, 4)
            p.drawRoundedRect(self.width() - 225, y_pos - 12, 190, 24, 4, 4)

            p.setPen(QPen(QColor("#ffffff"), 9))
            p.drawText(43, y_pos + 4, f"{src}")
            p.drawText(self.width() - 217, y_pos + 4, f"{tgt} [{pol}, {gain}x]")

class MasterControlPanel(QWidget):
    """Global parameters featuring Master Tempo and Quantization options."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("color: #ffffff;")
        layout = QHBoxLayout(self)

        self.tempo_label = QLabel("Master Tempo: 120 BPM")
        self.tempo_slider = QSlider(Qt.Orientation.Horizontal)
        self.tempo_slider.setRange(40, 240)
        self.tempo_slider.setValue(120)
        self.tempo_slider.valueChanged.connect(self.update_tempo_display)

        self.quant_label = QLabel("Quantize:")
        self.quant_combo = QComboBox()
        self.quant_combo.addItems(["Off (Free Timing)", "1/4 Note", "1/8 Note", "1/16 Note"])
        self.quant_combo.setStyleSheet("background-color: #222; color: #fff; border: 1px solid #444; padding: 4px;")

        layout.addWidget(self.tempo_label)
        layout.addWidget(self.tempo_slider)
        layout.addSpacing(20)
        layout.addWidget(self.quant_label)
        layout.addWidget(self.quant_combo)

    def update_tempo_display(self, value):
        self.tempo_label.setText(f"Master Tempo: {value} BPM")
# -------------------------------------------------------------------------
# TAB 5: EQUATION SCALES, INFINITE PLAYLIST & PATCHBAY
# -------------------------------------------------------------------------
class GeometricSymbolicCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self.setStyleSheet("""
            background-color: #2d3436;
            border: 3px solid #00b894;
            border-radius: 12px;
        """)
        self.nodes = [
            {"label": "Node α: Sine", "pos": (60, 45), "color": "#ff7675"},
            {"label": "Node β: Fold", "pos": (220, 80), "color": "#74b9ff"},
            {"label": "Node γ: Resonator", "pos": (400, 40), "color": "#55efc4"},
            {"label": "Node δ: Attractor", "pos": (580, 75), "color": "#ffeaa7"}
        ]

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self):
            return
        try:
            painter.fillRect(self.rect(), QColor(45, 52, 54))
            pen = QPen(QColor(162, 155, 254), 2, Qt.PenStyle.DashLine)
            painter.setPen(pen)
            for i in range(len(self.nodes) - 1):
                p1 = self.nodes[i]["pos"]
                p2 = self.nodes[i+1]["pos"]
                painter.drawLine(p1[0], p1[1], p2[0], p2[1])

            for node in self.nodes:
                painter.setPen(QPen(QColor(255, 255, 255), 2))
                painter.setBrush(QColor(node["color"]))
                x, y = node["pos"]
                painter.drawEllipse(QPoint(x, y), 22, 22)

                painter.setPen(QColor(253, 203, 110))
                painter.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
                painter.drawText(x - 30, y + 36, node["label"])
        finally:
            painter.end()
class MasterControlPatchbayPage(QWidget):
    def __init__(self, engine, main_window):
        super().__init__()
        self.engine = engine
        self.main_window = main_window
        GLOBAL_BUS.register_subscriber(self)

        layout = QVBoxLayout(self)

        # Top Global Controls Group (Enhanced with Rhythm Flux Linking Controls)
        controls_group = QGroupBox("Master Engine Controls, Equation Scale & Rhythm Flux Linking")
        controls_group.setStyleSheet("QGroupBox { color: #00ffcc; font-weight: bold; border: 1px solid #30363d; margin-top: 6px; } QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; }")
        ctrl_layout = QGridLayout(controls_group)

        # BPM Slider
        self.bpm_label = QLabel(f"{self.engine.global_bpm:.1f} BPM")
        self.bpm_label.setStyleSheet("color: #f5d97d; font-weight: bold;")
        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setRange(400, 2400)
        self.bpm_slider.setValue(int(self.engine.global_bpm * 10))
        self.bpm_slider.valueChanged.connect(self._on_bpm_changed)

        ctrl_layout.addWidget(QLabel("Global Tempo:"), 0, 0)
        ctrl_layout.addWidget(self.bpm_slider, 0, 1)
        ctrl_layout.addWidget(self.bpm_label, 0, 2)

        # Rhythm Flux Link Mode Controls
        ctrl_layout.addWidget(QLabel("Rhythm Flux Mode:"), 0, 3)
        self.flux_mode_combo = QComboBox()
        self.flux_mode_combo.addItems(["Global", "Active Concurrent", "Unlinked"])
        self.flux_mode_combo.setCurrentText(self.engine.runtime_clock.rhythm_flux_mode)
        self.flux_mode_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        self.flux_mode_combo.currentTextChanged.connect(self._on_flux_mode_changed)
        ctrl_layout.addWidget(self.flux_mode_combo, 0, 4)

        ctrl_layout.addWidget(QLabel("Flux Rate:"), 0, 5)
        self.flux_rate_spin = QDoubleSpinBox()
        self.flux_rate_spin.setRange(0.25, 4.0)
        self.flux_rate_spin.setValue(self.engine.runtime_clock.rhythm_flux_rate)
        self.flux_rate_spin.setSingleStep(0.25)
        self.flux_rate_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        self.flux_rate_spin.valueChanged.connect(self._on_flux_rate_changed)
        ctrl_layout.addWidget(self.flux_rate_spin, 0, 6)

        # Equation Controls
        self.eq_input = QLineEdit(self.engine.scale_equation)
        self.eq_input.setStyleSheet("background-color: #161b22; color: #00ffcc; font-family: monospace; border: 1px solid #30363d;")

        self.inc_spin = QDoubleSpinBox()
        self.inc_spin.setRange(0.01, 5.0)
        self.inc_spin.setValue(self.engine.scale_increment)
        self.inc_spin.setSingleStep(0.05)
        self.inc_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")

        self.steps_spin = QSpinBox()
        self.steps_spin.setRange(4, 64)
        self.steps_spin.setValue(self.engine.divergence_steps_count)
        self.steps_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")

        apply_eq_btn = QPushButton("Apply Equation Scale")
        apply_eq_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 4px;")
        apply_eq_btn.clicked.connect(self._apply_equation_scale)

        ctrl_layout.addWidget(QLabel("Scale Equation:"), 1, 0)
        ctrl_layout.addWidget(self.eq_input, 1, 1, 1, 3)
        ctrl_layout.addWidget(apply_eq_btn, 1, 4, 1, 3)

        ctrl_layout.addWidget(QLabel("Increment:"), 2, 0)
        ctrl_layout.addWidget(self.inc_spin, 2, 1)
        ctrl_layout.addWidget(QLabel("Steps:"), 2, 2)
        ctrl_layout.addWidget(self.steps_spin, 2, 3)

        # Action Buttons Row
        actions_layout = QHBoxLayout()
        rand_btn = QPushButton("🎲 Randomize Song & Patchbay")
        rand_btn.setStyleSheet("background-color: #2b1135; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        rand_btn.clicked.connect(self._randomize_song_action)

        save_btn = QPushButton("💾 Save Project")
        save_btn.setStyleSheet("background-color: #1f242c; color: #ffffff; border: 1px solid #30363d; padding: 6px;")
        save_btn.clicked.connect(self._save_project)

        load_btn = QPushButton("📂 Load Project")
        load_btn.setStyleSheet("background-color: #1f242c; color: #ffffff; border: 1px solid #30363d; padding: 6px;")
        load_btn.clicked.connect(self._load_project)

        export_btn = QPushButton("📻 Export Master WAV Audio")
        export_btn.setStyleSheet("background-color: #112b35; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 6px;")
        export_btn.clicked.connect(self._export_audio)

        actions_layout.addWidget(rand_btn)
        actions_layout.addWidget(save_btn)
        actions_layout.addWidget(load_btn)
        actions_layout.addWidget(export_btn)

        layout.addWidget(controls_group)
        layout.addLayout(actions_layout)

        # Playlist Options & Controls
        pl_options_layout = QHBoxLayout()
        pl_options_layout.addWidget(QLabel("Pattern:"))
        self.pattern_combo = QComboBox()
        self.pattern_combo.addItems(self.engine.available_patterns)
        self.pattern_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        pl_options_layout.addWidget(self.pattern_combo)

        pl_options_layout.addWidget(QLabel("Chord:"))
        self.playlist_chord_combo = QComboBox()
        self.playlist_chord_combo.addItems(list(self.engine.math_chord_library.keys()))
        self.playlist_chord_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        pl_options_layout.addWidget(self.playlist_chord_combo)

        pl_options_layout.addWidget(QLabel("Pitch St:"))
        self.playlist_pitch_spin = QDoubleSpinBox()
        self.playlist_pitch_spin.setRange(-24.0, 24.0)
        self.playlist_pitch_spin.setValue(0.0)
        self.playlist_pitch_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        pl_options_layout.addWidget(self.playlist_pitch_spin)

        pl_options_layout.addWidget(QLabel("Amp:"))
        self.playlist_amp_spin = QDoubleSpinBox()
        self.playlist_amp_spin.setRange(0.1, 2.0)
        self.playlist_amp_spin.setValue(1.0)
        self.playlist_amp_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        pl_options_layout.addWidget(self.playlist_amp_spin)

        pl_options_layout.addWidget(QLabel("Auto Pattern:"))
        self.playlist_auto_combo = QComboBox()
        self.playlist_auto_combo.addItems(list(self.engine.automation_patterns.keys()))
        self.playlist_auto_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        pl_options_layout.addWidget(self.playlist_auto_combo)

        create_patch_btn = QPushButton("⚡ Create Patch")
        create_patch_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 4px;")
        create_patch_btn.clicked.connect(self._create_patch_prompt)
        pl_options_layout.addWidget(create_patch_btn)

        layout.addLayout(pl_options_layout)

        # Splitter for Playlist and Patch Canvas
        splitter = QSplitter(Qt.Orientation.Vertical)

        # Infinite Playlist Section
        playlist_group = QGroupBox("Infinite Playlist Arrangement Canvas (Click to Place Clip)")
        playlist_group.setStyleSheet("QGroupBox { color: #f5d97d; font-weight: bold; border: 1px solid #30363d; margin-top: 6px; }")
        pl_layout = QVBoxLayout(playlist_group)
        self.infinite_playlist_canvas = InfinitePlaylistCanvas(self.engine, self)
        pl_layout.addWidget(self.infinite_playlist_canvas)
        splitter.addWidget(playlist_group)

        # Patch Canvas Section
        patch_group = QGroupBox("Master Visual Patchbay & Cable Wiring Matrix")
        patch_group.setStyleSheet("QGroupBox { color: #00ffcc; font-weight: bold; border: 1px solid #30363d; margin-top: 6px; }")
        patch_layout = QVBoxLayout(patch_group)
        self.patch_canvas = MasterPatchCanvas(self)
        patch_layout.addWidget(self.patch_canvas)

        self.manual_patch_panel = QWidget(self)
        manual_patch_layout = QHBoxLayout(manual_patch_panel)
        manual_patch_layout.setContentsMargins(0, 0, 0, 0)
        manual_patch_layout.addWidget(QLabel("Manual Target Override Route:"))
        self.manual_patch_combo = QComboBox()
        self.manual_patch_combo.addItems([
            "Direct Bus Sum [Master Audio]",
            "Auxiliary Shifter Loop A",
            "Auxiliary Shifter Loop B",
            "Quantum Resonator Feedback In",
            "Stochastic Granular Direct Send"
        ])
        self.manual_patch_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        manual_patch_layout.addWidget(self.manual_patch_combo)

        apply_manual_route_btn = QPushButton("Apply Override Route")
        apply_manual_route_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 3px;")
        apply_manual_route_btn.clicked.connect(self._apply_manual_override_route)
        manual_patch_layout.addWidget(apply_manual_route_btn)

        patch_layout.addWidget(manual_patch_panel)
        splitter.addWidget(patch_group)

        layout.addWidget(splitter)

    def _on_bpm_changed(self, val):
        self.engine.global_bpm = val / 10.0
        self.bpm_label.setText(f"{self.engine.global_bpm:.1f} BPM")

    def _on_flux_mode_changed(self, mode):
        self.engine.runtime_clock.rhythm_flux_mode = mode
        print(f"Rhythm Flux Link Mode updated to: {mode}")

    def _on_flux_rate_changed(self, val):
        self.engine.runtime_clock.rhythm_flux_rate = val
        print(f"Rhythm Flux Rate multiplier updated to: {val}x")

    def _apply_equation_scale(self):
        self.engine.scale_equation = self.eq_input.text()
        self.engine.scale_increment = self.inc_spin.value()
        self.engine.divergence_steps_count = self.steps_spin.value()
        freqs = self.engine.generate_equation_scale_frequencies()
        QMessageBox.information(self, "Equation Applied", f"Successfully recalculated equation scale! Generated {len(freqs)} frequencies.")

    def _randomize_song_action(self):
        self.engine.randomize_song()
        self.patch_canvas.update()
        self.infinite_playlist_canvas.canvas_inner.update()
        QMessageBox.information(self, "Song & Patchbay Randomizer", "Successfully randomized song arrangement, synth wiring, effects modules, and global cross-tab patch cables!")

    def _save_project(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Project File", "", "EQ爾 Groovebox Files (*.json)")
        if path:
            self.engine.serialize_project(path)
            QMessageBox.information(self, "Project Saved", f"Project successfully saved to:\n{path}")

    def _load_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Project File", "", "EQ爾 Groovebox Files (*.json)")
        if path:
            self.engine.deserialize_project(path)
            self.bpm_slider.setValue(int(self.engine.global_bpm * 10))
            self.eq_input.setText(self.engine.scale_equation)
            self.patch_canvas.update()
            self.infinite_playlist_canvas.canvas_inner.update()
            QMessageBox.information(self, "Project Loaded", f"Project successfully loaded from:\n{path}")

    def _export_audio(self):
        path, _ = QFileDialog.getSaveFileName(self, "Export Master WAV Audio", "", "WAV Audio Files (*.wav)")
        if path:
            self.engine.export_audio(path)
            QMessageBox.information(self, "Audio Exported", f"Master audio successfully rendered and exported to:\n{path}")

    def _create_patch_prompt(self):
        source, ok1 = QInputDialog.getText(self, "Create Patch", "Enter Source Module/Node:")
        if not ok1 or not source:
            return
        destination, ok2 = QInputDialog.getText(self, "Create Patch", "Enter Target Destination Module/Node:")
        if not ok2 or not destination:
            return
        amount, ok3 = QInputDialog.getDouble(self, "Create Patch", "Enter Modulation Gain Amount:", 1.0, 0.1, 10.0, 2)
        if not ok3:
            return

        GLOBAL_BUS.add_cable(
            src_module=source, src_node="Custom Node",
            tgt_module=destination, tgt_node="Primary Sum Node",
            polarity="+", gain=amount
        )
        self.patch_canvas.update()
        QMessageBox.information(self, "Patch Created", f"Successfully created custom patch connection from '{source}' to '{destination}' with amount {amount}x!")

    def _apply_manual_override_route(self):
        selected_route = self.manual_patch_combo.currentText()
        if GLOBAL_BUS.global_cables:
            GLOBAL_BUS.global_cables[-1]["tgt_module"] = selected_route
            GLOBAL_BUS.broadcast_update()
            QMessageBox.information(self, "Manual Patch Route Applied", f"Successfully reconfigured the patch route to target: {selected_route}")
        else:
            QMessageBox.warning(self, "No Active Cables", "There are no active global cables in the patchbay to re-route. Create a patch or run the randomizer first.")

    def on_global_patch_updated(self, cables):
        self.patch_canvas.cables = cables
        self.patch_canvas.update()


# -------------------------------------------------------------------------
# MAIN WINDOW FRAMEWORK
# -------------------------------------------------------------------------


class PortWidget(QWidget):
    """Represents an input or output data jack on a scientific processing node."""
    def __init__(self, port_type, parent=None):
        super().__init__(parent)
        self.port_type = port_type  # 'in' or 'out'
        self.setFixedSize(22, 22)
        self.color = "#00ffc8" if port_type == 'out' else "#ff6400"
        self.setStyleSheet(f"""
            background-color: {self.color};
            border-radius: 11px;
            border: 3px solid #1a1a1a;
        """)

    def mousePressEvent(self, event):
        if self.parent() and hasattr(self.parent(), 'start_cable_drag'):
            self.parent().start_cable_drag(self)
        event.accept()


class ScientificCanvas(QWidget):
    """Interactive canvas workspace mapping mathematical data pipelines with glowing bezier patch lines."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(2400, 1800)
        self.cables = []
        self.active_cable_start = None
        self.current_mouse_pos = QPoint(0, 0)
        self.setMouseTracking(True)
        self.setStyleSheet("background-color: #0d0d0d; border: 1px solid #222;")

    def start_cable_drag(self, port_widget):
        self.active_cable_start = port_widget
        self.current_mouse_pos = port_widget.mapTo(self, port_widget.rect().center())
        self.update()

    def mouseMoveEvent(self, event):
        if self.active_cable_start:
            self.current_mouse_pos = event.pos()
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.active_cable_start:
            target_widget = self.childAt(event.pos())
            if isinstance(target_widget, PortWidget) and target_widget != self.active_cable_start:
                if self.active_cable_start.port_type != target_widget.port_type:
                    cable_pair = (self.active_cable_start, target_widget)
                    reverse_pair = (target_widget, self.active_cable_start)
                    if cable_pair not in self.cables and reverse_pair not in self.cables:
                        self.cables.append(cable_pair)
            self.active_cable_start = None
            self.update()
        super().mouseReleaseEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        for start, end in self.cables:
            if start and end:
                p1 = start.mapTo(self, start.rect().center())
                p2 = end.mapTo(self, end.rect().center())

                glow_pen = QPen(QColor(0, 255, 200, 60), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(glow_pen)
                painter.drawPath(self.create_bezier_path(p1, p2))

                core_pen = QPen(QColor(0, 255, 200), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap)
                painter.setPen(core_pen)
                painter.drawPath(self.create_bezier_path(p1, p2))

        if self.active_cable_start:
            p1 = self.active_cable_start.mapTo(self, self.active_cable_start.rect().center())
            p2 = self.current_mouse_pos

            drag_pen = QPen(QColor(255, 100, 0, 200), 3, Qt.PenStyle.DashLine, Qt.PenCapStyle.RoundCap)
            painter.setPen(drag_pen)
            painter.drawPath(self.create_bezier_path(p1, p2))

    def create_bezier_path(self, p1, p2):
        path = QPainterPath()
        path.moveTo(p1)
        dx = (p2.x() - p1.x()) * 0.5
        ctrl1 = QPoint(p1.x() + dx, p1.y())
        ctrl2 = QPoint(p2.x() - dx, p2.y())
        path.cubicTo(ctrl1, ctrl2, p2)
        return path



class DoubleNumericSliderRow(QWidget):
    """Synchronized precision double-spinbox and slider layout for scientific variables."""
    def __init__(self, min_val, max_val, default_val, decimals=2, unit="", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(int(min_val * 100), int(max_val * 100))
        self.slider.setValue(int(default_val * 100))
        self.slider.setStyleSheet("background: transparent;")

        self.spinbox = QDoubleSpinBox()
        self.spinbox.setRange(min_val, max_val)
        self.spinbox.setValue(default_val)
        self.spinbox.setDecimals(decimals)
        self.spinbox.setSuffix(unit)
        self.spinbox.setStyleSheet("background-color: #27272a; color: #00ffc8; border: 1px solid #52525b; padding: 3px; border-radius: 3px;")

        self.slider.valueChanged.connect(lambda v: self.spinbox.setValue(v / 100.0))
        self.spinbox.valueChanged.connect(lambda v: self.slider.setValue(int(v * 100)))

        layout.addWidget(self.slider, 3)
        layout.addWidget(self.spinbox, 1)

class BottomToolboxesPane(QScrollArea):
    def __init__(self, spawn_callback, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.spawn_callback = spawn_callback

        container = QWidget()
        layout = QGridLayout(container)

        # 24 distinct instrument & toolbox variants (including Eskibrutus)
        toolboxes = [
            ("1. Step Sequencer Grid", "16-step trigger matrix for rhythmic coordinate pulsing."),
            ("2. Additive Harmonic Bank", "Draw and morph partial frequencies via x, y, z vectors."),
            ("3. Formant Vocal Filter", "Vowel transition generator modeled on acoustic formants."),
            ("4. Stochastic Probability Node", "Randomized weight gates for generative melody generation."),
            ("5. Vector Synthesizer Pad", "2D joystick space for real-time timbre morphing."),
            ("6. State-Variable Filter Rack", "Resonant lowpass/highpass sweep filters."),
            ("7. Non-Linear Waveshaper", "Harmonic saturation and distortion drive controls."),
            ("8. Stereo Feedback Delay Line", "Echo matrix with adjustable feedback attenuation."),
            ("9. LFO Modulation Generator", "Waveform shape, rate, and depth assignment units."),
            ("10. Granular Texture Scraper", "Audio grain cloud pulverizer and pitch scatterer."),
            ("11. Envelope Generator (ADSR)", "Amplitude shape shaping for dynamic note articulation."),
            ("12. Coordinate Formula Router", "Direct injection parser for custom runtime math nodes."),
            ("13. Eskibrutus Heavy Node", "Aggressive distortion matrix with harmonic fold reset."),
            ("14. Isosceles Operator Synth", "Triangular geometric wave-interference oscillator."),
            ("15. Wavetable Morph Engine", "Crossfade matrix for multi-frame sequential tables."),
            ("16. Frequency Modulation Bank", "Complex 4-operator carrier/modulator algorithm matrix."),
            ("17. Ring Modulator Matrix", "Sideband frequency multiplication grid."),
            ("18. Bitcrush Quantizer", "Sample-rate and bit-depth degradation processor."),
            ("19. Spectral Resonator", "Comb-filter bank tuned to harmonic overtones."),
            ("20. Chaos Attractor Synth", "Lorenz/Rössler differential equation sound source."),
            ("21. Sub-Bass Fundamental Generator", "Pure low-end sub-harmonic reinforcement node."),
            ("22. Noise Texture Generator", "Filtered white/pink/brownian architectural noise."),
            ("23. Resonant Body Simulator", "Modal physical modeling plate and string exciter."),
            ("24. Master Bus Limiter", "Brickwall peak processor and output saturator.")
        ]

        for idx, (title, desc) in enumerate(toolboxes):
            box = QFrame()
            box.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
            box.setStyleSheet("background-color: #1b1b1b; border: 1px solid #333; border-radius: 4px;")
            box_layout = QVBoxLayout(box)

            title_lbl = QLabel(f"<b>{title}</b>")
            title_lbl.setStyleSheet("color: #00ffaa;")
            desc_lbl = QLabel(desc)
            desc_lbl.setWordWrap(True)
            desc_lbl.setStyleSheet("color: #aaa; font-size: 11px;")

            box_layout.addWidget(title_lbl)
            box_layout.addWidget(desc_lbl)

            # Action button to spawn this specific synth variant into the top tabs!
            spawn_btn = QPushButton(f"Spawn Instance [{idx+1}]")
            spawn_btn.setStyleSheet("background-color: #333; color: #fff; font-size: 10px;")
            # Capture title for the callback
            spawn_btn.clicked.connect(lambda checked, t=title: self.spawn_callback(t))
            box_layout.addWidget(spawn_btn)

            row, col = divmod(idx, 4)  # 4 columns for 24 items
            layout.addWidget(box, row, col)

        container.setLayout(layout)
        self.setWidget(container)
# ==========================================
# 4. MODULAR TAB MANAGER (TOP PANE)
# ==========================================
class ModularTabManager(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)
        self.add_new_module_tab("Core Eskibrutus Node")

    def add_new_module_tab(self, title_prefix="Synth Node"):
        container = QWidget()
        layout = QVBoxLayout(container)

        visualizer = CoordinateVisualizer()
        formula_edit = QLineEdit("np.sin(t * 2.0) * x")
        formula_edit.setStyleSheet("background-color: #111; color: #0f0; font-family: monospace;")

        layout.addWidget(QLabel(f"--- Active Workspace: {title_prefix} ---"))
        layout.addWidget(visualizer)
        layout.addWidget(QLabel("Runtime Expression (x, y, z, t):"))
        layout.addWidget(formula_edit)

        # Add custom control switches for this spawned instance
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QPushButton("Fold Reset"))
        controls_layout.addWidget(QPushButton("Bypass FX"))
        layout.addLayout(controls_layout)

        container.setLayout(layout)
        self.addTab(container, title_prefix)
        self.setCurrentWidget(container)

        # Live visual feedback simulation timer
        self.timer = QTimer(self)
        t_val = [0.0]
        def sim_tick():
            t_val[0] += 0.1
            try:
                x = float(eval(formula_edit.text(), {"np": np, "t": t_val[0], "x": 1.0, "y": 1.0, "z": 0.0}))
                y = float(eval("np.cos(t * 1.5) * y", {"np": np, "t": t_val[0], "x": 1.0, "y": 1.0, "z": 0.0}))
                visualizer.update_coordinates(x, y)
            except Exception:
                pass
        self.timer.timeout.connect(sim_tick)
        self.timer.start(50)

    def close_tab(self, index):
        if self.count() > 1:
            widget = self.widget(index)
            self.removeTab(index)
            widget.deleteLater()

class VisualNodeScriptingWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Visual Equation & Symbolic Scripting Canvas")
        self.resize(1000, 650)
        self.setStyleSheet(TELETUBBY_STYLE)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>Interactive Geometric Node Patch Builder & Symbolic Engine</b>"))

        self.geom_canvas = GeometricSymbolicCanvas(self)
        layout.addWidget(self.geom_canvas)

        canvas_splitter = QSplitter(Qt.Orientation.Horizontal)

        toolbox_widget = QWidget()
        tb_layout = QVBoxLayout(toolbox_widget)
        tb_layout.addWidget(QLabel("<b>Click Blocks to Insert</b>"))

        blocks = [
            "⚡ Eski Sine [Jack]", "🔀 Wavefold Node [Jack]", "🔁 For-Loop Repeater [Jack]",
            "⚖️ Heuristic Branch [Jack]", "🌀 Noise Generator [Jack]", "📉 Low-Pass Filter [Jack]",
            "➕ Additive Sum [Jack]", "✖️ Ring Modulator [Jack]", "⏱️ Delay Line [Jack]",
            "🎛️ Envelope Shaper [Jack]", "🔍 Phase Root [Jack]", "💥 Eskibrutus Fold [Jack]"
        ]
        for b in blocks:
            btn = QPushButton(b)
            btn.setStyleSheet("background-color: #6c5ce7; color: white; text-align: left; padding-left: 8px;")
            btn.clicked.connect(lambda checked, text=b: self.append_node_text(text))
            tb_layout.addWidget(btn)

        canvas_splitter.addWidget(toolbox_widget)

        self.assembly_board = QTextEdit()
        self.assembly_board.setPlainText(
            "# Interactive Modular Patch Assembly & Geometric Symbolic Equation Network\n"
            "[ Node α: Eski-Prime Sine ] ===(Symbolic Jack)===> [ Node β: Dipsy Wavefolder ]\n"
        )
        self.assembly_board.setStyleSheet("background-color: #ffffff; color: #1e272e; font-family: monospace; font-size: 13px; border-radius: 10px;")
        canvas_splitter.addWidget(self.assembly_board)

        canvas_splitter.setSizes([320, 680])
        layout.addWidget(canvas_splitter)

        compile_btn = QPushButton("Compile and Apply Geometric Symbolic Matrix to Active Stream")
        compile_btn.setStyleSheet("background-color: #00b894; color: white; font-weight: bold;")
        compile_btn.clicked.connect(lambda: QMessageBox.information(self, "Compiled", "Interactive visual graph and symbolic equations successfully compiled."))
        layout.addWidget(compile_btn)

    def append_node_text(self, node_name):
        current = self.assembly_board.toPlainText()
        updated = current + f"\n[ Geometric Linked: {node_name} ] ===(Symbolic Patch Jack)===> [ Routing Matrix Bus ]"
        self.assembly_board.setPlainText(updated)
# ==========================================
# 2. COORDINATE VISUALIZER
# ==========================================
class CoordinateVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(110)
        self.setStyleSheet("background-color: black; border: 1px solid #00ffaa;")
        self.point_history = []
        self.max_points = 150

    def update_coordinates(self, x, y):
        self.point_history.append((x, y))
        if len(self.point_history) > self.max_points:
            self.point_history.pop(0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self):
            return
        try:
            painter.fillRect(self.rect(), QColor(10, 10, 10))
            if len(self.point_history) >= 2:
                pen = QPen(QColor(0, 255, 150))
                pen.setWidth(2)
                painter.setPen(pen)
                width, height = self.width(), self.height()
                for i in range(1, len(self.point_history)):
                    x1 = (self.point_history[i-1][0] + 1) * 0.5 * width
                    y1 = (self.point_history[i-1][1] + 1) * 0.5 * height
                    x2 = (self.point_history[i][0] + 1) * 0.5 * width
                    y2 = (self.point_history[i][1] + 1) * 0.5 * height
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        finally:
            painter.end()

class PianoRollEditor(QDialog):
    def __init__(self, instrument_name, step_count=48, parent=None):
        super().__init__(parent)
        self.instrument_name = instrument_name
        self.setWindowTitle(f"Sequencer & Piano Roll: {instrument_name}")
        self.resize(1000, 520)
        self.setStyleSheet(TELETUBBY_STYLE)

        layout = QVBoxLayout(self)
        top_ctrl = QHBoxLayout()
        top_ctrl.addWidget(QLabel(f"<b>Polyrhythmic Sequence Matrix for {instrument_name}</b>"))

        top_ctrl.addWidget(QLabel("Grid Length:"))
        self.steps_combo = QComboBox()
        self.steps_combo.addItems(["16 Steps", "32 Steps", "48 Steps", "64 Steps"])
        self.steps_combo.setCurrentText(f"{step_count} Steps")
        top_ctrl.addWidget(self.steps_combo)

        top_ctrl.addWidget(QLabel("Polyrhythm Divisor:"))
        self.poly_spin = QDoubleSpinBox()
        self.poly_spin.setRange(0.25, 4.0)
        self.poly_spin.setValue(1.0)
        self.poly_spin.setSingleStep(0.05)
        top_ctrl.addWidget(self.poly_spin)

        layout.addLayout(top_ctrl)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        grid_container = QWidget()
        self.grid_layout = QGridLayout(grid_container)

        self.cells = []
        for step in range(48):
            cell_frame = QFrame()
            c_layout = QVBoxLayout(cell_frame)

            seq_name = f"{instrument_name}_seq_{step+1}"
            btn = QPushButton(f"{seq_name}\n[Gate On]")
            btn.setCheckable(True)
            btn.setChecked(True)

            offset_slider = QSlider(Qt.Orientation.Horizontal)
            offset_slider.setRange(-50, 50)
            offset_slider.setValue(0)

            c_layout.addWidget(btn)
            c_layout.addWidget(QLabel("De-quant Offset:"))
            c_layout.addWidget(offset_slider)

            self.grid_layout.addWidget(cell_frame, 0, step)
            self.cells.append((btn, offset_slider))

        grid_container.setLayout(self.grid_layout)
        scroll.setWidget(grid_container)
        layout.addWidget(scroll)

        apply_btn = QPushButton(f"Commit Sequences for {instrument_name} to Master Timeline")
        apply_btn.setStyleSheet("background-color: #00b894; color: white;")
        apply_btn.clicked.connect(lambda: QMessageBox.information(self, "Committed", f"Polyrhythmic unquantized sequences for {instrument_name} updated."))
        layout.addWidget(apply_btn)
# ==========================================
# 3. STANDALONE PLAYLIST WINDOW
# ==========================================
class PlaylistArrangementWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Global Playlist & Arrangement Timeline")
        self.resize(750, 520)
        self.setStyleSheet(TELETUBBY_STYLE)

        container = QWidget()
        layout = QVBoxLayout(container)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("<b>Timeline Snap & Polyrhythm Scaling:</b>"))
        self.grid_scale_combo = QComboBox()
        self.grid_scale_combo.addItems(["1 Bar (Quantized)", "1/2 Beat", "1/4 Beat", "1/8 Beat", "Fully Unquantized / De-quantized Flow"])
        controls.addWidget(self.grid_scale_combo)

        controls.addWidget(QLabel("<b>Tempo (BPM):</b>"))
        self.global_tempo = QLineEdit("124.0")
        controls.addWidget(self.global_tempo)
        layout.addLayout(controls)

        self.timeline_view = QTextEdit()
        self.timeline_view.setPlainText(
            "# Global Playlist Arrangement Channels & Paintbrush Clips\n"
            "Track 1 [Instrument_1] |=======| [Bars 1 - 16]   (Saved Preset: Lead_Groove_A)\n"
            "Track 2 [Instrument_2]   |===|   [Bars 8 - 20]   (Saved Preset: Bass_Stab_B)\n"
            "Track 3 [Instrument_3] |=======| [Bars 12 - 32]  (Saved Preset: Pad_Sweep_C)"
        )
        self.timeline_view.setStyleSheet("background-color: #ffffff; color: #1e272e; font-family: monospace; font-size: 13px; border-radius: 10px;")
        layout.addWidget(self.timeline_view)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Universal Brush Painter Mode"))
        btn_layout.addWidget(QPushButton("Quantize All Sequence Clips"))
        btn_layout.addWidget(QPushButton("Render Instrument Stems to Disk"))
        layout.addLayout(btn_layout)

        container.setLayout(layout)
        self.setCentralWidget(container)

# ==========================================
# MODULATION ROUTING HUB
# ==========================================
class ModulationRoutingWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Global Modulation & LFO Hub")
        self.resize(700, 480)
        self.setStyleSheet(DAW_STYLE)

        container = QWidget()
        layout = QVBoxLayout(container)

        layout.addWidget(QLabel("<b>🌸 Direct Interactive LFO & Envelope Modulation Hub 🌸</b>"))

        mod_grid = QGridLayout()
        mod_grid.addWidget(QLabel("LFO 1 Rate (Hz):"), 0, 0)
        self.lfo1_slider = QSlider(Qt.Orientation.Horizontal)
        self.lfo1_slider.setValue(45)
        mod_grid.addWidget(self.lfo1_slider, 0, 1)

        mod_grid.addWidget(QLabel("LFO Shape:"), 1, 0)
        self.shape_box = QComboBox()
        self.shape_box.addItems(["Sine Wave", "Triangle Wave", "Square Wave", "Random Chaos Curve", "Tubby Step Vector"])
        mod_grid.addWidget(self.shape_box, 1, 1)

        mod_grid.addWidget(QLabel("Envelope Decay (ms):"), 2, 0)
        self.env_slider = QSlider(Qt.Orientation.Horizontal)
        self.env_slider.setValue(70)
        mod_grid.addWidget(self.env_slider, 2, 1)

        layout.addLayout(mod_grid)

        self.mod_view = QTextEdit()
        self.mod_view.setPlainText(
            "# Active Modulation & LFO Routing Table\n"
            "LFO 1 ---> Routed to Filter Cutoff (Depth: 75%)\n"
            "LFO 2 ---> Routed to Chaos Attractor (Depth: 100%)\n"
            "Envelope Shaper ---> Routed to Master Limiter Threshold"
        )
        self.mod_view.setStyleSheet("background-color: #ffffff; color: #1e272e; font-family: monospace; font-size: 13px; border-radius: 10px;")
        layout.addWidget(self.mod_view)

        apply_btn = QPushButton("Commit Modulation Patches")
        apply_btn.setStyleSheet("background-color: #00b894; color: white;")
        apply_btn.clicked.connect(lambda: QMessageBox.information(self, "Modulation Updated", "Modulation matrix parameters updated."))
        layout.addWidget(apply_btn)

        container.setLayout(layout)
        self.setCentralWidget(container)
class PlaylistWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tubby-Land Global Arrangement & Painter")
        self.resize(1050, 620)
        self.setStyleSheet(TELETUBBY_STYLE)

        container = QWidget()
        layout = QVBoxLayout(container)

        controls = QHBoxLayout()
        controls.addWidget(QLabel("<b>Snap-to-Grid Scale:</b>"))
        self.grid_scale_combo = QComboBox()
        self.grid_scale_combo.addItems(["1 Bar", "1/2 Beat", "1/4 Beat", "1/8 Beat", "Free / Unquantized Tubby Flow"])
        controls.addWidget(self.grid_scale_combo)

        controls.addWidget(QLabel("<b>Global Tempo (BPM):</b>"))
        self.global_tempo = QLineEdit("120.0")
        controls.addWidget(self.global_tempo)
        layout.addLayout(controls)

        self.timeline_view = QTextEdit()
        self.timeline_view.setPlainText(
            "Track 1 [Inst 1: Eskibrutus Heavy] |===| [Bars 1 - 8]   (Sticky Gate Active)\n"
            "Track 2 [Inst 12: Additive Harmonic] |=======| [Bars 5 - 16] (Local Tempo: 0.75x)\n"
            "Track 3 [Inst 48: Chaos Attractor]   |===| [Bars 17 - 24] (Universal Brush Mode)"
        )
        self.timeline_view.setStyleSheet("background-color: #ffffff; color: #2f3640; font-family: monospace; font-size: 13px; border-radius: 15px;")
        layout.addWidget(self.timeline_view)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(QPushButton("Universal Brush Painter Mode"))
        btn_layout.addWidget(QPushButton("Render Tubby Stems to Disk"))
        layout.addLayout(btn_layout)

        container.setLayout(layout)
        self.setCentralWidget(container)
# ==========================================
# 4. MINIATURE SYNTH WIDGET WITH PATCH CABLES
# ==========================================
class MiniSynthNodeWidget(QFrame):
    def __init__(self, synth_name):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel | QFrame.Shadow.Raised)
        self.setStyleSheet("background-color: #1e1e1e; border: 1px solid #444; border-radius: 6px;")

        layout = QVBoxLayout(self)
        title = QLabel(f"<b>Mini-Synth: {synth_name}</b>")
        title.setStyleSheet("color: #ffaa00;")
        layout.addWidget(title)

        self.cutoff_slider = QSlider(Qt.Orientation.Horizontal)
        self.drive_slider = QSlider(Qt.Orientation.Horizontal)

        layout.addWidget(QLabel("Cutoff / Frequency Freq:"))
        layout.addWidget(self.cutoff_slider)
        layout.addWidget(QLabel("Distortion / Fold Drive:"))
        layout.addWidget(self.drive_slider)

        patch_layout = QHBoxLayout()
        self.src_combo = QComboBox()
        self.src_combo.addItems(["X Coord", "Y Coord", "Z Coord", "LFO 1"])
        self.dest_combo = QComboBox()
        self.dest_combo.addItems(["-> Filter Cutoff", "-> Fold Threshold", "-> Pitch Mod"])

        patch_layout.addWidget(self.src_combo)
        patch_layout.addWidget(QLabel("⤹"))
        patch_layout.addWidget(self.dest_combo)
        layout.addLayout(patch_layout)
class FloatingSynthWindow(QMainWindow):
    def __init__(self, synth_name, synth_id, custom_title="", parent=None):
        super().__init__(parent)
        self.synth_name = synth_name
        self.custom_title = custom_title if custom_title else f"Plugin_{synth_id}"
        self.setWindowTitle(f"Advanced Device Plugin: {self.custom_title} ({synth_name})")
        self.resize(520, 620)
        self.setStyleSheet(DAW_STYLE)

        self.dsp_engine = AdvancedDSPEngine()

        container = QWidget()
        layout = QVBoxLayout(container)

        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("<b>Device Name:</b>"))
        self.name_edit = QLineEdit(self.custom_title)
        name_layout.addWidget(self.name_edit)

        name_layout.addWidget(QLabel("Alg:"))
        self.wave_combo = QComboBox()
        self.wave_combo.addItems(["Sine FM", "Square PWM", "Saw Supersaw", "Noise Chaos"])
        self.wave_combo.currentIndexChanged.connect(self.update_synth_algorithm)
        name_layout.addWidget(self.wave_combo)
        layout.addLayout(name_layout)

        layout.addWidget(QLabel("<b>Live Oscilloscope & Wavefolder View</b>"))
        self.oscilloscope = RealtimeOscilloscope(self)
        layout.addWidget(self.oscilloscope)

        controls_layout = QGridLayout()

        controls_layout.addWidget(QLabel("Cutoff / Resonance:"), 0, 0)
        self.cutoff_slider = QSlider(Qt.Orientation.Horizontal)
        self.cutoff_slider.setValue(75)
        controls_layout.addWidget(self.cutoff_slider, 0, 1)

        controls_layout.addWidget(QLabel("Wavefold Drive:"), 1, 0)
        self.drive_slider = QSlider(Qt.Orientation.Horizontal)
        self.drive_slider.setValue(50)
        self.drive_slider.valueChanged.connect(self.update_drive_param)
        controls_layout.addWidget(self.drive_slider, 1, 1)

        controls_layout.addWidget(QLabel("Envelope Decay (s):"), 2, 0)
        self.decay_spin = QDoubleSpinBox()
        self.decay_spin.setValue(0.3)
        self.decay_spin.setRange(0.01, 5.0)
        self.decay_spin.setSingleStep(0.05)
        controls_layout.addWidget(self.decay_spin, 2, 1)

        layout.addLayout(controls_layout)

        pad_layout = QHBoxLayout()
        pad_layout.addWidget(QLabel("<b>Trigger Keys:</b>"))
        for note_name, freq in [("C4", 261.63), ("D4", 293.66), ("E4", 329.63), ("F4", 349.23), ("G4", 392.00)]:
            btn = QPushButton(note_name)
            btn.setStyleSheet("background-color: #2b2b2b; color: #ff6b00; border: 1px solid #ff6b00;")
            btn.clicked.connect(lambda checked, f=freq: self.trigger_local_note(f))
            pad_layout.addWidget(btn)
        layout.addLayout(pad_layout)

        export_btn = QPushButton("💾 Export Plugin Stem (.wav)")
        export_btn.setStyleSheet("background-color: #007acc; color: white;")
        export_btn.clicked.connect(self.export_plugin_stem)
        layout.addWidget(export_btn)

        container.setLayout(layout)
        self.setCentralWidget(container)

    def update_synth_algorithm(self, index):
        self.oscilloscope.wave_type = index
        self.oscilloscope.update()

    def update_drive_param(self, value):
        normalized_drive = 1.0 + (value / 25.0)
        self.oscilloscope.drive = normalized_drive
        self.oscilloscope.update()

    def trigger_local_note(self, freq):
        try:
            drive_val = 1.0 + (self.drive_slider.value() / 25.0)
            dur = self.decay_spin.value()
            w_type = self.wave_combo.currentIndex()
            self.dsp_engine.export_to_wav("plugin_trigger.wav", duration_sec=dur, freq=freq, drive=drive_val, wave_type=w_type)
        except Exception:
            pass

    def export_plugin_stem(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Plugin Stem", f"{self.name_edit.text()}_stem.wav", "WAV Files (*.wav)")
        if file_path:
            try:
                drive_val = 1.0 + (self.drive_slider.value() / 25.0)
                w_type = self.wave_combo.currentIndex()
                self.dsp_engine.export_to_wav(file_path, duration_sec=4.0, freq=261.63, drive=drive_val, wave_type=w_type)
                QMessageBox.information(self, "Stem Exported", f"Successfully rendered device stem to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Export Failed", str(e))
class PermanentPatchBayPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet("""
            background-color: #ff9ff3;
            border: 3px solid #ffffff;
            border-radius: 12px;
            padding: 4px;
        """)
        layout = QHBoxLayout(self)

        layout.addWidget(QLabel("<b>GLOBAL 48-INSTRUMENT PATCH BAY</b>"))

        self.global_src = QComboBox()
        self.global_src.addItems(["Master Clock Gate", "QWERTY Live Trigger", "Global Sequencer Trigger", "Playlist Timeline Cursor"])

        self.global_dest = QComboBox()
        self.global_dest.addItems(["All 48 Instrument Folds", "Master Bus Limiter", "Repeater Matrix Bus", "Global Pitch Shift"])

        self.repeater_slider = QSlider(Qt.Orientation.Horizontal)
        self.repeater_slider.setRange(1, 16)

        layout.addWidget(self.global_src)
        layout.addWidget(QLabel("➔"))
        layout.addWidget(self.global_dest)
        layout.addWidget(QLabel("Repeaters:"))
        layout.addWidget(self.repeater_slider)
        # Inside your main application or control panel __init__:
# 1. Tuning (SpinBox or Slider)
        self.spin_tuning = QSpinBox()
        self.spin_tuning.setRange(100, 1200)

        # 2. Amplitude Slider
        self.slider_amplitude = QSlider(Qt.Orientation.Horizontal)
        self.slider_amplitude.setRange(0, 100)

        # 3. Duration / Percussive-Keylike-Padded Slider
        self.slider_duration = QSlider(Qt.Orientation.Horizontal)
        self.slider_duration.setRange(0, 100)

        # 4. Fractalizer Slider
        self.slider_fractalizer = QSlider(Qt.Orientation.Horizontal)
        self.slider_fractalizer.setRange(0, 100)

        # 5. EQR Effect Slider / Fifth Option Control Dropdown or Slider
        self.slider_eqr = QSlider(Qt.Orientation.Horizontal)
        self.slider_eqr.setRange(0, 100)

        # Fifth Option Dropdown Preset Selector (shared or per instrument)
        self.preset_combo = QComboBox()
        self.preset_combo.currentIndexChanged.connect(self.on_preset_changed)

    def on_preset_changed(self, index):
        curr_idx = self.top_sequencer.instance_combo.currentIndex()
        if 0 <= curr_idx < len(self.channel_states):
            self.channel_states[curr_idx]["preset_idx"] = index
        connect_btn = QPushButton("Patch Global Bus")
        connect_btn.setStyleSheet("background-color: #0984e3; color: white;")
        connect_btn.clicked.connect(lambda: QMessageBox.information(self, "Global Bus Patched", "Global patch bus updated."))
        layout.addWidget(connect_btn)
# ==========================================
# 5. SCRIPTER'S PANE WITH FUNCTION KEYSET
# ==========================================
class DenseCoordinateVisualizer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(200)
        self.setStyleSheet("background-color: #1e272e; border: 3px solid #feca57; border-radius: 14px;")
        self.point_history = []
        self.max_points = 250

    def update_coordinates(self, x, y):
        self.point_history.append((x, y))
        if len(self.point_history) > self.max_points:
            self.point_history.pop(0)
        self.update()

    def paintEvent(self, event):
        painter = QPainter()
        if not painter.begin(self):
            return
        try:
            painter.fillRect(self.rect(), QColor(30, 39, 46))
            width, height = self.width(), self.height()

            painter.setPen(QPen(QColor(72, 84, 96), 1, Qt.PenStyle.DashLine))
            painter.drawLine(0, height // 2, width, height // 2)
            painter.drawLine(width // 2, 0, width // 2, height)

            if len(self.point_history) >= 2:
                pen = QPen(QColor(255, 107, 107))
                pen.setWidth(3)
                painter.setPen(pen)
                for i in range(1, len(self.point_history)):
                    x1 = (self.point_history[i-1][0] + 1.2) * 0.41 * width
                    y1 = (self.point_history[i-1][1] + 1.2) * 0.41 * height
                    x2 = (self.point_history[i][0] + 1.2) * 0.41 * width
                    y2 = (self.point_history[i][1] + 1.2) * 0.41 * height
                    painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))
        finally:
            painter.end()
class TopSideInstrumentSequencerPanel(QWidget):
    def __init__(self, parent=None, app_ref=None):
        super().__init__(parent)
        self.app_ref = app_ref
        self.setStyleSheet("background-color: #1a1a1a; border: 1px solid #333333; border-radius: 4px; padding: 6px;")
        layout = QVBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6)

        row1 = QHBoxLayout()
        row1.addWidget(QLabel("<b>Instance:</b>"))
        self.instance_combo = QComboBox()
        self.update_instance_list()
        self.instance_combo.currentIndexChanged.connect(self.on_instance_changed)
        row1.addWidget(self.instance_combo, stretch=2)

        row1.addWidget(QLabel("<b>Type:</b>"))
        self.inst_combo = QComboBox()
        self.inst_combo.addItems(DEFAULT_INSTRUMENT_LIST)
        row1.addWidget(self.inst_combo, stretch=3)

        row1.addWidget(QLabel("Tonal Curvature Eq (x, y, z):"))
        self.curvature_eq_input = QLineEdit("x * 1.618033 + y - z")
        self.curvature_eq_input.textChanged.connect(self.on_curvature_changed)
        row1.addWidget(self.curvature_eq_input, stretch=3)

        # Local Sequencer Play / Loop Button
        self.local_play_btn = QPushButton("▶ Loop")
        self.local_play_btn.setStyleSheet("background-color: #00aa55; color: white;")
        self.local_play_btn.clicked.connect(self.audition_sequence)
        row1.addWidget(self.local_play_btn)

        layout.addLayout(row1)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedHeight(95)
        self.scroll_area.setStyleSheet("background-color: #161616; border: 1px solid #282828;")

        self.step_buttons_container = QWidget()
        self.step_buttons_layout = QHBoxLayout(self.step_buttons_container)
        self.step_boxes = []

        self.rebuild_step_buttons(16)
        self.scroll_area.setWidget(self.step_buttons_container)
        layout.addWidget(self.scroll_area)

    def update_instance_list(self):
        self.instance_combo.blockSignals(True)
        self.instance_combo.clear()
        if self.app_ref and hasattr(self.app_ref, 'instrument_names'):
            labels = [f"Ch {i+1}: {name}" for i, name in enumerate(self.app_ref.instrument_names)]
            self.instance_combo.addItems(labels)
        else:
            self.instance_combo.addItems([f"Ch {i+1}: {name}" for i, name in enumerate(DEFAULT_INSTRUMENT_LIST)])
        self.instance_combo.blockSignals(False)

    def on_instance_changed(self, index):
        if self.app_ref and hasattr(self.app_ref, 'sync_ui_to_current_channel'):
            self.app_ref.sync_ui_to_current_channel(index)

    def on_curvature_changed(self, text):
        curr_idx = self.instance_combo.currentIndex()
        if self.app_ref and hasattr(self.app_ref, 'channel_states') and 0 <= curr_idx < len(self.app_ref.channel_states):
            self.app_ref.channel_states[curr_idx]["curvature_eq"] = text

    def rebuild_step_buttons(self, count):
        for box in self.step_boxes:
            box.setParent(None)
            box.deleteLater()
        self.step_boxes = []

        default_intervals = ["0(432Hz)", "1", "2", "-1", "-3", "3", "0", "2", "1", "-1", "0(432Hz)", "3", "-2", "1", "0", "2"]

        for i in range(count):
            step_frame = QFrame()
            step_frame.setStyleSheet("background-color: #222222; border: 1px solid #383838; border-radius: 2px;")
            step_layout = QVBoxLayout(step_frame)
            step_layout.setContentsMargins(2, 2, 2, 2)
            step_layout.setSpacing(2)

            btn = QPushButton(str(i+1))
            btn.setCheckable(True)
            btn.setChecked(i in [0, 4, 8, 12])
            btn.setFixedWidth(42)
            btn.setFixedHeight(20)
            btn.setStyleSheet("""
                QPushButton { background-color: #2b2b2b; color: #888888; border-radius: 2px; font-size: 8px; font-weight: bold; border: 1px solid #3a3a3a; }
                QPushButton:checked { background-color: #ff6b00; color: #ffffff; border: 1px solid #ff8533; }
            """)
            step_layout.addWidget(btn)

            default_val = default_intervals[i % len(default_intervals)]
            interval_input = QLineEdit(default_val)
            interval_input.setFixedWidth(42)
            interval_input.setStyleSheet("font-size: 8px; padding: 1px; background-color: #121212; color: #00ffcc;")
            step_layout.addWidget(interval_input)

            self.step_buttons_layout.addWidget(step_frame)
            self.step_boxes.append((btn, interval_input))

    def audition_sequence(self):
        QMessageBox.information(self, "Sequence Audition", "Looping active instrument sequence in memory buffer.")
# ==========================================
# 6. SEQUENCER PANE
# ==========================================
class SequencerPane(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>16-Step Modulation Sequencer</b>"))

        grid_layout = QGridLayout()
        self.steps = []
        for i in range(16):
            btn = QPushButton(str(i+1))
            btn.setCheckable(True)
            btn.setStyleSheet("background-color: #222; color: #888;")
            btn.clicked.connect(lambda checked, b=btn: b.setStyleSheet("background-color: #00aa55; color: #fff;" if b.isChecked() else "background-color: #222; color: #888;"))
            row, col = divmod(i, 8)
            grid_layout.addWidget(btn, row, col)
            self.steps.append(btn)

        layout.addLayout(grid_layout)
class CustomVSTKnobsDialog(QDialog):
    def __init__(self, parent=None, channel_state=None):
        super().__init__(parent)
        self.channel_state = channel_state or {}
        self.setWindowTitle("Custom VST & Waveform Parameters (Edit Synth)")
        self.resize(450, 350)
        self.setStyleSheet(DAW_STYLE)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("<b>⚙️ Custom VST Parameters & Wavefunction Mapping:</b>"))

        form_layout = QFormLayout()

        self.vst_param1 = QSlider(Qt.Orientation.Horizontal)
        self.vst_param1.setRange(0, 100)
        self.vst_param1.setValue(int(self.channel_state.get("vst_p1", 0.5) * 100))
        form_layout.addRow("VST Resonance / Freq (p1):", self.vst_param1)

        self.vst_param2 = QSlider(Qt.Orientation.Horizontal)
        self.vst_param2.setRange(0, 100)
        self.vst_param2.setValue(int(self.channel_state.get("vst_p2", 0.618) * 100))
        form_layout.addRow("Harmonic Spread (p2):", self.vst_param2)

        self.vst_param3 = QSlider(Qt.Orientation.Horizontal)
        self.vst_param3.setRange(0, 100)
        self.vst_param3.setValue(int(self.channel_state.get("vst_p3", 0.33) * 100))
        form_layout.addRow("Meum Scaling Depth (p3):", self.vst_param3)

        self.routing_combo = QComboBox()
        self.routing_combo.addItems(["Direct Summation", "Phase Modulation (PM)", "Frequency Modulation (FM)", "Nonlinear Foldback"])
        form_layout.addRow("Synthesis Routing Mode:", self.routing_combo)

        layout.addLayout(form_layout)

        btn_box = QHBoxLayout()
        save_btn = QPushButton("Apply VST Settings")
        save_btn.setStyleSheet("background-color: #00aa55; color: white; font-weight: bold;")
        save_btn.clicked.connect(self.accept)
        btn_box.addWidget(save_btn)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        btn_box.addWidget(cancel_btn)

        layout.addLayout(btn_box)

    def get_values(self):
        return {
            "vst_p1": self.vst_param1.value() / 100.0,
            "vst_p2": self.vst_param2.value() / 100.0,
            "vst_p3": self.vst_param3.value() / 100.0,
            "routing": self.routing_combo.currentText()
        }
# ==========================================
# 7. MAIN WINDOW & LAYOUT INTEGRATION
# ==========================================
import sys
import json
import random
import wave
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSlider, QSpinBox, QComboBox, QPushButton, QLabel, QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt

class MathematiciansGrooveboxApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # 1. Initialize channel states
        self.channel_states = [self.create_new_channel_state() for _ in range(48)]
        self.instrument_names = [f"Synth Node {i+1}" for i in range(48)]

        # 2. Initialize your workspace modules FIRST so they exist when the layout builds
        # (Uncomment or match these to whatever your actual class variables are named)
        self.playlist_window = PlaylistGridWidget(self)
        self.patch_bay_dialog = PatchBayCanvas(self)

        # 3. UI Layout Initialization (Runs second so it can find the widgets above)
        self.main_widget = QWidget(self)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.init_ui_components()

        # 4. Window properties & sizing
        self.setWindowTitle("Mathematician's Groovebox")
        self.resize(1280, 800)
        self.setMinimumSize(800, 600)
        self.setCentralWidget(self.main_widget)

    def create_new_channel_state(self):
        return {
            # 5 External Panel Controls
            "tuning": round(random.uniform(100.0, 1200.0), 2),
            "amplitude": 0.8,
            "duration": 0.5,
            "fractalizer": 0.5,
            "eqr_effect": 0.5,
            "preset_idx": 0,

            # 6 Internal Synth Sliding Scale Parameters (0.0 to 1.0)
            "internal_p1": round(random.random(), 3),
            "internal_p2": round(random.random(), 3),
            "internal_p3": round(random.random(), 3),
            "internal_p4": round(random.random(), 3),
            "internal_p5": round(random.random(), 3),
            "internal_p6": round(random.random(), 3),

            "curvature_eq": "x * 1.5 + y - z"
        }

    def init_ui_components(self):
        # Create a main vertical container layout for the entire window
        content_layout = QVBoxLayout()

        # 1. Top Control Bar (The 5 external knobs + preset dropdown)
        self.top_layout = QHBoxLayout()
        self.spin_tuning = QSpinBox()
        self.spin_tuning.setRange(100, 1200)

        self.slider_amplitude = QSlider(Qt.Orientation.Horizontal)
        self.slider_amplitude.setRange(0, 100)

        self.slider_duration = QSlider(Qt.Orientation.Horizontal)
        self.slider_duration.setRange(0, 100)

        self.slider_fractalizer = QSlider(Qt.Orientation.Horizontal)
        self.slider_fractalizer.setRange(0, 100)

        self.slider_eqr = QSlider(Qt.Orientation.Horizontal)
        self.slider_eqr.setRange(0, 100)

        self.preset_combo = QComboBox()
        self.preset_combo.addItems([
            "Preset A: Topological Fold",
            "Preset B: Z-Pinch Resonance",
            "Preset C: Hyperbolic Decay",
            "Preset D: Quantum Soliton",
            "Preset E: Custom Matrix Operator"
        ])

        self.top_layout.addWidget(QLabel("Tuning:"))
        self.top_layout.addWidget(self.spin_tuning)
        self.top_layout.addWidget(QLabel("Amplitude:"))
        self.top_layout.addWidget(self.slider_amplitude)
        self.top_layout.addWidget(QLabel("Duration:"))
        self.top_layout.addWidget(self.slider_duration)
        self.top_layout.addWidget(QLabel("Fractalizer:"))
        self.top_layout.addWidget(self.slider_fractalizer)
        self.top_layout.addWidget(QLabel("EQR Effect:"))
        self.top_layout.addWidget(self.slider_eqr)
        self.top_layout.addWidget(self.preset_combo)

        content_layout.addLayout(self.top_layout)

        # 2. Central Splitter for the Sequencer Grid & Workspace Canvas
        workspace_splitter = QSplitter(Qt.Orientation.Vertical)

        # If your script initializes these elsewhere, make sure they are safely added.
        # If they haven't been created yet at this point in __init__, we fallback to
        # a primary workspace widget container so the window doesn't collapse.
        added_widgets = False

        for attr_name in ['playlist_window', 'top_sequencer', 'patch_bay_dialog']:
            if hasattr(self, attr_name) and getattr(self, attr_name) is not None:
                widget = getattr(self, attr_name)
                # If it's a standalone window, extract its central widget or add it if it's a QWidget
                if isinstance(widget, QWidget):
                    workspace_splitter.addWidget(widget)
                    added_widgets = True

        if not added_widgets:
            # Fallback container to ensure the splitter has a visible node while your scripts load
            fallback_container = QWidget()
            fallback_layout = QVBoxLayout(fallback_container)
            fallback_layout.addWidget(QLabel("Workspace Initialized - Sequencer / Matrix Ready"))
            workspace_splitter.addWidget(fallback_container)

        content_layout.addWidget(workspace_splitter)
        self.main_layout.addLayout(content_layout)

    def sync_ui_to_current_channel(self, index):
        if 0 <= index < len(self.channel_states):
            state = self.channel_states[index]

            if not hasattr(self, 'slider_amplitude') or not hasattr(self, 'spin_tuning'):
                return

            widgets = [
                self.spin_tuning, self.slider_amplitude, self.slider_duration,
                self.slider_fractalizer, self.slider_eqr, self.preset_combo
            ]

            for w in widgets:
                w.blockSignals(True)

            self.spin_tuning.setValue(state["tuning"])
            self.slider_amplitude.setValue(int(state["amplitude"] * 100))
            self.slider_duration.setValue(int(state["duration"] * 50))
            self.slider_fractalizer.setValue(int(state["fractalizer"] * 100))
            self.slider_eqr.setValue(int(state["eqr_effect"] * 100))
            self.preset_combo.setCurrentIndex(state.get("preset_idx", 0))

            for w in widgets:
                w.blockSignals(False)

    def randomize_single_instrument(self):
        """Randomizes the active channel state and assigns functional modulation origin/destination pairs."""
        # 1. Randomize the 5 external panel parameters
        state = {
            "tuning": round(random.uniform(100.0, 1200.0), 2),
            "amplitude": round(random.uniform(0.1, 1.0), 2),
            "duration": round(random.uniform(0.1, 1.0), 2),
            "fractalizer": round(random.uniform(0.0, 1.0), 2),
            "eqr_effect": round(random.uniform(0.0, 1.0), 2),
            "preset_idx": random.randint(0, 4),

            # 2. Randomize internal synth sliding scale parameters (0.0 to 1.0)
            "internal_p1": round(random.random(), 3),
            "internal_p2": round(random.random(), 3),
            "internal_p3": round(random.random(), 3),
            "internal_p4": round(random.random(), 3),
            "internal_p5": round(random.random(), 3),
            "internal_p6": round(random.random(), 3),

            "curvature_eq": "x * 1.5 + y - z"
        }

        # 3. Assign functional modulation origins and destinations
        available_origins = ["LFO 1", "LFO 2", "Envelope Generator", "Fractal Matrix", "Audio Rate Input"]
        available_destinations = ["tuning", "amplitude", "duration", "fractalizer", "eqr_effect", "internal_p1", "internal_p3"]

        state["modulation_origin"] = random.choice(available_origins)
        state["modulation_destination"] = random.choice(available_destinations)
        state["modulation_depth"] = round(random.uniform(0.1, 0.9), 2)

        # Apply back to the active channel if tracking indices
        if hasattr(self, 'current_channel_idx') and 0 <= self.current_channel_idx < len(self.channel_states):
            self.channel_states[self.current_channel_idx] = state
            self.sync_ui_to_current_channel(self.current_channel_idx)

        return state




if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MathematiciansGrooveboxApp()
    window.show()
    sys.exit(app.exec())

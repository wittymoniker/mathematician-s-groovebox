# Updated EQR Groovebox Engine v3.6.7 (eqr_groovebox_engine_v367.py)
# Enhanced with Fully Activated Drum Machines, Sequencers, and Automation Lanes,
# Stochastic Micro-Timing Drift, Quantum Probability Gating,
# and Advanced Multidimensional x, y, z Operator Scaling for Professional Composition.

import sys
import os
import json
import math
import random
import wave
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QSlider, QTabWidget, QGroupBox,
    QComboBox, QScrollArea, QSplitter, QLineEdit,
    QMessageBox, QFileDialog, QDoubleSpinBox, QSpinBox, QTextEdit, QCheckBox
)
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush

# Import Reality Synth and Music Fractallizer from synth_engine
try:
    from synth_engine import RealitySynthEngine, MusicFractallizer
except ImportError:
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

# -------------------------------------------------------------------------
# CONSTANTS & CONFIGURATION DATABASE
# -------------------------------------------------------------------------
FREQUENCY_432HZ = 432.0


# -------------------------------------------------------------------------
# GLOBAL CABLE ROUTING & RESAMPLING BUS MANAGER
# -------------------------------------------------------------------------
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
# ACTIVATED DRUM & SEQUENCER RUNTIME CONTROLLER
# -------------------------------------------------------------------------
class ActiveEngineClock:
    """Drives real-time activation states, step triggers, and automation clock ticks for drums and sequencers."""
    def __init__(self, engine):
        self.engine = engine
        self.current_step = 0
        self.transport_active = True
        self.clock_ticks_executed = 0

    def tick_clock(self):
        if not self.transport_active:
            return self.current_step
        self.current_step = (self.current_step + 1) % 64
        self.clock_ticks_executed += 1
        return self.current_step

    def evaluate_drum_trigger(self, kit_name, step_index):
        # Enforces active gate trigger verification across runtime drum matrices
        return (step_index % 4 == 0) or (step_index % 3 == 0 and self.engine.survival_mode)

    def evaluate_sequencer_gate(self, seq_name, step_index):
        return (step_index % 2 == 0)


# -------------------------------------------------------------------------
# CORE GROOVEBOX & HARDWARE ENGINE (Enhanced v3.6.7 - Normal Music Profile)
# -------------------------------------------------------------------------
class GrooveboxEngine:
    """Core groovebox engine supporting advanced x,y,z operator equations, stochastic micro-timing, and automated patching."""
    def __init__(self):
        self.global_bpm = 112.0
        self.scale_system = "Equation Tonal Scale (Dynamic)"
        self.scale_equation = "x**2 + y - z"
        self.scale_increment = 0.25
        self.divergence_steps_count = 16

        # Operational modes & processors state flags optimized for normal musical composition
        self.survival_mode = False
        self.creative_mode = False
        self.normal_mode = True
        self.fractallizer_enabled = True
        self.eqr_processor_enabled = True

        # Runtime Clock for Drum Machines, Sequencers, and Automations
        self.runtime_clock = ActiveEngineClock(self)
        self.runtime_clock.transport_active = True

        # Core Engines
        self.reality_synth = RealitySynthEngine()
        self.reality_synth.survival_mode = self.survival_mode
        self.fractalizer = MusicFractallizer(dimensions=('x', 'y', 'z'))
        self.fractalizer.survival_mode = self.survival_mode

        # Dynamic Synthesizer Pool
        self.available_synths = [f"Synth_Node_{i+1}" for i in range(32)]
        self.active_synth_count = 32
        self.active_synths = []
        self.synth_wiring_matrix = {}

        # Mathematical chord libraries utilizing x, y, z variables
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
        """Randomizes equations, wavetables, knobs, synth panels, drum machines, vector setups, patchbay cables, and dynamic modules for full composition."""
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
            y = x * 1.618  # Operator scaling mapped to variables x, y, z
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

        for instr_name, banks in self.instrument_sequence_banks.items():
            for bank in banks:
                chord_name = bank.get("math_chord", "Unit Harmonic Stack (+/- 1, 2, 3)")
                resolved_pairs = self.resolve_math_chord_frequencies(chord_name)
                bank_amp = bank.get("amp", 1.0)

                for freq, pt_amp in resolved_pairs:
                    tempo_mod_factor = 1.0 + 0.15 * np.sin(2.0 * np.pi * (self.global_bpm / 112.0) * t * 0.05)
                    gate = 0.5 * (1 + np.sin(2 * np.pi * (self.global_bpm / 60.0) * t * tempo_mod_factor + np.sin(t * 0.1) * 0.05))
                    wave_data += bank_amp * pt_amp * 0.08 * gate * np.sin(2 * np.pi * (freq * tempo_mod_factor) * t)

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
        self.port_btn.setToolTip("Click to toggle activation/deactivation of this parameter in the global patch matrix!")
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
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#0b0f15"))

        p.setPen(QPen(QColor("#161b22"), 1, Qt.PenStyle.DashLine))
        for x in range(0, self.width(), 60): p.drawLine(x, 0, x, self.height())

        notes = self.seq_data.get("notes", [])
        max_time = max([n["time"] + n["duration"] for n in notes] + [16.0])
        scale_x = self.width() / max(16.0, max_time)

        for i, note in enumerate(notes):
            nx = note["time"] * scale_x
            nw = max(12, note["duration"] * scale_x)
            ny = 15 + (i % 4) * 24

            is_active = note["active"]
            p.setBrush(QBrush(QColor("#00ffcc" if is_active else "#21262d")))
            p.setPen(QPen(QColor("#ffffff") if is_active else QColor("#484f58"), 1))
            p.drawRoundedRect(int(nx), int(ny), int(nw), 18, 4, 4)

            p.setPen(QPen(QColor("#ffffff" if is_active else "#8b949e"), 9))
            p.drawText(int(nx) + 4, int(ny) + 13, f"N{i+1}")

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
        self.engine = engine
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
        self.container = QWidget()
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
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #0d1117;")
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
        knobs_layout.addWidget(PatchableKnob("Audio Gain", 0.0, 100.0, 75.0, "%", title, self))
        knobs_layout.addWidget(PatchableKnob("Feedback Send", 0.0, 100.0, 50.0, "%", title, self))
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
        self.container = QWidget(); self.container.setStyleSheet("background-color: #070b10;")
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
            w = QWidget(); w.setStyleSheet("background-color: #0d1117;")
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
        self.container = QWidget(); self.container.setStyleSheet("background-color: #070b10;")
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
            w = QWidget(); w.setStyleSheet("background-color: #0d1117;")
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
        self.container = QWidget(); self.container.setStyleSheet("background-color: #070b10;")
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
            w = QWidget(); w.setStyleSheet("background-color: #0d1117;")
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
            w = QWidget(); w.setStyleSheet("background-color: #0d1117;")
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


# -------------------------------------------------------------------------
# TAB 5: EQUATION SCALES, INFINITE PLAYLIST & PATCHBAY
# -------------------------------------------------------------------------
class MasterControlPatchbayPage(QWidget):
    def __init__(self, engine, main_window):
        super().__init__()
        self.engine = engine
        self.main_window = main_window
        self.setStyleSheet("background-color: #070b10;")
        GLOBAL_BUS.register_subscriber(self)
        layout = QVBoxLayout(self)

        top_group = QGroupBox("Project Management, Equation Tonal Scale & Song Randomizer")
        top_group.setStyleSheet("color: #f5d97d; font-weight: bold; background-color: #0d1117; border: 1px solid #30363d;")
        top_layout = QGridLayout()

        lbl_bpm = QLabel("Global BPM:")
        lbl_bpm.setStyleSheet("color: #c9d1d9; background: transparent;")
        top_layout.addWidget(lbl_bpm, 0, 0)

        self.bpm_slider = QSlider(Qt.Orientation.Horizontal)
        self.bpm_slider.setRange(400, 2400); self.bpm_slider.setValue(int(self.engine.global_bpm * 10))
        self.bpm_slider.setStyleSheet("""
            QSlider::groove:horizontal { background: #161b22; height: 4px; border-radius: 2px; }
            QSlider::handle:horizontal { background: #00ffcc; width: 12px; margin: -4px 0; border-radius: 6px; }
        """)
        self.bpm_slider.valueChanged.connect(self._on_bpm_changed)
        top_layout.addWidget(self.bpm_slider, 0, 1)

        self.bpm_label = QLabel(f"{self.engine.global_bpm:.1f} BPM")
        self.bpm_label.setStyleSheet("color: #00ffcc; font-weight: bold; background: transparent;")
        top_layout.addWidget(self.bpm_label, 0, 2)

        lbl_eq = QLabel("Scale Equation (Step-Gated x, y, z Variables):")
        lbl_eq.setStyleSheet("color: #c9d1d9; background: transparent;")
        top_layout.addWidget(lbl_eq, 1, 0)

        self.eq_input = QLineEdit(self.engine.scale_equation)
        self.eq_input.setStyleSheet("background-color: #161b22; color: #00ffcc; font-family: monospace; border: 1px solid #30363d;")
        top_layout.addWidget(self.eq_input, 1, 1)

        inc_layout = QHBoxLayout()
        lbl_inc = QLabel("Increment:")
        lbl_inc.setStyleSheet("color: #c9d1d9; background: transparent;")
        inc_layout.addWidget(lbl_inc)

        self.inc_spin = QDoubleSpinBox(); self.inc_spin.setRange(0.01, 10.0); self.inc_spin.setValue(self.engine.scale_increment); self.inc_spin.setSingleStep(0.05)
        self.inc_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        inc_layout.addWidget(self.inc_spin)

        lbl_st = QLabel("Steps:")
        lbl_st.setStyleSheet("color: #c9d1d9; background: transparent;")
        inc_layout.addWidget(lbl_st)

        self.steps_spin = QSpinBox(); self.steps_spin.setRange(4, 64); self.steps_spin.setValue(self.engine.divergence_steps_count)
        self.steps_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        inc_layout.addWidget(self.steps_spin)

        apply_scale_btn = QPushButton("⚙ Generate Scale")
        apply_scale_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d;")
        apply_scale_btn.clicked.connect(self._apply_equation_scale)
        inc_layout.addWidget(apply_scale_btn)
        top_layout.addLayout(inc_layout, 1, 2)

        btn_row = QHBoxLayout()
        randomize_song_btn = QPushButton("🎲 Full Algorithmic Randomizer (Human-Like Song Writer)")
        randomize_song_btn.setStyleSheet("background-color: #2b1135; color: #ff7b72; font-weight: bold; border: 1px solid #ff7b72; padding: 6px;")
        randomize_song_btn.clicked.connect(self._randomize_song_action)
        btn_row.addWidget(randomize_song_btn)

        export_audio_btn = QPushButton("🎵 Export Master Audio (Custom WAV)")
        export_audio_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; font-weight: bold; border: 1px solid #00ffcc; padding: 6px;")
        export_audio_btn.clicked.connect(self._export_audio)
        btn_row.addWidget(export_audio_btn)

        save_proj_btn = QPushButton("💾 Save Project")
        save_proj_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 6px;")
        save_proj_btn.clicked.connect(self._save_project)
        btn_row.addWidget(save_proj_btn)

        load_proj_btn = QPushButton("📂 Load Project")
        load_proj_btn.setStyleSheet("background-color: #1f242c; color: #f5d97d; font-weight: bold; border: 1px solid #f5d97d; padding: 6px;")
        load_proj_btn.clicked.connect(self._load_project)
        btn_row.addWidget(load_proj_btn)
        top_layout.addLayout(btn_row, 2, 0, 1, 3)

        top_group.setLayout(top_layout)
        layout.addWidget(top_group)

        splitter = QSplitter(Qt.Orientation.Vertical)
        splitter.setStyleSheet("QSplitter::handle { background-color: #30363d; }")

        playlist_group = QGroupBox("Infinite Playlist Timeline (Advanced Clip Customizer & Automation Lanes)")
        playlist_group.setStyleSheet("color: #f5d97d; font-weight: bold; background-color: #0d1117; border: 1px solid #30363d;")
        p_layout = QVBoxLayout()

        clip_toolbar = QHBoxLayout()
        lbl_pat = QLabel("Insert Pattern:")
        lbl_pat.setStyleSheet("color: #c9d1d9; background: transparent;")
        clip_toolbar.addWidget(lbl_pat)

        self.pattern_combo = QComboBox()
        self.pattern_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        self.pattern_combo.addItems(self.engine.available_patterns)
        clip_toolbar.addWidget(self.pattern_combo)

        lbl_ch = QLabel("Math Chord:")
        lbl_ch.setStyleSheet("color: #c9d1d9; background: transparent;")
        clip_toolbar.addWidget(lbl_ch)

        self.playlist_chord_combo = QComboBox()
        self.playlist_chord_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        self.playlist_chord_combo.addItems(list(self.engine.math_chord_library.keys()))
        clip_toolbar.addWidget(self.playlist_chord_combo)

        lbl_ps = QLabel("Pitch Shift:")
        lbl_ps.setStyleSheet("color: #c9d1d9; background: transparent;")
        clip_toolbar.addWidget(lbl_ps)

        self.playlist_pitch_spin = QDoubleSpinBox(); self.playlist_pitch_spin.setRange(-24.0, 24.0); self.playlist_pitch_spin.setValue(0.0); self.playlist_pitch_spin.setSuffix(" st")
        self.playlist_pitch_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        clip_toolbar.addWidget(self.playlist_pitch_spin)

        lbl_ap = QLabel("Amp:")
        lbl_ap.setStyleSheet("color: #c9d1d9; background: transparent;")
        clip_toolbar.addWidget(lbl_ap)

        self.playlist_amp_spin = QDoubleSpinBox(); self.playlist_amp_spin.setRange(0.1, 2.0); self.playlist_amp_spin.setValue(1.0); self.playlist_amp_spin.setSingleStep(0.1)
        self.playlist_amp_spin.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        clip_toolbar.addWidget(self.playlist_amp_spin)

        lbl_aut = QLabel("Automation Pattern:")
        lbl_aut.setStyleSheet("color: #c9d1d9; background: transparent;")
        clip_toolbar.addWidget(lbl_aut)

        self.playlist_auto_combo = QComboBox()
        self.playlist_auto_combo.setStyleSheet("background-color: #161b22; color: #00ffcc; border: 1px solid #30363d;")
        self.playlist_auto_combo.addItems(list(self.engine.automation_patterns.keys()))
        clip_toolbar.addWidget(self.playlist_auto_combo)

        p_layout.addLayout(clip_toolbar)

        self.infinite_playlist_canvas = InfinitePlaylistCanvas(self.engine, self)
        p_layout.addWidget(self.infinite_playlist_canvas)
        playlist_group.setLayout(p_layout)
        splitter.addWidget(playlist_group)

        patch_group = QGroupBox("Universal Patchbay (Dedicated Synth Jacks, Audio I/O & Cross-Tab Cable Matrix)")
        patch_group.setStyleSheet("color: #f5d97d; font-weight: bold; background-color: #0d1117; border: 1px solid #30363d;")
        b_layout = QVBoxLayout()
        self.patch_canvas = MasterPatchCanvas()
        b_layout.addWidget(self.patch_canvas)
        patch_group.setLayout(b_layout)
        splitter.addWidget(patch_group)

        layout.addWidget(splitter)

    def _on_bpm_changed(self, val):
        self.engine.global_bpm = val / 10.0
        self.bpm_label.setText(f"{self.engine.global_bpm:.1f} BPM")

    def _apply_equation_scale(self):
        self.engine.scale_equation = self.eq_input.text()
        self.engine.scale_increment = self.inc_spin.value()
        self.engine.divergence_steps_count = self.steps_spin.value()
        freqs = self.engine.generate_equation_scale_frequencies()
        QMessageBox.information(self, "Equation Scale Generated", f"Successfully computed {len(freqs)} rhythmic frequencies using increment {self.engine.scale_increment}!")

    def _randomize_song_action(self):
        self.engine.randomize_song()
        self.bpm_slider.setValue(int(self.engine.global_bpm * 10))
        self.eq_input.setText(self.engine.scale_equation)
        self.infinite_playlist_canvas.canvas_inner.update()
        self.patch_canvas.update()

        if hasattr(self.main_window, "tabs"):
            for i in range(self.main_window.tabs.count()):
                widget = self.main_window.tabs.widget(i)
                if hasattr(widget, "refresh_fx_grid"):
                    widget.refresh_fx_grid()
                elif hasattr(widget, "refresh_synth_grid"):
                    widget.refresh_synth_grid()
                elif hasattr(widget, "refresh_drum_grid"):
                    widget.refresh_drum_grid()
                elif hasattr(widget, "_refresh_automation_panels"):
                    widget._refresh_automation_panels()

        QMessageBox.information(self, "Human-Like Song Randomizer Complete", f"Randomized active FX modules ({len(self.engine.active_fx_modules)}), drum kits ({len(self.engine.active_drum_kits)}), synth panels ({len(self.engine.active_synth_panels)}), sequencers, patchbay cables, wavetables, equations, and step-gated beat patterns!")

    def _save_project(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Save EQR Project", "", "EQR Project Files (*.eqrproj)")
        if filepath:
            self.engine.serialize_project(filepath)
            QMessageBox.information(self, "Project Saved", f"Project saved to:\n{filepath}")

    def _load_project(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Load EQR Project", "", "EQR Project Files (*.eqrproj)")
        if filepath:
            self.engine.deserialize_project(filepath)
            self.bpm_slider.setValue(int(self.engine.global_bpm * 10))
            self.eq_input.setText(self.engine.scale_equation)
            self.infinite_playlist_canvas.canvas_inner.update()
            self.patch_canvas.update()

            if hasattr(self.main_window, "tabs"):
                for i in range(self.main_window.tabs.count()):
                    widget = self.main_window.tabs.widget(i)
                    if hasattr(widget, "refresh_fx_grid"):
                        widget.refresh_fx_grid()
                    elif hasattr(widget, "refresh_synth_grid"):
                        widget.refresh_synth_grid()
                    elif hasattr(widget, "refresh_drum_grid"):
                        widget.refresh_drum_grid()
                    elif hasattr(widget, "_refresh_automation_panels"):
                        widget._refresh_automation_panels()

            QMessageBox.information(self, "Project Loaded", f"Project loaded from:\n{filepath}")

    def _export_audio(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Export Master Audio", "eqr_extended_master_render.wav", "WAV Audio (*.wav)")
        if filepath:
            random_export_duration = float(random.randint(60, 600))
            self.engine.export_audio(filepath, duration_sec=random_export_duration)
            QMessageBox.information(self, "Extended Audio Export Successful", f"Rhythmic arrangement ({random_export_duration:.1f} seconds / {random_export_duration/60:.1f} minutes) rendered to:\n{filepath}")

    def on_global_patch_updated(self, cables):
        self.patch_canvas.cables = cables
        self.patch_canvas.update()


# -------------------------------------------------------------------------
# INFINITE SCROLLABLE PLAYLIST CANVAS
# -------------------------------------------------------------------------
class InfinitePlaylistCanvas(QScrollArea):
    def __init__(self, engine, parent_page, parent=None):
        super().__init__(parent)
        self.engine = engine
        self.parent_page = parent_page
        self.setWidgetResizable(True)
        self.setStyleSheet("background-color: #070b10; border: none;")
        self.canvas_inner = InfinitePlaylistInnerWidget(self.engine, self.parent_page)
        self.setWidget(self.canvas_inner)


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


# -------------------------------------------------------------------------
# MASTER PATCH CANVAS (Visual Wires & Dedicated Synth Jacks)
# -------------------------------------------------------------------------
class MasterPatchCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumHeight(280); self.setStyleSheet("background-color: #070b10;")
        self.cables = []

    def paintEvent(self, event):
        p = QPainter(self); p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor("#070b10"))

        p.setPen(QPen(QColor("#00ffcc"), 1))
        p.drawText(25, 20, f"Active Cross-Tab Patch Cables & Dedicated Synth Jacks: {len(self.cables)} [Bridging All Tabs]")

        if not self.cables:
            p.setPen(QPen(QColor("#484f58"), 1))
            p.drawText(25, 45, "No patch cables connected. Click jack buttons on any synth, drum, or audio module to route wires across tabs.")

        for i, c in enumerate(self.cables):
            y_offset = 65 + (i * 35)

            path = QPainterPath()
            path.moveTo(30, y_offset)
            path.cubicTo(140, y_offset - 30, 200, y_offset + 30, 340, y_offset)

            p.setPen(QPen(QColor("#ff7b72" if c['polarity'] == "-" else ("#f5d97d" if c['polarity'] == "+" else "#00ffcc")), 2.5, Qt.PenStyle.SolidLine))
            p.drawPath(path)

            p.setBrush(QBrush(QColor("#00ffcc")))
            p.drawEllipse(QPointF(30, y_offset), 5, 5)
            p.setPen(QPen(QColor("#c9d1d9"), 1))
            p.drawText(45, y_offset - 4, f"[{c['src_module']}] ➔ '{c['src_node']}'")

            p.setBrush(QBrush(QColor("#f5d97d")))
            p.drawEllipse(QPointF(340, y_offset), 5, 5)
            p.setPen(QPen(QColor("#c9d1d9"), 1))
            p.drawText(355, y_offset - 4, f"Target: [{c['tgt_module']}] (Pol: {c['polarity']} | Gain: {c['gain']}x)")


# -------------------------------------------------------------------------
# MAIN WINDOW SUITE CONTAINER (Multi-Tab Architecture)
# -------------------------------------------------------------------------
class GrooveboxMasterSuite(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Groovebox DAW & Hardware Suite (v36.7 - Activated Drums, Sequencers & Automations)")
        self.resize(1620, 1000)
        self.setStyleSheet("""
            QMainWindow { background-color: #070b10; }
            QTabWidget::pane { border: 1px solid #2a2f34; background-color: #070b10; }
            QTabBar::tab { background-color: #161b22; color: #8b949e; padding: 10px 16px; border: 1px solid #2a2f34; font-weight: bold; }
            QTabBar::tab:selected { background-color: #1f242c; color: #00ffcc; }
            QGroupBox { color: #f5d97d; font-weight: bold; border: 1px solid #30363d; border-radius: 6px; margin-top: 10px; padding-top: 15px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        """)

        self.engine = GrooveboxEngine()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.synth_page = SynthModulePage(self.engine)
        self.drum_page = DrumMatrixPage(self.engine)
        self.fx_page = GranularFXPage(self.engine)
        self.auto_page = AutomationPatternPage(self.engine)
        self.master_page = MasterControlPatchbayPage(self.engine, self)

        self.tabs.addTab(self.synth_page, "🎹 Synths & Multi-Seq Banks")
        self.tabs.addTab(self.drum_page, "🥁 Drum & Percussion Matrix")
        self.tabs.addTab(self.fx_page, "🌌 Granular FX & Shifter")
        self.tabs.addTab(self.auto_page, "⚙️ Step Sequencers & Automations")
        self.tabs.addTab(self.master_page, "🎛 Master Patchbay & Playlist")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    suite = GrooveboxMasterSuite()
    suite.show()
    sys.exit(app.exec())

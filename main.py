# Filename: main.py

import sys
import math
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QSlider, QTabWidget, QGroupBox, QComboBox, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, QPointF

from synth_engine import ModularSynthEngine
from gui_workbench import ModularPatchbayCanvas
from eqr_constants import EQR_CONSTANTS, FREQUENCY_432HZ

class PatchableKnob(QWidget):
    """
    A fully interactive control knob with a patch port supporting polarity (+ / - / Neutral)
    and direct local cloning / cross-modulation between instances on the same page.
    """
    def __init__(self, label_text, min_val=0.0, max_val=100.0, default_val=50.0, parent=None):
        super().__init__(parent)
        self.label_text = label_text
        self.current_val = default_val

        layout = QVBoxLayout()
        layout.setContentsMargins(4, 4, 4, 4)

        self.label = QLabel(f"{label_text}: {default_val:.2f}")
        layout.addWidget(self.label)

        control_layout = QHBoxLayout()

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(int(min_val * 100), int(max_val * 100))
        self.slider.setValue(int(default_val * 100))
        self.slider.valueChanged.connect(self._on_slider_changed)
        control_layout.addWidget(self.slider)

        self.polarity_combo = QComboBox()
        self.polarity_combo.addItems(["Neutral", "+ (Positive)", "- (Inverted)"])
        self.polarity_combo.setToolTip("Set local modulation polarity for cross-cloning (+ / - / Neutral)")
        self.polarity_combo.setFixedWidth(95)
        control_layout.addWidget(self.polarity_combo)

        self.port_btn = QPushButton("○")
        self.port_btn.setFixedSize(30, 30)
        self.port_btn.setCheckable(True)
        self.port_btn.setStyleSheet("""
            QPushButton {
                background-color: #161b22;
                color: #8b949e;
                border: 1px solid #30363d;
                border-radius: 15px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:checked {
                background-color: #00ffcc;
                color: #0d1117;
                border: 1px solid #ffffff;
            }
        """)
        self.port_btn.setToolTip("○ Inactive (Black) | ● Active Patched (Green)\n[Scroll] to adjust amount | [Right-Click] Clone/Cross-Modulate")
        self.port_btn.clicked.connect(self._toggle_port_state)
        control_layout.addWidget(self.port_btn)

        layout.addLayout(control_layout)
        self.setLayout(layout)

    def _on_slider_changed(self, value):
        self.current_val = value / 100.0
        self.label.setText(f"{self.label_text}: {self.current_val:.2f}")

    def _toggle_port_state(self, checked):
        if checked:
            self.port_btn.setText("●")
        else:
            self.port_btn.setText("○")

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        current = self.slider.value()
        self.slider.setValue(current + (5 if delta > 0 else -5))

    def contextMenuEvent(self, event):
        pol = self.polarity_combo.currentText()
        factor = -1.0 if "-" in pol else (1.0 if "+" in pol else 0.5)
        modulated_val = max(0.0, self.current_val * (1.0 + (0.1 * factor)))
        self.slider.setValue(int(modulated_val * 100))


class InstrumentRackModule(QGroupBox):
    """A self-contained, clonable and layerable instrument rack unit."""
    def __init__(self, rack_id=1, parent=None):
        super().__init__(f"Instrument Rack Unit #{rack_id} (432Hz Core)")
        self.rack_id = rack_id

        grid = QGridLayout()
        self.knob_pitch = PatchableKnob(f"Pitch #{rack_id}", 100.0, 2000.0, FREQUENCY_432HZ if rack_id == 1 else FREQUENCY_432HZ * 1.618)
        self.knob_cutoff = PatchableKnob(f"Cutoff #{rack_id}", 50.0, 10000.0, 1000.0 * rack_id)
        self.knob_res = PatchableKnob(f"Resonance #{rack_id}", 0.1, 10.0, 1.2)
        self.knob_width = PatchableKnob(f"Wave Width #{rack_id}", 0.0, 1.0, 0.5)

        grid.addWidget(self.knob_pitch, 0, 0)
        grid.addWidget(self.knob_cutoff, 0, 1)
        grid.addWidget(self.knob_res, 1, 0)
        grid.addWidget(self.knob_width, 1, 1)

        self.setLayout(grid)


class GeneratorPage(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.rack_count = 1

        main_layout = QVBoxLayout()
        toolbar = QHBoxLayout()
        self.clone_btn = QPushButton("➕ Clone & Layer New Instrument Rack")
        self.clone_btn.setStyleSheet("background-color: #1f242c; color: #00ffcc; border: 1px solid #00ffcc; font-weight: bold; padding: 6px 12px;")
        self.clone_btn.clicked.connect(self._add_instrument_rack)
        toolbar.addWidget(self.clone_btn)
        toolbar.addStretch()
        main_layout.addLayout(toolbar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.racks_layout = QVBoxLayout(self.scroll_widget)

        self.initial_rack = InstrumentRackModule(rack_id=1)
        self.racks_layout.addWidget(self.initial_rack)
        self.racks_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)
        self.setLayout(main_layout)

    def _add_instrument_rack(self):
        self.rack_count += 1
        new_rack = InstrumentRackModule(rack_id=self.rack_count)
        self.racks_layout.insertWidget(self.racks_layout.count() - 1, new_rack)


class ModularPanePage(QWidget):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        layout = QVBoxLayout()
        group = QGroupBox("Global Modular Patch Bay & Cross-Wire Matrix")
        group_layout = QVBoxLayout()
        self.canvas = ModularPatchbayCanvas(self.engine)
        group_layout.addWidget(self.canvas)
        group.setLayout(group_layout)
        layout.addWidget(group)
        self.setLayout(layout)


class EQRAlgebraicCore:
    """Core mathematical engine for the Equation of Reality framework strictly using x, y, and z variables."""
    @staticmethod
    def evaluate(x: float, y: float, z: float) -> float:
        return (x ** 3) - (1.618 * (y ** 2)) + (0.5 * z) - math.sin(x * y)


class CustomPolynomialKeyboardCurve:
    def __init__(self):
        self.survival_mode = True
        self.creative_mode = False
        self.preset_override = False

    def configure_curve(self):
        print("--- Custom Polynomial Keyboard Curve Setup ---")
        if self.preset_override:
            self.preset_override = False

        print("\nEnter polynomial equations/coefficients for axes (x, y, z):")
        try:
            eq_x = input("Enter polynomial for X (using x, y, z): ").strip()
            eq_y = input("Enter polynomial for Y (using x, y, z): ").strip()
            eq_z = input("Enter polynomial for Z (using x, y, z): ").strip()
        except EOFError:
            eq_x, eq_y, eq_z = "0", "0", "0"

        if not all([eq_x, eq_y, eq_z]):
            print("Warning: One or more axes received empty inputs. Defaulting to baseline.")

        print("\n--- Repetition Range Configuration ---")
        while True:
            try:
                rep_min = float(input("Enter minimum repetition value: "))
                rep_max = float(input("Enter maximum repetition value: "))
                if rep_max < rep_min:
                    print("Maximum must be greater than or equal to minimum. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter numerical values for the repetition range.")

        return {
            "axes": {"x": eq_x, "y": eq_y, "z": eq_z},
            "repetition_range": (rep_min, rep_max),
            "survival_mode": self.survival_mode,
            "creative_mode": self.creative_mode
        }


class PlaylistArrangementEngine:
    def __init__(self, max_tracks: int = 8, max_bars: int = 32):
        self.max_tracks = max_tracks
        self.max_bars = max_bars
        self.playlist_grid = {}

    def assign_pattern(self, track_idx: int, bar_idx: int, pattern_id: int):
        if not (0 <= track_idx < self.max_tracks and 0 <= bar_idx < self.max_bars):
            return False
        self.playlist_grid[(track_idx, bar_idx)] = pattern_id
        return True

    def remove_pattern(self, track_idx: int, bar_idx: int):
        if (track_idx, bar_idx) in self.playlist_grid:
            del self.playlist_grid[(track_idx, bar_idx)]
            return True
        return False

    def render_playlist_view(self):
        print(f"\n--- Playlist Grid View ({self.max_tracks} Tracks x {self.max_bars} Bars) ---")
        for t in range(self.max_tracks):
            row_display = [str(self.playlist_grid.get((t, b), ".")) for b in range(self.max_bars)]
            print(f"Track {t:2d} | " + " ".join(row_display))
        print("-" * (12 + self.max_bars * 2))


class ModularSynthEngine:
    def __init__(self):
        self.core = EQRAlgebraicCore()
        self.curve_handler = CustomPolynomialKeyboardCurve()
        self.playlist_manager = PlaylistArrangementEngine()
        self.active_config = None

    def initialize_system(self):
        self.active_config = self.curve_handler.configure_curve()
        print(f"\nActive Curve Configured -> Axes: {self.active_config['axes']} | Range: {self.active_config['repetition_range']}")
        self.playlist_manager.assign_pattern(0, 0, 1)
        self.playlist_manager.assign_pattern(0, 4, 2)
        self.playlist_manager.assign_pattern(1, 2, 1)
        self.playlist_manager.render_playlist_view()


if __name__ == "__main__":
    synth_system = ModularSynthEngine()
    synth_system.initialize_system()

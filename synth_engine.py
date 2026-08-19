# Filename: synth_engine.py

import math
from eqr_constants import FREQUENCY_432HZ

class ModularSynthEngine:
    """
    Core backend audio and modulation engine for the EQR Groovebox V9 Suite.
    Modes removed; streamlined for clean, low-volume ambient synthesis.
    """
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        class DummyPlaylistManager:
            def __init__(self):
                self.grid = {}
            def assign_pattern(self, t, b, p): self.grid[(t, b)] = p
            def remove_pattern(self, t, b):
                if (t, b) in self.grid: del self.grid[(t, b)]
            def render_playlist_view(self): print("Playlist grid state rendered.")

        self.playlist_manager = DummyPlaylistManager()

    def process_frame(self, x: float, y: float, z: float):
        """Processes real-time audio frame updates using x, y, z parameters safely."""
        self.x = x
        self.y = y
        self.z = z

        # Strict denominator floor and dampening to eliminate infinite gain spikes
        r_sq = (x ** 2) + (y ** 2) + (z ** 2)
        safe_r_sq = max(r_sq, 0.5)
        field_val = (FREQUENCY_432HZ / (16.0 * math.pi * safe_r_sq)) * math.cos(math.sqrt(safe_r_sq))

        return field_val

import numpy as np

class MusicFractallizer:
    def __init__(self, dimensions=('x', 'y', 'z')):
        self.dimensions = dimensions
        self.active_patches = []

    def apply_p_e_operators(self, val, p_weight=0.2, e_weight=2.0):
        # Heavy exponential decay and tight tanh compression to block screeching feedback
        return np.tanh(val * p_weight) * np.exp(-e_weight * abs(val))

    def generate_fractal_stream(self, seed_data):
        stream = {}
        for dim in self.dimensions:
            # Ultra-low amplitude noise injection to prevent harsh audio clipping
            raw_signal = np.random.normal(0, 0.05, size=512) + (seed_data * 0.05)
            processed = self.apply_p_e_operators(raw_signal)
            stream[dim] = processed
        return stream

class RealitySynthEngine:
    def __init__(self):
        self.fractallizer = MusicFractallizer()

    def render_reality_patch(self, base_patch_data):
        signal_stream = self.fractallizer.generate_fractal_stream(base_patch_data)
        output_buffer = {
            coord: sig.tolist() for coord, sig in signal_stream.items()
        }
        return output_buffer

if __name__ == "__main__":
    synth = RealitySynthEngine()
    dummy_patch = np.linspace(-0.1, 0.1, 512)
    active_sequence = synth.render_reality_patch(dummy_patch)
    print("Streamlined Ambient Synth Active. Dimensions locked:", list(active_sequence.keys()))

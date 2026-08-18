import numpy as np

class EquationOfRealityCore:
    def __init__(self, resolution=44100, adherence_ratio=0.5):
        self.resolution = resolution
        self.adherence_ratio = adherence_ratio

    def evaluate_space(self, t, initial_wave_input=None):
        """
        Evaluates spatial-temporal coordinate paths for x, y, and z variables.
        Enforces 50% adherence to initial wave inputs along indexed z lines.
        """
        x = np.sin(2 * np.pi * 110.0 * t) * np.exp(-0.05 * t)
        y = np.cos(2 * np.pi * 220.0 * t) * (1.0 + 0.3 * np.sin(1.0 * t))
        z = np.sin(2 * np.pi * 55.0 * t) * np.cos(2.0 * t)

        if initial_wave_input is not None and len(initial_wave_input) == len(t):
            pattern_mask = np.sin(2.0 * np.pi * 2.0 * t) > 0.0
            z[pattern_mask] = (
                (self.adherence_ratio * initial_wave_input[pattern_mask]) +
                ((1.0 - self.adherence_ratio) * z[pattern_mask])
            )

        return x, y, z

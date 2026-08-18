import numpy as np

class TalentFXEngine:
    """Reverse-engineered hardware DSP engine emulating analog feedback, ladder filters, and granular scatter."""
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def apply_brute_feedback_drive(self, signal, drive_amount=2.8, feedback_gain=0.4):
        saturated = np.tanh(signal * drive_amount)
        feedback_delay = int(self.sample_rate * 0.005)
        feedback_buffer = np.zeros_like(saturated)

        for i in range(feedback_delay, len(saturated)):
            feedback_buffer[i] = saturated[i - feedback_delay] * feedback_gain

        return np.tanh(saturated + feedback_buffer)

    def apply_steiner_ladder_filter(self, signal, cutoff=1600.0, resonance=6.0):
        rc = 1.0 / (cutoff * 2.0 * np.pi)
        dt = 1.0 / self.sample_rate
        alpha = dt / (rc + dt)

        filtered = np.zeros_like(signal)
        prev_val = 0.0

        for i in range(len(signal)):
            res_boost = 1.0 + (resonance * 0.15 * np.sin(i * 0.02))
            raw_sample = signal[i] * res_boost
            prev_val = prev_val + (alpha * (raw_sample - prev_val))
            filtered[i] = prev_val

        return filtered

    def apply_granular_scatter_delay(self, signal, scatter_mix=0.35):
        delay_samples = int(self.sample_rate * 0.125)
        scattered = np.copy(signal)

        for i in range(delay_samples, len(signal)):
            scattered[i] += signal[i - delay_samples] * scatter_mix * np.cos(i * 0.001)

        return scattered

    def process_chain(self, signal, t, drive=2.8, cutoff=1600.0, resonance=6.0, scatter=0.35):
        driven = self.apply_brute_feedback_drive(signal, drive_amount=drive, feedback_gain=0.4)
        filtered = self.apply_steiner_ladder_filter(driven, cutoff=cutoff, resonance=resonance)
        spatialized = self.apply_granular_scatter_delay(filtered, scatter_mix=scatter)
        return spatialized

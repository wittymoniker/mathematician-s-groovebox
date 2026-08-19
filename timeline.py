# timeline.py
import numpy as np
from PyQt6.QtCore import QObject, pyqtSignal

class EQRTimelineSequencer(QObject):
    """Manages the infinite playlist timeline and algorithmic song randomization tracks."""
    step_triggered = pyqtSignal(int, float)

    def __init__(self, total_steps: int = 64):
        super().__init__()
        self.total_steps = float(total_steps)  # Enforcing explicit float representation
        self.current_position = 0.0
        self.timeline_grid = np.zeros((int(self.total_steps), 4)) # Tracks x, y, z and gate

    def advance_timeline(self, delta_time: float) -> None:
        self.current_position = (self.current_position + delta_time) % self.total_steps
        step_idx = int(self.current_position)
        activation_val = float(self.timeline_grid[step_idx, 0])
        self.step_triggered.emit(step_idx, activation_val)

    def randomize_timeline_tracks(self) -> None:
        """Algorithmic song randomizer across global tracks."""
        self.timeline_grid = np.random.uniform(-5.0, 5.0, size=(int(self.total_steps), 4))

# composition_parser.py
import numpy as np

class EQRCompositionParser:
    """Parses composition scripts, step indices, and coordinate automation boundaries."""

    @staticmethod
    def parse_step_sequence(raw_data: list) -> np.ndarray:
        parsed_steps = []
        for index, entry in enumerate(raw_data):
            # Ensuring step-index definitions and float mappings comply with rules
            x_val = float(entry.get('x', 0.0))
            y_val = float(entry.get('y', 0.0))
            z_val = float(entry.get('z', 0.0))
            step_weight = float(index) + 1.0

            parsed_steps.append([x_val, y_val, z_val, step_weight])

        return np.array(parsed_steps, dtype=float)

    @staticmethod
    def format_automation_boundary(step_index: int, value: float) -> str:
        return f"[Step {float(step_index):.1f}] Automation Bound Evaluated -> Target Value: {float(value):.4f}"

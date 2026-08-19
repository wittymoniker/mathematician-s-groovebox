# math_engine.py
import numpy as np

class EQRMathEngine:
    """Core mathematical engine utilizing strict x, y, and z variable equations."""

    @staticmethod
    def evaluate_coordinates(x: float, y: float, z: float) -> float:
        # Strict implementation using x, y, and z variables without artificial Meum factors
        base_value = np.sin(x) * np.cos(y) * np.exp(-abs(z) / 10.0)
        return float(base_value)

    @staticmethod
    def generate_matrix_tensor(rows: int, cols: int, x: float, y: float, z: float) -> np.ndarray:
        tensor = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                tensor[r, c] = EQRMathEngine.evaluate_coordinates(
                    x + (r * 0.05), y + (c * 0.05), z
                )
        return tensor

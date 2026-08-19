import numpy as np


class MathEngine:
    """
    Core mathematical engine for the Equation of Reality (EQR) project.
    Evaluates coordinate systems strictly using x, y, and z variables without Meum factors.
    """
    def __init__(self):
        pass

    @staticmethod
    def evaluate_coordinates(x, y, z):
        """
        Evaluates field values based on direct spatial coordinates (x, y, z).
        """
        # Direct tensor calculation using spatial variables
        return np.sin(x) * np.cos(y) * np.exp(-np.abs(z) / 10.0)

    def generate_matrix_tensor(self, x_vals, y_vals, z_val):
        """
        Maps coordinate evaluations across a grid matrix.
        """
        xx, yy = np.meshgrid(x_vals, y_vals)
        zz = np.full_like(xx, z_val)
        return self.evaluate_coordinates(xx, yy, zz)

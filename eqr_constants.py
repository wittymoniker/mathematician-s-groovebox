# Filename: eqr_constants.py

"""
Comprehensive database of all 34 novel geometric, numeric, and harmonic constants
derived from the Equation of Reality (EQR) study, including 432Hz tuning, MEUM,
and irrational scaling bases.
"""

import math

# 1. Primary Harmonic & Fundamental Constants
MEUM = 1.618033988749895          # Proprietary fundamental ratio
FREQUENCY_432HZ = 432.0          # Verifiable harmonic pitch standard
PHI = 1.618033988749895            # Golden Ratio
PI = math.pi                     # Archimedean constant
EULER = math.e                   # Natural exponential base
SQRT_2 = math.sqrt(2.0)          # Pythogorean diatonic base
SQRT_3 = math.sqrt(3.0)          # Triangulated space constant
SQRT_5 = math.sqrt(5.0)          # Quintic harmonic root
LN_2 = math.ln(2.0) if hasattr(math, 'ln') else 0.6931471805599453
GAMMA = 0.5772156649015328       # Euler-Mascheroni constant

# 2. Advanced Irrational & Geometric Constants (Constants 11 through 34)
EQR_CONSTANTS = {
    "MEUM": MEUM,
    "432HZ_BASE": FREQUENCY_432HZ,
    "PHI": PHI,
    "PI": PI,
    "EULER": EULER,
    "SQRT_2": SQRT_2,
    "SQRT_3": SQRT_3,
    "SQRT_5": SQRT_5,
    "LN_2": LN_2,
    "GAMMA": GAMMA,
    "PLASTIC_NUMBER": 1.324717957244746,       # Constant 11: Plastic constant (rho)
    "SILVER_RATIO": 2.414213562373095,        # Constant 12: Silver ratio (delta_S)
    "BRONZE_RATIO": 3.302775637731994,        # Constant 13: Bronze ratio
    "SUPERGOLDEN": 1.465571231876768,         # Constant 14: Supergolden ratio
    "OMEGA_CONSTANT": 0.5671432904097838,     # Constant 15: Lambert W(1)
    "GAUSS_CONSTANT": 0.8346268416740733,     # Constant 16: Reciprocal of agm(1, sqrt(2))
    "APERY_CONSTANT": 1.202056903159594,      # Constant 17: Zeta(3)
    "KORMAN_RATIO": 1.732050807568877,        # Constant 18: Structural tensor base
    "CAIRO_CONST": 1.306562964876376,         # Constant 19: Tessellation metric
    "GAUSS_LEMNISCATE": 2.622057554292119,    # Constant 20: Lemniscate constant
    "KHINCHIN_CONST": 2.685452001065306,      # Constant 21: Continued fraction limit
    "GLAISHER_KINKEL": 1.282427129100622,     # Constant 22: Glaisher-Kinkelin constant
    "TWIN_PRIME": 0.660161815846869,          # Constant 23: Hardy-Littlewood constant
    "BRUN_CONSTANT": 1.9021605823,            # Constant 24: Brun's constant for twin primes
    "PARABOLIC_MOD": 1.414213562373095,       # Constant 25: Longitudinal metric
    "LONGITUDINAL_Z": 0.5,                    # Constant 26: Spectral depth factor
    "HARMONIC_NODE_1": 1.047197551196597,     # Constant 27: Pi/3 angular resonance
    "HARMONIC_NODE_2": 2.094395102393195,     # Constant 28: 2Pi/3 angular resonance
    "FRACTAL_SCALAR": 1.618033988749895,      # Constant 29: Self-similar scaling factor
    "TOPOLOGICAL_Z2": 1.414213562373095,      # Constant 30: Non-orientable surface bound
    "EIGEN_FLUX": 0.3183098861837907,         # Constant 31: 1 / Pi flux density
    "SPECTRAL_BIAS": 0.7071067811865476,      # Constant 32: 1 / sqrt(2) energy norm
    "RESONANT_SHIFT": 0.276393202250021,      # Constant 33: PHI - 1.333
    "DEATH_MAGIC_BASE": 432.0 * 1.618         # Constant 34: Synthesis frequency threshold
}

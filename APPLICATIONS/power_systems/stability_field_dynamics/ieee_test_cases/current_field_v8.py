import numpy as np


def compute_current_field(field):
    """
    Compute current field I = -grad(V)
    """

    gy, gx = np.gradient(field)

    Ix = -gx
    Iy = -gy

    magnitude = np.sqrt(Ix**2 + Iy**2)

    return Ix, Iy, magnitude


def normalize_field(field):
    fmin = np.min(field)
    fmax = np.max(field)

    if np.isclose(fmax, fmin):
        return np.zeros_like(field)

    return (field - fmin) / (fmax - fmin)

import numpy as np


def compute_curl_field(gx, gy):
    """
    Computes curl (rotation) of the vector field
    curl = d(gy)/dx - d(gx)/dy
    """

    dgy_dx = np.gradient(gy, axis=1)
    dgx_dy = np.gradient(gx, axis=0)

    curl = dgy_dx - dgx_dy

    return curl


def compute_phase_field(gx, gy):
    """
    Compute angle of flow vectors (phase field)
    """

    phase = np.arctan2(gy, gx)

    return phase


def compute_vorticity_strength(curl):
    """
    Magnitude of rotation
    """

    return np.abs(curl)

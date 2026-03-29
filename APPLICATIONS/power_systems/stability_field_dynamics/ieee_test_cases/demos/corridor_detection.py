import numpy as np


def compute_flow_magnitude(u, v):
    return np.sqrt(u**2 + v**2)


def detect_corridors(flow_mag, threshold_quantile=0.8):
    """
    Detect high-flow regions (corridors)

    Parameters:
        flow_mag : 2D array
        threshold_quantile : float

    Returns:
        corridor_mask : 2D boolean array
    """

    threshold = np.quantile(flow_mag, threshold_quantile)
    corridor_mask = flow_mag >= threshold

    return corridor_mask


def detect_spaces(flow_mag, threshold_quantile=0.2):
    """
    Detect low-flow regions (spaces / voids)
    """

    threshold = np.quantile(flow_mag, threshold_quantile)
    space_mask = flow_mag <= threshold

    return space_mask


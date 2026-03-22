import numpy as np


# --------------------------------------------------
# BASIN DETECTION
# --------------------------------------------------

def compute_flow_magnitude(flow_x, flow_y):
    return np.sqrt(flow_x**2 + flow_y**2)


def detect_basins(flow_x, flow_y, threshold=0.2):
    """
    Detects basins where flow magnitude is low
    → candidates for "eye of the storm"
    """

    magnitude = compute_flow_magnitude(flow_x, flow_y)

    basins = np.zeros_like(magnitude)

    for i in range(magnitude.shape[0]):
        for j in range(magnitude.shape[1]):

            if magnitude[i, j] < threshold:
                basins[i, j] = 1

    return basins


# --------------------------------------------------
# BASIN STRENGTH (optional refinement)
# --------------------------------------------------

def compute_basin_strength(flow_x, flow_y):
    """
    Inverse magnitude → stronger basin = lower movement
    """

    magnitude = compute_flow_magnitude(flow_x, flow_y)

    strength = 1.0 / (magnitude + 1e-6)

    return strength

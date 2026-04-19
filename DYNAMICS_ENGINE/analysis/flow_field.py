import numpy as np


# --------------------------------------------------
# FLOW FIELD COMPUTATION
# --------------------------------------------------

def compute_flow_field(phase_grid):
    """
    Computes directional flow based on phase differences
    """

    h, w = phase_grid.shape

    flow_x = np.zeros_like(phase_grid, dtype=float)
    flow_y = np.zeros_like(phase_grid, dtype=float)

    for i in range(1, h - 1):
        for j in range(1, w - 1):

            # central differences
            dx = phase_grid[i, j + 1] - phase_grid[i, j - 1]
            dy = phase_grid[i + 1, j] - phase_grid[i - 1, j]

            flow_x[i, j] = dx
            flow_y[i, j] = dy

    return flow_x, flow_y


# --------------------------------------------------
# NORMALIZATION
# --------------------------------------------------

def normalize_flow(flow_x, flow_y):
    magnitude = np.sqrt(flow_x**2 + flow_y**2) + 1e-8

    return flow_x / magnitude, flow_y / magnitude

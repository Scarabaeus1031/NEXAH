# DISCOVERY_ENGINE/nexah_dynamics_engine/analysis/rotation_detector.py

import numpy as np


def compute_rotation_direction(trajectory):
    """
    Estimate rotation direction of trajectory:
    +1 → counter-clockwise (CCW)
    -1 → clockwise (CW)
    """

    total = 0.0

    for i in range(len(trajectory) - 1):
        x1, y1 = trajectory[i]
        x2, y2 = trajectory[i + 1]

        # 2D cross product (z-component)
        cross = x1 * y2 - y1 * x2
        total += cross

    if total > 0:
        return "CCW"
    elif total < 0:
        return "CW"
    else:
        return "NONE"


def compute_rotation_strength(trajectory):
    """
    How strong is the rotation (magnitude)
    """
    total = 0.0

    for i in range(len(trajectory) - 1):
        x1, y1 = trajectory[i]
        x2, y2 = trajectory[i + 1]

        cross = x1 * y2 - y1 * x2
        total += abs(cross)

    return float(total / len(trajectory))

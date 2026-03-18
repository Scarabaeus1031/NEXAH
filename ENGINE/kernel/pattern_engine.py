"""
NEXAH Pattern Engine
====================

Core generator for rotational symmetry + drift systems.
All demos should import from here.
"""

import numpy as np


def generate_pattern(
        n=7,
        drift_deg=0.0,
        iterations=2000,
        radius=5.0,
        radial_freq=0.02,
        radial_amp=0.3
):

    base_angle = 2 * np.pi / n
    drift = np.deg2rad(drift_deg)

    k = np.arange(iterations)

    theta = k * (base_angle + drift)

    r = radius * (1 - radial_amp + radial_amp * np.cos(k * radial_freq))

    x = r * np.cos(theta)
    y = r * np.sin(theta)

    return x, y


def generate_points(
        n=7,
        drift_deg=0,
        iterations=2000,
        radius=5
):

    x, y = generate_pattern(n, drift_deg, iterations, radius)

    return np.column_stack((x, y))

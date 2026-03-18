"""
NEXAH Resonance Metrics
=======================

Metrics used to analyze symmetry patterns.
"""

import numpy as np


def closure_error(x, y):

    dx = x[-1] - x[0]
    dy = y[-1] - y[0]

    return np.sqrt(dx*dx + dy*dy)


def radial_variance(x, y):

    r = np.sqrt(x*x + y*y)

    return np.var(r)


def angular_irregularity(x, y):

    angles = np.arctan2(y, x)

    diffs = np.diff(angles)

    return np.var(diffs)


def resonance_score(x, y):

    c = closure_error(x, y)
    r = radial_variance(x, y)
    a = angular_irregularity(x, y)

    score = 1 / (1 + c + r + a)

    return score


def compute_metrics(x, y):

    return {

        "closure_error": closure_error(x, y),

        "radial_variance": radial_variance(x, y),

        "angular_irregularity": angular_irregularity(x, y),

        "resonance_score": resonance_score(x, y)

    }

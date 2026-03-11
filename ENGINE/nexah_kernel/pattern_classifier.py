"""
NEXAH Pattern Classifier
========================

Classifies generated patterns.
"""

import numpy as np

from .resonance_metrics import compute_metrics


def classify_pattern(x, y):

    metrics = compute_metrics(x, y)

    c = metrics["closure_error"]
    r = metrics["radial_variance"]
    a = metrics["angular_irregularity"]

    if c < 0.01 and r < 0.05:

        pattern_type = "closed_ring"

    elif r < 0.2 and a < 0.5:

        pattern_type = "flower"

    elif a > 1:

        pattern_type = "chaotic_spiral"

    else:

        pattern_type = "quasi_resonant"

    return {

        "type": pattern_type,
        "metrics": metrics

    }

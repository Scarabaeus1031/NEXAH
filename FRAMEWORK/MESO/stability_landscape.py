import numpy as np


def compute_stability_landscape(regime_map, risk):
    """
    Compute a stability potential landscape.

    Lower potential → more stable
    Higher potential → collapse region
    """

    gradient = risk["risk_gradient"]

    landscape = {}

    for state in regime_map.nodes():

        stability = 1 - gradient[state]

        landscape[state] = {
            "potential": stability,
            "risk_gradient": gradient[state]
        }

    return landscape

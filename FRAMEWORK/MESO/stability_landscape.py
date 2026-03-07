def compute_stability_landscape(regime_map, risk):
    """
    Compute stability potential landscape.
    """

    gradient = risk["risk_gradient"]

    landscape = {}

    # iterate over actual system states
    for state in gradient:

        stability = 1 - gradient[state]

        landscape[state] = {
            "potential": stability,
            "risk_gradient": gradient[state]
        }

    return landscape

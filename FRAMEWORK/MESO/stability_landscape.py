def compute_stability_landscape(regime_map, risk):
    """
    Compute stability potential landscape.
    """

    gradient = risk["risk_gradient"]

    landscape = {}

    # regime_map ist ein dict
    nodes = regime_map["nodes"]

    for state in nodes:

        stability = 1 - gradient[state]

        landscape[state] = {
            "potential": stability,
            "risk_gradient": gradient[state]
        }

    return landscape

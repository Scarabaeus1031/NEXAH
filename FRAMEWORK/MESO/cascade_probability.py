def compute_cascade_probability(regime_map, risk):
    """
    Compute collapse probability for each state.

    The probability is derived from the risk gradient.

    collapse_state      probability = 1
    tipping_point       high probability
    stable_state        low probability
    """

    risk_gradient = risk["risk_gradient"]

    probabilities = {}

    for state, gradient in risk_gradient.items():

        # higher risk gradient → lower collapse probability
        collapse_probability = 1 - gradient

        probabilities[state] = collapse_probability

    return {
        "collapse_probability": probabilities
    }

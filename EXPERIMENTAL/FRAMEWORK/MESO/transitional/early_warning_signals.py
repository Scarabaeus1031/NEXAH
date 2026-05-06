def detect_early_warning_signals(regime_map, risk):
    """
    Detect early warning states in the system.

    Early warning states are defined as states
    that are two steps away from collapse.

    collapse state        risk_distance = 0
    tipping point         risk_distance = 1
    early warning zone    risk_distance = 2

    Returns
    -------
    dict
        {
            "early_warning_states": [...],
            "tipping_points": [...],
            "collapse_states": [...],
            "risk_distance": {...}
        }
    """

    risk_distance = risk["risk_distance"]

    early_warning_states = []
    tipping_points = []
    collapse_states = []

    for state, distance in risk_distance.items():

        if distance == 0:
            collapse_states.append(state)

        elif distance == 1:
            tipping_points.append(state)

        elif distance == 2:
            early_warning_states.append(state)

    return {
        "early_warning_states": early_warning_states,
        "tipping_points": tipping_points,
        "collapse_states": collapse_states,
        "risk_distance": risk_distance
    }

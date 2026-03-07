def detect_tipping_points(regime_map, risk):
    """
    Detect tipping points in the regime structure.

    Current simple criterion:
    - states with risk distance = 1
      are immediate predecessors of collapse states

    Returns:
        {
            "tipping_points": [...],
            "collapse_states": [...],
            "risk_distance": {...}
        }
    """

    collapse_states = set(regime_map.get("collapse_states", []))
    risk_distance = risk["risk_distance"]

    tipping_points = []

    for state, distance in risk_distance.items():
        if distance == 1:
            tipping_points.append(state)

    return {
        "tipping_points": tipping_points,
        "collapse_states": list(collapse_states),
        "risk_distance": risk_distance
    }

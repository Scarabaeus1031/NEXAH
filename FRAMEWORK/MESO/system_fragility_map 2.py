"""
NEXAH MESO Layer

system_fragility_map.py

Compute a fragility map for all system states.
"""


def compute_system_fragility_map(regime_map, risk):
    """
    Compute fragility for each system state.

    Fragility is defined as the inverse of the risk gradient.

    high fragility  -> close to collapse
    low fragility   -> structurally robust

    Parameters
    ----------
    regime_map : dict
        NEXAH regime structure

    risk : dict
        output of MESO risk_geometry

    Returns
    -------
    dict
        {
            "fragility_map": {state: fragility},
            "average_fragility": float,
            "most_fragile_states": [...],
            "least_fragile_states": [...]
        }
    """

    risk_gradient = risk["risk_gradient"]

    fragility_map = {}

    for state, gradient in risk_gradient.items():
        fragility = 1 - gradient
        fragility_map[state] = fragility

    total_fragility = sum(fragility_map.values())
    average_fragility = total_fragility / len(fragility_map) if fragility_map else 0.0

    max_fragility = max(fragility_map.values()) if fragility_map else 0.0
    min_fragility = min(fragility_map.values()) if fragility_map else 0.0

    most_fragile_states = [
        state for state, value in fragility_map.items()
        if value == max_fragility
    ]

    least_fragile_states = [
        state for state, value in fragility_map.items()
        if value == min_fragility
    ]

    return {
        "fragility_map": fragility_map,
        "average_fragility": average_fragility,
        "most_fragile_states": most_fragile_states,
        "least_fragile_states": least_fragile_states
    }

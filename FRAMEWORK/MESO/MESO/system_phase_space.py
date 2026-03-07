"""
NEXAH MESO Layer

system_phase_space.py

Construct a simplified phase space representation
of the system stability landscape.
"""


def compute_system_phase_space(regime_map, risk):
    """
    Compute a phase space representation of system states.

    The phase space assigns each state a potential value
    derived from the risk gradient.

    Parameters
    ----------
    regime_map : dict
        regime graph structure

    risk : dict
        output from risk_geometry

    Returns
    -------
    dict
        {
            "phase_space": {
                state: {
                    "potential": float,
                    "risk_gradient": float
                }
            },
            "stable_states": [...],
            "unstable_states": [...],
            "collapse_states": [...]
        }
    """

    risk_gradient = risk["risk_gradient"]

    phase_space = {}

    stable_states = []
    unstable_states = []

    collapse_states = list(risk.get("collapse_states", []))

    for state, gradient in risk_gradient.items():

        potential = 1 - gradient

        phase_space[state] = {
            "potential": potential,
            "risk_gradient": gradient
        }

        if gradient > 0.66:
            stable_states.append(state)

        elif gradient < 0.33:
            unstable_states.append(state)

    return {
        "phase_space": phase_space,
        "stable_states": stable_states,
        "unstable_states": unstable_states,
        "collapse_states": collapse_states
    }

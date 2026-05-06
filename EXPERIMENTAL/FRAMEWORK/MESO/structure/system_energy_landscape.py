"""
NEXAH MESO Layer

system_energy_landscape.py

Construct a system energy landscape based on risk gradients.
"""


def compute_system_energy_landscape(regime_map, risk):
    """
    Compute an energy landscape for the system.

    Lower energy = more stable state
    Higher energy = unstable or collapse state

    Parameters
    ----------
    regime_map : dict
        regime graph structure

    risk : dict
        output of risk_geometry

    Returns
    -------
    dict
        {
            "energy_landscape": {
                state: {
                    "energy": float,
                    "risk_gradient": float
                }
            },
            "energy_minima": [...],
            "energy_maxima": [...]
        }
    """

    risk_gradient = risk["risk_gradient"]

    energy_landscape = {}

    for state, gradient in risk_gradient.items():

        energy = 1 - gradient

        energy_landscape[state] = {
            "energy": energy,
            "risk_gradient": gradient
        }

    energies = [v["energy"] for v in energy_landscape.values()]

    min_energy = min(energies)
    max_energy = max(energies)

    energy_minima = [
        state for state, v in energy_landscape.items()
        if v["energy"] == min_energy
    ]

    energy_maxima = [
        state for state, v in energy_landscape.items()
        if v["energy"] == max_energy
    ]

    return {
        "energy_landscape": energy_landscape,
        "energy_minima": energy_minima,
        "energy_maxima": energy_maxima
    }

"""
NEXAH MESO Layer

resilience_score.py

Compute a resilience score for the entire system.
"""


def compute_resilience_score(regime_map, risk):
    """
    Compute system resilience based on the risk geometry.

    The resilience score reflects how far the system
    is from collapse on average.

    Parameters
    ----------
    regime_map : dict
        regime structure containing the system graph

    risk : dict
        output of MESO risk_geometry

    Returns
    -------
    dict
        {
            "resilience_score": float,
            "average_risk_gradient": float,
            "system_size": int
        }
    """

    risk_gradient = risk["risk_gradient"]

    system_size = len(risk_gradient)

    total_gradient = 0.0

    for gradient in risk_gradient.values():
        total_gradient += gradient

    average_gradient = total_gradient / system_size

    resilience_score = average_gradient

    return {
        "resilience_score": resilience_score,
        "average_risk_gradient": average_gradient,
        "system_size": system_size
    }

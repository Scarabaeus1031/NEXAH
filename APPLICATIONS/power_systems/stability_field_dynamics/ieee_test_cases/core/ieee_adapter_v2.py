# ieee_adapter.py (V2)

import numpy as np


def map_ieee_to_nexah(data):
    """
    Improved physical mapping IEEE → NEXAH

    Expected input:
    {
        "voltage_magnitude": array,
        "voltage_angle": array,
        "p_mismatch": array,
        "q_mismatch": array
    }
    """

    V = np.array(data["voltage_magnitude"])
    theta = np.array(data["voltage_angle"])
    P = np.array(data["p_mismatch"])
    Q = np.array(data["q_mismatch"])

    # --- C: FIELD INTENSITY (SPREAD, NOT MEAN) ---
    C = np.std(V)  # critical: reacts to instability

    # --- θ: ORIENTATION ---
    theta_mean = np.mean(theta)
    theta_spread = np.std(theta)

    # --- LOOPS: FLOW + IMBALANCE ---
    loop_P = np.sum(np.abs(P))
    loop_Q = np.sum(np.abs(Q))

    loops = loop_P + loop_Q

    # --- OPTIONAL: STRUCTURAL FEATURES ---
    stress = np.var(V) + np.var(theta)

    return {
        "C": C,
        "theta": theta_mean,
        "theta_spread": theta_spread,
        "loops": loops,
        "stress": stress
    }

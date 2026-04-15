# ieee_adapter.py

import numpy as np


def map_ieee_to_nexah(data):
    """
    Maps IEEE system variables to NEXAH representation.

    Expected input (per timestep or state):
    {
        "voltage_magnitude": array,
        "voltage_angle": array,
        "power_mismatch": array
    }
    """

    V = data["voltage_magnitude"]
    theta = data["voltage_angle"]
    mismatch = data["power_mismatch"]

    # --- MAPPING ---
    C = np.mean(V)                    # field intensity proxy
    theta_mean = np.mean(theta)       # orientation
    loops = np.sum(np.abs(mismatch))  # system imbalance

    return {
        "C": C,
        "theta": theta_mean,
        "loops": loops
    }

import numpy as np


# =========================================
# 1. RISK FIELD
# =========================================

def compute_collapse_risk(distance, d2c, labels, core_cluster=0):
    """
    Continuous collapse risk ∈ [0,1]
    """

    # normalize components
    d_norm = distance / (np.nanmax(distance) + 1e-8)
    d2c_norm = np.abs(d2c) / (np.nanmax(np.abs(d2c)) + 1e-8)

    cluster_risk = (labels != core_cluster).astype(float)

    # combine
    risk = 0.4 * d_norm + 0.4 * d2c_norm + 0.2 * cluster_risk

    return np.clip(risk, 0, 1)


# =========================================
# 2. EARLY WARNING
# =========================================

def detect_early_warning(risk, window=5, threshold=0.6):
    """
    Detect rising risk trend
    """

    warnings = np.zeros_like(risk, dtype=bool)

    for i in range(window, len(risk)):
        trend = np.mean(risk[i-window:i])

        if trend > threshold:
            warnings[i] = True

    return warnings


# =========================================
# 3. TIME-TO-COLLAPSE
# =========================================

def estimate_time_to_collapse(risk):
    """
    Estimate steps until collapse based on slope
    """

    ttc = np.full_like(risk, np.nan)

    for i in range(len(risk)-5):
        slope = np.mean(np.diff(risk[i:i+5]))

        if slope > 0:
            ttc[i] = (1 - risk[i]) / (slope + 1e-6)

    return ttc


# =========================================
# 4. MAIN WRAPPER
# =========================================

def run_predictor(distance, d2c, labels, core_cluster=0):
    risk = compute_collapse_risk(distance, d2c, labels, core_cluster)

    warnings = detect_early_warning(risk)

    ttc = estimate_time_to_collapse(risk)

    return {
        "risk": risk,
        "warnings": warnings,
        "time_to_collapse": ttc
    }

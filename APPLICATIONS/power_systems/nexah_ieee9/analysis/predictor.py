import numpy as np


# =========================================
# HELPERS
# =========================================

def normalize(x):
    xmin = np.nanmin(x)
    xmax = np.nanmax(x)
    return (x - xmin) / (xmax - xmin + 1e-8)


# =========================================
# 1. RISK FIELD
# =========================================

def compute_collapse_risk(distance, d2c, labels, core_cluster=0):

    d_norm = normalize(distance)
    d2c_norm = normalize(np.abs(d2c))

    cluster_risk = np.zeros_like(labels, dtype=float)
    cluster_risk[labels == -1] = 1.0
    cluster_risk[labels != core_cluster] = 0.6
    cluster_risk[labels == core_cluster] = 0.0

    risk = 0.4 * d_norm + 0.4 * d2c_norm + 0.2 * cluster_risk

    return np.clip(risk, 0, 1)


# =========================================
# 2. EARLY WARNING
# =========================================

def detect_early_warning(risk, window=5, threshold=0.6):

    warnings = np.zeros_like(risk, dtype=bool)

    for i in range(window, len(risk)):

        segment = risk[i-window:i]

        if not np.all(np.isfinite(segment)):
            continue

        trend = np.mean(segment)
        slope = np.mean(np.diff(segment))

        if trend > threshold or slope > 0.05:
            warnings[i] = True

    return warnings


# =========================================
# 3. TIME-TO-COLLAPSE
# =========================================

def estimate_time_to_collapse(risk):

    ttc = np.full_like(risk, np.nan)

    for i in range(len(risk) - 5):

        segment = risk[i:i+5]

        if not np.all(np.isfinite(segment)):
            continue

        slope = np.polyfit(range(5), segment, 1)[0]

        if slope > 0.01:
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

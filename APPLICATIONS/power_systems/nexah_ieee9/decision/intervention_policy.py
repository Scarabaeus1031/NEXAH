import numpy as np


# =========================================
# 1. RISK SLOPE
# =========================================

def compute_risk_slope(risk, window=5):
    slope = np.zeros_like(risk)

    for i in range(window, len(risk)):
        slope[i] = np.mean(np.diff(risk[i-window:i]))

    return slope


# =========================================
# 2. POLICY LOGIC
# =========================================

def decide_intervention(
    risk,
    warnings,
    ttc,
    states,
    slope=None
):
    """
    Core intervention policy

    Returns:
        actions: list of actions per timestep
        signal: continuous intervention strength [0,1]
    """

    n = len(risk)

    actions = []
    signal = np.zeros(n)

    # compute slope if not given
    if slope is None:
        slope = compute_risk_slope(risk)

    for i in range(n):

        r = risk[i]
        w = warnings[i]
        s = states[i]
        sl = slope[i]
        t = ttc[i]

        # =====================================
        # HARD COLLAPSE
        # =====================================
        if s == "COLLAPSED":
            actions.append("NONE")
            signal[i] = 0.0
            continue

        # =====================================
        # EARLY INTERVENTION (KEY UPGRADE)
        # =====================================
        if r > 0.6 and sl > 0:
            actions.append("EMERGENCY_SHED")
            signal[i] = 1.0
            continue

        # =====================================
        # WARNING PHASE
        # =====================================
        if w or s == "WARNING":
            actions.append("REDUCE_LOAD")
            signal[i] = 0.6
            continue

        # =====================================
        # CRITICAL PHASE
        # =====================================
        if s == "CRITICAL":
            actions.append("EMERGENCY_SHED")
            signal[i] = 0.9
            continue

        # =====================================
        # TTC-based intervention (optional layer)
        # =====================================
        if np.isfinite(t) and t < 10:
            actions.append("PREEMPTIVE_STABILIZE")
            signal[i] = 0.7
            continue

        # =====================================
        # SAFE
        # =====================================
        actions.append("STABILIZE")
        signal[i] = 0.3

    return actions, signal


# =========================================
# 3. WRAPPER
# =========================================

def run_intervention_policy(risk, warnings, ttc, states):
    actions, signal = decide_intervention(
        risk,
        warnings,
        ttc,
        states
    )

    return {
        "actions": actions,
        "signal": signal
    }

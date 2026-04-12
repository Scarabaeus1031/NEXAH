import numpy as np


# =========================================
# 1. INTERVENTION SIGNAL
# =========================================

def compute_intervention_signal(risk, ttc, warnings):
    """
    Continuous intervention intensity ∈ [0,1]
    """

    signal = np.zeros_like(risk)

    for i in range(len(risk)):

        if not np.isfinite(risk[i]):
            continue

        # base from risk
        s = risk[i]

        # boost if warning
        if warnings[i]:
            s += 0.2

        # boost if time-to-collapse is short
        if np.isfinite(ttc[i]):
            if ttc[i] < 10:
                s += 0.3
            elif ttc[i] < 20:
                s += 0.15

        signal[i] = s

    return np.clip(signal, 0, 1)


# =========================================
# 2. ACTION POLICY
# =========================================

def map_signal_to_action(signal):
    """
    Discrete control actions
    """

    actions = []

    for s in signal:

        if s < 0.3:
            actions.append("NONE")

        elif s < 0.6:
            actions.append("STABILIZE")

        elif s < 0.8:
            actions.append("REDUCE_LOAD")

        else:
            actions.append("EMERGENCY_SHED")

    return actions


# =========================================
# 3. MAIN WRAPPER
# =========================================

def run_intervention(risk, ttc, warnings):

    signal = compute_intervention_signal(risk, ttc, warnings)

    actions = map_signal_to_action(signal)

    return {
        "signal": signal,
        "actions": actions
    }

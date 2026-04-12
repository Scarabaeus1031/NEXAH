import numpy as np


# =========================================
# HELPERS
# =========================================

def moving_average(x, window=5):
    x = np.asarray(x, dtype=float)
    out = np.copy(x)

    for i in range(len(x)):
        start = max(0, i - window + 1)
        seg = x[start:i + 1]
        finite = np.isfinite(seg)

        if np.any(finite):
            out[i] = np.mean(seg[finite])
        else:
            out[i] = np.nan

    return out


def compute_risk_slope(risk, window=5):
    risk = np.asarray(risk, dtype=float)
    slope = np.zeros_like(risk)

    for i in range(window, len(risk)):
        seg = risk[i - window:i]

        if np.all(np.isfinite(seg)):
            slope[i] = np.polyfit(np.arange(len(seg)), seg, 1)[0]

    return slope


def normalize_ttc(ttc, horizon=20.0):
    """
    Maps TTC to urgency in [0,1]
    small TTC -> high urgency
    large TTC / nan -> low urgency
    """
    ttc = np.asarray(ttc, dtype=float)
    urgency = np.zeros_like(ttc)

    finite = np.isfinite(ttc)
    urgency[finite] = 1.0 - np.clip(ttc[finite] / horizon, 0.0, 1.0)

    return urgency


# =========================================
# POLICY CORE
# =========================================

def compute_policy_signal(risk, warnings, ttc, states):
    """
    Continuous control signal in [0,1]
    built from:
    - smoothed risk
    - risk slope
    - TTC urgency
    - state escalation
    """
    risk = np.asarray(risk, dtype=float)
    warnings = np.asarray(warnings, dtype=bool)
    ttc = np.asarray(ttc, dtype=float)

    risk_smooth = moving_average(risk, window=5)
    slope = compute_risk_slope(risk_smooth, window=5)
    ttc_urgency = normalize_ttc(ttc, horizon=20.0)

    signal = np.zeros_like(risk_smooth)

    for i in range(len(signal)):
        s = 0.0

        # 1) base risk
        if np.isfinite(risk_smooth[i]):
            s += 0.45 * risk_smooth[i]

        # 2) rising trend
        if slope[i] > 0:
            s += 0.25 * min(slope[i] * 8.0, 1.0)

        # 3) TTC urgency
        s += 0.20 * ttc_urgency[i]

        # 4) warning flag
        if warnings[i]:
            s += 0.10

        # 5) state escalation
        state = states[i]
        if state == "WARNING":
            s += 0.10
        elif state == "CRITICAL":
            s += 0.25
        elif state == "COLLAPSED":
            s = 0.0

        signal[i] = np.clip(s, 0.0, 1.0)

    return signal, risk_smooth, slope, ttc_urgency


def apply_persistence_gate(signal, states, persist_window=3):
    """
    Prevents noisy one-step spikes from triggering hard action.
    Only escalate if high signal persists.
    """
    signal = np.asarray(signal, dtype=float)
    gated = np.copy(signal)

    for i in range(len(signal)):
        start = max(0, i - persist_window + 1)
        seg = signal[start:i + 1]

        if np.mean(seg) < 0.55 and signal[i] > 0.8 and states[i] != "CRITICAL":
            gated[i] = 0.65

        if states[i] == "COLLAPSED":
            gated[i] = 0.0

    return gated


def map_signal_to_action(signal, states, ttc):
    """
    Final action mapping.
    Conservative escalation:
    STABILIZE -> PREEMPTIVE_STABILIZE -> REDUCE_LOAD -> EMERGENCY_SHED
    """
    actions = []

    for i, s in enumerate(signal):
        state = states[i]
        t = ttc[i]

        if state == "COLLAPSED":
            actions.append("NONE")
            continue

        if state == "CRITICAL" and np.isfinite(t) and t < 5 and s >= 0.8:
            actions.append("EMERGENCY_SHED")
            continue

        if s >= 0.65:
            actions.append("REDUCE_LOAD")
            continue

        if s >= 0.40:
            actions.append("PREEMPTIVE_STABILIZE")
            continue

        actions.append("STABILIZE")

    return actions


# =========================================
# WRAPPER
# =========================================

def run_intervention_policy(risk, warnings, ttc, states):
    raw_signal, risk_smooth, slope, ttc_urgency = compute_policy_signal(
        risk, warnings, ttc, states
    )

    signal = apply_persistence_gate(raw_signal, states, persist_window=3)
    actions = map_signal_to_action(signal, states, ttc)

    return {
        "actions": actions,
        "signal": signal,
        "raw_signal": raw_signal,
        "risk_smooth": risk_smooth,
        "slope": slope,
        "ttc_urgency": ttc_urgency,
    }

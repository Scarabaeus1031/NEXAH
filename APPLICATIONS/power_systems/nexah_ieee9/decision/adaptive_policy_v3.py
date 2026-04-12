# =========================================
# ADAPTIVE POLICY LAYER v3
# PRE-EMPTIVE FIELD CONTROL
# =========================================

import numpy as np


# =========================================
# HELPER
# =========================================

def _finite(x, default=0.0):
    if x is None:
        return float(default)
    try:
        x = float(x)
    except Exception:
        return float(default)
    if not np.isfinite(x):
        return float(default)
    return float(x)


# =========================================
# RECOVERY / SAFETY CORE
# =========================================

def enforce_recovery(action, state, state_history, risk_value):
    """
    Hard safety wrapper.
    Guarantees active recovery in unstable regimes.
    """

    risk_value = _finite(risk_value, 0.0)

    recent = state_history[-5:] if len(state_history) >= 5 else state_history

    collapsed_count = recent.count("COLLAPSED")
    critical_count = recent.count("CRITICAL")

    # -------------------------------------
    # 1. ACTIVE COLLAPSE RECOVERY
    # -------------------------------------
    if state == "COLLAPSED":
        if collapsed_count >= 3:
            return "EMERGENCY_SHED"
        elif collapsed_count == 2:
            return "REDUCE_LOAD"
        else:
            return "PREEMPTIVE_STABILIZE"

    # -------------------------------------
    # 2. CRITICAL ESCALATION
    # -------------------------------------
    if critical_count >= 4:
        return "REDUCE_LOAD"

    if critical_count >= 2 and action in ["NONE", "STABILIZE"]:
        return "PREEMPTIVE_STABILIZE"

    # -------------------------------------
    # 3. RISK-BASED GUARDRAILS
    # -------------------------------------
    if risk_value >= 0.70 and action == "NONE":
        return "REDUCE_LOAD"

    if risk_value >= 0.45 and action == "NONE":
        return "STABILIZE"

    return action


# =========================================
# TRAJECTORY ADAPTATION
# =========================================

def adaptive_override(action, state, risk_value, risk_slope):
    """
    Soft control layer based on trajectory.
    """

    risk_value = _finite(risk_value, 0.0)
    risk_slope = _finite(risk_slope, 0.0)

    if state == "COLLAPSED":
        return "EMERGENCY_SHED"

    # -------------------------------------
    # CRITICAL dynamics
    # -------------------------------------
    if state == "CRITICAL":
        if risk_slope > 0.03:
            return "REDUCE_LOAD"

        if risk_slope > 0.01 and action in ["NONE", "STABILIZE"]:
            return "PREEMPTIVE_STABILIZE"

    # -------------------------------------
    # WARNING dynamics
    # -------------------------------------
    if state == "WARNING":
        if risk_slope > 0.04:
            return "PREEMPTIVE_STABILIZE"

        if risk_slope > 0.02 and action == "NONE":
            return "STABILIZE"

    # -------------------------------------
    # SAFE but rising risk
    # -------------------------------------
    if state == "SAFE":
        if risk_slope > 0.05:
            return "PREEMPTIVE_STABILIZE"

    return action


# =========================================
# MEMORY-BASED ESCALATION
# =========================================

def memory_escalation(action, state_history):
    """
    Adds persistence-aware escalation.
    """

    if len(state_history) < 10:
        return action

    recent = state_history[-10:]

    instability = (
        recent.count("CRITICAL")
        + recent.count("WARNING")
        + 2 * recent.count("COLLAPSED")
    )

    if instability >= 12:
        return "EMERGENCY_SHED"

    if instability >= 8 and action in ["NONE", "STABILIZE"]:
        return "REDUCE_LOAD"

    return action


# =========================================
# PRE-EMPTIVE FIELD CONTROL (NEW CORE)
# =========================================

def preemptive_field_control(
    action,
    state,
    risk_value,
    risk_slope,
    curvature_value,
    distance_value,
):
    """
    New v3 layer:
    Uses field geometry BEFORE formal collapse.
    """

    risk_value = _finite(risk_value, 0.0)
    risk_slope = _finite(risk_slope, 0.0)
    curvature_value = abs(_finite(curvature_value, 0.0))
    distance_value = _finite(distance_value, 0.0)

    # -------------------------------------
    # 1. HARD PRE-COLLAPSE ENVELOPE
    # -------------------------------------
    if risk_value >= 0.80:
        return "EMERGENCY_SHED"

    if risk_value >= 0.60 and risk_slope > 0.015:
        return "REDUCE_LOAD"

    # -------------------------------------
    # 2. CURVATURE TRIGGER
    # Large second derivative = approaching structural rupture
    # -------------------------------------
    if curvature_value >= 120:
        return "EMERGENCY_SHED"

    if curvature_value >= 60:
        return "REDUCE_LOAD"

    if curvature_value >= 20 and action in ["NONE", "STABILIZE"]:
        return "PREEMPTIVE_STABILIZE"

    # -------------------------------------
    # 3. DISTANCE-TO-RIFT TRIGGER
    # Higher distance can indicate deviation into unstable field
    # -------------------------------------
    if distance_value >= 5.0:
        return "EMERGENCY_SHED"

    if distance_value >= 2.5:
        return "REDUCE_LOAD"

    if distance_value >= 1.0 and action == "NONE":
        return "PREEMPTIVE_STABILIZE"

    # -------------------------------------
    # 4. STATE-AWARE EARLY INTERVENTION
    # -------------------------------------
    if state == "WARNING":
        if risk_slope > 0.01 or curvature_value > 10:
            return "PREEMPTIVE_STABILIZE"

    if state == "SAFE":
        if risk_value > 0.35 and risk_slope > 0.01:
            return "PREEMPTIVE_STABILIZE"

    return action


# =========================================
# MAIN ENTRY
# =========================================

def run_adaptive_policy(
    base_action,
    state,
    state_history,
    risk_value,
    risk_slope,
    curvature_value=0.0,
    distance_value=0.0,
):
    """
    Full adaptive control pipeline v3.
    Order matters:
    1. trajectory adaptation
    2. recovery
    3. memory escalation
    4. pre-emptive field control
    """

    action = adaptive_override(base_action, state, risk_value, risk_slope)

    action = enforce_recovery(action, state, state_history, risk_value)

    action = memory_escalation(action, state_history)

    action = preemptive_field_control(
        action=action,
        state=state,
        risk_value=risk_value,
        risk_slope=risk_slope,
        curvature_value=curvature_value,
        distance_value=distance_value,
    )

    return action

# =========================================
# ADAPTIVE POLICY LAYER
# =========================================

import numpy as np


def enforce_recovery(action, state, state_history, risk_value):
    """
    Hard safety wrapper around the base policy.
    Prevents passive behavior during collapse / near-collapse.
    """

    recent = state_history[-5:] if len(state_history) >= 5 else state_history
    collapsed_count = recent.count("COLLAPSED")
    critical_count = recent.count("CRITICAL")

    # 1. Never do nothing while collapsed
    if state == "COLLAPSED":
        return "EMERGENCY_SHED"

    # 2. Strong recovery if repeated collapse / critical episodes
    if collapsed_count >= 2:
        return "EMERGENCY_SHED"

    if critical_count >= 4:
        return "REDUCE_LOAD"

    # 3. If risk is high, do not allow NONE
    if risk_value >= 0.7 and action == "NONE":
        return "PREEMPTIVE_STABILIZE"

    # 4. If risk is moderate, avoid passivity
    if risk_value >= 0.45 and action == "NONE":
        return "STABILIZE"

    return action


def adaptive_override(action, state, risk_value, risk_slope):
    """
    Soft adaptation layer.
    Escalates actions if the trajectory is worsening quickly.
    """

    if state == "COLLAPSED":
        return "EMERGENCY_SHED"

    # rising risk in critical regime
    if state == "CRITICAL" and risk_slope > 0.02:
        if action in ["NONE", "STABILIZE"]:
            return "REDUCE_LOAD"

    # rising risk in warning regime
    if state == "WARNING" and risk_slope > 0.03:
        if action == "NONE":
            return "STABILIZE"

    return action


def run_adaptive_policy(base_action, state, state_history, risk_value, risk_slope):
    """
    Final adaptive policy wrapper.
    """
    action = adaptive_override(base_action, state, risk_value, risk_slope)
    action = enforce_recovery(action, state, state_history, risk_value)
    return action

# =========================================
# ADAPTIVE POLICY LAYER v2 (RECOVERY + MEMORY)
# =========================================

import numpy as np


# =========================================
# RECOVERY / SAFETY CORE
# =========================================

def enforce_recovery(action, state, state_history, risk_value):
    """
    Hard safety wrapper.
    Guarantees active recovery in unstable regimes.
    """

    recent = state_history[-5:] if len(state_history) >= 5 else state_history

    collapsed_count = recent.count("COLLAPSED")
    critical_count = recent.count("CRITICAL")

    # -------------------------------------
    # 1. ACTIVE COLLAPSE RECOVERY (NEW)
    # -------------------------------------
    if state == "COLLAPSED":

        # escalating recovery strategy
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

    if critical_count >= 2:
        if action in ["NONE", "STABILIZE"]:
            return "PREEMPTIVE_STABILIZE"

    # -------------------------------------
    # 3. RISK-BASED GUARDRAILS
    # -------------------------------------
    if risk_value >= 0.7:
        if action == "NONE":
            return "REDUCE_LOAD"

    if risk_value >= 0.45:
        if action == "NONE":
            return "STABILIZE"

    return action


# =========================================
# TRAJECTORY ADAPTATION
# =========================================

def adaptive_override(action, state, risk_value, risk_slope):
    """
    Soft control layer based on trajectory.
    """

    # -------------------------------------
    # COLLAPSE always forces action
    # -------------------------------------
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
    # SAFE but rising risk (NEW)
    # -------------------------------------
    if state == "SAFE":

        if risk_slope > 0.05:
            return "PREEMPTIVE_STABILIZE"

    return action


# =========================================
# MEMORY-BASED ESCALATION (NEW)
# =========================================

def memory_escalation(action, state_history):
    """
    Adds persistence-aware escalation.
    """

    if len(state_history) < 10:
        return action

    recent = state_history[-10:]

    instability = (
        recent.count("CRITICAL") +
        recent.count("WARNING") +
        2 * recent.count("COLLAPSED")
    )

    # strong instability → force aggressive control
    if instability >= 12:
        return "EMERGENCY_SHED"

    if instability >= 8:
        if action in ["NONE", "STABILIZE"]:
            return "REDUCE_LOAD"

    return action


# =========================================
# MAIN ENTRY
# =========================================

def run_adaptive_policy(base_action, state, state_history, risk_value, risk_slope):
    """
    Full adaptive control pipeline.
    """

    action = adaptive_override(base_action, state, risk_value, risk_slope)

    action = enforce_recovery(action, state, state_history, risk_value)

    action = memory_escalation(action, state_history)

    return action

import numpy as np


# =========================================
# NEXAH SOLVER V2
# =========================================

def nexah_solver_v2(lam, action=None):
    """
    Physically inspired solver:
    intervention modifies effective load (lambda),
    not voltage directly.
    """

    n = 9

    # =========================================
    # 1. MAP ACTION → LOAD REDUCTION
    # =========================================

    load_shift = 0.0

    if action == "STABILIZE":
        load_shift = 0.02

    elif action == "PREEMPTIVE_STABILIZE":
        load_shift = 0.05

    elif action == "REDUCE_LOAD":
        load_shift = 0.10

    elif action == "EMERGENCY_SHED":
        load_shift = 0.18

    elif action == "NONE" or action is None:
        load_shift = 0.0

    # =========================================
    # 2. EFFECTIVE LOAD (KEY CHANGE)
    # =========================================

    lam_eff = lam - load_shift

    # prevent unrealistic negative load
    lam_eff = max(lam_eff, 0.3)

    # =========================================
    # 3. BASE VOLTAGE PROFILE
    # =========================================

    V_base = 1.0 - 0.15 * (lam_eff - 1.0)

    V = np.ones(n) * V_base

    # =========================================
    # 4. NOISE
    # =========================================

    V += np.random.normal(0, 0.01, n)

    theta = np.random.uniform(-0.1, 0.1, n)

    # =========================================
    # 5. COLLAPSE CONDITION
    # =========================================

    collapse_threshold = 2.2

    if lam_eff > collapse_threshold:
        V[:] = np.nan
        converged = False
    else:
        converged = True

    return {
        "V": V,
        "theta": theta,
        "converged": converged,
        "lam_eff": lam_eff,
        "load_shift": load_shift,
    }

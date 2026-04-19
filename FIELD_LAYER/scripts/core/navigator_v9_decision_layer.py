import numpy as np


# =========================
# DECISION LOGIC
# =========================

def classify_state(alpha, beta, flow_vx, threshold_core=0.1):
    """
    Classify current state into ENTRY / CORE / EXIT
    """

    if abs(flow_vx) < threshold_core:
        return "core"

    if (alpha > 0 and flow_vx < 0) or (alpha < 0 and flow_vx > 0):
        return "entry"

    return "exit"


def decision_policy(state, deviation, d_deviation):
    """
    Simple navigation policy
    """

    # 1. stable region
    if deviation < 0.5:
        return "STAY_STABLE"

    # 2. entering transition
    if state == "entry":
        return "PREPARE"

    # 3. core transition
    if state == "core":
        if d_deviation > 0:
            return "INTERVENE"
        else:
            return "ALLOW_TRANSITION"

    # 4. exiting transition
    if state == "exit":
        return "STABILIZE"

    return "UNKNOWN"


# =========================
# MOCK INTERFACE
# =========================

def navigator_step(alpha, beta, D, dD, flow_vx):
    """
    One step of navigation decision
    """

    state = classify_state(alpha, beta, flow_vx)

    action = decision_policy(
        state,
        deviation=D,
        d_deviation=dD
    )

    return state, action


# =========================
# DEMO RUN
# =========================

def demo():
    print("Running Navigator V9 Demo...")

    # fake example values (replace with real pipeline later)
    samples = [
        {"alpha": -10, "beta": 2, "D": 0.3, "dD": 0.01, "vx": 0.2},
        {"alpha": -2, "beta": 5, "D": 1.2, "dD": 0.2, "vx": 0.05},
        {"alpha": 0.5, "beta": 7, "D": 1.8, "dD": 0.3, "vx": -0.01},
        {"alpha": 8, "beta": 2, "D": 0.7, "dD": -0.2, "vx": -0.3},
    ]

    for i, s in enumerate(samples):
        state, action = navigator_step(
            s["alpha"],
            s["beta"],
            s["D"],
            s["dD"],
            s["vx"]
        )

        print(f"Sample {i}:")
        print(f"  State: {state}")
        print(f"  Action: {action}")


if __name__ == "__main__":
    demo()

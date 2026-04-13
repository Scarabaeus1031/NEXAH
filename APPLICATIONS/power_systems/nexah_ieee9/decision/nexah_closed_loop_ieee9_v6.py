import numpy as np

# ================================
# CONFIG
# ================================

class Config:
    target_distance = 0.45

    # steering gains
    k_steer = 0.15
    k_risk = 0.25
    k_curv = 0.15

    steer_clip = 0.05


cfg = Config()

INTERVENTION_SET = [
    "PREEMPTIVE_STABILIZE",
    "REDUCE_LOAD + REACTIVE_SUPPORT",
    "DAMPEN + SMOOTH_RECOVERY"
]


# ================================
# FIELD MODEL (placeholder IEEE9)
# ================================

def compute_distance(risk):
    # simplified separatrix distance model
    return 1.05 - 0.5 * risk


def compute_risk(lambda_val):
    # synthetic risk curve (replace with your real system)
    return max(0.0, min(1.0, (lambda_val - 1.8) * 0.25))


# ================================
# DERIVATIVES
# ================================

def compute_derivatives(risk_history):
    if len(risk_history) < 3:
        return 0.0, 0.0

    slope = risk_history[-1] - risk_history[-2]
    d2c = (risk_history[-1]
           - 2 * risk_history[-2]
           + risk_history[-3])

    return slope, d2c


# ================================
# CONTROLLER STATE MACHINE
# ================================

def controller_state(risk):
    if risk < 0.2:
        return "NEXIT"
    elif risk < 0.22:
        return "ENGAGE"
    elif risk < 0.28:
        return "LOCK"
    else:
        return "RELEASE"


def controller_action(state):
    if state == "ENGAGE":
        return "PREEMPTIVE_STABILIZE"
    elif state == "LOCK":
        return "REDUCE_LOAD + REACTIVE_SUPPORT"
    elif state == "RELEASE":
        return "DAMPEN + SMOOTH_RECOVERY"
    return "MONITOR"


def control_adjustment(action):
    if action == "PREEMPTIVE_STABILIZE":
        return -0.02
    elif action == "REDUCE_LOAD + REACTIVE_SUPPORT":
        return -0.04
    elif action == "DAMPEN + SMOOTH_RECOVERY":
        return -0.03
    return 0.0


# ================================
# 🔥 V6 STEERING
# ================================

def compute_steering(distance, risk_slope, d2c, action, cfg):

    # distance-based steering
    steer_d = cfg.k_steer * (distance - cfg.target_distance)

    # oppose risk growth
    steer_r = -cfg.k_risk * risk_slope

    # damp curvature
    steer_c = -cfg.k_curv * d2c

    steer = steer_d + steer_r + steer_c
    steer = float(np.clip(steer, -cfg.steer_clip, cfg.steer_clip))

    if action in INTERVENTION_SET:
        return steer

    return 0.0


# ================================
# SIMULATION LOOP
# ================================

def run_simulation(steps=120):

    lambda_val = 0.5

    risk_history = []
    distance_history = []
    lambda_history = []
    state_history = []
    steer_history = []

    for step in range(steps):

        # --- system evaluation ---
        risk = compute_risk(lambda_val)
        distance = compute_distance(risk)

        risk_history.append(risk)
        distance_history.append(distance)

        # --- derivatives ---
        slope, d2c = compute_derivatives(risk_history)

        # --- controller ---
        state = controller_state(risk)
        action = controller_action(state)
        ctrl = control_adjustment(action)

        # --- 🔥 v6 steering ---
        steer = compute_steering(distance, slope, d2c, action, cfg)

        # --- lambda update ---
        lambda_eff = lambda_val + ctrl + steer

        # --- progression (external stress) ---
        lambda_val = lambda_eff + 0.015

        # --- logging ---
        print(
            f"[STEP {step}] "
            f"lambda={lambda_val:.4f} "
            f"state={state} "
            f"risk={risk:.4f} "
            f"slope={slope:.4f} "
            f"d2c={d2c:.4f} "
            f"dist={distance:.4f} "
            f"steer={steer:.4f} "
            f"action={action}"
        )

        # --- store ---
        lambda_history.append(lambda_val)
        state_history.append(state)
        steer_history.append(steer)

    return {
        "risk": risk_history,
        "distance": distance_history,
        "lambda": lambda_history,
        "state": state_history,
        "steer": steer_history
    }


# ================================
# RUN
# ================================

if __name__ == "__main__":
    results = run_simulation()

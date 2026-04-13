import math
import numpy as np


# ================================
# CONFIG
# ================================

class Config:
    target_distance = 0.45

    # steering gains
    k_steer = 0.18
    k_risk = 0.35
    k_curv = 0.12
    steer_clip = 0.06

    # damping for v6.1
    lock_steer_damping = 0.60
    recover_steer_damping = 0.75

    # base stress increase
    lambda_step = 0.015

    # nonlinear risk model
    collapse_center = 1.95
    collapse_sharpness = 8.0


cfg = Config()

INTERVENTION_SET = {
    "PREEMPTIVE_STABILIZE",
    "REDUCE_LOAD + REACTIVE_SUPPORT",
    "DAMPEN + SMOOTH_RECOVERY",
}


# ================================
# FIELD MODEL
# ================================

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def compute_risk(lambda_val: float) -> float:
    """
    Nonlinear transition around collapse_center.
    """
    z = (lambda_val - cfg.collapse_center) * cfg.collapse_sharpness
    return sigmoid(z)


def compute_distance(risk: float, lambda_val: float) -> float:
    """
    Distance shrinks as risk rises and lambda grows.
    """
    d = 1.10 - 0.95 * risk - 0.12 * (lambda_val - 1.0)
    return max(0.0, d)


# ================================
# DERIVATIVES
# ================================

def compute_derivatives(risk_history):
    if len(risk_history) < 3:
        return 0.0, 0.0

    slope = risk_history[-1] - risk_history[-2]
    d2c = risk_history[-1] - 2 * risk_history[-2] + risk_history[-3]
    return slope, d2c


# ================================
# CONTROLLER STATE MACHINE
# ================================

def controller_state(risk, distance):
    # v6.1: slightly wider hysteresis bands
    if risk < 0.18 and distance > 0.65:
        return "NEXIT"
    elif risk < 0.30 and distance > 0.35:
        return "ENGAGE"
    elif distance < 0.30 or risk < 0.80:
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
        return -0.015
    elif action == "REDUCE_LOAD + REACTIVE_SUPPORT":
        return -0.030
    elif action == "DAMPEN + SMOOTH_RECOVERY":
        return -0.020
    return 0.0


# ================================
# V6.1 STEERING
# ================================

def soft_clip(x: float, clip_value: float) -> float:
    """
    Smooth saturation instead of hard np.clip.
    Prevents abrupt sign flips / bang-bang jumps.
    """
    return clip_value * math.tanh(x / clip_value)


def compute_steering(distance, risk_slope, d2c, action, cfg):
    steer_d = cfg.k_steer * (distance - cfg.target_distance)
    steer_r = -cfg.k_risk * risk_slope
    steer_c = -cfg.k_curv * d2c

    steer = steer_d + steer_r + steer_c

    # v6.1: soft clipping instead of hard clipping
    steer = soft_clip(steer, cfg.steer_clip)

    if action in INTERVENTION_SET:
        # v6.1: damp steering depending on action
        if action == "REDUCE_LOAD + REACTIVE_SUPPORT":
            steer *= cfg.lock_steer_damping
        elif action == "DAMPEN + SMOOTH_RECOVERY":
            steer *= cfg.recover_steer_damping

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
    action_history = []

    for step in range(steps):
        # --- system evaluation ---
        risk = compute_risk(lambda_val)
        distance = compute_distance(risk, lambda_val)

        risk_history.append(risk)
        distance_history.append(distance)

        # --- derivatives ---
        slope, d2c = compute_derivatives(risk_history)

        # --- controller ---
        state = controller_state(risk, distance)
        action = controller_action(state)
        ctrl = control_adjustment(action)

        # --- v6.1 steering ---
        steer = compute_steering(distance, slope, d2c, action, cfg)

        # --- lambda update ---
        lambda_eff = lambda_val + ctrl + steer
        lambda_val = max(0.0, lambda_eff + cfg.lambda_step)

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

        lambda_history.append(lambda_val)
        state_history.append(state)
        steer_history.append(steer)
        action_history.append(action)

    return {
        "risk": risk_history,
        "distance": distance_history,
        "lambda": lambda_history,
        "state": state_history,
        "steer": steer_history,
        "action": action_history,
    }


# ================================
# RUN
# ================================

if __name__ == "__main__":
    results = run_simulation()

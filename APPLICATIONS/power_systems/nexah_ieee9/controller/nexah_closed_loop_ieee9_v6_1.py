import math
import numpy as np
import matplotlib.pyplot as plt
import csv


# ================================
# CONFIG
# ================================

class Config:
    target_distance = 0.45

    k_steer = 0.18
    k_risk = 0.35
    k_curv = 0.12
    steer_clip = 0.06

    lock_steer_damping = 0.60
    recover_steer_damping = 0.75

    lambda_step = 0.015

    collapse_center = 1.95
    collapse_sharpness = 8.0


cfg = Config()

INTERVENTION_SET = {
    "PREEMPTIVE_STABILIZE",
    "REDUCE_LOAD + REACTIVE_SUPPORT",
    "DAMPEN + SMOOTH_RECOVERY",
}


# ================================
# MODEL
# ================================

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


def compute_risk(l):
    return sigmoid((l - cfg.collapse_center) * cfg.collapse_sharpness)


def compute_distance(risk, l):
    d = 1.10 - 0.95 * risk - 0.12 * (l - 1.0)
    return max(0.0, d)


def compute_derivatives(hist):
    if len(hist) < 3:
        return 0.0, 0.0
    slope = hist[-1] - hist[-2]
    d2c = hist[-1] - 2 * hist[-2] + hist[-3]
    return slope, d2c


# ================================
# CONTROLLER
# ================================

def controller_state(risk, distance):
    if risk < 0.18 and distance > 0.65:
        return "NEXIT"
    elif risk < 0.30 and distance > 0.35:
        return "ENGAGE"
    elif distance < 0.30 or risk < 0.80:
        return "LOCK"
    else:
        return "RELEASE"


def controller_action(state):
    return {
        "ENGAGE": "PREEMPTIVE_STABILIZE",
        "LOCK": "REDUCE_LOAD + REACTIVE_SUPPORT",
        "RELEASE": "DAMPEN + SMOOTH_RECOVERY",
    }.get(state, "MONITOR")


def control_adjustment(action):
    return {
        "PREEMPTIVE_STABILIZE": -0.015,
        "REDUCE_LOAD + REACTIVE_SUPPORT": -0.030,
        "DAMPEN + SMOOTH_RECOVERY": -0.020,
    }.get(action, 0.0)


# ================================
# STEERING
# ================================

def soft_clip(x, c):
    return c * math.tanh(x / c)


def compute_steering(distance, slope, d2c, action):
    steer = (
        cfg.k_steer * (distance - cfg.target_distance)
        - cfg.k_risk * slope
        - cfg.k_curv * d2c
    )

    steer = soft_clip(steer, cfg.steer_clip)

    if action in INTERVENTION_SET:
        if action == "REDUCE_LOAD + REACTIVE_SUPPORT":
            steer *= cfg.lock_steer_damping
        elif action == "DAMPEN + SMOOTH_RECOVERY":
            steer *= cfg.recover_steer_damping
        return steer

    return 0.0


# ================================
# SIMULATION
# ================================

def run(steps=120):
    l = 0.5

    data = []
    risk_hist = []

    for step in range(steps):
        risk = compute_risk(l)
        dist = compute_distance(risk, l)

        risk_hist.append(risk)
        slope, d2c = compute_derivatives(risk_hist)

        state = controller_state(risk, dist)
        action = controller_action(state)

        ctrl = control_adjustment(action)
        steer = compute_steering(dist, slope, d2c, action)

        l = max(0.0, l + ctrl + steer + cfg.lambda_step)

        print(f"[STEP {step}] lambda={l:.4f} state={state} risk={risk:.4f} dist={dist:.4f} steer={steer:.4f} action={action}")

        data.append([step, l, risk, slope, d2c, dist, steer, state, action])

    return data


# ================================
# EXPORT
# ================================

def save_csv(data):
    with open("output_v6_1_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "lambda", "risk", "slope", "d2c", "distance", "steer", "state", "action"])
        writer.writerows(data)


def plot(data):
    steps = [d[0] for d in data]
    lam = [d[1] for d in data]
    risk = [d[2] for d in data]
    dist = [d[5] for d in data]
    steer = [d[6] for d in data]

    plt.figure()

    plt.plot(steps, lam, label="lambda")
    plt.plot(steps, risk, label="risk")
    plt.plot(steps, dist, label="distance")
    plt.plot(steps, steer, label="steer")

    plt.legend()
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.title("NEXAH Closed Loop v6.1")

    plt.savefig("output_v6_1_plot.png")
    plt.show()


# ================================
# RUN
# ================================

if __name__ == "__main__":
    data = run()
    save_csv(data)
    plot(data)

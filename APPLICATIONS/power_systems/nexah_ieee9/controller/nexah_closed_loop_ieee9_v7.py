import math
import numpy as np
import matplotlib.pyplot as plt
import csv


# ================================
# CONFIG
# ================================

class Config:
    target_distance = 0.45

    lambda_step = 0.015

    collapse_center = 1.95
    collapse_sharpness = 8.0

    # Field weights
    w_risk = 1.0
    w_dist = 2.0

    # Gradient control
    k_grad = 0.08
    eps = 1e-3
    steer_clip = 0.05


cfg = Config()


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


# ================================
# FIELD
# ================================

def compute_potential(l):
    r = compute_risk(l)
    d = compute_distance(r, l)

    V = (
        cfg.w_risk * r +
        cfg.w_dist * (d - cfg.target_distance) ** 2
    )
    return V


def compute_gradient(l):
    eps = cfg.eps

    V_plus = compute_potential(l + eps)
    V_minus = compute_potential(l - eps)

    grad = (V_plus - V_minus) / (2 * eps)
    return grad


def compute_steering(l):
    grad = compute_gradient(l)

    steer = -cfg.k_grad * grad
    steer = max(-cfg.steer_clip, min(cfg.steer_clip, steer))

    return steer


# ================================
# STATE MACHINE (minimal retained)
# ================================

def controller_state(risk, distance):
    if risk < 0.18 and distance > 0.65:
        return "NEXIT"
    elif risk < 0.30 and distance > 0.35:
        return "ENGAGE"
    else:
        return "LOCK"


def control_adjustment(state):
    return {
        "ENGAGE": -0.010,
        "LOCK": -0.020,
    }.get(state, 0.0)


# ================================
# SIMULATION
# ================================

def run(steps=120):
    l = 0.5
    data = []

    for step in range(steps):
        risk = compute_risk(l)
        dist = compute_distance(risk, l)

        state = controller_state(risk, dist)
        ctrl = control_adjustment(state)

        steer = compute_steering(l)

        l = max(0.0, l + ctrl + steer + cfg.lambda_step)

        print(f"[STEP {step}] lambda={l:.4f} risk={risk:.4f} dist={dist:.4f} steer={steer:.4f} state={state}")

        data.append([step, l, risk, dist, steer, state])

    return data


# ================================
# EXPORT
# ================================

def save_csv(data):
    with open("output_v7_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["step", "lambda", "risk", "distance", "steer", "state"])
        writer.writerows(data)


def plot(data):
    steps = [d[0] for d in data]
    lam = [d[1] for d in data]
    risk = [d[2] for d in data]
    dist = [d[3] for d in data]
    steer = [d[4] for d in data]

    plt.figure()

    plt.plot(steps, lam, label="lambda")
    plt.plot(steps, risk, label="risk")
    plt.plot(steps, dist, label="distance")
    plt.plot(steps, steer, label="steer")

    plt.legend()
    plt.title("NEXAH Closed Loop v7 (Field-Based)")
    plt.xlabel("Step")
    plt.ylabel("Value")

    plt.savefig("output_v7_plot.png")
    plt.show()


# ================================
# RUN
# ================================

if __name__ == "__main__":
    data = run()
    save_csv(data)
    plot(data)

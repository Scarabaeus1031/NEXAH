import math
import csv
import os
import numpy as np
import matplotlib.pyplot as plt


# ============================================================
# CONFIG
# ============================================================

class Config:
    target_distance = 0.45

    # exogenous loading drift
    lambda_step = 0.015

    # base nonlinear system
    collapse_center = 1.95
    collapse_sharpness = 8.0

    # field weights
    w_risk = 1.0
    w_dist = 2.0
    w_barrier = 0.25

    # gradient control
    k_grad = 0.08
    eps = 1e-3
    steer_clip = 0.05

    # drift shaping
    drift_gain = 1.0
    drift_risk_damping = 0.80

    # controller layer
    engage_ctrl = -0.010
    lock_ctrl = -0.020

    # v8 rotation term
    rot_amp = 0.018
    rot_freq = 10.0
    rot_phase = 0.0

    # output
    out_dir = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v8"


cfg = Config()


# ============================================================
# FILESYSTEM
# ============================================================

def ensure_out_dir():
    os.makedirs(cfg.out_dir, exist_ok=True)


# ============================================================
# CORE MODEL
# ============================================================

def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def compute_risk(lmbd: float) -> float:
    return sigmoid((lmbd - cfg.collapse_center) * cfg.collapse_sharpness)


def compute_distance(risk: float, lmbd: float) -> float:
    d = 1.10 - 0.95 * risk - 0.12 * (lmbd - 1.0)
    return max(0.0, d)


# ============================================================
# FIELD / POTENTIAL
# ============================================================

def compute_barrier(lmbd: float) -> float:
    return cfg.w_barrier * math.exp(-((lmbd - 1.85) ** 2) / 0.01)


def compute_potential(lmbd: float) -> float:
    risk = compute_risk(lmbd)
    dist = compute_distance(risk, lmbd)

    V = (
        cfg.w_risk * risk
        + cfg.w_dist * (dist - cfg.target_distance) ** 2
        + compute_barrier(lmbd)
    )
    return V


def compute_gradient(lmbd: float) -> float:
    eps = cfg.eps
    vp = compute_potential(lmbd + eps)
    vm = compute_potential(lmbd - eps)
    return (vp - vm) / (2.0 * eps)


def compute_steering(lmbd: float) -> tuple[float, float]:
    grad = compute_gradient(lmbd)
    steer = -cfg.k_grad * grad
    steer = max(-cfg.steer_clip, min(cfg.steer_clip, steer))
    return steer, grad


# ============================================================
# CONTROLLER LAYER
# ============================================================

def controller_state(risk: float, dist: float) -> str:
    if risk < 0.18 and dist > 0.65:
        return "NEXIT"
    elif risk < 0.30 and dist > 0.35:
        return "ENGAGE"
    return "LOCK"


def control_adjustment(state: str) -> float:
    if state == "ENGAGE":
        return cfg.engage_ctrl
    if state == "LOCK":
        return cfg.lock_ctrl
    return 0.0


# ============================================================
# DRIFT TERM
# ============================================================

def compute_drift(risk: float) -> float:
    return cfg.lambda_step * cfg.drift_gain * (1.0 - cfg.drift_risk_damping * risk)


# ============================================================
# V8 ROTATIONAL TERM
# ============================================================

def compute_rotational_force(lmbd: float) -> float:
    """
    Non-conservative rotational forcing.
    This breaks pure descent and enables orbit-like phase motion.
    """
    return cfg.rot_amp * math.sin(cfg.rot_freq * lmbd + cfg.rot_phase)


# ============================================================
# SIMULATION
# ============================================================

def run(steps: int = 120):
    lmbd = 0.5
    data = []

    for step in range(steps):
        risk = compute_risk(lmbd)
        dist = compute_distance(risk, lmbd)

        state = controller_state(risk, dist)
        ctrl = control_adjustment(state)

        steer, grad = compute_steering(lmbd)
        drift = compute_drift(risk)
        rot = compute_rotational_force(lmbd)

        barrier = compute_barrier(lmbd)
        potential = compute_potential(lmbd)

        # v8 update
        lmbd = max(0.0, lmbd + ctrl + steer + drift + rot)

        print(
            f"[STEP {step}] "
            f"lambda={lmbd:.4f} "
            f"risk={risk:.4f} "
            f"dist={dist:.4f} "
            f"grad={grad:.4f} "
            f"steer={steer:.4f} "
            f"drift={drift:.4f} "
            f"rot={rot:.4f} "
            f"barrier={barrier:.4f} "
            f"V={potential:.4f} "
            f"state={state}"
        )

        data.append([
            step,
            lmbd,
            risk,
            dist,
            grad,
            steer,
            drift,
            rot,
            barrier,
            potential,
            state
        ])

    return data


# ============================================================
# EXPORT
# ============================================================

def save_csv(data):
    path = os.path.join(cfg.out_dir, "output_v8_data.csv")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "step",
            "lambda",
            "risk",
            "distance",
            "gradient",
            "steer",
            "drift",
            "rot",
            "barrier",
            "potential",
            "state",
        ])
        writer.writerows(data)
    return path


def plot_timeseries(data):
    steps = [d[0] for d in data]
    lmbd = [d[1] for d in data]
    risk = [d[2] for d in data]
    dist = [d[3] for d in data]
    steer = [d[5] for d in data]
    drift = [d[6] for d in data]
    rot = [d[7] for d in data]
    potential = [d[9] for d in data]

    plt.figure(figsize=(10, 6))
    plt.plot(steps, lmbd, label="lambda")
    plt.plot(steps, risk, label="risk")
    plt.plot(steps, dist, label="distance")
    plt.plot(steps, steer, label="steer")
    plt.plot(steps, drift, label="drift")
    plt.plot(steps, rot, label="rotation")
    plt.plot(steps, potential, label="potential")

    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.title("NEXAH Closed Loop v8 (Field + Drift + Rotation)")
    plt.legend()
    plt.tight_layout()

    path = os.path.join(cfg.out_dir, "output_v8_plot.png")
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def plot_phase(data):
    risk = [d[2] for d in data]
    dist = [d[3] for d in data]
    steps = [d[0] for d in data]

    plt.figure(figsize=(7, 6))
    sc = plt.scatter(risk, dist, c=steps, s=30)
    plt.plot(risk, dist, alpha=0.4)
    plt.axhline(cfg.target_distance, linestyle="--", label="target_distance")

    plt.xlabel("Risk")
    plt.ylabel("Distance")
    plt.title("NEXAH v8 Phase Plot (Risk vs Distance)")
    plt.legend()
    plt.colorbar(sc, label="Step")
    plt.tight_layout()

    path = os.path.join(cfg.out_dir, "output_v8_phase.png")
    plt.savefig(path, dpi=200)
    plt.close()
    return path


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    ensure_out_dir()
    data = run()
    csv_path = save_csv(data)
    ts_path = plot_timeseries(data)
    ph_path = plot_phase(data)

    print("\nSaved:")
    print(csv_path)
    print(ts_path)
    print(ph_path)

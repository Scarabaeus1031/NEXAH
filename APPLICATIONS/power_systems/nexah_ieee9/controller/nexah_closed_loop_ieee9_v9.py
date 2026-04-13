import math
import csv
import os
import matplotlib.pyplot as plt


# ============================================================
# CONFIG
# ============================================================

class Config:
    target_distance = 0.45

    # external loading drift
    lambda_step = 0.010

    # nonlinear grid proxy
    collapse_center = 1.95
    collapse_sharpness = 8.0

    # field potential
    w_risk = 1.0
    w_dist = 2.0
    w_barrier = 0.25

    # gradient steering
    k_grad = 0.08
    eps = 1e-3
    steer_clip = 0.05

    # drift shaping
    drift_gain = 1.0
    drift_risk_damping = 0.80

    # controller layer
    engage_ctrl = -0.010
    lock_ctrl = -0.020

    # V9 phase dynamics
    psi0 = 0.0
    lambda_ref = 1.75

    psi_damping = 0.18
    psi_restore = 0.22
    psi_rot_amp = 0.06
    psi_rot_freq = 8.0

    lambda_phase_coupling = 0.030

    # output
    out_dir = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v9"


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

    return (
        cfg.w_risk * risk
        + cfg.w_dist * (dist - cfg.target_distance) ** 2
        + compute_barrier(lmbd)
    )


def compute_gradient(lmbd: float) -> float:
    eps = cfg.eps
    vp = compute_potential(lmbd + eps)
    vm = compute_potential(lmbd - eps)
    return (vp - vm) / (2.0 * eps)


def compute_steering(lmbd: float):
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
# V9 PHASE DYNAMICS
# ============================================================

def update_psi(psi: float, lmbd: float) -> float:
    """
    Internal phase / momentum state.
    """
    dpsi = (
        -cfg.psi_damping * psi
        -cfg.psi_restore * (lmbd - cfg.lambda_ref)
        + cfg.psi_rot_amp * math.sin(cfg.psi_rot_freq * lmbd)
    )
    return psi + dpsi


# ============================================================
# SIMULATION
# ============================================================

def run(steps: int = 160):
    lmbd = 0.5
    psi = cfg.psi0

    data = []

    for step in range(steps):
        risk = compute_risk(lmbd)
        dist = compute_distance(risk, lmbd)

        state = controller_state(risk, dist)
        ctrl = control_adjustment(state)

        steer, grad = compute_steering(lmbd)
        drift = compute_drift(risk)
        barrier = compute_barrier(lmbd)
        potential = compute_potential(lmbd)

        # update internal phase state first
        psi = update_psi(psi, lmbd)

        # lambda update now coupled to psi
        lmbd = max(
            0.0,
            lmbd + drift + ctrl + steer + cfg.lambda_phase_coupling * psi
        )

        print(
            f"[STEP {step}] "
            f"lambda={lmbd:.4f} "
            f"psi={psi:.4f} "
            f"risk={risk:.4f} "
            f"dist={dist:.4f} "
            f"grad={grad:.4f} "
            f"steer={steer:.4f} "
            f"drift={drift:.4f} "
            f"barrier={barrier:.4f} "
            f"V={potential:.4f} "
            f"state={state}"
        )

        data.append([
            step,
            lmbd,
            psi,
            risk,
            dist,
            grad,
            steer,
            drift,
            barrier,
            potential,
            state
        ])

    return data


# ============================================================
# EXPORT
# ============================================================

def save_csv(data):
    path = os.path.join(cfg.out_dir, "output_v9_data.csv")
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "step",
            "lambda",
            "psi",
            "risk",
            "distance",
            "gradient",
            "steer",
            "drift",
            "barrier",
            "potential",
            "state",
        ])
        writer.writerows(data)
    return path


def plot_timeseries(data):
    steps = [d[0] for d in data]
    lmbd = [d[1] for d in data]
    psi = [d[2] for d in data]
    risk = [d[3] for d in data]
    dist = [d[4] for d in data]
    steer = [d[6] for d in data]
    drift = [d[7] for d in data]
    potential = [d[9] for d in data]

    plt.figure(figsize=(10, 6))
    plt.plot(steps, lmbd, label="lambda")
    plt.plot(steps, psi, label="psi")
    plt.plot(steps, risk, label="risk")
    plt.plot(steps, dist, label="distance")
    plt.plot(steps, steer, label="steer")
    plt.plot(steps, drift, label="drift")
    plt.plot(steps, potential, label="potential")

    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.title("NEXAH Closed Loop v9 (2D Phase System)")
    plt.legend()
    plt.tight_layout()

    path = os.path.join(cfg.out_dir, "output_v9_plot.png")
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def plot_phase_risk_distance(data):
    risk = [d[3] for d in data]
    dist = [d[4] for d in data]
    steps = [d[0] for d in data]

    plt.figure(figsize=(7, 6))
    sc = plt.scatter(risk, dist, c=steps, s=28)
    plt.plot(risk, dist, alpha=0.35)
    plt.axhline(cfg.target_distance, linestyle="--", label="target_distance")
    plt.xlabel("Risk")
    plt.ylabel("Distance")
    plt.title("NEXAH v9 Phase Plot (Risk vs Distance)")
    plt.legend()
    plt.colorbar(sc, label="Step")
    plt.tight_layout()

    path = os.path.join(cfg.out_dir, "output_v9_phase_risk_distance.png")
    plt.savefig(path, dpi=200)
    plt.close()
    return path


def plot_phase_lambda_psi(data):
    lmbd = [d[1] for d in data]
    psi = [d[2] for d in data]
    steps = [d[0] for d in data]

    plt.figure(figsize=(7, 6))
    sc = plt.scatter(lmbd, psi, c=steps, s=28)
    plt.plot(lmbd, psi, alpha=0.35)
    plt.xlabel("lambda")
    plt.ylabel("psi")
    plt.title("NEXAH v9 True Phase Portrait (lambda vs psi)")
    plt.colorbar(sc, label="Step")
    plt.tight_layout()

    path = os.path.join(cfg.out_dir, "output_v9_phase_lambda_psi.png")
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
    rd_path = plot_phase_risk_distance(data)
    lp_path = plot_phase_lambda_psi(data)

    print("\nSaved:")
    print(csv_path)
    print(ts_path)
    print(rd_path)
    print(lp_path)

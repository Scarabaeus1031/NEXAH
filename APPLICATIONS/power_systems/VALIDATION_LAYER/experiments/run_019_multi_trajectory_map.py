import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "outputs" / "run_019_multi_trajectory_map"


# ============================================================
# Scenario (parametrized)
# ============================================================

def make_synthetic_variant(seed=0, strength=1.0, n=500):
    rng = np.random.default_rng(seed)

    t = np.linspace(0, 100, n)

    # baseline
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    # nonlinear perturbation (scaled)
    V += strength * 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += strength * 0.01 * np.sin(0.8 * t) * (t < 25)

    # small noise variation
    V += 0.002 * rng.normal(size=len(t))

    return t, V


# ============================================================
# Signals
# ============================================================

def compute_state(t, V, sigma=2):
    V_s = gaussian_filter1d(V, sigma=sigma)
    dv = gaussian_filter1d(np.gradient(V_s, t), sigma=sigma)
    d2v = gaussian_filter1d(np.gradient(dv, t), sigma=sigma)

    x = np.vstack([V_s, dv, d2v]).T

    curvature = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma=sigma
    )

    return V_s, dv, d2v, curvature


def detect_transition(V_s, curvature):
    stable_idx = int(0.30 * len(V_s))

    kappa_th = np.mean(curvature[:stable_idx]) + 2 * np.std(curvature[:stable_idx])

    mask = curvature > kappa_th

    for i in range(len(mask)):
        if np.all(mask[i:i+3]):
            return i

    return None


# ============================================================
# MAIN
# ============================================================

def run():
    print("\n=== RUN 019 — MULTI TRAJECTORY MAP ===")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # generate multiple trajectories
    configs = [
        {"seed": 1, "strength": 0.8},
        {"seed": 2, "strength": 1.0},
        {"seed": 3, "strength": 1.2},
        {"seed": 4, "strength": 1.4},
        {"seed": 5, "strength": 0.6},
    ]

    trajectories = []

    for cfg in configs:
        t, V = make_synthetic_variant(**cfg)
        V_s, dv, d2v, curvature = compute_state(t, V)

        idx_transition = detect_transition(V_s, curvature)

        trajectories.append({
            "t": t,
            "V": V_s,
            "dv": dv,
            "d2v": d2v,
            "curvature": curvature,
            "transition_idx": idx_transition
        })

    # --------------------------------------------------------
    # 3D multi trajectory plot
    # --------------------------------------------------------
    from mpl_toolkits.mplot3d import Axes3D  # noqa

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")

    colors = ["blue", "green", "orange", "purple", "brown"]

    for i, traj in enumerate(trajectories):
        V = traj["V"]
        dv = traj["dv"]
        d2v = traj["d2v"]

        ax.plot(V, dv, d2v, color=colors[i], alpha=0.8, label=f"run {i}")

        # mark transition point
        idx = traj["transition_idx"]
        if idx is not None:
            ax.scatter(
                V[idx],
                dv[idx],
                d2v[idx],
                color="red",
                s=50
            )

    ax.set_title("Multi-Trajectory State Space")
    ax.set_xlabel("V(t)")
    ax.set_ylabel("dV/dt")
    ax.set_zlabel("d²V/dt²")

    ax.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_01_multi_trajectory.png", dpi=150)

    # --------------------------------------------------------
    # curvature comparison
    # --------------------------------------------------------
    plt.figure(figsize=(10, 5))

    for i, traj in enumerate(trajectories):
        k = traj["curvature"]
        k = k / (np.max(k) + 1e-8)

        plt.plot(traj["t"], k, label=f"run {i}")

    plt.title("Curvature Across Trajectories")
    plt.xlabel("time")
    plt.ylabel("normalized κ(t)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_02_curvature_compare.png", dpi=150)

    # --------------------------------------------------------
    # save summary
    # --------------------------------------------------------
    summary = []

    for i, traj in enumerate(trajectories):
        idx = traj["transition_idx"]
        t_val = float(traj["t"][idx]) if idx is not None else None

        summary.append({
            "run": i,
            "transition_time": t_val
        })

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(summary, f, indent=2)

    print("\nSaved to:", OUT_DIR)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run()

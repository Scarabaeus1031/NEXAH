# ============================================================
# RUN 033 — CONTROL INJECTION TEST
# ============================================================

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs/run_033_control_injection"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# BASE SYSTEM
# ------------------------------------------------------------
def make_scenario(n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
    V += 0.01 * np.sin(0.8 * t) * (t < 25)

    return t, V


def embedding(t, V):
    V_s = gaussian_filter1d(V, sigma=2)
    dV = gaussian_filter1d(np.gradient(V_s, t), sigma=2)
    return np.vstack([V_s, dV]).T


# ------------------------------------------------------------
# DECISION FIELD (simplified reuse)
# ------------------------------------------------------------
def compute_decision_mask(x, threshold=0.12, grid_size=40):
    dx = np.gradient(x, axis=0)

    angles = np.arctan2(dx[:, 1], dx[:, 0])
    mags = np.linalg.norm(dx, axis=1)

    # local entropy proxy (simple)
    entropy_proxy = np.abs(np.gradient(angles))
    entropy_proxy = gaussian_filter1d(entropy_proxy, sigma=2)

    flow_norm = mags / (mags.max() + 1e-8)

    decision = entropy_proxy * flow_norm

    return decision


# ------------------------------------------------------------
# CONTROLLED SIMULATION
# ------------------------------------------------------------
def simulate_control(t, V, decision, strength=0.02):
    V_ctrl = V.copy()

    for i in range(1, len(V_ctrl) - 1):
        if decision[i] > 0.12:
            # push upward (example intervention)
            V_ctrl[i] += strength * np.sign(-V_ctrl[i])  # simple bias

    return V_ctrl


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== RUN 033 — CONTROL INJECTION TEST ===\n")

    t, V = make_scenario()
    x = embedding(t, V)

    decision = compute_decision_mask(x)

    # controlled version
    V_ctrl = simulate_control(t, V, decision, strength=0.02)

    # embeddings
    x_base = embedding(t, V)
    x_ctrl = embedding(t, V_ctrl)

    # --------------------------------------------------------
    # PLOT TRAJECTORIES
    # --------------------------------------------------------
    plt.figure(figsize=(6, 5))
    plt.plot(x_base[:, 0], x_base[:, 1], label="baseline", color="white")
    plt.plot(x_ctrl[:, 0], x_ctrl[:, 1], label="controlled", color="red")
    plt.title("State Space: Baseline vs Controlled")
    plt.xlabel("V")
    plt.ylabel("dV")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_01_state_comparison.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # TIME DOMAIN
    # --------------------------------------------------------
    plt.figure(figsize=(8, 4))
    plt.plot(t, V, label="baseline", color="white")
    plt.plot(t, V_ctrl, label="controlled", color="red")
    plt.title("Time Series: Control Effect")
    plt.xlabel("time")
    plt.ylabel("V")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_02_time_series.png", dpi=150)
    plt.close()

    # --------------------------------------------------------
    # DIFFERENCE
    # --------------------------------------------------------
    diff = np.abs(V_ctrl - V)

    plt.figure(figsize=(8, 4))
    plt.plot(t, diff, color="orange")
    plt.title("Control Impact (|ΔV|)")
    plt.xlabel("time")
    plt.ylabel("difference")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_03_difference.png", dpi=150)
    plt.close()

    result = {
        "max_deviation": float(diff.max()),
        "mean_deviation": float(diff.mean()),
        "interpretation": "Deviation indicates controllability in high-decision zones.",
    }

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    print(f"\nSaved to: {OUT_DIR}")

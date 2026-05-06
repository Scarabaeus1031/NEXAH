# ============================================================
# RUN 032 — DECISION FIELD / CONTROL ZONES
# ============================================================

import json
from pathlib import Path
from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from scipy.stats import entropy


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------
OUT_DIR = Path(__file__).resolve().parent.parent / "outputs/run_032_decision_field"
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ------------------------------------------------------------
# SCENARIO
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
# FIELDS
# ------------------------------------------------------------
def compute_fields(x, grid_size=40):
    x_min, x_max = x[:, 0].min(), x[:, 0].max()
    y_min, y_max = x[:, 1].min(), x[:, 1].max()

    dx = np.gradient(x, axis=0)

    cell_angles = defaultdict(list)
    cell_magnitudes = defaultdict(list)

    for i in range(len(x) - 1):
        gx = int((x[i, 0] - x_min) / (x_max - x_min + 1e-8) * (grid_size - 1))
        gy = int((x[i, 1] - y_min) / (y_max - y_min + 1e-8) * (grid_size - 1))

        v = dx[i]
        angle = np.arctan2(v[1], v[0])
        mag = np.linalg.norm(v)

        cell_angles[(gx, gy)].append(angle)
        cell_magnitudes[(gx, gy)].append(mag)

    entropy_field = np.zeros((grid_size, grid_size))
    flow_field = np.zeros((grid_size, grid_size))
    count_field = np.zeros((grid_size, grid_size))

    for (gx, gy), angles in cell_angles.items():
        if len(angles) < 3:
            continue

        hist, _ = np.histogram(
            angles,
            bins=12,
            range=(-np.pi, np.pi),
            density=False,
        )

        hist = hist / (hist.sum() + 1e-12)
        H = entropy(hist + 1e-12)

        mag = np.mean(cell_magnitudes[(gx, gy)])

        entropy_field[gy, gx] = H
        flow_field[gy, gx] = mag
        count_field[gy, gx] = len(angles)

    if flow_field.max() > 0:
        flow_norm = flow_field / flow_field.max()
    else:
        flow_norm = flow_field

    decision_field = entropy_field * flow_norm

    return entropy_field, flow_field, decision_field, count_field, (x_min, x_max, y_min, y_max)


def save_field(field, x, bounds, title, filename, cmap):
    x_min, x_max, y_min, y_max = bounds

    plt.figure(figsize=(8, 5))
    plt.imshow(
        field,
        origin="lower",
        extent=[x_min, x_max, y_min, y_max],
        aspect="auto",
        cmap=cmap,
    )
    plt.colorbar()
    plt.plot(x[:, 0], x[:, 1], color="white", linewidth=1)
    plt.title(title)
    plt.xlabel("V")
    plt.ylabel("dV")
    plt.tight_layout()
    plt.savefig(OUT_DIR / filename, dpi=150)
    plt.close()


# ------------------------------------------------------------
# MAIN
# ------------------------------------------------------------
if __name__ == "__main__":
    print("\n=== RUN 032 — DECISION FIELD / CONTROL ZONES ===\n")

    t, V = make_scenario()
    x = embedding(t, V)

    entropy_field, flow_field, decision_field, count_field, bounds = compute_fields(x)

    save_field(entropy_field, x, bounds, "Entropy Field", "figure_01_entropy_field.png", "inferno")
    save_field(flow_field, x, bounds, "Flow Magnitude Field", "figure_02_flow_magnitude.png", "viridis")
    save_field(decision_field, x, bounds, "Decision Field / Control Zones", "figure_03_decision_field.png", "plasma")

    # decision over time
    x_min, x_max, y_min, y_max = bounds
    grid_size = decision_field.shape[0]

    decision_along = []
    for i in range(len(x)):
        gx = int((x[i, 0] - x_min) / (x_max - x_min + 1e-8) * (grid_size - 1))
        gy = int((x[i, 1] - y_min) / (y_max - y_min + 1e-8) * (grid_size - 1))
        decision_along.append(decision_field[gy, gx])

    plt.figure(figsize=(9, 4))
    plt.plot(t, decision_along, color="red")
    plt.title("Decision Intensity over Time")
    plt.xlabel("time")
    plt.ylabel("decision score")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_04_decision_timeline.png", dpi=150)
    plt.close()

    nonzero = decision_field[decision_field > 0]
    threshold = float(np.percentile(nonzero, 90)) if len(nonzero) else 0.0

    result = {
        "max_decision": float(decision_field.max()),
        "threshold_p90": threshold,
        "active_control_cells": int(np.sum(decision_field >= threshold)) if threshold > 0 else 0,
        "interpretation": "Decision zones are cells where local flow entropy and flow magnitude overlap.",
    }

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    print(f"\nSaved to: {OUT_DIR}")

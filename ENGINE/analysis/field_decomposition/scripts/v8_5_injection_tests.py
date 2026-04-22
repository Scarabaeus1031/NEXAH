# ENGINE/analysis/field_decomposition/scripts/v8_5_injection_tests.py

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LOCAL SAVE
# ============================================================

def save_figure(script_path):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = os.path.join("ENGINE/analysis/field_decomposition/outputs", script_name)
    os.makedirs(outdir, exist_ok=True)

    outfile = os.path.join(outdir, f"{script_name}.png")
    plt.savefig(outfile, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ saved figure -> {outfile}")
    return outdir

def save_run_info(script_path, extra=None):
    script_name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = os.path.join("ENGINE/analysis/field_decomposition/outputs", script_name)
    os.makedirs(outdir, exist_ok=True)

    info_path = os.path.join(outdir, "run_info.txt")
    with open(info_path, "w", encoding="utf-8") as f:
        f.write(f"script: {script_name}\n")
        f.write(f"time: {datetime.now()}\n")
        if extra:
            for k, v in extra.items():
                f.write(f"{k}: {v}\n")

# ============================================================
# CONFIG
# ============================================================

BASE = "ENGINE/analysis/field_decomposition/outputs"
GATE_DIR = os.path.join(BASE, "v8_4_extract_gate_points")

gate_points_path = os.path.join(GATE_DIR, "gate_points.npy")
gate_values_path = os.path.join(GATE_DIR, "gate_values.npy")

DT = 0.05
STEPS = 180
PUSH_SCALE = 0.12
TOP_K = 5

# directions to test
DIRECTIONS = {
    "right": np.array([1.0, 0.0]),
    "left":  np.array([-1.0, 0.0]),
    "up":    np.array([0.0, 1.0]),
    "down":  np.array([0.0, -1.0]),
    "diag1": np.array([1.0, 1.0]),
    "diag2": np.array([1.0, -1.0]),
    "diag3": np.array([-1.0, 1.0]),
    "diag4": np.array([-1.0, -1.0]),
}

# ============================================================
# LOAD GATE POINTS
# ============================================================

gate_points = np.load(gate_points_path)
gate_values = np.load(gate_values_path)

gate_points = gate_points[:TOP_K]
gate_values = gate_values[:TOP_K]

# ============================================================
# FIELD DEFINITION
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(-((x - center[0])**2 + (y - center[1])**2) / (2 * sigma**2))

def scalar_field(x, y):
    return (
        gaussian(x, y, clusters["C0"], 1.5)
        + gaussian(x, y, clusters["C1"], 2.0)
        + gaussian(x, y, clusters["C2"], 3.0)
        - gaussian(x, y, clusters["C3"], 2.0)
    )

def grad_field(x, y, eps=1e-4):
    dx = (scalar_field(x + eps, y) - scalar_field(x - eps, y)) / (2 * eps)
    dy = (scalar_field(x, y + eps) - scalar_field(x, y - eps)) / (2 * eps)
    return np.array([dx, dy])

def rotational_field(x, y):
    p = np.array([x, y], dtype=float)
    v = np.zeros(2)

    r2 = p - clusters["C2"]
    d2 = np.linalg.norm(r2) + 1e-9
    v += 0.6 * np.array([r2[1], -r2[0]]) * np.exp(-(d2**2)/(2*1.6**2))

    r3 = p - clusters["C3"]
    d3 = np.linalg.norm(r3) + 1e-9
    v += 0.55 * np.array([-r3[1], r3[0]]) * np.exp(-(d3**2)/(2*1.3**2))

    return v

def field(x):
    return grad_field(x[0], x[1]) + rotational_field(x[0], x[1])

# ============================================================
# SIMULATION
# ============================================================

def simulate(x0):
    x = x0.copy()
    traj = [x.copy()]

    for _ in range(STEPS):
        v = field(x)
        x = x + DT * v
        traj.append(x.copy())

    return np.array(traj)

# ============================================================
# CLASSIFICATION (simple basin check)
# ============================================================

def classify_endpoint(x):
    dists = {k: np.linalg.norm(x - v) for k, v in clusters.items()}
    return min(dists, key=dists.get)

# ============================================================
# RUN TESTS
# ============================================================

results = []

plt.figure(figsize=(10, 7))

for i, (p, val) in enumerate(zip(gate_points, gate_values)):

    for name, d in DIRECTIONS.items():

        d_norm = d / (np.linalg.norm(d) + 1e-9)
        start = p + PUSH_SCALE * d_norm

        traj = simulate(start)
        end = traj[-1]
        target = classify_endpoint(end)

        results.append((i, name, target))

        plt.plot(traj[:, 0], traj[:, 1], alpha=0.5)

    # mark gate point
    plt.scatter(p[0], p[1], s=120, c="white", edgecolor="black")

# draw cluster centers
for k, c in clusters.items():
    plt.scatter(c[0], c[1], s=150, label=k)

plt.title("V8.5 — Injection Tests from Gate Points")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)

save_run_info(
    __file__,
    extra={
        "tested_gate_points": int(len(gate_points)),
        "directions_per_point": int(len(DIRECTIONS)),
    }
)

# optional: print results summary
print("\n--- INJECTION RESULTS ---")
for r in results:
    print(f"G{r[0]+1} | {r[1]} -> {r[2]}")

print("Done.")

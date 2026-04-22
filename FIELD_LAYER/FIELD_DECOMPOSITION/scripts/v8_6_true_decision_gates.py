# ENGINE/analysis/field_decomposition/scripts/v8_6_true_decision_gates.py

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# SAVE
# ============================================================

def save_figure(script_path):
    name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = f"ENGINE/analysis/field_decomposition/outputs/{name}"
    os.makedirs(outdir, exist_ok=True)
    path = f"{outdir}/{name}.png"
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"✓ saved -> {path}")
    return outdir

def save_run_info(script_path, extra=None):
    name = os.path.splitext(os.path.basename(script_path))[0]
    outdir = f"ENGINE/analysis/field_decomposition/outputs/{name}"
    os.makedirs(outdir, exist_ok=True)
    with open(f"{outdir}/run_info.txt", "w") as f:
        f.write(f"script: {name}\n")
        f.write(f"time: {datetime.now()}\n")
        if extra:
            for k, v in extra.items():
                f.write(f"{k}: {v}\n")

# ============================================================
# LOAD DATA
# ============================================================

BASE = "ENGINE/analysis/field_decomposition/outputs"

boundary = np.load(f"{BASE}/v7_4/boundary_map.npy")
L = np.load(f"{BASE}/v8_0_lyapunov_map/lyapunov_map.npy")
xv = np.load(f"{BASE}/v8_0_lyapunov_map/grid_x.npy")
yv = np.load(f"{BASE}/v8_0_lyapunov_map/grid_y.npy")

X, Y = np.meshgrid(xv, yv)

boundary_mask = boundary > 0.5

# ============================================================
# FIELD (same as before)
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(-((x-center[0])**2 + (y-center[1])**2)/(2*sigma**2))

def scalar_field(x, y):
    return (
        gaussian(x, y, clusters["C0"], 1.5)
        + gaussian(x, y, clusters["C1"], 2.0)
        + gaussian(x, y, clusters["C2"], 3.0)
        - gaussian(x, y, clusters["C3"], 2.0)
    )

def grad(x, y, eps=1e-4):
    dx = (scalar_field(x+eps,y)-scalar_field(x-eps,y))/(2*eps)
    dy = (scalar_field(x,y+eps)-scalar_field(x,y-eps))/(2*eps)
    return np.array([dx,dy])

def rot(x, y):
    p = np.array([x,y])
    v = np.zeros(2)

    r2 = p - clusters["C2"]
    v += 0.6 * np.array([r2[1], -r2[0]]) * np.exp(-(np.linalg.norm(r2)**2)/(2*1.6**2))

    r3 = p - clusters["C3"]
    v += 0.55 * np.array([-r3[1], r3[0]]) * np.exp(-(np.linalg.norm(r3)**2)/(2*1.3**2))

    return v

def field(x):
    return grad(x[0],x[1]) + rot(x[0],x[1])

# ============================================================
# SIMULATION
# ============================================================

def simulate(x0, steps=120):
    x = x0.copy()
    for _ in range(steps):
        x = x + 0.05 * field(x)
    return x

def classify(x):
    d = {k: np.linalg.norm(x - v) for k,v in clusters.items()}
    return min(d, key=d.get)

# ============================================================
# SEARCH DECISION GATES
# ============================================================

DIRECTIONS = [
    np.array([1,0]), np.array([-1,0]),
    np.array([0,1]), np.array([0,-1]),
    np.array([1,1]), np.array([1,-1]),
    np.array([-1,1]), np.array([-1,-1]),
]

decision_points = []

print("Searching decision gates...")

for i in range(0, len(xv), 3):
    for j in range(0, len(yv), 3):

        if not boundary_mask[j,i]:
            continue

        p = np.array([X[j,i], Y[j,i]])

        outcomes = set()

        for d in DIRECTIONS:
            d = d / (np.linalg.norm(d)+1e-9)
            end = simulate(p + 0.08*d)
            outcomes.add(classify(end))

        if len(outcomes) >= 2:
            decision_points.append((p[0], p[1], len(outcomes)))

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10,6))

plt.contourf(X, Y, L, levels=60, cmap="inferno")

if decision_points:
    dp = np.array(decision_points)
    plt.scatter(dp[:,0], dp[:,1], c="cyan", s=50, label="decision gates")

for name, c in clusters.items():
    plt.scatter(c[0], c[1], s=120, label=name)

plt.legend()
plt.title("V8.6 — True Decision Gates")
plt.xlabel("x")
plt.ylabel("y")

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)

np.save(f"{outdir}/decision_points.npy", decision_points)

save_run_info(__file__, {
    "num_decision_points": len(decision_points)
})

print(f"\nFound {len(decision_points)} decision gates")

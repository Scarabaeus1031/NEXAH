# ENGINE/analysis/field_decomposition/scripts/v8_0_lyapunov_map.py

import os
from datetime import datetime

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# LOCAL SAVE (NO IMPORT)
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
# PARAMETERS
# ============================================================

DT = 0.05
STEPS = 80
EPS = 1e-4
GRID_RES = 60

# ============================================================
# FIELD
# ============================================================

clusters = {
    "C0": np.array([10.0, 25.0]),
    "C1": np.array([12.0, 24.0]),
    "C2": np.array([13.5, 26.0]),
    "C3": np.array([11.0, 28.5]),
}

def gaussian(x, y, center, strength, sigma=1.2):
    return strength * np.exp(
        -((x - center[0])**2 + (y - center[1])**2) / (2 * sigma**2)
    )

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
    v += 0.6 * np.array([r2[1], -r2[0]]) * np.exp(-(d2**2) / (2 * 1.6**2))

    r3 = p - clusters["C3"]
    d3 = np.linalg.norm(r3) + 1e-9
    v += 0.55 * np.array([-r3[1], r3[0]]) * np.exp(-(d3**2) / (2 * 1.3**2))

    return v

def field(x):
    return grad_field(x[0], x[1]) + rotational_field(x[0], x[1])

# ============================================================
# SIMULATION
# ============================================================

def simulate(x0):
    x = x0.copy()
    traj = []

    for _ in range(STEPS):
        v = field(x)
        x = x + DT * v
        traj.append(x.copy())

    return np.array(traj)

# ============================================================
# LYAPUNOV
# ============================================================

def lyapunov_at_point(x0):
    x1 = x0.copy()
    x2 = x0 + np.array([EPS, 0.0])

    traj1 = simulate(x1)
    traj2 = simulate(x2)

    d0 = np.linalg.norm(x2 - x1) + 1e-12
    dT = np.linalg.norm(traj2[-1] - traj1[-1]) + 1e-12

    return np.log(dT / d0) / (STEPS * DT)

# ============================================================
# GRID
# ============================================================

xv = np.linspace(8, 16, GRID_RES)
yv = np.linspace(23, 30, GRID_RES)

X, Y = np.meshgrid(xv, yv)
L = np.zeros_like(X)

print("Computing Lyapunov map...")

for i in range(GRID_RES):
    for j in range(GRID_RES):
        x0 = np.array([X[i, j], Y[i, j]])
        L[i, j] = lyapunov_at_point(x0)

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(10, 6))
plt.contourf(X, Y, L, levels=60, cmap="inferno")
plt.colorbar(label="Lyapunov exponent")
plt.title("V8.0 — Lyapunov Map (Stability Field)")
plt.xlabel("x")
plt.ylabel("y")

# optional cluster markers
for name, c in clusters.items():
    plt.scatter(c[0], c[1], s=50, edgecolor="black", linewidth=0.8, label=name)

plt.legend(loc="upper right", fontsize=8)

# ============================================================
# SAVE
# ============================================================

outdir = save_figure(__file__)
np.save(os.path.join(outdir, "lyapunov_map.npy"), L)
np.save(os.path.join(outdir, "grid_x.npy"), xv)
np.save(os.path.join(outdir, "grid_y.npy"), yv)

save_run_info(
    __file__,
    extra={
        "DT": DT,
        "STEPS": STEPS,
        "EPS": EPS,
        "GRID_RES": GRID_RES,
    },
)

print("Done.")

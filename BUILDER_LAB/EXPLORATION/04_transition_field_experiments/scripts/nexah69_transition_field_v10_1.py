import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------
# CONFIG
# ----------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASE = "ieee118"

PRED_STEPS = 35
STEP = 0.03

# ----------------------------
# LOAD
# ----------------------------

df = pd.read_csv(BASE_PATH / f"{CASE}_v43_dataset.csv").dropna()
cloud = pd.read_csv(BASE_PATH / f"{CASE}_v68_off_manifold_cloud.csv").dropna()

def norm(x):
    m = np.max(np.abs(x))
    return x if m == 0 else x/m

c = norm(df["c"].values)
dc = norm(df["dc"].values)
traj = np.column_stack([c, dc])

# ----------------------------
# BASICS
# ----------------------------

def unit(v):
    n = np.linalg.norm(v)
    return v/n if n > 0 else np.zeros_like(v)

def nearest(p):
    d = traj - p
    i = np.argmin(np.sum(d*d, axis=1))
    return i, traj[i]

def tangent(i):
    if i <= 0: v = traj[1]-traj[0]
    elif i >= len(traj)-1: v = traj[-1]-traj[-2]
    else: v = traj[i+1]-traj[i-1]
    return unit(v)

def density(p):
    d = traj - p
    dist = np.sqrt(np.sum(d*d, axis=1))
    return np.exp(-np.mean(np.sort(dist)[:20]))

theta = np.unwrap(np.arctan2(traj[:,1], traj[:,0]))
omega = np.gradient(theta)
omega_mean = np.mean(omega)

# ----------------------------
# CONTROL MODES
# ----------------------------

def naive_vec(p, target):
    return unit(target - p)

def phase_vec(p, target):
    i, _ = nearest(p)
    t = tangent(i)
    return unit(0.7*t + 0.6*(target-p))

def nexah_vec(p, target):
    i, near = nearest(p)
    t = tangent(i)

    dens = density(p)
    gate = 1 - dens
    mismatch = abs(omega[i] - omega_mean)

    perp = np.array([-t[1], t[0]])

    v = (
        0.7*t
        + 0.1*(near - p)
        + 0.5*(gate*perp)
        + 0.4*(mismatch*perp)
        + 1.2*(target - p)
        + 1.0*(gate*unit(near - p))
    )

    return unit(v)

# ----------------------------
# SIMULATION
# ----------------------------

def simulate(start, target, mode):

    p = start.copy()
    path = [p.copy()]

    for _ in range(PRED_STEPS):

        if mode == "naive":
            v = naive_vec(p, target)
        elif mode == "phase":
            v = phase_vec(p, target)
        else:
            v = nexah_vec(p, target)

        p = p + STEP*v
        path.append(p.copy())

    return np.array(path)

# ----------------------------
# DOMAIN
# ----------------------------

xmin, xmax = cloud["c"].min(), cloud["c"].max()
ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

target = np.array([
    xmin + 0.7*(xmax-xmin),
    ymin + 0.6*(ymax-ymin)
])

# ----------------------------
# FIGURE
# ----------------------------

fig, axs = plt.subplots(1, 3, figsize=(15, 5))
titles = ["Naive Control", "Phase-Aware", "NEXAH Control"]

# choose snapshot point
IDX = int(len(traj) * 0.6)
sub = traj[:IDX]
current = sub[-1]

modes = ["naive", "phase", "nexah"]
paths = []

for i, (ax, mode, title) in enumerate(zip(axs, modes, titles)):

    ax.set_facecolor("black")
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_title(title, color="white")

    # background trajectory
    ax.plot(traj[:,0], traj[:,1], color="white", alpha=0.05, lw=1)
    ax.plot(sub[:,0], sub[:,1], color="white", alpha=0.2, lw=1)

    # simulate path
    path = simulate(current, target, mode)
    paths.append(path)

    ax.plot(path[:,0], path[:,1], lw=2)
    ax.scatter(*current, color="white", s=30)
    ax.scatter(*target, color="red", s=60)

# ----------------------------
# LABELS
# ----------------------------

labels = [
    "direct path\n(ignores structure)",
    "follows drift\n(partial alignment)",
    "structure-aware\nnavigation"
]

for i, ax in enumerate(axs):
    path = paths[i]
    mid = path[len(path)//2]

    ax.text(
        mid[0], mid[1],
        labels[i],
        color="white",
        fontsize=9,
        ha="center",
        va="bottom"
    )

# target label
for ax in axs:
    ax.text(
        target[0], target[1],
        "target",
        color="red",
        fontsize=9,
        ha="left",
        va="bottom"
    )

# current label (middle panel)
axs[1].text(
    current[0], current[1],
    "current state",
    color="white",
    fontsize=8,
    ha="right",
    va="top"
)

# ----------------------------
# TITLE
# ----------------------------

fig.suptitle(
    "NEXAH Control Comparison — From Force to Structure",
    color="white",
    fontsize=14
)

plt.tight_layout()
plt.subplots_adjust(top=0.88)

# ----------------------------
# SAVE
# ----------------------------

out = BASE_PATH / f"{CASE}_v10_annotated.png"
plt.savefig(out, dpi=260, facecolor="black")
plt.close()

print(f"[OK] saved → {out}")

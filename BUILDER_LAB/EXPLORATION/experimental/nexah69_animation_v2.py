import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASE = "ieee118"

GRID_RES = 35

ALPHA_RETURN = 0.15
ALPHA_DRIFT = 0.8

PHASE_SPEED = 0.02
SWIRL_STRENGTH = 0.6
NOISE_STRENGTH = 0.05

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_dataset(case):
    return pd.read_csv(BASE_PATH / f"{case}_v43_dataset.csv").dropna()

def load_off_field(case):
    return pd.read_csv(BASE_PATH / f"{case}_v68_off_manifold_cloud.csv").dropna()

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    m = np.max(np.abs(x))
    return x if m == 0 else x / m

def nearest_traj_point(px, py, traj):
    diff = traj - np.array([px, py])
    idx = np.argmin(np.sum(diff**2, axis=1))
    return idx, traj[idx]

def local_tangent(traj, idx):
    if idx == 0:
        v = traj[1] - traj[0]
    elif idx == len(traj) - 1:
        v = traj[-1] - traj[-2]
    else:
        v = traj[idx + 1] - traj[idx - 1]

    n = np.linalg.norm(v)
    return v / n if n > 0 else np.zeros(2)

# --------------------------------------------------
# GRID
# --------------------------------------------------

def build_grid(xmin, xmax, ymin, ymax, res):
    xs = np.linspace(xmin, xmax, res)
    ys = np.linspace(ymin, ymax, res)
    return np.meshgrid(xs, ys)

# --------------------------------------------------
# 🔥 DYNAMIC FIELD (SWARM)
# --------------------------------------------------

def build_dynamic_field(traj, X, Y, t):

    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    phase = PHASE_SPEED * t

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            px, py = X[i, j], Y[i, j]

            idx, nearest = nearest_traj_point(px, py, traj)
            tangent = local_tangent(traj, idx)

            # ----------------------------------
            # 1. BASE DRIFT (entlang trajectory)
            # ----------------------------------
            drift = ALPHA_DRIFT * tangent

            # ----------------------------------
            # 2. RETURN (zur Struktur)
            # ----------------------------------
            return_vec = ALPHA_RETURN * (nearest - np.array([px, py]))

            # ----------------------------------
            # 3. SWIRL (🔥 neu!)
            # ----------------------------------
            swirl = SWIRL_STRENGTH * np.array([
                - (py - nearest[1]),
                  (px - nearest[0])
            ])

            # ----------------------------------
            # 4. PHASE ROTATION (global motion)
            # ----------------------------------
            rot = np.array([
                np.cos(phase) * drift[0] - np.sin(phase) * drift[1],
                np.sin(phase) * drift[0] + np.cos(phase) * drift[1]
            ])

            # ----------------------------------
            # 5. SMALL NOISE (organisch)
            # ----------------------------------
            noise = NOISE_STRENGTH * np.random.randn(2)

            vec = rot + return_vec + swirl + noise

            U[i, j] = vec[0]
            V[i, j] = vec[1]

    return U, V

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("🔥 NEXAH V2 — SWARM FIELD")

    df = load_dataset(CASE)
    cloud = load_off_field(CASE)

    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)

    traj = np.column_stack([c, dc])
    T = len(traj)

    xmin, xmax = cloud["c"].min(), cloud["c"].max()
    ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

    X, Y = build_grid(xmin, xmax, ymin, ymax, GRID_RES)

    # ------------------------------------------
    # PHASE COLOR (dein Layer bleibt drin)
    # ------------------------------------------

    theta = np.unwrap(np.arctan2(dc, c))
    phase_norm = (theta - theta.min()) / (theta.max() - theta.min())
    colors = plt.cm.hsv(phase_norm)

    # ------------------------------------------
    # FIGURE
    # ------------------------------------------

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_facecolor("white")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_xticks([])
    ax.set_yticks([])

    # initial field
    U, V = build_dynamic_field(traj, X, Y, 0)

    quiver = ax.quiver(X, Y, U, V, color="black", alpha=0.2, scale=2)

    line, = ax.plot([], [], color="black", lw=2)
    scatter = ax.scatter([], [], s=8)

    title = ax.text(0.5, 1.02, "", transform=ax.transAxes, ha="center")

    # ------------------------------------------
    # UPDATE
    # ------------------------------------------

    def update(frame):

        U, V = build_dynamic_field(traj, X, Y, frame)

        quiver.set_UVC(U, V)

        x = traj[:frame, 0]
        y = traj[:frame, 1]

        line.set_data(x, y)

        scatter.set_offsets(np.c_[x, y])
        scatter.set_color(colors[:frame])

        title.set_text(f"NEXAH Swarm Field — t={frame}")

        return quiver, line, scatter, title

    # ------------------------------------------
    # ANIMATION
    # ------------------------------------------

    anim = FuncAnimation(
        fig,
        update,
        frames=min(T, 400),   # begrenzen für speed
        interval=30
    )

    out = BASE_PATH / f"{CASE}_v2_swarm_field.gif"
    anim.save(out, writer="pillow", fps=25)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()

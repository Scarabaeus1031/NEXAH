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
GRID_RES = 45

ALPHA_RETURN = 0.18
ALPHA_DRIFT = 0.85

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_dataset(case):
    path = BASE_PATH / f"{case}_v43_dataset.csv"
    return pd.read_csv(path).dropna()

def load_off_field(case):
    path = BASE_PATH / f"{case}_v68_off_manifold_cloud.csv"
    return pd.read_csv(path).dropna()

# --------------------------------------------------
# HELPERS (dein Code)
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    m = np.max(np.abs(x))
    return x if m == 0 else x / m

def nearest_traj_point(px, py, traj):
    diff = traj - np.array([px, py])
    dist2 = np.sum(diff**2, axis=1)
    idx = np.argmin(dist2)
    return idx, traj[idx]

def local_tangent(traj, idx):
    if idx == 0:
        v = traj[1] - traj[0]
    elif idx == len(traj) - 1:
        v = traj[-1] - traj[-2]
    else:
        v = traj[idx + 1] - traj[idx - 1]

    n = np.linalg.norm(v)
    return np.array([0.0, 0.0]) if n == 0 else v / n

# --------------------------------------------------
# FLOW FIELD
# --------------------------------------------------

def build_flow_field(traj, xmin, xmax, ymin, ymax, grid_res=45):
    xs = np.linspace(xmin, xmax, grid_res)
    ys = np.linspace(ymin, ymax, grid_res)
    X, Y = np.meshgrid(xs, ys)

    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            px, py = X[i, j], Y[i, j]

            idx, nearest = nearest_traj_point(px, py, traj)
            tangent = local_tangent(traj, idx)

            drift = ALPHA_DRIFT * tangent
            return_vec = ALPHA_RETURN * (nearest - np.array([px, py]))

            vec = drift + return_vec

            U[i, j], V[i, j] = vec

    return X, Y, U, V

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("NEXAH V69 — CLEAN ANIMATION")

    df = load_dataset(CASE)
    cloud = load_off_field(CASE)

    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)

    trajectory = np.column_stack([c, dc])
    T = len(trajectory)

    xmin, xmax = cloud["c"].min(), cloud["c"].max()
    ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

    X, Y, U, V = build_flow_field(trajectory, xmin, xmax, ymin, ymax)

    # --------------------------------------------------
    # PHASE (dein neuer Layer 🔥)
    # --------------------------------------------------

    theta = np.unwrap(np.arctan2(dc, c))
    phase_norm = (theta - theta.min()) / (theta.max() - theta.min())
    colors = plt.cm.hsv(phase_norm)

    # --------------------------------------------------
    # FIGURE (clean)
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_facecolor("white")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    ax.set_xticks([])
    ax.set_yticks([])

    # flow (leicht!)
    quiver = ax.quiver(X, Y, U, V, color="black", alpha=0.15, scale=2)

    # trajectory
    line, = ax.plot([], [], color="black", lw=2)

    # phase points
    scatter = ax.scatter([], [], s=8)

    # drift text
    drift_text = ax.text(0.02, 0.95, "", transform=ax.transAxes, fontsize=9)

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(frame):

        x = trajectory[:frame, 0]
        y = trajectory[:frame, 1]

        line.set_data(x, y)

        scatter.set_offsets(np.c_[x, y])
        scatter.set_color(colors[:frame])

        if frame > 20:
            drift = np.mean(np.diff(theta[:frame]))
            drift_text.set_text(f"μΔθ ≈ {drift:.4f}")

        return line, scatter, drift_text

    # --------------------------------------------------
    # ANIMATION
    # --------------------------------------------------

    anim = FuncAnimation(
        fig,
        update,
        frames=T,
        interval=20
    )

    out_path = BASE_PATH / f"{CASE}_v69_flow_animation.gif"
    anim.save(out_path, writer="pillow", fps=30)

    print(f"Saved animation: {out_path}")


if __name__ == "__main__":
    main()

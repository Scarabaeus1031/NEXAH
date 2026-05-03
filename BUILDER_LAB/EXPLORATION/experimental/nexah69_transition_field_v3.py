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

ALPHA_RETURN = 0.12
ALPHA_DRIFT = 0.7

GATE_STRENGTH = 1.2
PHASE_RESPONSE = 0.8

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
# 🔥 STRUCTURAL COMPONENTS
# --------------------------------------------------

def estimate_density(px, py, traj, k=20):
    diff = traj - np.array([px, py])
    dist = np.sqrt(np.sum(diff**2, axis=1))
    return np.exp(-np.mean(np.sort(dist)[:k]))

def estimate_phase(traj):
    return np.unwrap(np.arctan2(traj[:,1], traj[:,0]))

def compute_phase_velocity(theta):
    return np.gradient(theta)

# --------------------------------------------------
# 🔥 FIELD WITH STRUCTURE
# --------------------------------------------------

def build_transition_field(traj, theta, omega, X, Y, t):

    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    mean_omega = np.mean(omega)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):

            px, py = X[i, j], Y[i, j]

            idx, nearest = nearest_traj_point(px, py, traj)
            tangent = local_tangent(traj, idx)

            # ----------------------------------
            # 1. BASE FLOW
            # ----------------------------------
            drift = ALPHA_DRIFT * tangent

            # ----------------------------------
            # 2. RETURN TO STRUCTURE
            # ----------------------------------
            return_vec = ALPHA_RETURN * (nearest - np.array([px, py]))

            # ----------------------------------
            # 3. GATE DETECTION
            # ----------------------------------
            density = estimate_density(px, py, traj)
            gate = 1 - density   # low density = gate

            # ----------------------------------
            # 4. PHASE MISMATCH
            # ----------------------------------
            local_omega = omega[idx]
            mismatch = np.abs(local_omega - mean_omega)

            # ----------------------------------
            # 5. TRANSITION ACTIVATION
            # ----------------------------------
            activation = GATE_STRENGTH * gate * PHASE_RESPONSE * mismatch

            # ----------------------------------
            # 6. DIRECTIONAL PUSH (🔥 KEY!)
            # ----------------------------------
            perp = np.array([-tangent[1], tangent[0]])

            transition_vec = activation * perp

            # ----------------------------------
            # FINAL VECTOR
            # ----------------------------------
            vec = drift + return_vec + transition_vec

            U[i, j] = vec[0]
            V[i, j] = vec[1]

    return U, V

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("🔥 NEXAH V3 — TRANSITION FIELD")

    df = load_dataset(CASE)
    cloud = load_off_field(CASE)

    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)

    traj = np.column_stack([c, dc])

    xmin, xmax = cloud["c"].min(), cloud["c"].max()
    ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

    xs = np.linspace(xmin, xmax, GRID_RES)
    ys = np.linspace(ymin, ymax, GRID_RES)
    X, Y = np.meshgrid(xs, ys)

    # ------------------------------------------
    # PHASE SYSTEM
    # ------------------------------------------

    theta = estimate_phase(traj)
    omega = compute_phase_velocity(theta)

    phase_norm = (theta - theta.min()) / (theta.max() - theta.min())
    colors = plt.cm.hsv(phase_norm)

    # ------------------------------------------
    # FIGURE
    # ------------------------------------------

    fig, ax = plt.subplots(figsize=(6,6))
    ax.set_facecolor("white")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([])
    ax.set_yticks([])

    U, V = build_transition_field(traj, theta, omega, X, Y, 0)

    quiver = ax.quiver(X, Y, U, V, color="black", alpha=0.25, scale=2)

    line, = ax.plot([], [], color="black", lw=2)
    scatter = ax.scatter([], [], s=10)

    title = ax.text(0.5, 1.02, "", transform=ax.transAxes, ha="center")

    # ------------------------------------------
    # UPDATE
    # ------------------------------------------

    def update(frame):

        U, V = build_transition_field(traj, theta, omega, X, Y, frame)
        quiver.set_UVC(U, V)

        x = traj[:frame,0]
        y = traj[:frame,1]

        line.set_data(x, y)
        scatter.set_offsets(np.c_[x, y])
        scatter.set_color(colors[:frame])

        title.set_text(f"NEXAH Transition Field — t={frame}")

        return quiver, line, scatter, title

    anim = FuncAnimation(
        fig,
        update,
        frames=min(len(traj), 400),
        interval=30
    )

    out = BASE_PATH / f"{CASE}_v3_transition_field.gif"
    anim.save(out, writer="pillow", fps=25)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()

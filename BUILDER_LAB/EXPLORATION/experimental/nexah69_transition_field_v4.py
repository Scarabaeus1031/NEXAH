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

GRID_RES = 40

ALPHA_RETURN = 0.12
ALPHA_DRIFT = 0.7

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
    m = np.max(np.abs(x))
    return x if m == 0 else x / m

def nearest_traj_point(px, py, traj):
    diff = traj - np.array([px, py])
    idx = np.argmin(np.sum(diff**2, axis=1))
    return idx, traj[idx]

def local_tangent(traj, idx):
    if idx == 0:
        v = traj[1] - traj[0]
    elif idx == len(traj)-1:
        v = traj[-1] - traj[-2]
    else:
        v = traj[idx+1] - traj[idx-1]
    n = np.linalg.norm(v)
    return v/n if n > 0 else np.zeros(2)

# --------------------------------------------------
# STRUCTURE ESTIMATION
# --------------------------------------------------

def estimate_density(px, py, traj, k=25):
    diff = traj - np.array([px, py])
    dist = np.sqrt(np.sum(diff**2, axis=1))
    return np.exp(-np.mean(np.sort(dist)[:k]))

def estimate_phase(traj):
    return np.unwrap(np.arctan2(traj[:,1], traj[:,0]))

def compute_phase_velocity(theta):
    return np.gradient(theta)

# --------------------------------------------------
# FIELD + MAPS
# --------------------------------------------------

def build_all_maps(traj, theta, omega, X, Y):

    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    gate_map = np.zeros_like(X)
    mismatch_map = np.zeros_like(X)
    activation_map = np.zeros_like(X)

    mean_omega = np.mean(omega)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):

            px, py = X[i,j], Y[i,j]

            idx, nearest = nearest_traj_point(px, py, traj)
            tangent = local_tangent(traj, idx)

            # --- base flow
            drift = ALPHA_DRIFT * tangent
            return_vec = ALPHA_RETURN * (nearest - np.array([px, py]))

            # --- structure
            density = estimate_density(px, py, traj)
            gate = 1 - density

            # --- phase mismatch
            mismatch = abs(omega[idx] - mean_omega)

            # --- activation
            activation = gate * mismatch

            # --- transition direction
            perp = np.array([-tangent[1], tangent[0]])
            transition_vec = activation * perp

            vec = drift + return_vec + transition_vec

            U[i,j] = vec[0]
            V[i,j] = vec[1]

            gate_map[i,j] = gate
            mismatch_map[i,j] = mismatch
            activation_map[i,j] = activation

    return U, V, gate_map, mismatch_map, activation_map

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("🔥 NEXAH V4 — GATE + PHASE FIELD")

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

    theta = estimate_phase(traj)
    omega = compute_phase_velocity(theta)

    # --------------------------------------------------
    # FIGURE (3 LAYERS)
    # --------------------------------------------------

    fig, axes = plt.subplots(1, 3, figsize=(15,5))

    titles = ["Gate (low density)", "Phase Mismatch", "Activation (Transition)"]

    for ax, t in zip(axes, titles):
        ax.set_title(t)
        ax.set_xticks([])
        ax.set_yticks([])

    # initial
    U, V, G, M, A = build_all_maps(traj, theta, omega, X, Y)

    im1 = axes[0].imshow(G, origin='lower', cmap='inferno')
    im2 = axes[1].imshow(M, origin='lower', cmap='viridis')
    im3 = axes[2].imshow(A, origin='lower', cmap='plasma')

    # overlay flow on activation
    quiver = axes[2].quiver(X, Y, U, V, color="white", alpha=0.3, scale=3)

    # trajectory
    line, = axes[2].plot([], [], color="white", lw=2)

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(frame):

        sub_traj = traj[:frame+10]

        U, V, G, M, A = build_all_maps(sub_traj, theta, omega, X, Y)

        im1.set_data(G)
        im2.set_data(M)
        im3.set_data(A)

        quiver.set_UVC(U, V)

        line.set_data(sub_traj[:,0], sub_traj[:,1])

        return im1, im2, im3, quiver, line

    anim = FuncAnimation(
        fig,
        update,
        frames=min(len(traj)-10, 300),
        interval=40
    )

    out = BASE_PATH / f"{CASE}_v4_transition_maps.gif"
    anim.save(out, writer="pillow", fps=20)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()

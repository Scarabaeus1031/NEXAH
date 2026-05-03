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

ALPHA_RETURN = 0.12
ALPHA_DRIFT = 0.7

PRED_STEPS = 25
FRAME_SKIP = 2   # smoother + longer animation
FPS = 25

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
# STRUCTURE
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
# FIELD + PROBABILITY
# --------------------------------------------------

def build_field_and_prob(traj, theta, omega, X, Y):

    U = np.zeros_like(X)
    V = np.zeros_like(Y)
    P = np.zeros_like(X)

    mean_omega = np.mean(omega)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):

            px, py = X[i,j], Y[i,j]

            idx, nearest = nearest_traj_point(px, py, traj)
            tangent = local_tangent(traj, idx)

            drift = ALPHA_DRIFT * tangent
            return_vec = ALPHA_RETURN * (nearest - np.array([px, py]))

            density = estimate_density(px, py, traj)
            gate = 1 - density

            mismatch = abs(omega[idx] - mean_omega)

            activation = gate * mismatch

            # normalize probability locally
            P[i,j] = activation

            perp = np.array([-tangent[1], tangent[0]])
            transition_vec = activation * perp

            vec = drift + return_vec + transition_vec

            U[i,j] = vec[0]
            V[i,j] = vec[1]

    # normalize probability map
    P = P / (np.max(P) + 1e-8)

    return U, V, P

# --------------------------------------------------
# 🔮 PREDICTION
# --------------------------------------------------

def predict_future(point, traj, theta, omega, steps=20):

    path = [point.copy()]

    for _ in range(steps):

        idx, nearest = nearest_traj_point(point[0], point[1], traj)
        tangent = local_tangent(traj, idx)

        drift = ALPHA_DRIFT * tangent
        return_vec = ALPHA_RETURN * (nearest - point)

        mismatch = abs(omega[idx] - np.mean(omega))
        perp = np.array([-tangent[1], tangent[0]])

        step_vec = drift + return_vec + mismatch * perp

        point = point + 0.02 * step_vec
        path.append(point.copy())

    return np.array(path)

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("🔥 NEXAH V5 — PREDICTION FIELD")

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
    # FIGURE
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_facecolor("black")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([])
    ax.set_yticks([])

    U, V, P = build_field_and_prob(traj, theta, omega, X, Y)

    prob_map = ax.imshow(P, origin='lower', cmap='plasma', alpha=0.6)

    quiver = ax.quiver(X, Y, U, V, color="white", alpha=0.25, scale=3)

    line, = ax.plot([], [], color="white", lw=2)
    pred_line, = ax.plot([], [], color="cyan", lw=2, linestyle="--")

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(frame):

        idx = frame * FRAME_SKIP

        sub_traj = traj[:idx+10]

        U, V, P = build_field_and_prob(sub_traj, theta, omega, X, Y)

        prob_map.set_data(P)
        quiver.set_UVC(U, V)

        line.set_data(sub_traj[:,0], sub_traj[:,1])

        # 🔮 prediction
        current = sub_traj[-1]
        future = predict_future(current, traj, theta, omega, PRED_STEPS)

        pred_line.set_data(future[:,0], future[:,1])

        return prob_map, quiver, line, pred_line

    frames = min(len(traj)//FRAME_SKIP, 500)

    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=40
    )

    out = BASE_PATH / f"{CASE}_v5_prediction_field.gif"
    anim.save(out, writer="pillow", fps=FPS)

    print(f"Saved: {out}")


if __name__ == "__main__":
    main()

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

GRID_RES = 30
BINS = 20   # discretization

FPS = 25
FRAME_SKIP = 2

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

# --------------------------------------------------
# 🔥 LEARNING TRANSITIONS
# --------------------------------------------------

def build_transition_model(traj):

    # discretize space
    x = traj[:,0]
    y = traj[:,1]

    x_bins = np.linspace(x.min(), x.max(), BINS)
    y_bins = np.linspace(y.min(), y.max(), BINS)

    # store counts
    model = {}

    dx = np.gradient(x)
    dy = np.gradient(y)

    for t in range(len(traj)-1):

        xi = np.digitize(x[t], x_bins)
        yi = np.digitize(y[t], y_bins)

        # direction vector
        vx, vy = dx[t], dy[t]
        norm = np.linalg.norm([vx,vy])

        if norm == 0:
            continue

        direction = (vx/norm, vy/norm)

        key = (xi, yi)

        if key not in model:
            model[key] = []

        model[key].append(direction)

    # average direction per cell
    learned = {}

    for key, dirs in model.items():
        arr = np.array(dirs)
        mean_dir = np.mean(arr, axis=0)
        learned[key] = mean_dir

    return learned, x_bins, y_bins

# --------------------------------------------------
# FIELD FROM MODEL
# --------------------------------------------------

def build_learned_field(model, x_bins, y_bins, X, Y):

    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):

            xi = np.digitize(X[i,j], x_bins)
            yi = np.digitize(Y[i,j], y_bins)

            key = (xi, yi)

            if key in model:
                vec = model[key]
            else:
                vec = np.array([0.0, 0.0])

            U[i,j] = vec[0]
            V[i,j] = vec[1]

    return U, V

# --------------------------------------------------
# 🔮 PREDICTION (LEARNED)
# --------------------------------------------------

def predict_learned(point, model, x_bins, y_bins, steps=20):

    path = [point.copy()]

    for _ in range(steps):

        xi = np.digitize(point[0], x_bins)
        yi = np.digitize(point[1], y_bins)

        key = (xi, yi)

        if key in model:
            vec = model[key]
        else:
            vec = np.zeros(2)

        point = point + 0.02 * vec
        path.append(point.copy())

    return np.array(path)

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("🔥 NEXAH V6 — LEARNED TRANSITION FIELD")

    df = load_dataset(CASE)
    cloud = load_off_field(CASE)

    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)

    traj = np.column_stack([c, dc])

    # --------------------------------------------------
    # LEARN MODEL
    # --------------------------------------------------

    model, x_bins, y_bins = build_transition_model(traj)

    xmin, xmax = cloud["c"].min(), cloud["c"].max()
    ymin, ymax = cloud["dc"].min(), cloud["dc"].max()

    xs = np.linspace(xmin, xmax, GRID_RES)
    ys = np.linspace(ymin, ymax, GRID_RES)
    X, Y = np.meshgrid(xs, ys)

    U, V = build_learned_field(model, x_bins, y_bins, X, Y)

    # --------------------------------------------------
    # FIGURE
    # --------------------------------------------------

    fig, ax = plt.subplots(figsize=(7,7))
    ax.set_facecolor("black")

    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xticks([])
    ax.set_yticks([])

    quiver = ax.quiver(X, Y, U, V, color="white", alpha=0.4, scale=2)

    line, = ax.plot([], [], color="white", lw=2)
    pred_line, = ax.plot([], [], color="cyan", lw=2, linestyle="--")

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(frame):

        idx = frame * FRAME_SKIP
        sub_traj = traj[:idx+10]

        line.set_data(sub_traj[:,0], sub_traj[:,1])

        current = sub_traj[-1]
        future = predict_learned(current, model, x_bins, y_bins)

        pred_line.set_data(future[:,0], future[:,1])

        return line, pred_line

    frames = min(len(traj)//FRAME_SKIP, 500)

    anim = FuncAnimation(
        fig,
        update,
        frames=frames,
        interval=40
    )

    out = BASE_PATH / f"{CASE}_v6_learned_field.gif"
    anim.save(out, writer="pillow", fps=FPS)

    print(f"Saved: {out}")

# --------------------------------------------------

if __name__ == "__main__":
    main()

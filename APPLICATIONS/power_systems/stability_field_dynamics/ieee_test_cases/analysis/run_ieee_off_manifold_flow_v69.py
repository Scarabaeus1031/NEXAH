import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

GRID_RES = 45
ALPHA_RETURN = 0.18   # Rückzug zur Trajectory
ALPHA_DRIFT = 0.85    # Drift entlang der Hauptbahn

# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_dataset(case):
    path = BASE_PATH / f"{case}_v43_dataset.csv"
    if not path.exists():
        print(f"Missing dataset: {path}")
        return None
    return pd.read_csv(path).dropna()


def load_off_field(case):
    path = BASE_PATH / f"{case}_v68_off_manifold_cloud.csv"
    if not path.exists():
        print(f"Missing off-manifold cloud: {path}")
        return None
    return pd.read_csv(path).dropna()

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize_safe(x):
    x = np.asarray(x, dtype=float)
    m = np.max(np.abs(x))
    if m == 0:
        return x
    return x / m


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
    if n == 0:
        return np.array([0.0, 0.0])
    return v / n

# --------------------------------------------------
# BUILD FLOW FIELD
# --------------------------------------------------

def build_flow_field(traj, xmin, xmax, ymin, ymax, grid_res=45):
    xs = np.linspace(xmin, xmax, grid_res)
    ys = np.linspace(ymin, ymax, grid_res)
    X, Y = np.meshgrid(xs, ys)

    U = np.zeros_like(X)
    V = np.zeros_like(Y)

    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            px = X[i, j]
            py = Y[i, j]

            idx, nearest = nearest_traj_point(px, py, traj)
            tangent = local_tangent(traj, idx)

            # Drift entlang der Bahn
            drift = ALPHA_DRIFT * tangent

            # Rückzug zur Bahn
            return_vec = nearest - np.array([px, py])
            return_vec = ALPHA_RETURN * return_vec

            vec = drift + return_vec

            U[i, j] = vec[0]
            V[i, j] = vec[1]

    return X, Y, U, V

# --------------------------------------------------
# MAIN CASE
# --------------------------------------------------

def process_case(case):
    print(f"\n--- {case.upper()} ---")

    df = load_dataset(case)
    cloud = load_off_field(case)

    if df is None or cloud is None:
        return

    c = normalize_safe(df["c"].values)
    dc = normalize_safe(df["dc"].values)

    traj = np.column_stack([c, dc])

    xmin = cloud["c"].min()
    xmax = cloud["c"].max()
    ymin = cloud["dc"].min()
    ymax = cloud["dc"].max()

    X, Y, U, V = build_flow_field(traj, xmin, xmax, ymin, ymax, grid_res=GRID_RES)

    # --------------------------------------------------
    # PLOT 1: VECTOR FIELD
    # --------------------------------------------------

    plt.figure(figsize=(9, 7))
    plt.quiver(X, Y, U, V, angles="xy", scale_units="xy", scale=1.8, alpha=0.8)
    plt.plot(c, dc, color="black", linewidth=2, label="trajectory")
    plt.title(f"{case.upper()} — OFF-MANIFOLD FLOW (V69)")
    plt.xlabel("c")
    plt.ylabel("dc")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v69_off_manifold_flow.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # PLOT 2: STREAM STYLE
    # --------------------------------------------------

    plt.figure(figsize=(9, 7))
    speed = np.sqrt(U**2 + V**2)
    plt.streamplot(X, Y, U, V, density=1.1, color=speed, cmap="viridis")
    plt.plot(c, dc, color="white", linewidth=2, label="trajectory")
    plt.title(f"{case.upper()} — STREAM FIELD (V69)")
    plt.xlabel("c")
    plt.ylabel("dc")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(BASE_PATH / f"{case}_v69_stream_field.png", dpi=150)
    plt.close()

    print(f"Saved: {case}_v69_off_manifold_flow.png")
    print(f"Saved: {case}_v69_stream_field.png")

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V69 — OFF-MANIFOLD FLOW")

    for case in CASES:
        process_case(case)

if __name__ == "__main__":
    main()

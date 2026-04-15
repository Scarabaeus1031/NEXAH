import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

# ==============================
# CONFIG
# ==============================
BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

# ==============================
# LOAD DATA (ROBUST)
# ==============================
def load_data():

    trajectory = np.load(os.path.join(BASE_DIR, "trajectory_pca.npy"))

    # ---- flexible rift loading ----
    candidates = ["rift_curve.npy", "rift.npy", "rift_points.npy"]

    rift_curve = None
    for f in candidates:
        path = os.path.join(RIFT_DIR, f)
        if os.path.exists(path):
            rift_curve = np.load(path)
            print(f"✅ Loaded rift file: {f}")
            break

    if rift_curve is None:
        raise FileNotFoundError(
            f"❌ No rift file found in {RIFT_DIR}\nTried: {candidates}"
        )

    print("✅ Trajectory loaded:", trajectory.shape)
    print("✅ Rift curve loaded:", rift_curve.shape)

    return trajectory, rift_curve

# ==============================
# DISTANCE COMPUTATION
# ==============================
def compute_distances(trajectory, rift_curve):

    # KDTree = fast nearest neighbor
    tree = cKDTree(rift_curve)

    distances, _ = tree.query(trajectory)

    print("✅ Distance computed")
    return distances

# ==============================
# PLOT
# ==============================
def plot_distances(distances):

    plt.figure(figsize=(8, 4))

    plt.plot(distances, linewidth=2)
    plt.scatter(len(distances)-1, distances[-1], color="red", label="collapse point")

    plt.title("Distance of Trajectory to Rift Curve")
    plt.xlabel("Trajectory step")
    plt.ylabel("Distance")

    plt.legend()
    plt.tight_layout()
    plt.show()

# ==============================
# SCATTER (INSIGHT)
# ==============================
def plot_scatter(distances):

    steps = np.arange(len(distances))

    plt.figure(figsize=(6, 5))
    sc = plt.scatter(distances, steps, c=steps, cmap="viridis")

    plt.xlabel("Distance to rift")
    plt.ylabel("Trajectory step")
    plt.title("Distance vs Time")

    plt.colorbar(sc, label="step")
    plt.tight_layout()
    plt.show()

# ==============================
# MAIN
# ==============================
def main():

    trajectory, rift_curve = load_data()

    distances = compute_distances(trajectory, rift_curve)

    # ---- SAVE ----
    np.save(os.path.join(RIFT_DIR, "rift_distances.npy"), distances)
    print(f"💾 Saved → {RIFT_DIR}/rift_distances.npy")

    plot_distances(distances)
    plot_scatter(distances)

    print("🚀 Rift distance analysis complete")

# ==============================
if __name__ == "__main__":
    main()

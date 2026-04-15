import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree

# ==============================
# CONFIG
# ==============================
BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

# control parameters
ALPHA = 0.35       # how strongly trajectory is pulled toward rift
BETA = 0.90        # how much original step direction is preserved
MAX_FORCE = 0.02   # cap for force magnitude
EPS = 1e-9

# ==============================
# LOAD
# ==============================
def load_data():
    trajectory = np.load(os.path.join(BASE_DIR, "trajectory_pca.npy"))
    rift_curve = np.load(os.path.join(RIFT_DIR, "rift_curve.npy"))

    print("✅ Data loaded")
    print("trajectory:", trajectory.shape)
    print("rift:", rift_curve.shape)

    return trajectory, rift_curve

# ==============================
# NEAREST RIFT POINTS
# ==============================
def build_rift_tree(rift_curve):
    return cKDTree(rift_curve)

def nearest_rift_info(points, tree, rift_curve):
    distances, indices = tree.query(points)
    nearest = rift_curve[indices]
    return distances, indices, nearest

# ==============================
# FORCE FIELD CONTROL
# ==============================
def control_trajectory(trajectory, rift_curve, alpha=ALPHA, beta=BETA, max_force=MAX_FORCE):
    tree = build_rift_tree(rift_curve)

    controlled = [trajectory[0].copy()]
    force_vectors = []

    for t in range(len(trajectory) - 1):
        current = controlled[-1]
        target_next = trajectory[t + 1]

        # original motion
        original_step = target_next - current

        # nearest rift point relative to CURRENT controlled point
        dist, idx = tree.query(current)
        nearest_rift = rift_curve[idx]

        # pull direction toward rift
        pull_vec = nearest_rift - current
        pull_norm = np.linalg.norm(pull_vec)

        if pull_norm > EPS:
            pull_dir = pull_vec / pull_norm
        else:
            pull_dir = np.zeros_like(pull_vec)

        # stronger force when closer structure is relevant, but bounded
        force_mag = min(alpha * pull_norm, max_force)
        force = force_mag * pull_dir

        # blended controlled step
        controlled_step = beta * original_step + force
        next_controlled = current + controlled_step

        controlled.append(next_controlled)
        force_vectors.append(force)

    controlled = np.array(controlled)
    force_vectors = np.array(force_vectors)

    print("✅ Controlled trajectory computed")
    return controlled, force_vectors

# ==============================
# DISTANCE ANALYSIS
# ==============================
def compute_distance_to_rift(path, rift_curve):
    tree = cKDTree(rift_curve)
    distances, _ = tree.query(path)
    return distances

# ==============================
# PLOTS
# ==============================
def plot_overlay(original, rift_curve, controlled):
    plt.figure(figsize=(7, 6))

    plt.plot(original[:, 0], original[:, 1], color="lime", linewidth=1.5, label="original")
    plt.plot(rift_curve[:, 0], rift_curve[:, 1], color="cyan", linewidth=2.0, label="rift")
    plt.plot(controlled[:, 0], controlled[:, 1], color="yellow", linewidth=1.8, label="controlled")

    plt.scatter(original[-1, 0], original[-1, 1], color="red", s=35, label="original end", zorder=5)
    plt.scatter(controlled[-1, 0], controlled[-1, 1], color="orange", s=35, label="controlled end", zorder=5)

    plt.title("Rift Force Field Control")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_force_vectors(controlled, force_vectors, step=6):
    plt.figure(figsize=(7, 6))

    plt.plot(controlled[:, 0], controlled[:, 1], color="yellow", linewidth=1.5, label="controlled")

    sample_idx = np.arange(0, len(force_vectors), step)
    plt.quiver(
        controlled[sample_idx, 0],
        controlled[sample_idx, 1],
        force_vectors[sample_idx, 0],
        force_vectors[sample_idx, 1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color="magenta",
        alpha=0.8
    )

    plt.title("Rift Force Vectors")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend()
    plt.tight_layout()
    plt.show()

def plot_distance_compare(original_dist, controlled_dist):
    plt.figure(figsize=(8, 4))

    plt.plot(original_dist, label="original distance to rift", linewidth=1.8)
    plt.plot(controlled_dist, label="controlled distance to rift", linewidth=1.8)

    plt.title("Distance to Rift: Original vs Controlled")
    plt.xlabel("Trajectory step")
    plt.ylabel("Distance")
    plt.legend()
    plt.tight_layout()
    plt.show()

# ==============================
# SAVE
# ==============================
def save_outputs(controlled, force_vectors, original_dist, controlled_dist):
    np.save(os.path.join(RIFT_DIR, "trajectory_controlled_force.npy"), controlled)
    np.save(os.path.join(RIFT_DIR, "rift_force_vectors.npy"), force_vectors)
    np.save(os.path.join(RIFT_DIR, "distance_original_to_rift.npy"), original_dist)
    np.save(os.path.join(RIFT_DIR, "distance_controlled_to_rift.npy"), controlled_dist)

    print("💾 Saved control outputs")

# ==============================
# MAIN
# ==============================
def main():
    trajectory, rift_curve = load_data()

    controlled, force_vectors = control_trajectory(trajectory, rift_curve)

    original_dist = compute_distance_to_rift(trajectory, rift_curve)
    controlled_dist = compute_distance_to_rift(controlled, rift_curve)

    print(f"mean original distance   : {original_dist.mean():.6f}")
    print(f"mean controlled distance : {controlled_dist.mean():.6f}")

    plot_overlay(trajectory, rift_curve, controlled)
    plot_force_vectors(controlled, force_vectors)
    plot_distance_compare(original_dist, controlled_dist)

    save_outputs(controlled, force_vectors, original_dist, controlled_dist)

    print("🚀 Rift force-field control complete")

if __name__ == "__main__":
    main()

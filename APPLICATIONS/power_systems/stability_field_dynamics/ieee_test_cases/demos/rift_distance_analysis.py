import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

# ==============================
# CONFIG
# ==============================
BASE_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs/analysis_export"
RIFT_DIR = os.path.join(BASE_DIR, "rift_extraction")

# ==============================
# LOAD DATA
# ==============================
def load_data():
    trajectory = np.load(os.path.join(BASE_DIR, "trajectory_pca.npy"))
    rift_curve = np.load(os.path.join(RIFT_DIR, "rift_curve.npy"))
    collapse_likelihood = np.load(os.path.join(BASE_DIR, "collapse_likelihood.npy"))
    PC1_grid = np.load(os.path.join(BASE_DIR, "PC1_grid.npy"))
    PC2_grid = np.load(os.path.join(BASE_DIR, "PC2_grid.npy"))

    print("✅ Data loaded")
    return trajectory, rift_curve, collapse_likelihood, PC1_grid, PC2_grid

# ==============================
# DISTANCE TO RIFT
# ==============================
def compute_distance_to_rift(trajectory, rift_curve):
    # pairwise distances
    dists = cdist(trajectory, rift_curve)
    min_dist = np.min(dists, axis=1)
    return min_dist

# ==============================
# SAMPLE LIKELIHOOD ALONG TRAJECTORY
# ==============================
def sample_likelihood(trajectory, collapse_likelihood, PC1_grid, PC2_grid):
    likelihood_vals = []

    for p in trajectory:
        idx = np.argmin((PC1_grid - p[0])**2 + (PC2_grid - p[1])**2)
        likelihood_vals.append(collapse_likelihood.flatten()[idx])

    return np.array(likelihood_vals)

# ==============================
# HOTSPOT DETECTION
# ==============================
def detect_hotspots(distance, likelihood, threshold=0.7):
    mask = likelihood > threshold
    return np.where(mask)[0]

# ==============================
# PLOTS
# ==============================
def plot_results(distance, likelihood, hotspots):

    # ---- Distance vs Likelihood ----
    plt.figure(figsize=(6, 5))
    plt.scatter(distance, likelihood, c=np.arange(len(distance)), cmap='viridis')
    plt.xlabel("Distance to Rift")
    plt.ylabel("Collapse likelihood")
    plt.title("Distance vs Rift Likelihood")
    plt.colorbar(label="trajectory step")
    plt.tight_layout()
    plt.show()

    # ---- Time evolution ----
    plt.figure(figsize=(8, 4))
    plt.plot(distance, label="distance to rift")
    plt.plot(likelihood, label="likelihood")
    plt.scatter(hotspots, likelihood[hotspots], color="red", label="hotspots")
    plt.legend()
    plt.title("Rift proximity vs likelihood over time")
    plt.xlabel("trajectory step")
    plt.tight_layout()
    plt.show()

# ==============================
# MAIN
# ==============================
def main():
    trajectory, rift_curve, collapse_likelihood, PC1_grid, PC2_grid = load_data()

    distance = compute_distance_to_rift(trajectory, rift_curve)
    likelihood = sample_likelihood(trajectory, collapse_likelihood, PC1_grid, PC2_grid)

    hotspots = detect_hotspots(distance, likelihood)

    print(f"🔥 Hotspots detected: {len(hotspots)}")

    plot_results(distance, likelihood, hotspots)

    # save
    np.save(os.path.join(RIFT_DIR, "distance_to_rift.npy"), distance)
    np.save(os.path.join(RIFT_DIR, "likelihood_along_trajectory.npy"), likelihood)

    print("💾 Saved analysis results")

if __name__ == "__main__":
    main()

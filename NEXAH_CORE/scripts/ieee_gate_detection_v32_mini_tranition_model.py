# ieee_gate_detection_v32_minimal_transition_model.py

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
from scipy.spatial import KDTree
import os

# =========================
# LOAD DATA (fallback)
# =========================
data_path = "BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/v28_data.npz"

if os.path.exists(data_path):
    print("Loading V28 data...")
    data = np.load(data_path)
    theta = data["theta"]
    r_vals = data["r"]
else:
    print("No data found → using test data")
    np.random.seed(0)
    N = 1000
    theta = np.linspace(0, 300, N)
    r_vals = 0.5 + 0.5 * np.sin(theta * 0.2)
    transition = 600
    r_vals[transition:] += np.random.normal(0, 0.5, N - transition)

N = len(theta)

# =========================
# DERIVATIVES
# =========================
dr_dtheta = np.gradient(r_vals) / np.gradient(theta)

# =========================
# DENSITY FIELD
# =========================
bins = 80
heatmap, xedges, yedges = np.histogram2d(theta, r_vals, bins=bins)
heatmap = gaussian_filter(heatmap, sigma=2)

# =========================
# GREYSPACE
# =========================
density_vals = []

for t, r_ in zip(theta, r_vals):
    xi = np.searchsorted(xedges, t) - 1
    yi = np.searchsorted(yedges, r_) - 1

    if 0 <= xi < bins and 0 <= yi < bins:
        density_vals.append(heatmap[xi, yi])
    else:
        density_vals.append(0)

density_vals = np.array(density_vals)

greyspace = 1 / (density_vals + 1e-3)
greyspace = (greyspace - greyspace.min()) / (greyspace.max() - greyspace.min())

# =========================
# RIDGE (high-density region)
# =========================
ridge_mask = heatmap > np.percentile(heatmap, 85)

x_centers = (xedges[:-1] + xedges[1:]) / 2
y_centers = (yedges[:-1] + yedges[1:]) / 2

ridge_points = []

for i in range(len(x_centers)):
    for j in range(len(y_centers)):
        if ridge_mask[i, j]:
            ridge_points.append([x_centers[i], y_centers[j]])

ridge_points = np.array(ridge_points)
ridge_tree = KDTree(ridge_points) if len(ridge_points) > 0 else None

# =========================
# RIDGE DISTANCE
# =========================
ridge_dist = np.zeros(N)

if ridge_tree is not None:
    for i in range(N):
        d, _ = ridge_tree.query([theta[i], r_vals[i]])
        ridge_dist[i] = d
else:
    ridge_dist[:] = np.nan

ridge_dist = (ridge_dist - np.nanmin(ridge_dist)) / (
    np.nanmax(ridge_dist) - np.nanmin(ridge_dist)
)

# =========================
# IOTA DETECTION
# =========================
threshold = np.percentile(np.abs(dr_dtheta), 98)
iota_idx = np.where(np.abs(dr_dtheta) > threshold)[0]

# =========================
# VISUALIZATION
# =========================
plt.figure(figsize=(12, 6))

# all points
plt.scatter(theta, r_vals, s=5, c="lightgrey", alpha=0.5)

# IOTA
plt.scatter(theta[iota_idx], r_vals[iota_idx], c="red", s=80, label="IOTA")

# greyspace overlay
plt.scatter(theta, r_vals, c=greyspace, cmap="viridis", s=5, alpha=0.5)

# transition line (reference)
plt.axvline(x=120, linestyle="--", color="black", label="transition")

plt.title("V32 — Minimal Transition Model")
plt.xlabel("theta")
plt.ylabel("r")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("BUILDER_LAB/ZETA_EXPERIMENTS/outputs/ieee_gates/v32_minimal_model.png", dpi=150)
plt.show()

# =========================
# OUTPUT
# =========================
print("\n--- V32 RESULTS ---")
print(f"IOTA events: {len(iota_idx)}")
print(f"Mean greyspace at IOTA: {np.mean(greyspace[iota_idx]):.3f}")
print(f"Mean ridge distance at IOTA: {np.mean(ridge_dist[iota_idx]):.3f}")

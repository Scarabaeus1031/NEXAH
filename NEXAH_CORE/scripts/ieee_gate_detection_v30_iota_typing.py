# V30 — IOTA Typisierung + Ridge Distance + Greyspace/YUGO Integration (FIXED)

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from scipy.ndimage import gaussian_filter
import os

# =========================
# LOAD DATA (auto fallback)
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
yugo_angle = np.arctan2(dr_dtheta, np.gradient(theta))

# =========================
# 1. DENSITY FIELD
# =========================
bins = 80
heatmap, xedges, yedges = np.histogram2d(theta, r_vals, bins=bins)
heatmap_smooth = gaussian_filter(heatmap, sigma=2)

x_centers = (xedges[:-1] + xedges[1:]) / 2
y_centers = (yedges[:-1] + yedges[1:]) / 2

# =========================
# 2. RIDGE DETECTION
# =========================
ridge_mask = heatmap_smooth > np.percentile(heatmap_smooth, 85)

ridge_points = []
for i in range(len(x_centers)):
    for j in range(len(y_centers)):
        if ridge_mask[i, j]:
            ridge_points.append([x_centers[i], y_centers[j]])

ridge_points = np.array(ridge_points)

ridge_tree = KDTree(ridge_points) if len(ridge_points) > 0 else None

# =========================
# 3. GREYSPACE SCORE
# =========================
density_vals = []

for t, r_ in zip(theta, r_vals):
    xi = np.searchsorted(xedges, t) - 1
    yi = np.searchsorted(yedges, r_) - 1

    if 0 <= xi < bins and 0 <= yi < bins:
        density_vals.append(heatmap_smooth[xi, yi])
    else:
        density_vals.append(0)

density_vals = np.array(density_vals)

greyspace_score = 1 / (density_vals + 1e-3)
greyspace_score = (greyspace_score - greyspace_score.min()) / (
    greyspace_score.max() - greyspace_score.min()
)

# =========================
# 4. IOTA DETECTION
# =========================
IOTA_THRESHOLD = np.percentile(np.abs(dr_dtheta), 98)
iota_indices = np.where(np.abs(dr_dtheta) > IOTA_THRESHOLD)[0]

# =========================
# 5. RIDGE DISTANCE
# =========================
ridge_dist = np.zeros(N)

if ridge_tree is not None:
    for i in range(N):
        dist, _ = ridge_tree.query([theta[i], r_vals[i]])
        ridge_dist[i] = dist
else:
    ridge_dist[:] = np.nan

ridge_dist_norm = (ridge_dist - np.nanmin(ridge_dist)) / (
    np.nanmax(ridge_dist) - np.nanmin(ridge_dist)
)

# =========================
# 6. IOTA CLASSIFICATION
# =========================
iota_types = []

for idx in iota_indices:
    gs = greyspace_score[idx]
    rd = ridge_dist_norm[idx]

    if gs > 0.6 and rd > 0.6:
        iota_types.append("GAP_ESCAPE")
    else:
        iota_types.append("BOUNDARY_COLLAPSE")

# =========================
# 7. VISUALIZATION
# =========================
plt.figure(figsize=(12, 6))

plt.scatter(theta, r_vals, s=5, c="lightgrey", label="all")

if len(ridge_points) > 0:
    plt.scatter(
        ridge_points[:, 0],
        ridge_points[:, 1],
        s=10,
        c="cyan",
        alpha=0.3,
        label="ridge"
    )

labels_added = set()

for idx, t in zip(iota_indices, iota_types):
    color = "red" if t == "GAP_ESCAPE" else "orange"
    label = t if t not in labels_added else ""
    plt.scatter(theta[idx], r_vals[idx], c=color, s=80, label=label)
    labels_added.add(t)

plt.axvline(x=120, linestyle="--", color="black", label="transition")

plt.xlabel("theta")
plt.ylabel("r")
plt.title("V30 — IOTA Types (Gap vs Boundary)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("v30_iota_types.png", dpi=150)
plt.show()

# =========================
# OUTPUT
# =========================
print("\n--- V30 RESULTS ---")
print(f"Total IOTA: {len(iota_indices)}")

gap_count = sum(1 for t in iota_types if t == "GAP_ESCAPE")
boundary_count = sum(1 for t in iota_types if t == "BOUNDARY_COLLAPSE")

print(f"GAP_ESCAPE: {gap_count}")
print(f"BOUNDARY_COLLAPSE: {boundary_count}")

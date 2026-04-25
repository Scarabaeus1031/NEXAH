# V30 — IOTA Typisierung + Ridge Distance + Greyspace/YUGO Integration

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import KDTree
from scipy.ndimage import gaussian_filter

# =========================
# INPUT (ersetzen falls nötig)
# =========================
theta = theta_unwrapped
r_vals = r
dr_dtheta = np.gradient(r_vals, theta)
yugo_angle = np.arctan2(dr_dtheta, np.gradient(theta))

N = len(theta)

# =========================
# 1. DENSITY FIELD (für Greyspace + Ridge)
# =========================
bins = 80
heatmap, xedges, yedges = np.histogram2d(theta, r_vals, bins=bins)
heatmap_smooth = gaussian_filter(heatmap, sigma=2)

# Koordinaten-Gitter
x_centers = (xedges[:-1] + xedges[1:]) / 2
y_centers = (yedges[:-1] + yedges[1:]) / 2

# =========================
# 2. RIDGE DETECTION (Maxima im Feld)
# =========================
ridge_mask = heatmap_smooth > np.percentile(heatmap_smooth, 85)

ridge_points = []
for i in range(len(x_centers)):
    for j in range(len(y_centers)):
        if ridge_mask[i, j]:
            ridge_points.append([x_centers[i], y_centers[j]])

ridge_points = np.array(ridge_points)

# KDTree für Distanz
if len(ridge_points) > 0:
    ridge_tree = KDTree(ridge_points)
else:
    ridge_tree = None

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

# invertierte Dichte = Greyspace
greyspace_score = 1 / (density_vals + 1e-3)

# normalisieren
greyspace_score = (greyspace_score - greyspace_score.min()) / (
    greyspace_score.max() - greyspace_score.min()
)

# =========================
# 4. IOTA DETECTION (wie V28)
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

# normalisieren
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

# all points
plt.scatter(theta, r_vals, s=5, c="lightgrey", label="all")

# ridge
if len(ridge_points) > 0:
    plt.scatter(
        ridge_points[:, 0],
        ridge_points[:, 1],
        s=10,
        c="cyan",
        alpha=0.3,
        label="ridge"
    )

# IOTA
for idx, t in zip(iota_indices, iota_types):
    if t == "GAP_ESCAPE":
        plt.scatter(theta[idx], r_vals[idx], c="red", s=80, label="GAP" if "GAP" not in plt.gca().get_legend_handles_labels()[1] else "")
    else:
        plt.scatter(theta[idx], r_vals[idx], c="orange", s=80, label="BOUNDARY" if "BOUNDARY" not in plt.gca().get_legend_handles_labels()[1] else "")

# transition line (optional)
plt.axvline(x=120, linestyle="--", color="black", label="transition")

plt.xlabel("theta")
plt.ylabel("r")
plt.title("V30 — IOTA Types (Gap vs Boundary) + Ridge Field")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("v30_iota_types.png", dpi=150)
plt.show()

# =========================
# 8. OUTPUT
# =========================
print("\n--- V30 RESULTS ---")
print(f"Total IOTA: {len(iota_indices)}")

gap_count = sum(1 for t in iota_types if t == "GAP_ESCAPE")
boundary_count = sum(1 for t in iota_types if t == "BOUNDARY_COLLAPSE")

print(f"GAP_ESCAPE: {gap_count}")
print(f"BOUNDARY_COLLAPSE: {boundary_count}")

print("\nDetails:")
for idx, t in zip(iota_indices, iota_types):
    print(
        f"t={idx:4d} | theta={theta[idx]:7.2f} | r={r_vals[idx]:5.3f} | "
        f"dr/dθ={dr_dtheta[idx]:7.2f} | GS={greyspace_score[idx]:.2f} | "
        f"ridge_d={ridge_dist_norm[idx]:.2f} | TYPE={t}"
    )

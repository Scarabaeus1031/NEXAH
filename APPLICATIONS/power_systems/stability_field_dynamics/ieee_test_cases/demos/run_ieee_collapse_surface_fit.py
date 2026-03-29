import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.interpolate import griddata

# =========================================================
# PATHS
# =========================================================

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
sys.path.append(ROOT)

IEEE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(IEEE_DIR)

ANALYSIS_DIR = os.path.join(IEEE_DIR, "analysis")
sys.path.append(ANALYSIS_DIR)

OUTPUT_DIR = os.path.join(IEEE_DIR, "outputs", "collapse_surface_fit")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# IMPORTS
# =========================================================

from nexah.field_layer import Field

# =========================================================
# DUMMY PIPELINE (replace later)
# =========================================================

def run_powerflow(lam):
    n = 10
    V = 1.0 - 0.3 * lam + 0.01 * np.random.randn(n)
    theta = 0.1 * lam + 0.01 * np.random.randn(n)
    return V, theta

# =========================================================
# DATA
# =========================================================

lambda_values = np.linspace(0.5, 1.5, 120)

states = []
for lam in lambda_values:
    V, theta = run_powerflow(lam)
    states.append(np.concatenate([V, theta]))

states = np.array(states)

# =========================================================
# FIELD
# =========================================================

field = Field(states)
vectors = field.get_vector_field()

# =========================================================
# PCA 2D
# =========================================================

pca = PCA(n_components=2)
states_2d = pca.fit_transform(states)
vectors_2d = pca.transform(states + vectors) - states_2d

x = states_2d[:, 0]
y = states_2d[:, 1]

u = vectors_2d[:, 0]
v = vectors_2d[:, 1]

# =========================================================
# GRID FIELD
# =========================================================

xi = np.linspace(x.min(), x.max(), 180)
yi = np.linspace(y.min(), y.max(), 180)
grid_x, grid_y = np.meshgrid(xi, yi)

grid_u = griddata((x, y), u, (grid_x, grid_y), method="cubic")
grid_v = griddata((x, y), v, (grid_x, grid_y), method="cubic")

grid_u = np.nan_to_num(grid_u)
grid_v = np.nan_to_num(grid_v)

# =========================================================
# TOPOLOGY METRICS
# =========================================================

dx = xi[1] - xi[0]
dy = yi[1] - yi[0]

du_dx = np.gradient(grid_u, dx, axis=1)
du_dy = np.gradient(grid_u, dy, axis=0)

dv_dx = np.gradient(grid_v, dx, axis=1)
dv_dy = np.gradient(grid_v, dy, axis=0)

divergence = du_dx + dv_dy
curl = dv_dx - du_dy

# =========================================================
# COLLAPSE CANDIDATE ZONE
# =========================================================

# strong compressive zones (negative divergence)
collapse_mask = divergence < np.quantile(divergence, 0.05)

# extract candidate points
candidate_points = np.column_stack([
    grid_x[collapse_mask],
    grid_y[collapse_mask]
])

# =========================================================
# FIT COLLAPSE BOUNDARY
# =========================================================

# choose lower envelope by binning x and taking min y in each bin
num_bins = 60
bins = np.linspace(x.min(), x.max(), num_bins + 1)

fit_x = []
fit_y = []

if len(candidate_points) > 0:
    cx = candidate_points[:, 0]
    cy = candidate_points[:, 1]

    for i in range(num_bins):
        mask = (cx >= bins[i]) & (cx < bins[i + 1])
        if np.any(mask):
            fit_x.append(np.mean(cx[mask]))
            fit_y.append(np.min(cy[mask]))

fit_x = np.array(fit_x)
fit_y = np.array(fit_y)

# polynomial fit if enough points
if len(fit_x) >= 6:
    poly_coeff = np.polyfit(fit_x, fit_y, deg=3)
    poly = np.poly1d(poly_coeff)

    fit_x_dense = np.linspace(fit_x.min(), fit_x.max(), 300)
    fit_y_dense = poly(fit_x_dense)
else:
    fit_x_dense = fit_x
    fit_y_dense = fit_y

# =========================================================
# DISTANCE OF TRAJECTORY TO COLLAPSE BOUNDARY
# =========================================================

def point_to_curve_distance(px, py, curve_x, curve_y):
    if len(curve_x) == 0:
        return np.nan
    d = np.sqrt((curve_x - px) ** 2 + (curve_y - py) ** 2)
    return np.min(d)

traj_distances = np.array([
    point_to_curve_distance(px, py, fit_x_dense, fit_y_dense)
    for px, py in zip(x, y)
])

# =========================================================
# PLOT 1 — COLLAPSE BOUNDARY FIT
# =========================================================

plt.figure(figsize=(11, 8))

im = plt.imshow(
    divergence,
    extent=[xi.min(), xi.max(), yi.min(), yi.max()],
    origin="lower",
    cmap="coolwarm",
    aspect="auto",
    alpha=0.88
)

plt.streamplot(
    grid_x,
    grid_y,
    grid_u,
    grid_v,
    color="black",
    density=1.3,
    linewidth=0.7,
    arrowsize=0.8
)

# candidate zone
if len(candidate_points) > 0:
    plt.scatter(
        candidate_points[:, 0],
        candidate_points[:, 1],
        s=5,
        color="yellow",
        alpha=0.25,
        label="collapse candidates"
    )

# fitted boundary
if len(fit_x_dense) > 0:
    plt.plot(
        fit_x_dense,
        fit_y_dense,
        color="cyan",
        linewidth=2.5,
        label="fitted collapse boundary"
    )

# trajectory
plt.plot(x, y, color="lime", linewidth=1.5, alpha=0.9, label="trajectory")

# collapse point
plt.scatter(x[-1], y[-1], color="black", s=40, label="collapse", zorder=5)

plt.title("NEXAH FIELD — Collapse Surface Fit")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(im, label="Divergence")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "collapse_surface_fit.png"), dpi=220)
plt.show()

# =========================================================
# PLOT 2 — DISTANCE TO COLLAPSE BOUNDARY
# =========================================================

plt.figure(figsize=(10, 4))

plt.plot(np.arange(len(traj_distances)), traj_distances, linewidth=2)
plt.scatter(len(traj_distances) - 1, traj_distances[-1], color="red", label="collapse point")

plt.title("Distance of Trajectory to Fitted Collapse Boundary")
plt.xlabel("Trajectory step")
plt.ylabel("Distance")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "distance_to_collapse_boundary.png"), dpi=220)
plt.show()

# =========================================================
# SAVE RAW
# =========================================================
np.save(os.path.join(OUTPUT_DIR, "collapse_likelihood.npy"), collapse_likelihood)
np.save(os.path.join(OUTPUT_DIR, "PC1_grid.npy"), PC1_grid)
np.save(os.path.join(OUTPUT_DIR, "PC2_grid.npy"), PC2_grid)
np.save(os.path.join(OUTPUT_DIR, "divergence.npy"), divergence)
np.save(os.path.join(OUTPUT_DIR, "collapse_candidates.npy"), candidate_points)
np.save(os.path.join(OUTPUT_DIR, "fit_x.npy"), fit_x_dense)
np.save(os.path.join(OUTPUT_DIR, "fit_y.npy"), fit_y_dense)
np.save(os.path.join(OUTPUT_DIR, "trajectory_distances.npy"), traj_distances)

print("✅ Collapse surface fit saved to:", OUTPUT_DIR)


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

OUTPUT_DIR = os.path.join(IEEE_DIR, "outputs", "collapse_likelihood")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# IMPORTS
# =========================================================

from nexah.field_layer import Field
from corridor_detection import (
    compute_flow_magnitude,
    detect_corridors,
    detect_spaces
)

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
criticality = np.abs(divergence) * np.abs(curl)

# =========================================================
# COLLAPSE BOUNDARY EXTRACTION
# =========================================================

collapse_mask = divergence < np.quantile(divergence, 0.05)

candidate_points = np.column_stack([
    grid_x[collapse_mask],
    grid_y[collapse_mask]
])

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

if len(fit_x) >= 6:
    poly_coeff = np.polyfit(fit_x, fit_y, deg=3)
    poly = np.poly1d(poly_coeff)

    fit_x_dense = np.linspace(fit_x.min(), fit_x.max(), 300)
    fit_y_dense = poly(fit_x_dense)
else:
    fit_x_dense = fit_x
    fit_y_dense = fit_y

# =========================================================
# DISTANCE TO FITTED BOUNDARY (FOR EVERY GRID POINT)
# =========================================================

def point_to_curve_distance(px, py, curve_x, curve_y):
    if len(curve_x) == 0:
        return np.nan
    d = np.sqrt((curve_x - px) ** 2 + (curve_y - py) ** 2)
    return np.min(d)

distance_map = np.zeros_like(grid_x, dtype=float)

for i in range(grid_x.shape[0]):
    for j in range(grid_x.shape[1]):
        distance_map[i, j] = point_to_curve_distance(
            grid_x[i, j],
            grid_y[i, j],
            fit_x_dense,
            fit_y_dense
        )

# =========================================================
# COLLAPSE LIKELIHOOD
# =========================================================

alpha = 25.0  # decay strength

criticality_norm = criticality / (np.max(criticality) + 1e-12)
distance_weight = np.exp(-alpha * distance_map)

likelihood = criticality_norm * distance_weight
likelihood = likelihood / (np.max(likelihood) + 1e-12)

# =========================================================
# TRAJECTORY DISTANCE & LIKELIHOOD
# =========================================================

traj_distances = np.array([
    point_to_curve_distance(px, py, fit_x_dense, fit_y_dense)
    for px, py in zip(x, y)
])

def sample_grid_value(px, py, gx, gy, values):
    ix = np.argmin(np.abs(xi - px))
    iy = np.argmin(np.abs(yi - py))
    return values[iy, ix]

traj_likelihood = np.array([
    sample_grid_value(px, py, grid_x, grid_y, likelihood)
    for px, py in zip(x, y)
])

# =========================================================
# PLOT 1 — LIKELIHOOD MAP
# =========================================================

plt.figure(figsize=(11, 8))

im = plt.imshow(
    likelihood,
    extent=[xi.min(), xi.max(), yi.min(), yi.max()],
    origin="lower",
    cmap="inferno",
    aspect="auto",
    alpha=0.95
)

plt.streamplot(
    grid_x,
    grid_y,
    grid_u,
    grid_v,
    color="white",
    density=1.2,
    linewidth=0.7,
    arrowsize=0.8
)

if len(fit_x_dense) > 0:
    plt.plot(
        fit_x_dense,
        fit_y_dense,
        color="cyan",
        linewidth=2.2,
        label="fitted collapse boundary"
    )

plt.plot(x, y, color="lime", linewidth=1.5, alpha=0.9, label="trajectory")
plt.scatter(x[-1], y[-1], color="yellow", edgecolor="black", s=45, label="collapse", zorder=6)

plt.title("NEXAH FIELD — Collapse Likelihood Map")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(im, label="Collapse likelihood")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "collapse_likelihood_map.png"), dpi=220)
plt.show()

# =========================================================
# PLOT 2 — TRAJECTORY LIKELIHOOD OVER TIME
# =========================================================

plt.figure(figsize=(10, 4))
plt.plot(np.arange(len(traj_likelihood)), traj_likelihood, linewidth=2)
plt.scatter(len(traj_likelihood) - 1, traj_likelihood[-1], color="red", label="collapse point")

plt.title("Trajectory Collapse Likelihood Over Time")
plt.xlabel("Trajectory step")
plt.ylabel("Likelihood")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "trajectory_likelihood.png"), dpi=220)
plt.show()

# =========================================================
# PLOT 3 — DISTANCE VS LIKELIHOOD
# =========================================================

plt.figure(figsize=(6, 5))
plt.scatter(traj_distances, traj_likelihood, c=np.arange(len(traj_likelihood)), cmap="viridis", s=30)
plt.xlabel("Distance to boundary")
plt.ylabel("Collapse likelihood")
plt.title("Distance vs Collapse Likelihood")
plt.colorbar(label="Trajectory step")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "distance_vs_likelihood.png"), dpi=220)
plt.show()

# =========================================================
# SAVE RAW
# =========================================================

np.save(os.path.join(OUTPUT_DIR, "likelihood.npy"), likelihood)
np.save(os.path.join(OUTPUT_DIR, "distance_map.npy"), distance_map)
np.save(os.path.join(OUTPUT_DIR, "trajectory_likelihood.npy"), traj_likelihood)
np.save(os.path.join(OUTPUT_DIR, "trajectory_distances.npy"), traj_distances)

print("✅ Collapse likelihood outputs saved to:", OUTPUT_DIR)

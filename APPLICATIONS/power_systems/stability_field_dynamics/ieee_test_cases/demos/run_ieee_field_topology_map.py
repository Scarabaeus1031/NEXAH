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

OUTPUT_DIR = os.path.join(IEEE_DIR, "outputs", "topology_map")
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

# =========================================================
# GRID FIELD
# =========================================================

x = states_2d[:, 0]
y = states_2d[:, 1]
u = vectors_2d[:, 0]
v = vectors_2d[:, 1]

xi = np.linspace(x.min(), x.max(), 140)
yi = np.linspace(y.min(), y.max(), 140)
grid_x, grid_y = np.meshgrid(xi, yi)

grid_u = griddata((x, y), u, (grid_x, grid_y), method="cubic")
grid_v = griddata((x, y), v, (grid_x, grid_y), method="cubic")

grid_u = np.nan_to_num(grid_u)
grid_v = np.nan_to_num(grid_v)

flow_mag = compute_flow_magnitude(grid_u, grid_v) + 1e-6
corridors = detect_corridors(flow_mag)
spaces = detect_spaces(flow_mag)

# =========================================================
# TOPOLOGY METRICS
# =========================================================

dx = xi[1] - xi[0]
dy = yi[1] - yi[0]

du_dx = np.gradient(grid_u, dx, axis=1)
du_dy = np.gradient(grid_u, dy, axis=0)

dv_dx = np.gradient(grid_v, dx, axis=1)
dv_dy = np.gradient(grid_v, dy, axis=0)

# divergence: compression / expansion
divergence = du_dx + dv_dy

# 2D curl (z-component): local rotation
curl = dv_dx - du_dy

# combined "criticality"
criticality = np.abs(divergence) * np.abs(curl)

# masks
compressive_mask = divergence < np.quantile(divergence, 0.1)
expansive_mask = divergence > np.quantile(divergence, 0.9)
rotational_mask = np.abs(curl) > np.quantile(np.abs(curl), 0.9)
critical_mask = criticality > np.quantile(criticality, 0.95)

# =========================================================
# PLOT 1 — DIVERGENCE
# =========================================================

plt.figure(figsize=(11, 8))

im = plt.imshow(
    divergence,
    extent=[xi.min(), xi.max(), yi.min(), yi.max()],
    origin="lower",
    cmap="coolwarm",
    aspect="auto",
    alpha=0.9
)

plt.streamplot(
    grid_x,
    grid_y,
    grid_u,
    grid_v,
    color="black",
    density=1.4,
    linewidth=0.7,
    arrowsize=0.8
)

plt.contour(grid_x, grid_y, corridors, levels=[0.5], colors="white", linewidths=1.1, alpha=0.8)
plt.contour(grid_x, grid_y, spaces, levels=[0.5], colors="yellow", linewidths=0.8, alpha=0.6)

plt.plot(x, y, color="lime", linewidth=1.5, alpha=0.8, label="trajectory")
plt.scatter(x[-1], y[-1], color="black", s=35, label="collapse", zorder=5)

plt.title("NEXAH FIELD — Divergence Map")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(im, label="Divergence")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "divergence_map.png"), dpi=220)
plt.show()

# =========================================================
# PLOT 2 — CURL / ROTATION
# =========================================================

plt.figure(figsize=(11, 8))

im = plt.imshow(
    curl,
    extent=[xi.min(), xi.max(), yi.min(), yi.max()],
    origin="lower",
    cmap="PiYG",
    aspect="auto",
    alpha=0.9
)

plt.streamplot(
    grid_x,
    grid_y,
    grid_u,
    grid_v,
    color="black",
    density=1.4,
    linewidth=0.7,
    arrowsize=0.8
)

plt.contour(grid_x, grid_y, rotational_mask, levels=[0.5], colors="cyan", linewidths=1.2, alpha=0.9)
plt.plot(x, y, color="white", linewidth=1.5, alpha=0.8, label="trajectory")
plt.scatter(x[-1], y[-1], color="black", s=35, label="collapse", zorder=5)

plt.title("NEXAH FIELD — Curl / Rotation Map")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(im, label="Curl")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "curl_map.png"), dpi=220)
plt.show()

# =========================================================
# PLOT 3 — CRITICAL ZONES
# =========================================================

plt.figure(figsize=(11, 8))

im = plt.imshow(
    criticality,
    extent=[xi.min(), xi.max(), yi.min(), yi.max()],
    origin="lower",
    cmap="magma",
    aspect="auto",
    alpha=0.92
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

plt.contour(grid_x, grid_y, critical_mask, levels=[0.5], colors="red", linewidths=1.5, alpha=0.9)
plt.contour(grid_x, grid_y, compressive_mask, levels=[0.5], colors="blue", linewidths=1.0, alpha=0.8)
plt.contour(grid_x, grid_y, expansive_mask, levels=[0.5], colors="lime", linewidths=1.0, alpha=0.8)

plt.plot(x, y, color="yellow", linewidth=1.4, alpha=0.85, label="trajectory")
plt.scatter(x[-1], y[-1], color="cyan", s=40, label="collapse", zorder=5)

plt.title("NEXAH FIELD — Critical Topology Map")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(im, label="Criticality = |div| × |curl|")
plt.legend()
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "critical_topology_map.png"), dpi=220)
plt.show()

# =========================================================
# SAVE RAW ARRAYS
# =========================================================

np.save(os.path.join(OUTPUT_DIR, "divergence.npy"), divergence)
np.save(os.path.join(OUTPUT_DIR, "curl.npy"), curl)
np.save(os.path.join(OUTPUT_DIR, "criticality.npy"), criticality)

print("✅ Topology maps saved to:", OUTPUT_DIR)


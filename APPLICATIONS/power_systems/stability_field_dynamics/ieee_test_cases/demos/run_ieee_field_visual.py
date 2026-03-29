import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.interpolate import griddata

# =========================================================
# PATH FIX (robust)
# =========================================================

# repo root
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
sys.path.append(ROOT)

# ieee_test_cases
IEEE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(IEEE_DIR)

# analysis folder direkt
ANALYSIS_DIR = os.path.join(IEEE_DIR, "analysis")
sys.path.append(ANALYSIS_DIR)


# =========================================================
# IMPORTS
# =========================================================

from nexah.field_layer import Field

# 🔥 DIREKT importieren (kein package stress)
from corridor_detection import (
    compute_flow_magnitude,
    detect_corridors,
    detect_spaces
)


# =========================================================
# ⚠️ REPLACE WITH YOUR REAL IEEE PIPELINE
# =========================================================
def run_powerflow(lam):
    n = 10
    V = 1.0 - 0.3 * lam + 0.01 * np.random.randn(n)
    theta = 0.1 * lam + 0.01 * np.random.randn(n)
    return V, theta


# =========================================================
# GENERATE STATES
# =========================================================

lambda_values = np.linspace(0.5, 1.5, 120)

states = []
lambdas = []

for lam in lambda_values:
    V, theta = run_powerflow(lam)
    state = np.concatenate([V, theta])

    states.append(state)
    lambdas.append(lam)

states = np.array(states)
lambdas = np.array(lambdas)


# =========================================================
# FIELD
# =========================================================

field = Field(states)
vectors = field.get_vector_field()


# =========================================================
# PCA
# =========================================================

pca = PCA(n_components=2)
states_2d = pca.fit_transform(states)

vectors_2d = pca.transform(states + vectors) - states_2d


# =========================================================
# GRID
# =========================================================

x = states_2d[:, 0]
y = states_2d[:, 1]

u = vectors_2d[:, 0]
v = vectors_2d[:, 1]

xi = np.linspace(x.min(), x.max(), 120)
yi = np.linspace(y.min(), y.max(), 120)
grid_x, grid_y = np.meshgrid(xi, yi)

grid_u = griddata((x, y), u, (grid_x, grid_y), method='cubic')
grid_v = griddata((x, y), v, (grid_x, grid_y), method='cubic')

grid_u = np.nan_to_num(grid_u)
grid_v = np.nan_to_num(grid_v)


# =========================================================
# STRUCTURE
# =========================================================

flow_mag = compute_flow_magnitude(grid_u, grid_v)

corridors = detect_corridors(flow_mag)
spaces = detect_spaces(flow_mag)


# =========================================================
# PLOT
# =========================================================

plt.figure(figsize=(10, 8))

# FIELD
plt.streamplot(
    grid_x,
    grid_y,
    grid_u,
    grid_v,
    color=flow_mag,
    cmap='viridis',
    density=2,
    linewidth=1
)

# trajectory
plt.plot(x, y, color='white', linewidth=2, alpha=0.7, label="trajectory")

# collapse
plt.scatter(x[-1], y[-1], color='red', label='collapse', zorder=5)

# corridors
plt.contour(
    grid_x,
    grid_y,
    corridors,
    levels=[0.5],
    colors='red',
    linewidths=1.5,
    alpha=0.8
)

# spaces
plt.contour(
    grid_x,
    grid_y,
    spaces,
    levels=[0.5],
    colors='blue',
    linewidths=1,
    alpha=0.5
)

plt.title("NEXAH FIELD — Corridors & Spaces")
plt.xlabel("PC1")
plt.ylabel("PC2")

plt.colorbar(label="Flow magnitude")
plt.legend()

plt.grid(alpha=0.2)
plt.tight_layout()

plt.show()

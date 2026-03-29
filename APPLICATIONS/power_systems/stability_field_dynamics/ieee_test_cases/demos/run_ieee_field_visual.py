```python
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.interpolate import griddata

# --- ensure repo root is in path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")))

from nexah.field_layer import Field


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
# DIMENSION REDUCTION (PCA)
# =========================================================

pca = PCA(n_components=2)
states_2d = pca.fit_transform(states)

vectors_2d = pca.transform(states + vectors) - states_2d


# =========================================================
# INTERPOLATED FIELD (REAL FIELD STRUCTURE)
# =========================================================

x = states_2d[:, 0]
y = states_2d[:, 1]

u = vectors_2d[:, 0]
v = vectors_2d[:, 1]

# --- stable grid ---
xi = np.linspace(x.min(), x.max(), 120)
yi = np.linspace(y.min(), y.max(), 120)

grid_x, grid_y = np.meshgrid(xi, yi)

# --- interpolation ---
grid_u = griddata((x, y), u, (grid_x, grid_y), method='cubic')
grid_v = griddata((x, y), v, (grid_x, grid_y), method='cubic')

# --- fallback for NaNs ---
grid_u = np.nan_to_num(grid_u)
grid_v = np.nan_to_num(grid_v)


# =========================================================
# FLOW MAGNITUDE (for visualization)
# =========================================================

flow_mag = np.sqrt(grid_u**2 + grid_v**2)


# =========================================================
# PLOT
# =========================================================

plt.figure(figsize=(10, 8))

# --- continuous flow field ---
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

# --- trajectory ---
plt.plot(x, y, color='white', linewidth=2, alpha=0.7, label="trajectory")

# --- collapse point ---
plt.scatter(x[-1], y[-1], color='red', label='collapse', zorder=5)

plt.title("NEXAH FIELD — Continuous Flow Geometry")
plt.xlabel("PC1")
plt.ylabel("PC2")

plt.colorbar(label="Flow magnitude")
plt.legend()

plt.grid(alpha=0.2)
plt.tight_layout()

plt.show()
```

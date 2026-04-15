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

OUTPUT_DIR = os.path.join(IEEE_DIR, "outputs", "analysis_export")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# IMPORTS
# =========================================================

from nexah.field_layer import Field

# =========================================================
# DUMMY PIPELINE
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
# PCA
# =========================================================

pca3 = PCA(n_components=3)
states_3d = pca3.fit_transform(states)
vectors_3d = pca3.transform(states + vectors) - states_3d

pca2 = PCA(n_components=2)
states_2d = pca2.fit_transform(states)
vectors_2d = pca2.transform(states + vectors) - states_2d

# =========================================================
# GRID (for density)
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

flow_mag = np.sqrt(grid_u**2 + grid_v**2)

# =========================================================
# 1. SAVE DENSITY MAP
# =========================================================

plt.figure(figsize=(10, 3))
plt.imshow(
    flow_mag,
    extent=[xi.min(), xi.max(), yi.min(), yi.max()],
    origin='lower',
    aspect='auto',
    cmap='inferno'
)
plt.colorbar(label="Flow magnitude")
plt.title("Density Map")
plt.tight_layout()

plt.savefig(os.path.join(OUTPUT_DIR, "density_map.png"), dpi=200)
plt.close()

# =========================================================
# 2. SAVE 3D SNAPSHOT
# =========================================================

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')

ax.plot(
    states_3d[:, 0],
    states_3d[:, 1],
    states_3d[:, 2],
    color='white',
    alpha=0.6
)

for i in range(0, len(states_3d), 5):
    ax.quiver(
        states_3d[i, 0],
        states_3d[i, 1],
        states_3d[i, 2],
        vectors_3d[i, 0],
        vectors_3d[i, 1],
        vectors_3d[i, 2],
        length=0.05,
        normalize=True
    )

ax.scatter(
    states_3d[-1, 0],
    states_3d[-1, 1],
    states_3d[-1, 2],
    color='yellow',
    s=50
)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "3d_snapshot.png"), dpi=200)
plt.close()

# =========================================================
# 3. ROTATION FRAMES (FOR GIF LATER)
# =========================================================

for angle in range(0, 360, 10):
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(projection='3d')

    ax.plot(
        states_3d[:, 0],
        states_3d[:, 1],
        states_3d[:, 2],
        color='white',
        alpha=0.6
    )

    ax.view_init(elev=25, azim=angle)

    plt.savefig(os.path.join(OUTPUT_DIR, f"frame_{angle:03d}.png"), dpi=120)
    plt.close()

# =========================================================
# 4. SAVE RAW DATA (WICHTIG!)
# =========================================================

np.save(os.path.join(OUTPUT_DIR, "states.npy"), states)
np.save(os.path.join(OUTPUT_DIR, "vectors.npy"), vectors)
np.save(os.path.join(OUTPUT_DIR, "states_3d.npy"), states_3d)

print("✅ Export complete →", OUTPUT_DIR)


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

OUTPUT_DIR = os.path.join(IEEE_DIR, "outputs", "multi_agent")
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
# PCA (3D)
# =========================================================

pca = PCA(n_components=3)
states_3d = pca.fit_transform(states)
vectors_3d = pca.transform(states + vectors) - states_3d

# also 2D for grid
pca2 = PCA(n_components=2)
states_2d = pca2.fit_transform(states)
vectors_2d = pca2.transform(states + vectors) - states_2d

# =========================================================
# GRID (2D FIELD)
# =========================================================

x = states_2d[:, 0]
y = states_2d[:, 1]
u = vectors_2d[:, 0]
v = vectors_2d[:, 1]

xi = np.linspace(x.min(), x.max(), 120)
yi = np.linspace(y.min(), y.max(), 120)

grid_x, grid_y = np.meshgrid(xi, yi)

grid_u = griddata((x, y), u, (grid_x, grid_y), method="cubic")
grid_v = griddata((x, y), v, (grid_x, grid_y), method="cubic")

grid_u = np.nan_to_num(grid_u)
grid_v = np.nan_to_num(grid_v)

flow_mag = compute_flow_magnitude(grid_u, grid_v)

# =========================================================
# AGENTS
# =========================================================

def sample_vector(px, py):
    ix = np.argmin(np.abs(xi - px))
    iy = np.argmin(np.abs(yi - py))
    return grid_u[iy, ix], grid_v[iy, ix]

def run_agent(start, steps=200):
    pos = np.array(start, dtype=float)
    path = [pos.copy()]

    for _ in range(steps):
        vx, vy = sample_vector(pos[0], pos[1])
        direction = np.array([vx, vy])

        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            break

        direction = direction / norm
        pos = pos + 0.01 * direction

        path.append(pos.copy())

    return np.array(path)

# seeds
num_agents = 60
seed_idx = np.random.choice(len(states_2d), num_agents)
seed_points = states_2d[seed_idx]

agent_paths = [run_agent(p) for p in seed_points]

# =========================================================
# DENSITY MAP
# =========================================================

density = np.zeros_like(grid_u)

for path in agent_paths:
    for px, py in path:
        ix = np.argmin(np.abs(xi - px))
        iy = np.argmin(np.abs(yi - py))
        density[iy, ix] += 1

density = density / density.max()

# =========================================================
# PLOT 1 — 3D FIELD
# =========================================================

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(projection='3d')

ax.plot(
    states_3d[:, 0],
    states_3d[:, 1],
    states_3d[:, 2],
    color='white',
    linewidth=2
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

ax.set_title("NEXAH FIELD — 3D Projection")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "field_3d.png"), dpi=200)
plt.show()

# =========================================================
# PLOT 2 — DENSITY
# =========================================================

plt.figure(figsize=(10, 8))

plt.imshow(
    density,
    extent=[x.min(), x.max(), y.min(), y.max()],
    origin='lower',
    cmap='inferno',
    alpha=0.85
)

plt.title("Agent Density Map (Highways)")
plt.colorbar(label="Agent density")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "agent_density.png"), dpi=200)
plt.show()

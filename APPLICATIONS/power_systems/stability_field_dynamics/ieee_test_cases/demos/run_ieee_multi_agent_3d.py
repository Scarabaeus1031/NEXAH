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

OUTPUT_DIR = os.path.join(IEEE_DIR, "outputs", "multi_agent_3d")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# IMPORTS
# =========================================================

from nexah.field_layer import Field
from corridor_detection import compute_flow_magnitude

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
# PCA 3D + 2D
# =========================================================

pca3 = PCA(n_components=3)
states_3d = pca3.fit_transform(states)
vectors_3d = pca3.transform(states + vectors) - states_3d

pca2 = PCA(n_components=2)
states_2d = pca2.fit_transform(states)
vectors_2d = pca2.transform(states + vectors) - states_2d

# =========================================================
# GRID IN 2D FOR AGENT SAMPLING
# =========================================================

x2 = states_2d[:, 0]
y2 = states_2d[:, 1]
u2 = vectors_2d[:, 0]
v2 = vectors_2d[:, 1]

xi = np.linspace(x2.min(), x2.max(), 140)
yi = np.linspace(y2.min(), y2.max(), 140)
grid_x, grid_y = np.meshgrid(xi, yi)

grid_u = griddata((x2, y2), u2, (grid_x, grid_y), method="cubic")
grid_v = griddata((x2, y2), v2, (grid_x, grid_y), method="cubic")

grid_u = np.nan_to_num(grid_u)
grid_v = np.nan_to_num(grid_v)

flow_mag = compute_flow_magnitude(grid_u, grid_v) + 1e-6

# =========================================================
# AGENT LOGIC IN 2D
# =========================================================

def sample_vector(px, py):
    ix = np.argmin(np.abs(xi - px))
    iy = np.argmin(np.abs(yi - py))
    return grid_u[iy, ix], grid_v[iy, ix]

def inside_bounds(px, py):
    return (xi.min() <= px <= xi.max()) and (yi.min() <= py <= yi.max())

def run_agent(start, steps=250, step_size=0.008, noise=0.04):
    pos = np.array(start, dtype=float)
    path = [pos.copy()]

    for _ in range(steps):
        if not inside_bounds(pos[0], pos[1]):
            break

        vx, vy = sample_vector(pos[0], pos[1])
        direction = np.array([vx, vy], dtype=float)

        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            break

        direction = direction / norm
        direction += noise * np.random.randn(2)

        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            break

        direction = direction / norm
        pos = pos + step_size * direction
        path.append(pos.copy())

    return np.array(path)

# =========================================================
# MULTI AGENTS
# =========================================================

num_agents = 40
seed_indices = np.linspace(0, len(states_2d) - 1, num_agents, dtype=int)
seed_points_2d = states_2d[seed_indices]

agent_paths_2d = [run_agent(seed) for seed in seed_points_2d]

# =========================================================
# PROJECT AGENT PATHS INTO 3D
# =========================================================

# Build inverse-style lift by nearest state neighbor in 2D
def lift_to_3d(path_2d):
    lifted = []
    for px, py in path_2d:
        d = np.linalg.norm(states_2d - np.array([px, py]), axis=1)
        idx = np.argmin(d)
        lifted.append(states_3d[idx])
    return np.array(lifted)

agent_paths_3d = [lift_to_3d(path) for path in agent_paths_2d]

# =========================================================
# PLOT 3D
# =========================================================

fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(projection="3d")

# system trajectory
ax.plot(
    states_3d[:, 0],
    states_3d[:, 1],
    states_3d[:, 2],
    color="white",
    linewidth=2,
    alpha=0.55,
    label="system trajectory"
)

# field vectors
for i in range(0, len(states_3d), 5):
    ax.quiver(
        states_3d[i, 0],
        states_3d[i, 1],
        states_3d[i, 2],
        vectors_3d[i, 0],
        vectors_3d[i, 1],
        vectors_3d[i, 2],
        length=0.045,
        normalize=True,
        alpha=0.7
    )

# agents
for path3 in agent_paths_3d:
    if len(path3) < 2:
        continue
    ax.plot(path3[:, 0], path3[:, 1], path3[:, 2], linewidth=1.2, alpha=0.85)

# seeds
seed_points_3d = states_3d[seed_indices]
ax.scatter(
    seed_points_3d[:, 0],
    seed_points_3d[:, 1],
    seed_points_3d[:, 2],
    color="lime",
    s=20,
    label="agent seeds"
)

# collapse
ax.scatter(
    states_3d[-1, 0],
    states_3d[-1, 1],
    states_3d[-1, 2],
    color="yellow",
    edgecolor="black",
    s=45,
    label="collapse"
)

ax.set_title("NEXAH FIELD — 3D Multi-Agent Projection")
ax.set_xlabel("PC1")
ax.set_ylabel("PC2")
ax.set_zlabel("PC3")
ax.legend()

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "multi_agent_3d.png"), dpi=220)
plt.show()


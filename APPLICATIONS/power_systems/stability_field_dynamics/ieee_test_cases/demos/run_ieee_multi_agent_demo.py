```python id="q8d9i7"
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from scipy.interpolate import griddata

# =========================================================
# PATH FIX
# =========================================================

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../"))
sys.path.append(ROOT)

IEEE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(IEEE_DIR)

ANALYSIS_DIR = os.path.join(IEEE_DIR, "analysis")
sys.path.append(ANALYSIS_DIR)

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
# DUMMY IEEE PIPELINE (replace later)
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

# =========================================================
# STRUCTURE
# =========================================================

flow_mag = compute_flow_magnitude(grid_u, grid_v) + 1e-6
corridors = detect_corridors(flow_mag)
spaces = detect_spaces(flow_mag)

# =========================================================
# AGENT HELPERS
# =========================================================

def sample_vector(px, py):
    ix = np.argmin(np.abs(xi - px))
    iy = np.argmin(np.abs(yi - py))
    return grid_u[iy, ix], grid_v[iy, ix], corridors[iy, ix], spaces[iy, ix]

def inside_bounds(px, py):
    return (xi.min() <= px <= xi.max()) and (yi.min() <= py <= yi.max())

def run_agent(start, steps=250, step_size=0.008, noise=0.05):
    pos = np.array(start, dtype=float)
    trajectory = [pos.copy()]

    for _ in range(steps):
        if not inside_bounds(pos[0], pos[1]):
            break

        vx, vy, is_corridor, is_space = sample_vector(pos[0], pos[1])
        direction = np.array([vx, vy], dtype=float)

        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            break

        direction = direction / norm

        # local exploration noise
        direction += noise * np.random.randn(2)

        norm = np.linalg.norm(direction)
        if norm < 1e-10:
            break

        direction = direction / norm

        # corridor / space bias
        speed = 1.0
        if is_corridor:
            speed *= 1.6
        if is_space:
            speed *= 0.35

        pos = pos + step_size * speed * direction
        trajectory.append(pos.copy())

    return np.array(trajectory)

# =========================================================
# MULTI-AGENT SEEDS
# =========================================================

num_agents = 40

seed_indices = np.linspace(0, len(states_2d) - 1, num_agents, dtype=int)
seed_points = states_2d[seed_indices]

agent_paths = [run_agent(seed) for seed in seed_points]

# =========================================================
# PLOT
# =========================================================

plt.figure(figsize=(11, 9))

# field
stream = plt.streamplot(
    grid_x,
    grid_y,
    grid_u,
    grid_v,
    color=flow_mag,
    cmap="viridis",
    density=2,
    linewidth=1
)

# corridors
plt.contour(
    grid_x,
    grid_y,
    corridors,
    levels=[0.5],
    colors="red",
    linewidths=1.2,
    alpha=0.75
)

# spaces
plt.contour(
    grid_x,
    grid_y,
    spaces,
    levels=[0.5],
    colors="blue",
    linewidths=0.8,
    alpha=0.5
)

# original system trajectory
plt.plot(x, y, color="white", linewidth=2, alpha=0.35, label="system trajectory")

# agents
for i, path in enumerate(agent_paths):
    if len(path) < 2:
        continue

    plt.plot(path[:, 0], path[:, 1], linewidth=1.2, alpha=0.8)

# seeds
plt.scatter(seed_points[:, 0], seed_points[:, 1], s=18, color="lime", alpha=0.9, label="agent seeds")

# collapse
plt.scatter(x[-1], y[-1], color="yellow", s=40, edgecolor="black", label="collapse", zorder=5)

plt.title("NEXAH Multi-Agent Field Exploration")
plt.xlabel("PC1")
plt.ylabel("PC2")

plt.colorbar(stream.lines, label="Flow magnitude")
plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()

plt.show()
```

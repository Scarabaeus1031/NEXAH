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

flow_mag = compute_flow_magnitude(grid_u, grid_v) + 1e-6

corridors = detect_corridors(flow_mag)
spaces = detect_spaces(flow_mag)

# =========================================================
# AGENT (ANT)
# =========================================================

def sample_vector(px, py):
    """Nearest neighbor sampling"""
    ix = np.argmin(np.abs(xi - px))
    iy = np.argmin(np.abs(yi - py))
    return grid_u[iy, ix], grid_v[iy, ix], corridors[iy, ix], spaces[iy, ix]


def run_agent(start, steps=200, step_size=0.01):
    pos = np.array(start)
    trajectory = [pos.copy()]

    for _ in range(steps):

        vx, vy, is_corridor, is_space = sample_vector(pos[0], pos[1])

        direction = np.array([vx, vy])

        if np.linalg.norm(direction) == 0:
            break

        # normalize direction
        direction = direction / np.linalg.norm(direction)

        # bias rules
        if is_corridor:
            direction *= 1.5  # accelerate in corridor
        if is_space:
            direction *= 0.3  # slow down in space

        pos = pos + step_size * direction
        trajectory.append(pos.copy())

    return np.array(trajectory)


# =========================================================
# RUN AGENT
# =========================================================

start_point = states_2d[0]  # start at beginning of system

agent_path = run_agent(start_point)

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

# CORRIDORS
plt.contour(grid_x, grid_y, corridors, levels=[0.5], colors='red', linewidths=1)

# SPACES
plt.contour(grid_x, grid_y, spaces, levels=[0.5], colors='blue', linewidths=1)

# AGENT PATH
plt.plot(agent_path[:, 0], agent_path[:, 1], color='white', linewidth=2, label="agent")

# START
plt.scatter(agent_path[0, 0], agent_path[0, 1], color='green', label="start")

# END
plt.scatter(agent_path[-1, 0], agent_path[-1, 1], color='yellow', label="end")

plt.title("NEXAH Agent — Field Navigation")
plt.xlabel("PC1")
plt.ylabel("PC2")

plt.legend()
plt.grid(alpha=0.2)
plt.tight_layout()

plt.show()


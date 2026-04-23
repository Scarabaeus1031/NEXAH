import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

print("⚡ NEXAH Separatrix Extraction")

# --------------------------------------------------
# OUTPUT PATH
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../outputs/demo"))
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD DEFINITION
# --------------------------------------------------

def field(x, y):
    dx = -y - x * (x**2 + y**2 - 1)
    dy = x - y * (x**2 + y**2 - 1)
    return dx, dy

# --------------------------------------------------
# TRAJECTORY SIMULATION
# --------------------------------------------------

def simulate_trajectory(x0, y0, steps=220, dt=0.05):
    x, y = x0, y0
    traj = []

    for _ in range(steps):
        dx, dy = field(x, y)
        x += dx * dt
        y += dy * dt
        traj.append([x, y])

    return np.array(traj)

# --------------------------------------------------
# SAMPLE START POINTS
# --------------------------------------------------

np.random.seed(42)

n_points = 300
start_points = np.random.uniform(-2, 2, (n_points, 2))

endpoints = []
trajectories = []

for (x0, y0) in start_points:
    traj = simulate_trajectory(x0, y0)
    trajectories.append(traj)
    endpoints.append(traj[-1])

endpoints = np.array(endpoints)

# --------------------------------------------------
# BASIN CLUSTERING
# --------------------------------------------------

n_basins = 3
kmeans = KMeans(n_clusters=n_basins, n_init=10, random_state=42)
labels = kmeans.fit_predict(endpoints)
centers = kmeans.cluster_centers_

# --------------------------------------------------
# SEPARATRIX DETECTION
# --------------------------------------------------
# Idea:
# If a start point has neighbors that fall into different basins,
# it lies near a basin boundary / separatrix.

nbrs = NearestNeighbors(n_neighbors=8).fit(start_points)
distances, indices = nbrs.kneighbors(start_points)

separatrix_mask = np.zeros(n_points, dtype=bool)
separatrix_strength = np.zeros(n_points)

for i in range(n_points):
    local_labels = labels[indices[i]]
    unique_labels = np.unique(local_labels)

    # if neighbors disagree on basin destination -> boundary candidate
    if len(unique_labels) > 1:
        separatrix_mask[i] = True
        separatrix_strength[i] = len(unique_labels) - 1

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, ax = plt.subplots(figsize=(9, 8))

# background field
grid_x, grid_y = np.meshgrid(
    np.linspace(-2, 2, 30),
    np.linspace(-2, 2, 30)
)
dx, dy = field(grid_x, grid_y)
ax.streamplot(grid_x, grid_y, dx, dy, color='black', density=1.1)

# trajectories, lightly colored by basin
colors = ['blue', 'green', 'red', 'purple', 'orange']

for i, traj in enumerate(trajectories):
    c = colors[labels[i] % len(colors)]
    ax.plot(traj[:, 0], traj[:, 1], color=c, alpha=0.18, linewidth=1)

# all start points
ax.scatter(start_points[:, 0], start_points[:, 1],
           c='lightgray', s=12, alpha=0.7, label='start points')

# basin endpoints
for i in range(n_basins):
    pts = endpoints[labels == i]
    ax.scatter(pts[:, 0], pts[:, 1],
               color=colors[i], s=24, alpha=0.9, label=f'basin {i}')

# basin centers
ax.scatter(centers[:, 0], centers[:, 1],
           color='yellow', s=180, edgecolor='black', linewidth=1.0,
           label='basin centers')

# separatrix points
sep_pts = start_points[separatrix_mask]
sep_strength = separatrix_strength[separatrix_mask]

if len(sep_pts) > 0:
    sc = ax.scatter(
        sep_pts[:, 0], sep_pts[:, 1],
        c=sep_strength,
        cmap='magma',
        s=55,
        edgecolor='white',
        linewidth=0.4,
        label='separatrix'
    )
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("boundary complexity")

ax.set_title("NEXAH Separatrix Extraction")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, alpha=0.25)
ax.legend(loc='best', fontsize=9)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

out_path = os.path.join(OUT_DIR, "nexah_separatrix_extraction.png")
plt.tight_layout()
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

# --------------------------------
# SAVE separatrix points
# --------------------------------

import os

OUTPUT_PATH = "ARCHITECTURE/CORE/control_layer/outputs/demo/"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# --------------------------------
# SAVE separatrix points (FIXED)
# --------------------------------

sep_array = sep_pts  # ← DAS ist deine separatrix!

np.save(
    os.path.join(OUT_DIR, "separatrix_points.npy"),
    sep_array
)

print("✔ Saved → separatrix_points.npy")

# falls mehr Dimensionen → nur x,y
if sep_array.shape[1] > 2:
    sep_array = sep_array[:, :2]

np.save(
    os.path.join(OUTPUT_PATH, "separatrix_points.npy"),
    sep_array
)

print("✔ Saved → separatrix_points.npy")

# --------------------------------------------------
# INTERPRETATION
# --------------------------------------------------

print("""
🧠 Interpretation:

Colored trajectories → basin membership
Yellow points       → approximate basin attractors
Bright boundary pts → separatrix candidates

→ separatrix marks transition structure between basins
→ nearby initial conditions diverge into different long-term states
→ this is the first explicit basin-boundary approximation
""")

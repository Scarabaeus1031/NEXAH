# ENGINE/analysis/navigation_level48c_torus_tuned.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter, label, center_of_mass

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG (TUNED)
# --------------------------------------------------

SIZE = 80
N_AGENTS = 120
STEPS = 900

STEP_SIZE = 0.18        # 🔥 mehr Dynamik
NOISE = 0.002
DAMPING = 0.96

FIELD_BLEND = 0.65
MEMORY_BLEND = 0.35
MEMORY_DECAY = 0.995    # 🔥 stabilere Erinnerung

NODE_THRESHOLD = 0.35   # 🔥 sensibler
EDGE_DISTANCE = 22.0    # 🔥 mehr Verbindungen

LOOP_MIN_LENGTH = 3

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level48c_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

trajectory_map = np.zeros((SIZE, SIZE))

# --------------------------------------------------
# TORUS DISTANCE
# --------------------------------------------------

def torus_distance(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])

    dx = min(dx, SIZE - dx)
    dy = min(dy, SIZE - dy)

    return np.sqrt(dx**2 + dy**2)

# --------------------------------------------------
# GRADIENT (WRAP)
# --------------------------------------------------

def gradient_at(pos, arr):
    x, y = int(pos[0]), int(pos[1])

    xm = (x - 1) % SIZE
    xp = (x + 1) % SIZE
    ym = (y - 1) % SIZE
    yp = (y + 1) % SIZE

    dx = arr[y, xp] - arr[y, xm]
    dy = arr[yp, x] - arr[ym, x]

    return np.array([dx, dy])

# --------------------------------------------------
# SIMULATION (TORUS)
# --------------------------------------------------

for step in range(STEPS):

    combined = FIELD_BLEND * field + MEMORY_BLEND * memory

    for i in range(N_AGENTS):
        pos = positions[i]
        vel = velocities[i]

        grad = gradient_at(pos, combined)
        noise = np.random.randn(2) * NOISE

        vel = DAMPING * vel + STEP_SIZE * grad + noise

        # 🔥 TORUS WRAP
        new_pos = (pos + vel) % SIZE

        x, y = int(new_pos[0]), int(new_pos[1])

        memory[y, x] += 1.0
        trajectory_map[y, x] += 1.0

        positions[i] = new_pos
        velocities[i] = vel

    memory *= MEMORY_DECAY

# --------------------------------------------------
# PHASE FIELD
# --------------------------------------------------

phase_field = np.zeros((SIZE, SIZE))
count_map = np.zeros((SIZE, SIZE))

for pos, vel in zip(positions, velocities):
    x, y = int(pos[0]), int(pos[1])

    angle = np.arctan2(vel[1], vel[0])

    phase_field[y, x] += angle
    count_map[y, x] += 1

mask = count_map > 0
phase_field[mask] /= count_map[mask]

phase_field = gaussian_filter(phase_field, sigma=1.2)

# --------------------------------------------------
# NODE SCORE
# --------------------------------------------------

phase_norm = np.abs(np.sin(phase_field))
crossing_norm = trajectory_map / (np.max(trajectory_map) + 1e-8)

node_score = 0.7 * phase_norm + 0.3 * crossing_norm

node_mask = node_score > NODE_THRESHOLD

labeled, num_features = label(node_mask)

nodes = []
for i in range(1, num_features + 1):
    cy, cx = center_of_mass(node_mask, labeled, i)
    nodes.append((cx, cy))

# --------------------------------------------------
# EDGES (TORUS DIST)
# --------------------------------------------------

edges = []
adj = {i: [] for i in range(len(nodes))}

for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        dist = torus_distance(nodes[i], nodes[j])

        if dist < EDGE_DISTANCE:
            edges.append((i, j))
            adj[i].append(j)
            adj[j].append(i)

# --------------------------------------------------
# LOOP DETECTION (DEDUPED)
# --------------------------------------------------

def normalize_loop(loop):
    return tuple(sorted(loop))

unique_loops = set()

def dfs(path, start):
    current = path[-1]

    for neighbor in adj[current]:
        if neighbor == start and len(path) >= LOOP_MIN_LENGTH:
            unique_loops.add(normalize_loop(path))
        elif neighbor not in path:
            dfs(path + [neighbor], start)

for node in adj:
    dfs([node], node)

loops = list(unique_loops)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(10, 10))

plt.subplot(2, 2, 1)
plt.title("Field")
plt.imshow(field, cmap="viridis")

plt.subplot(2, 2, 2)
plt.title("Node Score")
plt.imshow(node_score, cmap="magma")

node_map = np.zeros((SIZE, SIZE))
for x, y in nodes:
    node_map[int(y), int(x)] = 1

plt.subplot(2, 2, 3)
plt.title("Detected Nodes")
plt.imshow(node_map, cmap="plasma")

lattice_map = np.zeros((SIZE, SIZE))
for i, j in edges:
    x1, y1 = nodes[i]
    x2, y2 = nodes[j]
    lattice_map[int(y1), int(x1)] = 1
    lattice_map[int(y2), int(x2)] = 1

plt.subplot(2, 2, 4)
plt.title("Resonant Lattice")
plt.imshow(lattice_map, cmap="coolwarm")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "torus_tuned.png"))
plt.close()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

result = {
    "num_nodes": len(nodes),
    "num_edges": len(edges),
    "num_loops": len(loops),
    "loops": loops
}

with open(os.path.join(OUTPUT_DIR, "torus_tuned_data.json"), "w") as f:
    json.dump(result, f, indent=2)

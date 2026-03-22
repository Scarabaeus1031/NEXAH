# ENGINE/analysis/navigation_level47_resonant_lattice_v2.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter, label, center_of_mass

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80
N_AGENTS = 120
STEPS = 900

STEP_SIZE = 0.14
NOISE = 0.002
DAMPING = 0.96

FIELD_BLEND = 0.7
MEMORY_BLEND = 0.3
MEMORY_DECAY = 0.992

PHASE_SMOOTH = 1.2

# 🔥 entscheidende Änderungen
NODE_THRESHOLD = 0.42
EDGE_DISTANCE = 28.0

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level47_v2_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

all_angles = []
trajectory_map = np.zeros((SIZE, SIZE))

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def gradient_at(pos, arr):
    x, y = int(pos[0]), int(pos[1])
    x = np.clip(x, 1, SIZE - 2)
    y = np.clip(y, 1, SIZE - 2)

    dx = arr[y, x + 1] - arr[y, x - 1]
    dy = arr[y + 1, x] - arr[y - 1, x]
    return np.array([dx, dy])

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    combined = FIELD_BLEND * field + MEMORY_BLEND * memory

    for i in range(N_AGENTS):
        pos = positions[i]
        vel = velocities[i]

        grad = gradient_at(pos, combined)
        noise = np.random.randn(2) * NOISE

        vel = DAMPING * vel + STEP_SIZE * grad + noise
        new_pos = np.clip(pos + vel, 0, SIZE - 1)

        angle = np.arctan2(vel[1], vel[0])

        memory[int(new_pos[1]), int(new_pos[0])] += 1.0
        trajectory_map[int(new_pos[1]), int(new_pos[0])] += 1.0

        positions[i] = new_pos
        velocities[i] = vel

        all_angles.append(angle)

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

phase_field = gaussian_filter(phase_field, sigma=PHASE_SMOOTH)

# --------------------------------------------------
# NODE SCORE (🔥 verändert)
# --------------------------------------------------

phase_norm = np.abs(np.sin(phase_field))
crossing_norm = trajectory_map / (np.max(trajectory_map) + 1e-8)

node_score = 0.7 * phase_norm + 0.3 * crossing_norm

# --------------------------------------------------
# NODE DETECTION
# --------------------------------------------------

node_mask = node_score > NODE_THRESHOLD

labeled, num_features = label(node_mask)

nodes = []
for i in range(1, num_features + 1):
    cy, cx = center_of_mass(node_mask, labeled, i)
    nodes.append((cx, cy))

# --------------------------------------------------
# EDGE DETECTION
# --------------------------------------------------

edges = []

for i in range(len(nodes)):
    for j in range(i + 1, len(nodes)):
        dx = nodes[i][0] - nodes[j][0]
        dy = nodes[i][1] - nodes[j][1]
        dist = np.sqrt(dx**2 + dy**2)

        if dist < EDGE_DISTANCE:
            edges.append((i, j))

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0, 0].imshow(field)
axs[0, 0].set_title("Field")

axs[0, 1].imshow(node_score)
axs[0, 1].set_title("Node Score")

node_map = np.zeros_like(field)
for x, y in nodes:
    node_map[int(y), int(x)] = 1.0

axs[1, 0].imshow(node_map)
axs[1, 0].set_title("Detected Nodes")

axs[1, 1].imshow(node_score * node_map)
axs[1, 1].set_title("Resonant Lattice")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "resonant_lattice.png"))
plt.close()

# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

result = {
    "num_nodes": len(nodes),
    "nodes": [{"x": float(x), "y": float(y)} for x, y in nodes],
    "num_edges": len(edges),
    "edges": edges,
}

with open(os.path.join(OUTPUT_DIR, "lattice_data.json"), "w") as f:
    json.dump(result, f, indent=2)

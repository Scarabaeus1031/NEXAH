# ENGINE/analysis/navigation_level47_resonant_lattice.py

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

FIELD_BLEND = 0.75
MEMORY_BLEND = 0.25
MEMORY_DECAY = 0.993

SMOOTH = 1.2

# NODE / LATTICE
PHASE_RADIUS = 14.0
MIN_CLUSTER_SIZE = 4
EDGE_DISTANCE = 18.0

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level47_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

phase_field = np.zeros((SIZE, SIZE))
crossing_map = np.zeros((SIZE, SIZE))

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


def compute_phase(vel):
    return np.arctan2(vel[1], vel[0])


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

        x, y = int(new_pos[0]), int(new_pos[1])

        # memory
        memory[y, x] += 1.0

        # phase
        phase = compute_phase(vel)
        phase_field[y, x] += phase

        # crossings (gradient activity)
        if np.linalg.norm(grad) > 0.05:
            crossing_map[y, x] += 1.0

        positions[i] = new_pos
        velocities[i] = vel

    memory *= MEMORY_DECAY

# --------------------------------------------------
# POST PROCESSING
# --------------------------------------------------

memory_s = gaussian_filter(memory, SMOOTH)
phase_s = gaussian_filter(phase_field, SMOOTH)
crossing_s = gaussian_filter(crossing_map, SMOOTH)

# normalize
phase_norm = (phase_s - np.min(phase_s)) / (np.max(phase_s) - np.min(phase_s) + 1e-9)
crossing_norm = crossing_s / (np.max(crossing_s) + 1e-9)

# node score (combined field)
node_score = 0.5 * phase_norm + 0.5 * crossing_norm

# threshold
node_mask = node_score > 0.55

# --------------------------------------------------
# CLUSTER DETECTION
# --------------------------------------------------

labeled, num_features = label(node_mask)

clusters = []
centroids = []

for i in range(1, num_features + 1):
    coords = np.argwhere(labeled == i)

    if len(coords) < MIN_CLUSTER_SIZE:
        continue

    clusters.append(coords)

    cy, cx = np.mean(coords[:, 0]), np.mean(coords[:, 1])
    centroids.append((cx, cy))

# --------------------------------------------------
# BUILD LATTICE (EDGES)
# --------------------------------------------------

edges = []

for i in range(len(centroids)):
    for j in range(i + 1, len(centroids)):

        p1 = np.array(centroids[i])
        p2 = np.array(centroids[j])

        dist = np.linalg.norm(p1 - p2)

        if dist < EDGE_DISTANCE:
            edges.append((i, j))

# --------------------------------------------------
# SAVE JSON
# --------------------------------------------------

output = {
    "num_nodes": len(centroids),
    "nodes": [{"x": float(c[0]), "y": float(c[1])} for c in centroids],
    "num_edges": len(edges),
    "edges": edges
}

with open(f"{OUTPUT_DIR}/lattice.json", "w") as f:
    json.dump(output, f, indent=2)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(10, 10))

# field
plt.subplot(2, 2, 1)
plt.title("Field")
plt.imshow(field, origin="lower")

# node score
plt.subplot(2, 2, 2)
plt.title("Node Score")
plt.imshow(node_score, origin="lower")

# clusters
plt.subplot(2, 2, 3)
plt.title("Detected Nodes")
plt.imshow(node_mask, origin="lower")

for cx, cy in centroids:
    plt.scatter(cx, cy, c="cyan", s=40)

# lattice
plt.subplot(2, 2, 4)
plt.title("Resonant Lattice")

plt.imshow(node_score, origin="lower", alpha=0.4)

# draw edges
for i, j in edges:
    x1, y1 = centroids[i]
    x2, y2 = centroids[j]

    plt.plot([x1, x2], [y1, y2], "white", linewidth=1)

# draw nodes
for cx, cy in centroids:
    plt.scatter(cx, cy, c="yellow", s=50)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/resonant_lattice.png", dpi=150)
plt.close()

# --------------------------------------------------
# DONE
# --------------------------------------------------

print(f"Run complete: {run_id}")
print(f"Nodes: {len(centroids)}")
print(f"Edges: {len(edges)}")

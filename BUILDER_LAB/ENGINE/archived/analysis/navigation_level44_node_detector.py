# ENGINE/analysis/navigation_level44_node_detector.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

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

FIELD_BLEND = 0.8
MEMORY_BLEND = 0.2
MEMORY_DECAY = 0.993

NODE_THRESHOLD = 0.6
MIN_NODE_DISTANCE = 4

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level44_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE))

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

node_map = np.zeros((SIZE, SIZE))

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


def is_local_max(arr, x, y):
    val = arr[y, x]
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            if arr[y + dy, x + dx] > val:
                return False
    return True


def extract_nodes(arr):
    nodes = []
    threshold = NODE_THRESHOLD * np.max(arr)

    for x in range(1, SIZE - 1):
        for y in range(1, SIZE - 1):

            if arr[y, x] > threshold and is_local_max(arr, x, y):
                nodes.append((x, y, arr[y, x]))

    return nodes


def prune_nodes(nodes):
    pruned = []

    for n in nodes:
        keep = True
        for p in pruned:
            dist = np.linalg.norm(np.array(n[:2]) - np.array(p[:2]))
            if dist < MIN_NODE_DISTANCE:
                keep = False
                break
        if keep:
            pruned.append(n)

    return pruned


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

        memory[int(new_pos[1]), int(new_pos[0])] += 1.0

        positions[i] = new_pos
        velocities[i] = vel

    memory *= MEMORY_DECAY

# --------------------------------------------------
# NODE DETECTION
# --------------------------------------------------

smooth_memory = gaussian_filter(memory, sigma=1.2)

raw_nodes = extract_nodes(smooth_memory)
nodes = prune_nodes(raw_nodes)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(1, 2, figsize=(10, 5))

axs[0].imshow(field)
axs[0].set_title("Field")

axs[1].imshow(smooth_memory)
axs[1].set_title("Node Map")

for x, y, v in nodes:
    axs[1].scatter(x, y)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/nodes.png")
plt.close()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

output = {
    "num_nodes": len(nodes),
    "nodes": [(float(x), float(y), float(v)) for x, y, v in nodes]
}

with open(f"{OUTPUT_DIR}/nodes.json", "w") as f:
    json.dump(output, f, indent=2)

print("Run complete:", run_id)
print("Nodes found:", len(nodes))

import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime
from scipy.ndimage import label, center_of_mass
from scipy.spatial.distance import cdist

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80
N_AGENTS = 120
STEPS = 700

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

MEMORY_DECAY = 0.992
SYMBOL_THRESHOLD = 0.12

GROUP_DISTANCE = 10.0
COMPOSITION_DISTANCE = 18.0
MAX_CONNECTIONS = 3

# --------------------------------------------------
# SETUP
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_DIR = "ENGINE/visuals/navigation_level33"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD
# --------------------------------------------------

field = generate_stability_landscape(size=SIZE)

# --------------------------------------------------
# AGENTS
# --------------------------------------------------

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)
memory = np.zeros((SIZE, SIZE))

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    grads = np.gradient(field)

    for i in range(N_AGENTS):
        x, y = positions[i]
        xi, yi = int(x), int(y)

        gx = grads[1][yi % SIZE, xi % SIZE]
        gy = grads[0][yi % SIZE, xi % SIZE]

        force = np.array([gx, gy])

        velocities[i] += STEP_SIZE * force
        velocities[i] += NOISE * np.random.randn(2)
        velocities[i] *= DAMPING

        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], 0, SIZE - 1)

        px, py = int(positions[i][0]), int(positions[i][1])
        memory[py, px] += 1.0

    memory *= MEMORY_DECAY

# --------------------------------------------------
# SYMBOL DETECTION
# --------------------------------------------------

mem_norm = memory / (memory.max() + 1e-8)
symbol_mask = mem_norm > SYMBOL_THRESHOLD

labeled, num_features = label(symbol_mask)

symbol_centroids = center_of_mass(
    symbol_mask,
    labeled,
    range(1, num_features + 1)
)

symbol_centroids = np.array(symbol_centroids) if len(symbol_centroids) > 0 else np.zeros((0, 2))

# --------------------------------------------------
# SEMANTIC GROUPING (Level 32)
# --------------------------------------------------

semantic_groups = []

if len(symbol_centroids) > 0:
    dist_matrix = cdist(symbol_centroids, symbol_centroids)
    visited = set()

    for i in range(len(symbol_centroids)):
        if i in visited:
            continue

        stack = [i]
        group = []

        while stack:
            n = stack.pop()
            if n not in visited:
                visited.add(n)
                group.append(n)

                neighbors = np.where(dist_matrix[n] < GROUP_DISTANCE)[0]
                stack.extend(neighbors)

        semantic_groups.append(group)

# group centroids
group_centroids = []

for group in semantic_groups:
    pts = symbol_centroids[group]
    center = np.mean(pts, axis=0)
    group_centroids.append(center)

group_centroids = np.array(group_centroids) if len(group_centroids) > 0 else np.zeros((0, 2))

# --------------------------------------------------
# COMPOSITION GRAPH (Level 33)
# --------------------------------------------------

edges = []

if len(group_centroids) > 1:
    dist_matrix = cdist(group_centroids, group_centroids)

    for i in range(len(group_centroids)):
        nearest = np.argsort(dist_matrix[i])[1:MAX_CONNECTIONS+1]

        for j in nearest:
            if dist_matrix[i][j] < COMPOSITION_DISTANCE:
                edges.append((i, j))

# --------------------------------------------------
# COMPONENTS (SYNTAX)
# --------------------------------------------------

graph = {i: set() for i in range(len(group_centroids))}

for i, j in edges:
    graph[i].add(j)
    graph[j].add(i)

visited = set()
components = []

for node in graph:
    if node not in visited:
        stack = [node]
        comp = []

        while stack:
            n = stack.pop()
            if n not in visited:
                visited.add(n)
                comp.append(n)
                stack.extend(graph[n])

        components.append(comp)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

component_sizes = [len(c) for c in components]

metrics = {
    "semantic_groups": int(len(semantic_groups)),
    "components": int(len(components)),
    "avg_component_size": float(np.mean(component_sizes) if component_sizes else 0),
    "max_component_size": int(max(component_sizes) if component_sizes else 0)
}

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# FIELD
axs[0, 0].imshow(field, cmap='viridis')
axs[0, 0].set_title("Field")

# MEMORY
axs[0, 1].imshow(memory, cmap='magma')
axs[0, 1].set_title("Symbol Memory")

# SEMANTIC GROUPS
axs[1, 0].imshow(symbol_mask, cmap='gray')
axs[1, 0].set_title("Semantic Groups")

for group in semantic_groups:
    pts = symbol_centroids[group]
    axs[1, 0].scatter(pts[:, 1], pts[:, 0], s=10)

# COMPOSITION GRAPH
axs[1, 1].imshow(symbol_mask, cmap='gray')
axs[1, 1].set_title("Semantic Composition")

for i, j in edges:
    y1, x1 = group_centroids[i]
    y2, x2 = group_centroids[j]
    axs[1, 1].plot([x1, x2], [y1, y2], color='cyan', linewidth=2)

axs[1, 1].scatter(group_centroids[:, 1], group_centroids[:, 0], c='red', s=40)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

img_path = os.path.join(OUTPUT_DIR, f"level33_{run_id}.png")
plt.tight_layout()
plt.savefig(img_path, dpi=200)
plt.close()

json_path = os.path.join(OUTPUT_DIR, f"level33_{run_id}.json")

with open(json_path, "w") as f:
    json.dump({
        "run_id": run_id,
        "metrics": metrics
    }, f, indent=2)

# --------------------------------------------------
# DONE
# --------------------------------------------------

print("Run complete:", run_id)
print("Semantic groups:", metrics["semantic_groups"])
print("Components:", metrics["components"])

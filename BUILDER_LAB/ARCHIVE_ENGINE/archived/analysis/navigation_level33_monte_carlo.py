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

RUNS = 30

SIZE = 80
N_AGENTS = 120
STEPS = 700

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

MEMORY_DECAY = 0.992
SYMBOL_THRESHOLD = 0.12

GROUP_DISTANCE = 6.0
COMPOSITION_DISTANCE = 10.0
MAX_CONNECTIONS = 3

OUTPUT_DIR = "ENGINE/visuals/navigation_level33_monte_carlo"
os.makedirs(OUTPUT_DIR, exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --------------------------------------------------
# STORAGE
# --------------------------------------------------

all_metrics = []

# --------------------------------------------------
# RUN LOOP
# --------------------------------------------------

for run in range(RUNS):

    field = generate_stability_landscape(size=SIZE)

    positions = np.random.rand(N_AGENTS, 2) * SIZE
    velocities = np.zeros_like(positions)
    memory = np.zeros((SIZE, SIZE))

    # ------------------------------
    # SIMULATION
    # ------------------------------

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

    # ------------------------------
    # SYMBOL DETECTION
    # ------------------------------

    mem_norm = memory / (memory.max() + 1e-8)
    symbol_mask = mem_norm > SYMBOL_THRESHOLD

    labeled, num_features = label(symbol_mask)
    symbol_centroids = center_of_mass(
        symbol_mask,
        labeled,
        range(1, num_features + 1)
    )

    symbol_centroids = np.array(symbol_centroids) if len(symbol_centroids) > 0 else np.zeros((0, 2))

    # ------------------------------
    # SEMANTIC GROUPS
    # ------------------------------

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

    # ------------------------------
    # GROUP CENTROIDS
    # ------------------------------

    group_centroids = []

    for group in semantic_groups:
        pts = symbol_centroids[group]
        center = np.mean(pts, axis=0)
        group_centroids.append(center)

    group_centroids = np.array(group_centroids) if len(group_centroids) > 0 else np.zeros((0, 2))

    # ------------------------------
    # COMPOSITION GRAPH
    # ------------------------------

    edges = []

    if len(group_centroids) > 1:
        dist_matrix = cdist(group_centroids, group_centroids)

        for i in range(len(group_centroids)):
            nearest = np.argsort(dist_matrix[i])[1:MAX_CONNECTIONS+1]

            for j in nearest:
                if dist_matrix[i][j] < COMPOSITION_DISTANCE:
                    edges.append((i, j))

    # ------------------------------
    # COMPONENTS
    # ------------------------------

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

    # ------------------------------
    # METRICS
    # ------------------------------

    component_sizes = [len(c) for c in components]

    metrics = {
        "run": run,
        "semantic_groups": len(semantic_groups),
        "components": len(components),
        "avg_component_size": float(np.mean(component_sizes) if component_sizes else 0),
        "max_component_size": int(max(component_sizes) if component_sizes else 0)
    }

    all_metrics.append(metrics)

    print(f"Run {run+1}/{RUNS} → groups: {metrics['semantic_groups']} | components: {metrics['components']}")

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

groups = [m["semantic_groups"] for m in all_metrics]
components = [m["components"] for m in all_metrics]

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.hist(groups, bins=range(0, max(groups)+2))
plt.title("Semantic Groups Distribution")

plt.subplot(1,2,2)
plt.hist(components, bins=range(0, max(components)+2))
plt.title("Components Distribution")

plt.tight_layout()

img_path = os.path.join(OUTPUT_DIR, f"monte_carlo_{run_id}.png")
plt.savefig(img_path, dpi=200)
plt.close()

# --------------------------------------------------
# SAVE JSON
# --------------------------------------------------

json_path = os.path.join(OUTPUT_DIR, f"monte_carlo_{run_id}.json")

with open(json_path, "w") as f:
    json.dump(all_metrics, f, indent=2)

print("\nMonte Carlo complete:", run_id)

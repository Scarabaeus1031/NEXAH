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
N_AGENTS = 100          # etwas reduziert → stabiler
STEPS = 600             # reduziert → kein Hängen

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

MEMORY_DECAY = 0.992
SYMBOL_THRESHOLD = 0.12

GROUP_DISTANCE = 6.0
GRAMMAR_DISTANCE = 14.0
MAX_CONNECTIONS = 3

TRANSITION_RADIUS = 8.0

# --------------------------------------------------
# SETUP
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_DIR = "ENGINE/visuals/navigation_level34"
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
centroids = center_of_mass(symbol_mask, labeled, range(1, num_features + 1))
centroids = np.array(centroids) if len(centroids) > 0 else np.zeros((0, 2))

# --------------------------------------------------
# GRAMMAR GRAPH (DIRECTED EDGES)
# --------------------------------------------------

edges = []
directions = []

if len(centroids) > 1:
    dist_matrix = cdist(centroids, centroids)

    for i in range(len(centroids)):
        nearest = np.argsort(dist_matrix[i])[1:MAX_CONNECTIONS+1]

        for j in nearest:
            d = dist_matrix[i][j]
            if d < GRAMMAR_DISTANCE:
                edges.append((i, j))

                # Richtung bestimmen (Vektor)
                y1, x1 = centroids[i]
                y2, x2 = centroids[j]
                directions.append((x2 - x1, y2 - y1))

# --------------------------------------------------
# TRANSITION MATRIX (SEHR SIMPEL)
# --------------------------------------------------

transition_matrix = np.zeros((len(centroids), len(centroids)))

for i, j in edges:
    transition_matrix[i][j] += 1

# --------------------------------------------------
# METRICS
# --------------------------------------------------

total_edges = len(edges)

metrics = {
    "symbols": int(len(centroids)),
    "edges": int(total_edges),
    "density": float(total_edges / (len(centroids)**2 + 1e-8))
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

# GRAMMAR GRAPH (PFEILE!)
axs[1, 0].imshow(symbol_mask, cmap='gray')
axs[1, 0].set_title("Symbol Grammar (Directed)")

for idx, (i, j) in enumerate(edges):
    y1, x1 = centroids[i]
    y2, x2 = centroids[j]

    axs[1, 0].arrow(
        x1, y1,
        x2 - x1, y2 - y1,
        color='cyan',
        head_width=1.2,
        length_includes_head=True,
        alpha=0.7
    )

axs[1, 0].scatter(centroids[:, 1], centroids[:, 0], c='red', s=12)

# TRANSITION MATRIX
axs[1, 1].imshow(transition_matrix, cmap='plasma')
axs[1, 1].set_title("Transition Matrix")

# --------------------------------------------------
# SAVE
# --------------------------------------------------

img_path = os.path.join(OUTPUT_DIR, f"level34_{run_id}.png")
plt.tight_layout()
plt.savefig(img_path, dpi=200)
plt.close()

json_path = os.path.join(OUTPUT_DIR, f"level34_{run_id}.json")
with open(json_path, "w") as f:
    json.dump({
        "run_id": run_id,
        "metrics": metrics
    }, f, indent=2)

# --------------------------------------------------
# PRINT
# --------------------------------------------------

print("Run complete:", run_id)
print("Symbols:", metrics["symbols"])
print("Edges:", metrics["edges"])
print("Density:", metrics["density"])

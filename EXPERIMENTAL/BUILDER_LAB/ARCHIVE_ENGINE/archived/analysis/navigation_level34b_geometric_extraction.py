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
N_AGENTS = 100
STEPS = 600

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

MEMORY_DECAY = 0.992
SYMBOL_THRESHOLD = 0.12

PHI = (1 + np.sqrt(5)) / 2

# --------------------------------------------------
# SETUP
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_DIR = "ENGINE/visuals/navigation_level34b"
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

if len(centroids) > 0:
    centroids = np.array(centroids)
else:
    centroids = np.zeros((0, 2))

# --------------------------------------------------
# GEOMETRY ANALYSIS
# --------------------------------------------------

distances = []
angles = []
phi_matches = []

def compute_angle(a, b, c):
    ba = a - b
    bc = c - b

    denom = (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-8)
    cos_angle = np.dot(ba, bc) / denom
    cos_angle = np.clip(cos_angle, -1.0, 1.0)

    return np.degrees(np.arccos(cos_angle))

# --- distances ---
if len(centroids) >= 2:
    dist_matrix = cdist(centroids, centroids)

    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            distances.append(dist_matrix[i][j])

# --- angles ---
if len(centroids) >= 3:
    for i in range(len(centroids)):
        for j in range(len(centroids)):
            for k in range(len(centroids)):
                if i != j and j != k and i != k:
                    A = centroids[i]
                    B = centroids[j]
                    C = centroids[k]

                    angle = compute_angle(A, B, C)
                    angles.append(angle)

# --- phi detection ---
for d1 in distances:
    for d2 in distances:
        if d2 > 0:
            ratio = d1 / d2
            if abs(ratio - PHI) < 0.1:
                phi_matches.append(ratio)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

metrics = {
    "symbols": int(len(centroids)),
    "avg_distance": float(np.mean(distances) if distances else 0),
    "avg_angle": float(np.mean(angles) if angles else 0),
    "phi_matches": int(len(phi_matches))
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

# GEOMETRY GRAPH
axs[1, 0].imshow(symbol_mask, cmap='gray')
axs[1, 0].set_title("Geometric Structure")

for i in range(len(centroids)):
    for j in range(i + 1, len(centroids)):
        y1, x1 = centroids[i]
        y2, x2 = centroids[j]

        axs[1, 0].plot([x1, x2], [y1, y2], color='cyan', alpha=0.5)

if len(centroids) > 0:
    axs[1, 0].scatter(centroids[:, 1], centroids[:, 0], c='red', s=12)

# ANGLE HISTOGRAM
axs[1, 1].hist(angles, bins=20)
axs[1, 1].set_title("Angle Distribution")

# --------------------------------------------------
# SAVE
# --------------------------------------------------

img_path = os.path.join(OUTPUT_DIR, f"level34b_{run_id}.png")
plt.tight_layout()
plt.savefig(img_path, dpi=200)
plt.close()

json_path = os.path.join(OUTPUT_DIR, f"level34b_{run_id}.json")
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
print("Avg distance:", metrics["avg_distance"])
print("Avg angle:", metrics["avg_angle"])
print("Phi matches:", metrics["phi_matches"])

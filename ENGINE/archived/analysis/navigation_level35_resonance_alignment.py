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
STEPS = 650

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

MEMORY_DECAY = 0.992
SYMBOL_THRESHOLD = 0.12

PHI = (1 + np.sqrt(5)) / 2

# angle clustering
ANGLE_BINS = 36  # 10° resolution
GATE_THRESHOLD = 0.08  # tolerance for phi-alignment

# --------------------------------------------------
# SETUP
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_DIR = "ENGINE/visuals/navigation_level35"
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
# ANGLE + AXIS DETECTION
# --------------------------------------------------

angles = []
axes = []

if len(centroids) >= 2:
    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            dy = centroids[j][0] - centroids[i][0]
            dx = centroids[j][1] - centroids[i][1]

            angle = np.degrees(np.arctan2(dy, dx)) % 180
            angles.append(angle)
            axes.append((i, j, angle))

angles = np.array(angles)

# histogram → dominant axes
hist, bin_edges = np.histogram(angles, bins=ANGLE_BINS, range=(0, 180))

dominant_bins = np.where(hist > np.mean(hist))[0]

dominant_angles = []
for b in dominant_bins:
    angle_center = (bin_edges[b] + bin_edges[b + 1]) / 2
    dominant_angles.append(angle_center)

# --------------------------------------------------
# PHI ALIGNMENT
# --------------------------------------------------

phi_aligned_edges = []

if len(centroids) >= 2:
    dist_matrix = cdist(centroids, centroids)

    for i in range(len(centroids)):
        for j in range(i + 1, len(centroids)):
            for k in range(len(centroids)):
                if k != i and k != j:

                    d1 = dist_matrix[i][j]
                    d2 = dist_matrix[j][k]

                    if d2 > 1e-6:
                        ratio = d1 / d2

                        if abs(ratio - PHI) < GATE_THRESHOLD:
                            phi_aligned_edges.append((i, j))

# --------------------------------------------------
# METRICS
# --------------------------------------------------

metrics = {
    "symbols": int(len(centroids)),
    "dominant_axes": len(dominant_angles),
    "phi_aligned_edges": len(phi_aligned_edges),
    "avg_angle": float(np.mean(angles) if len(angles) > 0 else 0)
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

# AXIS + PHI GRAPH
axs[1, 0].imshow(symbol_mask, cmap='gray')
axs[1, 0].set_title("Resonance Alignment")

# draw all connections faint
for i in range(len(centroids)):
    for j in range(i + 1, len(centroids)):
        y1, x1 = centroids[i]
        y2, x2 = centroids[j]

        axs[1, 0].plot([x1, x2], [y1, y2], color='cyan', alpha=0.2)

# highlight phi-aligned edges
for i, j in phi_aligned_edges:
    y1, x1 = centroids[i]
    y2, x2 = centroids[j]

    axs[1, 0].plot([x1, x2], [y1, y2], color='magenta', linewidth=2)

# plot centroids
if len(centroids) > 0:
    axs[1, 0].scatter(centroids[:, 1], centroids[:, 0], c='red', s=15)

# ANGLE HISTOGRAM
axs[1, 1].hist(angles, bins=ANGLE_BINS)
axs[1, 1].set_title("Axis Distribution")

# --------------------------------------------------
# SAVE
# --------------------------------------------------

img_path = os.path.join(OUTPUT_DIR, f"level35_{run_id}.png")
plt.tight_layout()
plt.savefig(img_path, dpi=200)
plt.close()

json_path = os.path.join(OUTPUT_DIR, f"level35_{run_id}.json")
with open(json_path, "w") as f:
    json.dump({
        "run_id": run_id,
        "metrics": metrics,
        "dominant_angles": dominant_angles
    }, f, indent=2)

# --------------------------------------------------
# PRINT
# --------------------------------------------------

print("Run complete:", run_id)
print("Symbols:", metrics["symbols"])
print("Dominant axes:", metrics["dominant_axes"])
print("Phi-aligned edges:", metrics["phi_aligned_edges"])
print("Avg angle:", metrics["avg_angle"])

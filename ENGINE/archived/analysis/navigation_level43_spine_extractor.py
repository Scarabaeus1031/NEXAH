# ENGINE/analysis/navigation_level43_spine_extractor.py

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

FIELD_BLEND = 0.80
MEMORY_BLEND = 0.20
MEMORY_DECAY = 0.993

ANGLE_BINS = 180
SPINE_SMOOTH = 1.2
MIN_SPINE_POINTS = 8

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level43_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

trajectories = [[] for _ in range(N_AGENTS)]
all_angles = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def get_gradient(f, x, y):
    xi, yi = int(x), int(y)
    if xi <= 1 or yi <= 1 or xi >= SIZE - 2 or yi >= SIZE - 2:
        return np.zeros(2)

    dx = f[yi, xi + 1] - f[yi, xi - 1]
    dy = f[yi + 1, xi] - f[yi - 1, xi]

    return np.array([dx, dy])


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    memory *= MEMORY_DECAY

    for i in range(N_AGENTS):

        x, y = positions[i]

        grad_field = get_gradient(field, x, y)
        grad_memory = get_gradient(memory, x, y)

        force = (
            FIELD_BLEND * grad_field +
            MEMORY_BLEND * grad_memory
        )

        velocities[i] += STEP_SIZE * force
        velocities[i] *= DAMPING
        velocities[i] += NOISE * np.random.randn(2)

        positions[i] += velocities[i]

        positions[i] = np.clip(positions[i], 0, SIZE - 1)

        xi, yi = int(positions[i][0]), int(positions[i][1])
        memory[yi, xi] += 1.0

        trajectories[i].append(positions[i].copy())

        angle = np.arctan2(velocities[i][1], velocities[i][0])
        all_angles.append(angle)


# --------------------------------------------------
# ANGLE DISTRIBUTION
# --------------------------------------------------

hist, bin_edges = np.histogram(all_angles, bins=ANGLE_BINS, range=(-np.pi, np.pi))
hist_smooth = gaussian_filter(hist.astype(float), sigma=SPINE_SMOOTH)

# dominant peaks = "spine directions"
threshold = np.mean(hist_smooth) * 1.5
spine_indices = np.where(hist_smooth > threshold)[0]

# filter clusters
spine_angles = []
current_cluster = []

for idx in spine_indices:
    if not current_cluster:
        current_cluster = [idx]
    elif idx == current_cluster[-1] + 1:
        current_cluster.append(idx)
    else:
        if len(current_cluster) >= MIN_SPINE_POINTS:
            spine_angles.append(np.mean(current_cluster))
        current_cluster = [idx]

if len(current_cluster) >= MIN_SPINE_POINTS:
    spine_angles.append(np.mean(current_cluster))

spine_angles = np.array(spine_angles)
spine_angles = bin_edges[0] + spine_angles * (2 * np.pi / ANGLE_BINS)

# --------------------------------------------------
# SAVE RESULTS
# --------------------------------------------------

result = {
    "num_spines": int(len(spine_angles)),
    "spine_angles": spine_angles.tolist()
}

with open(os.path.join(OUTPUT_DIR, "spine_data.json"), "w") as f:
    json.dump(result, f, indent=2)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig = plt.figure(figsize=(12, 10))

# Field
plt.subplot(2, 2, 1)
plt.title("Field")
plt.imshow(field, cmap="viridis")

# Memory
plt.subplot(2, 2, 2)
plt.title("Memory")
plt.imshow(memory, cmap="magma")

# Angle distribution
plt.subplot(2, 2, 3, projection="polar")
plt.title("Spine Distribution")

theta = np.linspace(-np.pi, np.pi, ANGLE_BINS)
plt.plot(theta, hist_smooth)

# draw detected spines
for angle in spine_angles:
    plt.plot([angle, angle], [0, np.max(hist_smooth)], linewidth=2)

# Trajectories
plt.subplot(2, 2, 4)
plt.title("Trajectories")

for traj in trajectories:
    traj = np.array(traj)
    plt.plot(traj[:, 0], traj[:, 1], alpha=0.2)

# draw spine directions
center = np.array([SIZE/2, SIZE/2])
for angle in spine_angles:
    direction = np.array([np.cos(angle), np.sin(angle)])
    end = center + direction * SIZE/2
    plt.plot([center[0], end[0]], [center[1], end[1]], linewidth=2)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "spine_plot.png"))
plt.close()

print("Run complete:", run_id)
print("Spines found:", len(spine_angles))

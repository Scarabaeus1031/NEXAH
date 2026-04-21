# ENGINE/analysis/navigation_level44b_phase_boundary_detector.py

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

FIELD_BLEND = 0.75
MEMORY_BLEND = 0.25
MEMORY_DECAY = 0.993

PHASE_RADIUS = 14.0
PHASE_SMOOTH = 1.2
BOUNDARY_THRESHOLD = 0.55
MIN_PHASE_SAMPLES = 3

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level44b_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

all_states = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


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
        speed = np.linalg.norm(vel)

        memory[int(new_pos[1]), int(new_pos[0])] += 1.0

        positions[i] = new_pos
        velocities[i] = vel

        all_states.append((new_pos[0], new_pos[1], angle, speed))

    memory *= MEMORY_DECAY

# --------------------------------------------------
# PHASE FIELD
# --------------------------------------------------

center = np.array([SIZE / 2, SIZE / 2])

phase_sum = np.zeros((SIZE, SIZE), dtype=float)
phase_count = np.zeros((SIZE, SIZE), dtype=float)

for x, y, angle, speed in all_states:
    vec = np.array([x, y]) - center
    r = np.linalg.norm(vec)

    if r < 1e-6 or r > PHASE_RADIUS:
        continue

    radial_angle = np.arctan2(vec[1], vec[0])
    phase = wrap_angle(angle - radial_angle)

    px, py = int(x), int(y)
    phase_sum[py, px] += phase
    phase_count[py, px] += 1.0

phase_field = np.zeros((SIZE, SIZE), dtype=float)
mask = phase_count >= MIN_PHASE_SAMPLES
phase_field[mask] = phase_sum[mask] / phase_count[mask]

phase_field = gaussian_filter(phase_field, sigma=PHASE_SMOOTH)

# --------------------------------------------------
# BOUNDARY DETECTION
# --------------------------------------------------

gy, gx = np.gradient(phase_field)
boundary_strength = np.sqrt(gx**2 + gy**2)

if np.max(boundary_strength) > 0:
    boundary_norm = boundary_strength / np.max(boundary_strength)
else:
    boundary_norm = boundary_strength.copy()

boundary_mask = boundary_norm > BOUNDARY_THRESHOLD

# boundary coordinates
boundary_points = np.argwhere(boundary_mask)

# --------------------------------------------------
# OPTIONAL: CENTRAL BOUNDARY CLUSTERS
# --------------------------------------------------

central_points = []
for py, px in boundary_points:
    dist = np.linalg.norm(np.array([px, py]) - center)
    if dist <= PHASE_RADIUS + 4:
        central_points.append((int(px), int(py)))

# crude "anchor" estimation by quadrant
anchors = []
if len(central_points) > 0:
    pts = np.array(central_points, dtype=float)

    quadrants = [
        pts[(pts[:, 0] < center[0]) & (pts[:, 1] < center[1])],  # upper-left
        pts[(pts[:, 0] >= center[0]) & (pts[:, 1] < center[1])], # upper-right
        pts[(pts[:, 0] < center[0]) & (pts[:, 1] >= center[1])], # lower-left
        pts[(pts[:, 0] >= center[0]) & (pts[:, 1] >= center[1])] # lower-right
    ]

    for q in quadrants:
        if len(q) > 0:
            mx, my = np.mean(q[:, 0]), np.mean(q[:, 1])
            anchors.append((float(mx), float(my)))

# --------------------------------------------------
# SAVE
# --------------------------------------------------

result = {
    "num_boundary_points": int(len(boundary_points)),
    "num_central_boundary_points": int(len(central_points)),
    "num_anchor_regions": int(len(anchors)),
    "anchors": anchors
}

with open(os.path.join(OUTPUT_DIR, "phase_boundaries.json"), "w") as f:
    json.dump(result, f, indent=2)

# --------------------------------------------------
# PLOTS
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Field
axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

# Memory
axs[0, 1].imshow(memory, cmap="magma")
axs[0, 1].set_title("Memory")

# Phase field
im = axs[1, 0].imshow(phase_field, cmap="twilight", vmin=-np.pi, vmax=np.pi)
axs[1, 0].set_title("Phase Field")
plt.colorbar(im, ax=axs[1, 0], fraction=0.046, pad=0.04)

# Boundary map
axs[1, 1].imshow(boundary_norm, cmap="inferno")
axs[1, 1].contour(boundary_mask.astype(float), levels=[0.5], colors="cyan", linewidths=1.0)
axs[1, 1].scatter(center[0], center[1], c="white", s=30, label="center")

if len(anchors) > 0:
    ax_x = [a[0] for a in anchors]
    ax_y = [a[1] for a in anchors]
    axs[1, 1].scatter(ax_x, ax_y, c="lime", s=45, label="anchors")

axs[1, 1].set_title("Phase Boundary Detector")
axs[1, 1].legend(loc="upper right", fontsize=8)

for ax in axs.flat:
    ax.set_xlim(0, SIZE - 1)
    ax.set_ylim(SIZE - 1, 0)

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "phase_boundaries.png"))
plt.close()

# --------------------------------------------------
# DONE
# --------------------------------------------------

print(f"Run complete: {run_id}")

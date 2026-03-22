# ENGINE/analysis/navigation_level46_spine_phase_field.py

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

ANGLE_BINS = 180
SMOOTH = 1.2
PEAK_THRESHOLD = 0.6

PHASE_RADIUS = 10.0
MIN_SAMPLES_PER_CELL = 3

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level46_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

all_angles = []
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


def detect_peaks(hist, threshold=0.6):
    max_val = np.max(hist)
    peaks = []

    for i in range(len(hist)):
        if hist[i] > threshold * max_val:
            peaks.append(i)

    return peaks


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

        all_angles.append(angle)
        all_states.append((new_pos[0], new_pos[1], angle, speed))

    memory *= MEMORY_DECAY

# --------------------------------------------------
# ANGLE ANALYSIS (SPINE BASE)
# --------------------------------------------------

hist, bins = np.histogram(all_angles, bins=ANGLE_BINS, range=(-np.pi, np.pi))
hist = gaussian_filter(hist.astype(float), SMOOTH)

bin_centers = (bins[:-1] + bins[1:]) / 2
peaks = detect_peaks(hist, PEAK_THRESHOLD)
peak_angles = bin_centers[peaks]

# --------------------------------------------------
# PHASE FIELD BUILDING
# --------------------------------------------------

center = np.array([SIZE / 2, SIZE / 2])

phase_field = np.zeros((SIZE, SIZE))
phase_count = np.zeros((SIZE, SIZE))

cw_field = np.zeros((SIZE, SIZE))
ccw_field = np.zeros((SIZE, SIZE))

for x, y, angle, speed in all_states:

    px, py = int(x), int(y)

    vec = np.array([x, y]) - center
    r = np.linalg.norm(vec)

    if r < 1e-5:
        continue

    radial_angle = np.arctan2(vec[1], vec[0])
    phase = wrap_angle(angle - radial_angle)

    phase_field[py, px] += phase
    phase_count[py, px] += 1

    # rotation classification
    if phase > 0:
        ccw_field[py, px] += 1
    else:
        cw_field[py, px] += 1

# normalize phase
mask = phase_count > MIN_SAMPLES_PER_CELL
phase_field[mask] /= phase_count[mask]

# smooth everything
phase_field = gaussian_filter(phase_field, 1.0)
cw_field = gaussian_filter(cw_field, 1.0)
ccw_field = gaussian_filter(ccw_field, 1.0)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

cw_total = np.sum(cw_field)
ccw_total = np.sum(ccw_field)

if cw_total + ccw_total > 0:
    rotation_bias = (ccw_total - cw_total) / (cw_total + ccw_total)
else:
    rotation_bias = 0.0

result = {
    "num_peaks": int(len(peak_angles)),
    "peak_angles": peak_angles.tolist(),
    "rotation_bias": float(rotation_bias),
    "cw_total": float(cw_total),
    "ccw_total": float(ccw_total),
}

with open(os.path.join(OUTPUT_DIR, "phase_field.json"), "w") as f:
    json.dump(result, f, indent=2)

# --------------------------------------------------
# PLOTS
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Field
axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

# Phase Field
im = axs[0, 1].imshow(phase_field, cmap="twilight")
axs[0, 1].set_title("Phase Field (Rotation)")
plt.colorbar(im, ax=axs[0, 1], fraction=0.046)

# CW vs CCW
axs[1, 0].imshow(ccw_field - cw_field, cmap="bwr")
axs[1, 0].set_title("CCW vs CW Dominance")

# Polar Peaks
axp = plt.subplot(2, 2, 4, projection="polar")
axp.plot(bin_centers, hist)

for a in peak_angles:
    axp.plot([a, a], [0, np.max(hist)], linewidth=2)

axp.set_title("Spine + Phase Anchors")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "phase_field.png"))
plt.close()

# --------------------------------------------------
# DONE
# --------------------------------------------------

print(f"Run complete: {run_id}")
print(f"Peaks: {len(peak_angles)}")
print(f"Rotation bias (CCW positive): {rotation_bias:.3f}")

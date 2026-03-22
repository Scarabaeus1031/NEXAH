# ENGINE/analysis/navigation_level43b_spine_peak_extractor.py

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
SMOOTH = 1.0

PEAK_THRESHOLD = 1.15   # softer than before
MIN_PEAK_DISTANCE = 3   # bins

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level43b_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

all_angles = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi

def gradient_at(pos, field):
    x, y = int(pos[0]), int(pos[1])
    x = np.clip(x, 1, SIZE - 2)
    y = np.clip(y, 1, SIZE - 2)

    dx = field[y, x + 1] - field[y, x - 1]
    dy = field[y + 1, x] - field[y - 1, x]

    return np.array([dx, dy])

def find_peaks(hist):
    peaks = []
    threshold = np.mean(hist) * PEAK_THRESHOLD

    for i in range(len(hist)):
        left = hist[i - 1]
        center = hist[i]
        right = hist[(i + 1) % len(hist)]

        if center > left and center > right and center > threshold:
            peaks.append(i)

    # merge nearby peaks
    filtered = []
    for p in peaks:
        if not any(abs(p - fp) < MIN_PEAK_DISTANCE for fp in filtered):
            filtered.append(p)

    return filtered

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        pos = positions[i]
        vel = velocities[i]

        grad = gradient_at(pos, field)

        mem_val = memory[int(pos[1]), int(pos[0])]
        grad_mem = gradient_at(pos, memory)

        total_force = (
            FIELD_BLEND * grad +
            MEMORY_BLEND * grad_mem
        )

        vel = DAMPING * vel + STEP_SIZE * total_force
        vel += np.random.randn(2) * NOISE

        new_pos = pos + vel
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        angle = np.arctan2(vel[1], vel[0])
        all_angles.append(angle)

        memory[int(new_pos[1]), int(new_pos[0])] += 1.0

        positions[i] = new_pos
        velocities[i] = vel

    memory *= MEMORY_DECAY

# --------------------------------------------------
# ANALYSIS: PEAK SPINES
# --------------------------------------------------

hist, bins = np.histogram(all_angles, bins=ANGLE_BINS, range=(-np.pi, np.pi))
hist_smooth = gaussian_filter(hist.astype(float), sigma=SMOOTH)

peaks = find_peaks(hist_smooth)

peak_angles = []
for p in peaks:
    angle = (bins[p] + bins[p + 1]) / 2
    peak_angles.append(angle)

# --------------------------------------------------
# PLOTS
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

# Polar
ax = plt.subplot(2, 2, 3, polar=True)
ax.plot((bins[:-1] + bins[1:]) / 2, hist_smooth)

for angle in peak_angles:
    ax.plot([angle, angle], [0, max(hist_smooth)], linewidth=2)

ax.set_title("Spine Peaks")

# Cartesian visualization
plt.subplot(2, 2, 4)
plt.title("Peak Directions")

center = np.array([SIZE/2, SIZE/2])

for angle in peak_angles:
    vec = np.array([np.cos(angle), np.sin(angle)])
    p2 = center + vec * 30
    plt.plot([center[0], p2[0]], [center[1], p2[1]])

plt.xlim(0, SIZE)
plt.ylim(0, SIZE)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/spine_peaks.png")
plt.close()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

result = {
    "num_peaks": len(peak_angles),
    "peak_angles": peak_angles
}

with open(f"{OUTPUT_DIR}/spine_peaks.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Run complete: {run_id}")
print(f"Spine Peaks found: {len(peak_angles)}")

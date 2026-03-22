# ENGINE/analysis/navigation_level45_spine_coupling.py

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

PEAK_THRESHOLD = 0.6   # relative threshold for peak detection
COUPLING_RADIUS = 6    # radius around center for coupling detection

# --------------------------------------------------
# INIT
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
OUTPUT_DIR = f"ENGINE/visuals/level45_{run_id}"
os.makedirs(OUTPUT_DIR, exist_ok=True)

field = generate_stability_landscape(size=SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

trajectories = [[] for _ in range(N_AGENTS)]
angles = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


def compute_gradient(f, x, y):
    xi, yi = int(x), int(y)
    if xi <= 1 or xi >= SIZE - 2 or yi <= 1 or yi >= SIZE - 2:
        return np.array([0.0, 0.0])

    gx = f[yi, xi + 1] - f[yi, xi - 1]
    gy = f[yi + 1, xi] - f[yi - 1, xi]
    return np.array([gx, gy])


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

        x, y = positions[i]

        grad = compute_gradient(combined, x, y)

        noise = np.random.randn(2) * NOISE

        velocities[i] = DAMPING * velocities[i] + STEP_SIZE * grad + noise
        positions[i] += velocities[i]

        positions[i] = np.clip(positions[i], 0, SIZE - 1)

        px, py = int(positions[i][0]), int(positions[i][1])
        memory[py, px] += 1.0

        trajectories[i].append(positions[i].copy())

        if np.linalg.norm(velocities[i]) > 1e-6:
            angle = np.arctan2(velocities[i][1], velocities[i][0])
            angles.append(angle)

    memory *= MEMORY_DECAY


# --------------------------------------------------
# ANGLE ANALYSIS
# --------------------------------------------------

hist, bins = np.histogram(angles, bins=ANGLE_BINS, range=(-np.pi, np.pi))
hist = gaussian_filter(hist.astype(float), SMOOTH)

bin_centers = (bins[:-1] + bins[1:]) / 2

peaks = detect_peaks(hist, PEAK_THRESHOLD)

peak_angles = bin_centers[peaks]

# --------------------------------------------------
# COUPLING DETECTION (CENTER REGION)
# --------------------------------------------------

center = np.array([SIZE / 2, SIZE / 2])
coupled_vectors = []

for traj in trajectories:
    for p in traj:
        if np.linalg.norm(p - center) < COUPLING_RADIUS:
            coupled_vectors.append(p - center)

coupled_vectors = np.array(coupled_vectors)

# PCA-like dominant direction
if len(coupled_vectors) > 10:
    cov = np.cov(coupled_vectors.T)
    eigvals, eigvecs = np.linalg.eig(cov)
    dominant_vec = eigvecs[:, np.argmax(eigvals)]
else:
    dominant_vec = np.array([1.0, 0.0])

# --------------------------------------------------
# SAVE DATA
# --------------------------------------------------

result = {
    "num_peaks": int(len(peak_angles)),
    "peak_angles": peak_angles.tolist(),
    "dominant_direction": dominant_vec.tolist(),
}

with open(os.path.join(OUTPUT_DIR, "spine_coupling.json"), "w") as f:
    json.dump(result, f, indent=2)

# --------------------------------------------------
# PLOTS
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Field
axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

# Memory
axs[0, 1].imshow(memory, cmap="magma")
axs[0, 1].set_title("Memory")

# Polar Peaks
axp = plt.subplot(2, 2, 3, projection="polar")
axp.plot(bin_centers, hist)

for a in peak_angles:
    axp.plot([a, a], [0, np.max(hist)], linewidth=2)

axp.set_title("Spine Coupling Peaks")

# Coupling Field
axs[1, 1].imshow(field, cmap="viridis", alpha=0.5)

cx, cy = center
axs[1, 1].arrow(cx, cy,
                dominant_vec[0] * 15,
                dominant_vec[1] * 15,
                color="red", width=0.5)

axs[1, 1].set_title("Coupling Direction")

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "spine_coupling.png"))
plt.close()

# --------------------------------------------------
# DONE
# --------------------------------------------------

print(f"Run complete: {run_id}")
print(f"Peaks: {len(peak_angles)}")
print(f"Dominant direction: {dominant_vec}")

import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80
N_AGENTS = 100
STEPS = 700

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

MEMORY_DECAY = 0.992
FIELD_BLEND = 0.75
MEMORY_BLEND = 0.25

PHI = (1 + np.sqrt(5)) / 2
PHI_TOL = 0.08

TRACK_AGENT_COUNT = 12
MIN_TRACK_LENGTH = 40

# --------------------------------------------------
# SETUP
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

OUTPUT_DIR = "ENGINE/visuals/navigation_level36"
LOG_DIR = "ENGINE/logs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

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

tracked_indices = np.arange(min(TRACK_AGENT_COUNT, N_AGENTS))
tracked_paths = {idx: [] for idx in tracked_indices}

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def gradient(arr, x, y):
    xi = int(np.clip(x, 1, SIZE - 2))
    yi = int(np.clip(y, 1, SIZE - 2))

    gx = arr[yi, xi + 1] - arr[yi, xi - 1]
    gy = arr[yi + 1, xi] - arr[yi - 1, xi]

    return np.array([gx, gy])

def norm(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros_like(v)
    return v / n

def phi_hits_from_path(path):
    pts = np.array(path)
    n = len(pts)

    if n < MIN_TRACK_LENGTH:
        return [], []

    step_lengths = np.linalg.norm(np.diff(pts, axis=0), axis=1)

    ratios = []
    hit_positions = []

    for i in range(len(step_lengths) - 1):
        a = step_lengths[i]
        b = step_lengths[i + 1]

        if a < 1e-8 or b < 1e-8:
            continue

        r1 = a / b
        r2 = b / a

        if abs(r1 - PHI) < PHI_TOL:
            ratios.append(r1)
            hit_positions.append((pts[i + 1][0], pts[i + 1][1]))

        elif abs(r2 - PHI) < PHI_TOL:
            ratios.append(r2)
            hit_positions.append((pts[i + 1][0], pts[i + 1][1]))

    return ratios, hit_positions

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        x, y = positions[i]

        g_field = gradient(field, x, y)
        g_memory = gradient(memory, x, y)

        force = (
            FIELD_BLEND * norm(g_field) +
            MEMORY_BLEND * norm(g_memory)
        )

        velocities[i] += STEP_SIZE * force
        velocities[i] += NOISE * np.random.randn(2)
        velocities[i] *= DAMPING

        positions[i] += velocities[i]
        positions[i] = np.clip(positions[i], 0, SIZE - 1)

        px, py = int(positions[i][0]), int(positions[i][1])
        memory[py, px] += 1.0

        if i in tracked_paths:
            tracked_paths[i].append(positions[i].copy())

    memory *= MEMORY_DECAY

# --------------------------------------------------
# RESONANCE ANALYSIS
# --------------------------------------------------

all_phi_ratios = []
all_phi_points = []
agent_phi_counts = {}

for idx in tracked_indices:
    ratios, hits = phi_hits_from_path(tracked_paths[idx])

    all_phi_ratios.extend(ratios)
    all_phi_points.extend(hits)

    agent_phi_counts[int(idx)] = len(ratios)

total_steps = sum(max(0, len(tracked_paths[idx]) - 2) for idx in tracked_indices)
phi_density = len(all_phi_ratios) / max(1, total_steps)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# FIELD
axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

# MEMORY
axs[0, 1].imshow(memory, cmap="magma")
axs[0, 1].set_title("Resonance Memory")

# TRAJECTORIES
axs[1, 0].imshow(memory, cmap="gray", alpha=0.25)
axs[1, 0].set_title("Resonance Dynamics")

for idx in tracked_indices:
    path = np.array(tracked_paths[idx])
    if len(path) > 1:
        axs[1, 0].plot(path[:, 0], path[:, 1], alpha=0.6)

# PHI HITS
if len(all_phi_points) > 0:
    pts = np.array(all_phi_points)
    axs[1, 0].scatter(pts[:, 0], pts[:, 1], c="cyan", s=20)

# HISTOGRAM
if len(all_phi_ratios) > 0:
    axs[1, 1].hist(all_phi_ratios, bins=20)
    axs[1, 1].axvline(PHI, color="red", linestyle="--")
else:
    axs[1, 1].text(0.5, 0.5, "No phi hits", ha="center", va="center")

axs[1, 1].set_title("Phi Distribution")

plt.tight_layout()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

img_path = os.path.join(OUTPUT_DIR, f"level36_{run_id}.png")
plt.savefig(img_path, dpi=200)
plt.close()

metrics = {
    "phi_hits": len(all_phi_ratios),
    "phi_density": phi_density,
    "mean_phi": float(np.mean(all_phi_ratios)) if all_phi_ratios else 0,
    "std_phi": float(np.std(all_phi_ratios)) if all_phi_ratios else 0
}

json_path = os.path.join(LOG_DIR, f"level36_{run_id}.json")
with open(json_path, "w") as f:
    json.dump(metrics, f, indent=2)

# --------------------------------------------------
# PRINT
# --------------------------------------------------

print("Run complete:", run_id)
print("Phi hits:", metrics["phi_hits"])
print("Phi density:", metrics["phi_density"])
print("Mean phi:", metrics["mean_phi"])

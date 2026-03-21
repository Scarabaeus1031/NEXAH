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
PHI_TOL = 0.02

STREAK_THRESHOLD = 3   # 🔥 wichtig: nur stabile φ zählen

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE))

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

phi_streak = np.zeros(N_AGENTS)
basin_map = np.zeros((SIZE, SIZE))

all_ratios = []

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        x, y = positions[i]

        ix = int(np.clip(x, 1, SIZE - 2))
        iy = int(np.clip(y, 1, SIZE - 2))

        # Gradient field
        gx = field[ix + 1, iy] - field[ix - 1, iy]
        gy = field[ix, iy + 1] - field[ix, iy - 1]

        # Memory gradient
        mx = memory[ix + 1, iy] - memory[ix - 1, iy]
        my = memory[ix, iy + 1] - memory[ix, iy - 1]

        # Combine
        fx = FIELD_BLEND * gx + MEMORY_BLEND * mx
        fy = FIELD_BLEND * gy + MEMORY_BLEND * my

        prev_velocity = velocities[i].copy()

        # Update velocity
        velocities[i] = DAMPING * velocities[i] + STEP_SIZE * np.array([fx, fy])
        velocities[i] += np.random.randn(2) * NOISE

        # Move
        new_pos = positions[i] + velocities[i]
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        # --------------------------------------------------
        # φ CHECK
        # --------------------------------------------------

        d_now = np.linalg.norm(velocities[i])
        d_prev = np.linalg.norm(prev_velocity)

        if d_prev > 1e-4:

            ratio = d_now / d_prev
            all_ratios.append(ratio)

            if abs(ratio - PHI) < PHI_TOL:
                phi_streak[i] += 1
            else:
                phi_streak[i] = 0

            # 🔥 nur stabile φ-Zustände zählen
            if phi_streak[i] >= STREAK_THRESHOLD:
                ix2 = int(new_pos[0])
                iy2 = int(new_pos[1])
                basin_map[ix2, iy2] += 1

        # Update memory
        memory[ix, iy] += 1.0

        positions[i] = new_pos

    # decay outside loop
    memory *= MEMORY_DECAY

# --------------------------------------------------
# NORMALIZE
# --------------------------------------------------

if basin_map.max() > 0:
    basin_map /= basin_map.max()

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

phi_cells = int(np.sum(basin_map > 0))
phi_density = phi_cells / (SIZE * SIZE)
mean_ratio = float(np.mean(all_ratios)) if all_ratios else 0.0

# --------------------------------------------------
# SAVE
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = f"output/level38_{run_id}"
os.makedirs(out_dir, exist_ok=True)

metrics = {
    "phi_cells": phi_cells,
    "phi_density": phi_density,
    "mean_ratio": mean_ratio
}

with open(os.path.join(out_dir, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=2)

# --------------------------------------------------
# PLOTS
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0, 0].imshow(field)
axs[0, 0].set_title("Field")

axs[0, 1].imshow(memory)
axs[0, 1].set_title("Memory")

axs[1, 0].imshow(basin_map)
axs[1, 0].set_title("Phi Basin Locking")

axs[1, 1].hist(all_ratios, bins=50)
axs[1, 1].axvline(PHI, linestyle="--")
axs[1, 1].set_title("Ratio Distribution")

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "plot.png"))
plt.close()

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print(f"Run complete: {run_id}")
print(f"Phi basin cells: {phi_cells}")
print(f"Phi density: {phi_density}")
print(f"Mean ratio: {mean_ratio}")

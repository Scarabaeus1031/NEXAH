import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG (SOFT LOCK VERSION)
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

# softer detection
PHI_TOL = 0.05
STREAK_THRESHOLD = 2

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE))

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

phi_lock_map = np.zeros((SIZE, SIZE))
all_ratios = []

# streak counter per agent
phi_streak = np.zeros(N_AGENTS)

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        x, y = positions[i]

        ix = int(np.clip(x, 1, SIZE - 2))
        iy = int(np.clip(y, 1, SIZE - 2))

        # gradient
        gx = field[ix + 1, iy] - field[ix - 1, iy]
        gy = field[ix, iy + 1] - field[ix, iy - 1]

        # memory gradient
        mx = memory[ix + 1, iy] - memory[ix - 1, iy]
        my = memory[ix, iy + 1] - memory[ix, iy - 1]

        fx = FIELD_BLEND * gx + MEMORY_BLEND * mx
        fy = FIELD_BLEND * gy + MEMORY_BLEND * my

        prev_velocity = velocities[i].copy()

        # update velocity
        velocities[i] = DAMPING * velocities[i] + STEP_SIZE * np.array([fx, fy])
        velocities[i] += np.random.randn(2) * NOISE

        # move
        new_pos = positions[i] + velocities[i]
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        # ratio
        d_now = np.linalg.norm(velocities[i])
        d_prev = np.linalg.norm(prev_velocity)

        if d_prev > 1e-4:

            ratio = d_now / d_prev
            all_ratios.append(ratio)

            # check phi proximity
            if abs(ratio - PHI) < PHI_TOL:
                phi_streak[i] += 1
            else:
                phi_streak[i] = 0

            # SOFT LOCK CONDITION
            if phi_streak[i] >= STREAK_THRESHOLD:
                ix2 = int(new_pos[0])
                iy2 = int(new_pos[1])
                phi_lock_map[ix2, iy2] += 1

        # memory update
        memory[ix, iy] += 1.0

        positions[i] = new_pos

    # decay
    memory *= MEMORY_DECAY

# --------------------------------------------------
# NORMALIZE
# --------------------------------------------------

if phi_lock_map.max() > 0:
    phi_lock_map /= phi_lock_map.max()

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

phi_cells = int(np.sum(phi_lock_map > 0))
phi_density = phi_cells / (SIZE * SIZE)
mean_ratio = float(np.mean(all_ratios))

# --------------------------------------------------
# SAVE
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = f"output/level38b_{run_id}"
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

axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

axs[0, 1].imshow(memory, cmap="inferno")
axs[0, 1].set_title("Memory")

axs[1, 0].imshow(phi_lock_map, cmap="plasma")
axs[1, 0].set_title("Phi Soft Lock Map")

axs[1, 1].hist(all_ratios, bins=50)
axs[1, 1].axvline(PHI, linestyle="--", color="red")
axs[1, 1].set_title("Ratio Distribution")

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "plot.png"))
plt.close()

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print(f"Run complete: {run_id}")
print(f"Phi soft-lock cells: {phi_cells}")
print(f"Phi density: {phi_density}")
print(f"Mean ratio: {mean_ratio}")

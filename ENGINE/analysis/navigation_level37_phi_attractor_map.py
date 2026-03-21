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
PHI_TOL = 0.015  # etwas großzügiger für stabile Hits

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE))

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

phi_hits_map = np.zeros((SIZE, SIZE))
all_ratios = []

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        x, y = positions[i]

        ix = int(np.clip(x, 1, SIZE - 2))
        iy = int(np.clip(y, 1, SIZE - 2))

        # Gradient
        gx = field[ix + 1, iy] - field[ix - 1, iy]
        gy = field[ix, iy + 1] - field[ix, iy - 1]

        # Memory influence
        mx = memory[ix + 1, iy] - memory[ix - 1, iy]
        my = memory[ix, iy + 1] - memory[ix, iy - 1]

        # Combine
        fx = FIELD_BLEND * gx + MEMORY_BLEND * mx
        fy = FIELD_BLEND * gy + MEMORY_BLEND * my

        # Update velocity
        velocities[i] = DAMPING * velocities[i] + STEP_SIZE * np.array([fx, fy])
        velocities[i] += np.random.randn(2) * NOISE

        # Move
        new_pos = positions[i] + velocities[i]

        # Boundary clamp
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        # --- Phi check ---
        dist = np.linalg.norm(new_pos - positions[i])
        prev_dist = np.linalg.norm(velocities[i]) + 1e-6

        ratio = dist / prev_dist
        all_ratios.append(ratio)

        if abs(ratio - PHI) < PHI_TOL:
            phi_hits_map[int(new_pos[0]), int(new_pos[1])] += 1

        # Update memory
        memory[ix, iy] += 1.0

        # Apply decay
        memory *= MEMORY_DECAY

        positions[i] = new_pos

# --------------------------------------------------
# NORMALIZE MAP
# --------------------------------------------------

if phi_hits_map.max() > 0:
    phi_hits_map /= phi_hits_map.max()

# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------

phi_hits = np.sum(phi_hits_map > 0)
phi_density = phi_hits / (SIZE * SIZE)
mean_phi = np.mean(all_ratios)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = f"output/level37_{run_id}"
os.makedirs(out_dir, exist_ok=True)

metrics = {
    "phi_hits": int(phi_hits),
    "phi_density": float(phi_density),
    "mean_phi": float(mean_phi)
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

axs[1, 0].imshow(phi_hits_map, cmap="plasma")
axs[1, 0].set_title("Phi Attractor Map")

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
print(f"Phi attractor cells: {phi_hits}")
print(f"Phi density: {phi_density}")
print(f"Mean ratio: {mean_phi}")

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
PHI_TOL = 0.02   # leicht erhöht für robustere detection

# --------------------------------------------------
# PATHS (FIXED)
# --------------------------------------------------

OUTPUT_DIR = "ENGINE/visuals/navigation_level37"
LOG_DIR = "ENGINE/logs"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

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

        gx = field[ix + 1, iy] - field[ix - 1, iy]
        gy = field[ix, iy + 1] - field[ix, iy - 1]

        mx = memory[ix + 1, iy] - memory[ix - 1, iy]
        my = memory[ix, iy + 1] - memory[ix, iy - 1]

        fx = FIELD_BLEND * gx + MEMORY_BLEND * mx
        fy = FIELD_BLEND * gy + MEMORY_BLEND * my

        prev_velocity = velocities[i].copy()

        velocities[i] = DAMPING * velocities[i] + STEP_SIZE * np.array([fx, fy])
        velocities[i] += np.random.randn(2) * NOISE

        new_pos = positions[i] + velocities[i]
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        # φ detection
        d_now = np.linalg.norm(velocities[i])
        d_prev = np.linalg.norm(prev_velocity)

        if d_prev > 1e-4:
            ratio = d_now / d_prev
            all_ratios.append(ratio)

            if abs(ratio - PHI) < PHI_TOL:
                phi_hits_map[int(new_pos[0]), int(new_pos[1])] += 1

        memory[ix, iy] += 1.0
        positions[i] = new_pos

    memory *= MEMORY_DECAY

# --------------------------------------------------
# NORMALIZE
# --------------------------------------------------

if phi_hits_map.max() > 0:
    phi_hits_map /= phi_hits_map.max()

# --------------------------------------------------
# METRICS
# --------------------------------------------------

phi_hits = int(np.sum(phi_hits_map > 0))
phi_density = phi_hits / (SIZE * SIZE)
mean_phi = float(np.mean(all_ratios)) if len(all_ratios) > 0 else 0.0

metrics = {
    "run_id": run_id,
    "phi_hits": phi_hits,
    "phi_density": phi_density,
    "mean_phi": mean_phi
}

# --------------------------------------------------
# SAVE JSON
# --------------------------------------------------

json_path = os.path.join(LOG_DIR, f"level37_{run_id}.json")
with open(json_path, "w") as f:
    json.dump(metrics, f, indent=2)

# --------------------------------------------------
# SAVE IMAGE
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

axs[0, 1].imshow(memory, cmap="inferno")
axs[0, 1].set_title("Memory")

axs[1, 0].imshow(phi_hits_map, cmap="plasma")
axs[1, 0].set_title("Phi Attractor Map")

axs[1, 1].hist(all_ratios, bins=50)
axs[1, 1].axvline(PHI, linestyle="--", color="red")
axs[1, 1].set_title("Ratio Distribution")

plt.tight_layout()

img_path = os.path.join(OUTPUT_DIR, f"level37_{run_id}.png")
plt.savefig(img_path, dpi=200)
plt.close()

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print("Run complete:", run_id)
print("Phi attractor cells:", phi_hits)
print("Phi density:", phi_density)
print("Mean ratio:", mean_phi)

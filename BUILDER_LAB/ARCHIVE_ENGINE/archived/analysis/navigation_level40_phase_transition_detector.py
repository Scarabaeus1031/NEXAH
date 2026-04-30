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
N_AGENTS = 120
STEPS = 900

STEP_SIZE = 0.14
NOISE = 0.002
DAMPING = 0.96

MEMORY_DECAY = 0.993
FIELD_BLEND = 0.7
MEMORY_BLEND = 0.3

PHI = (1 + np.sqrt(5)) / 2
PHI_TOL = 0.02

# Phase detection
WINDOW = 20
STABILITY_THRESHOLD = 0.08   # orbit stability
TRANSITION_THRESHOLD = 0.25  # strong change

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE))

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

trajectories = [[] for _ in range(N_AGENTS)]
radius_history = [[] for _ in range(N_AGENTS)]

phase_map = np.zeros((SIZE, SIZE))
transition_points = []

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

        # Memory
        mx = memory[ix + 1, iy] - memory[ix - 1, iy]
        my = memory[ix, iy + 1] - memory[ix, iy - 1]

        fx = FIELD_BLEND * gx + MEMORY_BLEND * mx
        fy = FIELD_BLEND * gy + MEMORY_BLEND * my

        velocities[i] = DAMPING * velocities[i] + STEP_SIZE * np.array([fx, fy])
        velocities[i] += np.random.randn(2) * NOISE

        new_pos = positions[i] + velocities[i]
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        # Track
        trajectories[i].append(new_pos.copy())

        # Radius relative to local center (rolling)
        traj = np.array(trajectories[i][-WINDOW:])
        center = np.mean(traj, axis=0)
        radius = np.linalg.norm(new_pos - center)

        radius_history[i].append(radius)

        # --------------------------------------------------
        # PHASE TRANSITION DETECTION
        # --------------------------------------------------

        if len(radius_history[i]) > WINDOW:

            recent = np.array(radius_history[i][-WINDOW:])
            prev = np.array(radius_history[i][-2*WINDOW:-WINDOW])

            if len(prev) == WINDOW:

                r_std_now = np.std(recent)
                r_std_prev = np.std(prev)

                # detect stabilization (spiral → orbit)
                if r_std_now < STABILITY_THRESHOLD and r_std_prev > TRANSITION_THRESHOLD:

                    px = int(new_pos[0])
                    py = int(new_pos[1])

                    phase_map[px, py] += 1
                    transition_points.append([px, py])

        # Memory update
        memory[ix, iy] += 1.0
        positions[i] = new_pos

    memory *= MEMORY_DECAY

# --------------------------------------------------
# NORMALIZE
# --------------------------------------------------

if phase_map.max() > 0:
    phase_map /= phase_map.max()

transition_count = len(transition_points)
transition_density = transition_count / (SIZE * SIZE)

# --------------------------------------------------
# SAVE
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = f"ENGINE/visuals/level40_{run_id}"
os.makedirs(out_dir, exist_ok=True)

metrics = {
    "transitions": transition_count,
    "transition_density": transition_density
}

with open(os.path.join(out_dir, "metrics.json"), "w") as f:
    json.dump(metrics, f, indent=2)

# --------------------------------------------------
# PLOT
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

axs[0, 1].imshow(memory, cmap="inferno")
axs[0, 1].set_title("Memory")

axs[1, 0].imshow(phase_map, cmap="plasma")
axs[1, 0].set_title("Phase Transition Map")

if transition_points:
    tp = np.array(transition_points)
    axs[1, 1].scatter(tp[:, 1], tp[:, 0], s=5)
axs[1, 1].set_title("Transition Points")

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "plot.png"))
plt.close()

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print(f"Run complete: {run_id}")
print(f"Transitions: {transition_count}")
print(f"Transition density: {transition_density}")
print(f"Saved to: {out_dir}")

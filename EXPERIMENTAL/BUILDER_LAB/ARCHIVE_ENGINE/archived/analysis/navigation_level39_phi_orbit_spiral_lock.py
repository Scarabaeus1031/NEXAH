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
STEPS = 800

STEP_SIZE = 0.14
NOISE = 0.002
DAMPING = 0.96

MEMORY_DECAY = 0.993
FIELD_BLEND = 0.7
MEMORY_BLEND = 0.3

PHI = (1 + np.sqrt(5)) / 2
PHI_TOL = 0.02

# Orbit detection
MIN_ORBIT_LENGTH = 25
SPIRAL_THRESHOLD = 0.15  # radial drift tolerance

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE))

positions = np.random.rand(N_AGENTS, 2) * SIZE
velocities = np.zeros_like(positions)

# tracking
trajectories = [[] for _ in range(N_AGENTS)]
phi_hits_map = np.zeros((SIZE, SIZE))
all_ratios = []

orbit_centers = []
orbit_types = []

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

        # Force
        fx = FIELD_BLEND * gx + MEMORY_BLEND * mx
        fy = FIELD_BLEND * gy + MEMORY_BLEND * my

        prev_velocity = velocities[i].copy()

        velocities[i] = DAMPING * velocities[i] + STEP_SIZE * np.array([fx, fy])
        velocities[i] += np.random.randn(2) * NOISE

        new_pos = positions[i] + velocities[i]
        new_pos = np.clip(new_pos, 0, SIZE - 1)

        # --- φ ratio ---
        d_now = np.linalg.norm(velocities[i])
        d_prev = np.linalg.norm(prev_velocity)

        if d_prev > 1e-5:
            ratio = d_now / d_prev
            all_ratios.append(ratio)

            if abs(ratio - PHI) < PHI_TOL:
                ix2 = int(new_pos[0])
                iy2 = int(new_pos[1])
                phi_hits_map[ix2, iy2] += 1

        # Track trajectory
        trajectories[i].append(new_pos.copy())

        # Memory
        memory[ix, iy] += 1.0

        positions[i] = new_pos

    memory *= MEMORY_DECAY

# --------------------------------------------------
# ORBIT ANALYSIS
# --------------------------------------------------

def analyze_orbit(traj):
    if len(traj) < MIN_ORBIT_LENGTH:
        return None

    traj = np.array(traj)

    center = np.mean(traj, axis=0)
    radii = np.linalg.norm(traj - center, axis=1)

    r_mean = np.mean(radii)
    r_std = np.std(radii)

    # Spiral vs Orbit
    drift = np.abs(radii[-1] - radii[0]) / (r_mean + 1e-6)

    if drift < SPIRAL_THRESHOLD:
        orbit_type = "closed_orbit"
    else:
        orbit_type = "spiral"

    return center, orbit_type


for traj in trajectories:
    result = analyze_orbit(traj)
    if result is not None:
        c, t = result
        orbit_centers.append(c)
        orbit_types.append(t)

# --------------------------------------------------
# NORMALIZE
# --------------------------------------------------

if phi_hits_map.max() > 0:
    phi_hits_map /= phi_hits_map.max()

phi_hits = int(np.sum(phi_hits_map > 0))
phi_density = phi_hits / (SIZE * SIZE)
mean_phi = float(np.mean(all_ratios)) if len(all_ratios) > 0 else 0.0

closed_orbits = orbit_types.count("closed_orbit")
spirals = orbit_types.count("spiral")

# --------------------------------------------------
# SAVE (ENGINE/visuals)
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
out_dir = f"ENGINE/visuals/level39_{run_id}"
os.makedirs(out_dir, exist_ok=True)

metrics = {
    "phi_hits": phi_hits,
    "phi_density": phi_density,
    "mean_ratio": mean_phi,
    "closed_orbits": closed_orbits,
    "spirals": spirals
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
axs[1, 0].set_title("Phi Orbit Map")

axs[1, 1].hist(all_ratios, bins=60)
axs[1, 1].axvline(PHI, linestyle="--", color="red")
axs[1, 1].set_title("Ratio Distribution")

plt.tight_layout()
plt.savefig(os.path.join(out_dir, "plot.png"))
plt.close()

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

print(f"Run complete: {run_id}")
print(f"Phi cells: {phi_hits}")
print(f"Phi density: {phi_density}")
print(f"Mean ratio: {mean_phi}")
print(f"Closed orbits: {closed_orbits}")
print(f"Spirals: {spirals}")
print(f"Saved to: {out_dir}")

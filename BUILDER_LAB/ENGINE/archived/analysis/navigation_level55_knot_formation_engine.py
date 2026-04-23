# ENGINE/analysis/navigation_level55_knot_formation_engine.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80

N_PARTICLES = 160
STEPS = 1400

STEP_SIZE = 0.16

ROTATION = 0.34
RETURN = 0.10
REJOIN = 0.18

ORBIT_STRENGTH = 0.26
R_TARGET = 18.4

HELIX_STRENGTH = 0.32
PHASE_DRIFT = 0.06
PHASE_COUPLING = 0.18

# 🔥 NEW: Knot mechanics
CROSS_COUPLING = 0.22     # forces crossing of trajectories
KNOT_LOCK = 0.28          # stabilizes loop closure

SMOOTH = 1.2

OUTPUT_DIR = "ENGINE/visuals"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD
# --------------------------------------------------

def generate_field(size):
    field = np.zeros((size, size))

    centers = [
        (int(size * 0.3), int(size * 0.3)),
        (int(size * 0.7), int(size * 0.7))
    ]

    for cx, cy in centers:
        for i in range(size):
            for j in range(size):
                dist = np.sqrt((i - cx)**2 + (j - cy)**2)
                field[i, j] += np.exp(-dist / 10)

    return gaussian_filter(field, sigma=SMOOTH)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def sample(arr, x, y):
    return arr[int(x) % SIZE, int(y) % SIZE]

def normalize(v):
    n = np.linalg.norm(v) + 1e-8
    return v / n

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_field(SIZE)
memory = np.zeros_like(field)

particles = np.random.rand(N_PARTICLES, 2) * SIZE
velocities = np.zeros_like(particles)

visit = np.zeros_like(field)

phases = np.random.rand(N_PARTICLES) * 2 * np.pi

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    grad_y, grad_x = np.gradient(field)

    for i in range(N_PARTICLES):

        x, y = particles[i]

        gx = sample(grad_x, x, y)
        gy = sample(grad_y, x, y)

        grad = np.array([gx, gy])

        # ----------------------------
        # FLOW
        # ----------------------------
        flow = grad

        # ----------------------------
        # ROTATION
        # ----------------------------
        rot = np.array([-gy, gx]) * ROTATION

        # ----------------------------
        # RETURN
        # ----------------------------
        center = np.array([SIZE/2, SIZE/2])
        to_center = center - particles[i]
        return_force = normalize(to_center) * RETURN

        # ----------------------------
        # ORBIT
        # ----------------------------
        r_vec = particles[i] - center
        r = np.linalg.norm(r_vec) + 1e-8
        orbit_dir = np.array([-r_vec[1], r_vec[0]])
        orbit = normalize(orbit_dir) * ORBIT_STRENGTH

        radial_correction = normalize(r_vec) * (R_TARGET - r) * 0.05

        # ----------------------------
        # HELIX
        # ----------------------------
        phases[i] += PHASE_DRIFT
        helix = np.array([
            np.cos(phases[i]),
            np.sin(phases[i])
        ]) * HELIX_STRENGTH

        # ----------------------------
        # PHASE COUPLING
        # ----------------------------
        phase_align = helix * PHASE_COUPLING

        # ----------------------------
        # CROSS COUPLING (🔥 NEW)
        # pushes trajectories across center line
        # ----------------------------
        cross = np.array([y - SIZE/2, -(x - SIZE/2)])
        cross = normalize(cross) * CROSS_COUPLING

        # ----------------------------
        # MEMORY
        # ----------------------------
        mem = sample(memory, x, y)
        mem_force = grad * mem * 0.2

        # ----------------------------
        # KNOT LOCK (🔥 NEW)
        # pulls particles into closed loop behavior
        # ----------------------------
        loop_vec = normalize(r_vec)
        knot_force = -loop_vec * KNOT_LOCK * np.sin(phases[i])

        # ----------------------------
        # COMBINE
        # ----------------------------
        force = (
            flow
            + rot
            + return_force
            + orbit
            + radial_correction
            + helix
            + phase_align
            + cross
            + mem_force
            + knot_force
        )

        # update
        velocities[i] = velocities[i] * 0.92 + force * STEP_SIZE
        particles[i] += velocities[i]
        particles[i] %= SIZE

        xi, yi = int(particles[i][0]), int(particles[i][1])
        visit[xi, yi] += 1
        memory[xi, yi] += 1

    memory *= 0.995

# --------------------------------------------------
# VISUALIZE
# --------------------------------------------------

density = gaussian_filter(visit, sigma=1.0)

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Field")
plt.imshow(field)

plt.subplot(1, 2, 2)
plt.title("Knot Formation Engine (Level 55)")
plt.imshow(density)

plt.tight_layout()

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
out_path = f"{OUTPUT_DIR}/level55_knot_{run_id}.png"

plt.savefig(out_path, dpi=200)
plt.show()
plt.close()

# --------------------------------------------------
# SAVE CONFIG
# --------------------------------------------------

config = {
    "particles": N_PARTICLES,
    "steps": STEPS,
    "config": {
        "rotation": ROTATION,
        "return": RETURN,
        "orbit_strength": ORBIT_STRENGTH,
        "helix_strength": HELIX_STRENGTH,
        "cross_coupling": CROSS_COUPLING,
        "knot_lock": KNOT_LOCK
    }
}

with open(f"{OUTPUT_DIR}/level55_knot_{run_id}.json", "w") as f:
    json.dump(config, f, indent=2)

print("Saved:", out_path)

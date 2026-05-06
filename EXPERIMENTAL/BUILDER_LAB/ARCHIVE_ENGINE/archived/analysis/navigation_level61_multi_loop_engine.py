# ENGINE/analysis/navigation_level61_multi_loop_engine.py

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

N_PARTICLES = 260
STEPS = 2600

STEP_SIZE = 0.11

ROTATION = 0.26
RETURN = 0.04
REJOIN = 0.10

ORBIT_STRENGTH = 0.22
R_TARGET = 16.0

HELIX_STRENGTH = 0.28
PHASE_DRIFT = 0.055

MEMORY_DECAY = 0.996
FIELD_DECAY = 0.990

FLOW_MEMORY_STRENGTH = 0.35
QUANTIZATION = 0.18

# NEW
LOOP_COUPLING = 0.22
CHANNEL_COUPLING = 0.20

SAVE_DIR = "ENGINE/visuals/navigation_level61"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


# --------------------------------------------------
# FIELD GENERATION (3 nodes now)
# --------------------------------------------------

def generate_field(size=80):
    x = np.linspace(0, size - 1, size)
    y = np.linspace(0, size - 1, size)
    X, Y = np.meshgrid(x, y)

    c1 = np.array([size * 0.25, size * 0.30])
    c2 = np.array([size * 0.70, size * 0.65])
    c3 = np.array([size * 0.50, size * 0.20])

    d1 = np.exp(-((X - c1[0])**2 + (Y - c1[1])**2) / (2 * 7**2))
    d2 = np.exp(-((X - c2[0])**2 + (Y - c2[1])**2) / (2 * 8**2))
    d3 = np.exp(-((X - c3[0])**2 + (Y - c3[1])**2) / (2 * 6**2))

    return d1 + d2 + d3


def sample(field, x, y):
    xi = int(x) % SIZE
    yi = int(y) % SIZE
    return field[xi, yi]


# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_field(SIZE)
memory = np.zeros_like(field)

particles = np.random.rand(N_PARTICLES, 2) * SIZE
vel = np.zeros_like(particles)

visit = np.zeros_like(field)


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    grad_y, grad_x = np.gradient(field)

    phase = step * PHASE_DRIFT

    for i in range(N_PARTICLES):

        x, y = particles[i]

        gx = sample(grad_x, x, y)
        gy = sample(grad_y, x, y)

        flow = np.array([gx, gy])
        swirl = np.array([-gy, gx])

        center = np.array([SIZE/2, SIZE/2])
        r_vec = particles[i] - center
        r = np.linalg.norm(r_vec) + 1e-8

        orbit_force = (R_TARGET - r) * (r_vec / r)

        helix = np.array([
            np.cos(phase + x * 0.04),
            np.sin(phase + y * 0.04)
        ])

        # Flow memory direction
        mem = sample(memory, x, y)
        mem_force = flow * mem

        # Quantization
        angle = np.arctan2(flow[1], flow[0])
        quant_angle = np.round(angle / (np.pi/6)) * (np.pi/6)
        quant_vec = np.array([np.cos(quant_angle), np.sin(quant_angle)])

        # LOOP COUPLING (new)
        loop_force = np.array([
            np.sin(y * 0.06),
            np.cos(x * 0.06)
        ])

        # CHANNEL FORCE (connect loops)
        channel = np.array([
            np.cos(x * 0.03 + y * 0.02),
            np.sin(y * 0.03 + x * 0.02)
        ])

        force = (
            flow +
            ROTATION * swirl +
            RETURN * (-flow) +
            REJOIN * mem_force +
            ORBIT_STRENGTH * orbit_force +
            HELIX_STRENGTH * helix +
            FLOW_MEMORY_STRENGTH * mem_force +
            QUANTIZATION * quant_vec +
            LOOP_COUPLING * loop_force +
            CHANNEL_COUPLING * channel
        )

        vel[i] = vel[i] * 0.88 + force * STEP_SIZE
        particles[i] += vel[i]

        particles[i] %= SIZE

        xi, yi = int(particles[i][0]), int(particles[i][1])
        visit[xi, yi] += 1
        memory[xi, yi] += 1

    memory *= MEMORY_DECAY
    field *= FIELD_DECAY


# --------------------------------------------------
# METRICS
# --------------------------------------------------

visit_norm = visit / (visit.sum() + 1e-8)
entropy = -np.sum(visit_norm * np.log(visit_norm + 1e-12))


# --------------------------------------------------
# SAVE LOG
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

log_data = {
    "run_id": run_id,
    "entropy": float(entropy),
    "config": {
        "loop": LOOP_COUPLING,
        "channel": CHANNEL_COUPLING,
        "quant": QUANTIZATION
    }
}

with open(f"{LOG_DIR}/log_level61_{run_id}.json", "w") as f:
    json.dump(log_data, f, indent=2)


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(12, 4))

plt.subplot(1, 3, 1)
plt.title("Field")
plt.imshow(field)

plt.subplot(1, 3, 2)
plt.title("Multi-Loop Density (Level 61)")
plt.imshow(gaussian_filter(visit_norm, sigma=1.2))

plt.subplot(1, 3, 3)
plt.title("Flow Skeleton")
plt.imshow(visit_norm > np.percentile(visit_norm, 96), cmap="gray")

plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/level61_{run_id}.png", dpi=200)
plt.show()
plt.close()

print("Level 61 complete:", run_id)

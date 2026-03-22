# ENGINE/analysis/navigation_level56_knot_channel_engine.py

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

N_PARTICLES = 180
STEPS = 1800

STEP_SIZE = 0.14

ROTATION = 0.30
RETURN = 0.06
REJOIN = 0.12

ORBIT_STRENGTH = 0.26
R_TARGET = 18.0

HELIX_STRENGTH = 0.34
PHASE_DRIFT = 0.060
PHASE_COUPLING = 0.18

CROSS_COUPLING = 0.24
KNOT_LOCK = 0.30
CHANNEL_STRENGTH = 0.22

MEMORY_DECAY = 0.995
FIELD_DECAY = 0.988

SAVE_DIR = “ENGINE/visuals/navigation_level56”
LOG_DIR = “ENGINE/logs”

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

–––––––––––––––––––––––––

FIELD GENERATION

–––––––––––––––––––––––––

def generate_field(size=80):
x = np.linspace(0, size - 1, size)
y = np.linspace(0, size - 1, size)
X, Y = np.meshgrid(x, y)

c1 = np.array([size * 0.3, size * 0.3])
c2 = np.array([size * 0.7, size * 0.7])

d1 = np.exp(-((X - c1[0])**2 + (Y - c1[1])**2) / (2 * 8**2))
d2 = np.exp(-((X - c2[0])**2 + (Y - c2[1])**2) / (2 * 8**2))

return d1 + d2

def sample(field, x, y):
xi = int(x) % SIZE
yi = int(y) % SIZE
return field[xi, yi]

–––––––––––––––––––––––––

INIT

–––––––––––––––––––––––––

field = generate_field(SIZE)
memory = np.zeros_like(field)

particles = np.random.rand(N_PARTICLES, 2) * SIZE
vel = np.zeros_like(particles)

visit = np.zeros_like(field)
trajectories = [[] for _ in range(N_PARTICLES)]

–––––––––––––––––––––––––

SIMULATION

–––––––––––––––––––––––––

for step in range(STEPS):

grad_y, grad_x = np.gradient(field)

phase = step * PHASE_DRIFT

for i in range(N_PARTICLES):

    x, y = particles[i]

    gx = sample(grad_x, x, y)
    gy = sample(grad_y, x, y)

    flow = np.array([gx, gy])
    swirl = np.array([-gy, gx])

    # Orbit lock
    center = np.array([SIZE/2, SIZE/2])
    r_vec = particles[i] - center
    r = np.linalg.norm(r_vec) + 1e-8
    orbit_force = (R_TARGET - r) * (r_vec / r)

    # Helix modulation
    helix = np.array([
        np.cos(phase + x * 0.05),
        np.sin(phase + y * 0.05)
    ])

    # Phase coupling
    phase_vec = np.array([
        np.sin(phase + x * 0.03),
        np.cos(phase + y * 0.03)
    ])

    # Cross coupling (orthogonal interference)
    cross = np.array([
        np.sin(x * 0.08) * np.cos(y * 0.08),
        np.cos(x * 0.08) * np.sin(y * 0.08)
    ])

    # Memory attraction
    mem = sample(memory, x, y)
    mem_force = flow * mem

    # Channel force (NEW)
    direction = flow + swirl + helix
    norm = np.linalg.norm(direction) + 1e-8
    channel_dir = direction / norm

    # Knot lock (stabilizes intersections)
    knot = (flow + swirl + cross)
    knot_norm = np.linalg.norm(knot) + 1e-8
    knot_dir = knot / knot_norm

    # Combine
    force = (
        flow +
        ROTATION * swirl +
        RETURN * (-flow) +
        REJOIN * mem_force +
        ORBIT_STRENGTH * orbit_force +
        HELIX_STRENGTH * helix +
        PHASE_COUPLING * phase_vec +
        CROSS_COUPLING * cross +
        KNOT_LOCK * knot_dir +
        CHANNEL_STRENGTH * channel_dir
    )

    vel[i] = vel[i] * 0.90 + force * STEP_SIZE
    particles[i] += vel[i]

    particles[i] %= SIZE

    xi, yi = int(particles[i][0]), int(particles[i][1])
    visit[xi, yi] += 1
    memory[xi, yi] += 1

    trajectories[i].append(particles[i].copy())

    memory *= MEMORY_DECAY
    field *= FIELD_DECAY

    –––––––––––––––––––––––––

METRICS

–––––––––––––––––––––––––

visit_norm = visit / (visit.sum() + 1e-8)
entropy = -np.sum(visit_norm * np.log(visit_norm + 1e-12))

–––––––––––––––––––––––––

SAVE LOG

–––––––––––––––––––––––––

run_id = datetime.now().strftime(”%Y%m%d_%H%M%S”)

log_data = {
“run_id”: run_id,
“entropy”: float(entropy),
“config”: {
“orbit”: ORBIT_STRENGTH,
“helix”: HELIX_STRENGTH,
“knot”: KNOT_LOCK,
“channel”: CHANNEL_STRENGTH
}
}

with open(f”{LOG_DIR}/log_level56_{run_id}.json”, “w”) as f:
json.dump(log_data, f, indent=2)

–––––––––––––––––––––––––

VISUALIZATION

–––––––––––––––––––––––––

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title(“Field”)
plt.imshow(field)

plt.subplot(1, 2, 2)
plt.title(“Knot Channel Engine (Level 56)”)
plt.imshow(gaussian_filter(visit_norm, sigma=1.2))

plt.tight_layout()
plt.savefig(f”{SAVE_DIR}/level56_{run_id}.png”, dpi=200)
plt.show()
plt.close()

print(“Level 56 complete:”, run_id)

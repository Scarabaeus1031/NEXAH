# ENGINE/analysis/navigation_level57_network_coupling_engine.py

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

N_PARTICLES = 200
STEPS = 2000

STEP_SIZE = 0.13

ROTATION = 0.28
RETURN = 0.05
REJOIN = 0.14

ORBIT_STRENGTH = 0.24
R_TARGET = 18.5

HELIX_STRENGTH = 0.32
PHASE_DRIFT = 0.065
PHASE_COUPLING = 0.20

CROSS_COUPLING = 0.26
KNOT_LOCK = 0.32
CHANNEL_STRENGTH = 0.26

# NEW: NETWORK COUPLING
NODE_ATTRACTION = 0.22
EDGE_FLOW = 0.18
GLOBAL_SYNC = 0.12

MEMORY_DECAY = 0.995
FIELD_DECAY = 0.988

SAVE_DIR = "ENGINE/visuals/navigation_level57"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD GENERATION
# --------------------------------------------------

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

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_field(SIZE)
memory = np.zeros_like(field)

particles = np.random.rand(N_PARTICLES, 2) * SIZE
vel = np.zeros_like(particles)

visit = np.zeros_like(field)
trajectories = [[] for _ in range(N_PARTICLES)]

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    grad_y, grad_x = np.gradient(field)
    phase = step * PHASE_DRIFT

    # dynamic node centers (learned from system)
    high_density_points = np.argwhere(visit > np.percentile(visit, 98))
    if len(high_density_points) > 3:
        nodes = high_density_points[np.random.choice(len(high_density_points), 3)]
    else:
        nodes = np.array([
            [SIZE*0.3, SIZE*0.3],
            [SIZE*0.7, SIZE*0.7],
            [SIZE*0.5, SIZE*0.5]
        ])

    for i in range(N_PARTICLES):

        x, y = particles[i]

        gx = sample(grad_x, x, y)
        gy = sample(grad_y, x, y)

        flow = np.array([gx, gy])
        swirl = np.array([-gy, gx])

        # ORBIT
        center = np.array([SIZE/2, SIZE/2])
        r_vec = particles[i] - center
        r = np.linalg.norm(r_vec) + 1e-8
        orbit_force = (R_TARGET - r) * (r_vec / r)

        # HELIX
        helix = np.array([
            np.cos(phase + x * 0.05),
            np.sin(phase + y * 0.05)
        ])

        # PHASE
        phase_vec = np.array([
            np.sin(phase + x * 0.03),
            np.cos(phase + y * 0.03)
        ])

        # CROSS
        cross = np.array([
            np.sin(x * 0.08) * np.cos(y * 0.08),
            np.cos(x * 0.08) * np.sin(y * 0.08)
        ])

        # MEMORY
        mem = sample(memory, x, y)
        mem_force = flow * mem

        # CHANNEL
        direction = flow + swirl + helix
        channel_dir = direction / (np.linalg.norm(direction) + 1e-8)

        # KNOT
        knot = flow + swirl + cross
        knot_dir = knot / (np.linalg.norm(knot) + 1e-8)

        # ----------------------------
        # NEW: NETWORK FORCES
        # ----------------------------

        # Node attraction (towards learned centers)
        node_force = np.zeros(2)
        for n in nodes:
            vec = n - particles[i]
            dist = np.linalg.norm(vec) + 1e-8
            node_force += (vec / dist) * np.exp(-dist / 15)

        # Edge flow (connect nodes)
        edge_force = np.zeros(2)
        if len(nodes) >= 2:
            for j in range(len(nodes)-1):
                edge = nodes[j+1] - nodes[j]
                edge_force += edge / (np.linalg.norm(edge) + 1e-8)

        # Global sync (align all motion slightly)
        global_dir = np.mean(vel, axis=0)
        global_dir = global_dir / (np.linalg.norm(global_dir) + 1e-8)

        # ----------------------------
        # COMBINE
        # ----------------------------

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
            CHANNEL_STRENGTH * channel_dir +
            NODE_ATTRACTION * node_force +
            EDGE_FLOW * edge_force +
            GLOBAL_SYNC * global_dir
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
        "orbit": ORBIT_STRENGTH,
        "helix": HELIX_STRENGTH,
        "knot": KNOT_LOCK,
        "channel": CHANNEL_STRENGTH,
        "network": NODE_ATTRACTION
    }
}

with open(f"{LOG_DIR}/log_level57_{run_id}.json", "w") as f:
    json.dump(log_data, f, indent=2)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.title("Field")
plt.imshow(field)

plt.subplot(1, 2, 2)
plt.title("Network Coupling Engine (Level 57)")
plt.imshow(gaussian_filter(visit_norm, sigma=1.2))

plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/level57_{run_id}.png", dpi=200)
plt.show()
plt.close()

print("Level 57 complete:", run_id)

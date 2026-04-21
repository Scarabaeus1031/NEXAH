import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

N_AGENTS = 120
STEPS = 320

STEP_SIZE = 0.28
NOISE = 0.010
DAMPING = 0.91

ALPHA_FLOW = 0.95       # gradient flow
BETA_SWIRL = 0.65       # vortex rotation
GAMMA_MEMORY = 0.40     # memory attraction
DELTA_RESONANCE = 0.25  # NEW: resonance lock strength

FIELD_DECAY = 0.987
MEMORY_DECAY = 0.995

SAVE_DIR = "ENGINE/visuals/navigation_level19"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD SAMPLING
# --------------------------------------------------

def sample_field(field, x, y):
    h, w = field.shape
    x = int(x) % h
    y = int(y) % w
    return field[x, y]

# --------------------------------------------------
# INITIALIZATION
# --------------------------------------------------

field = generate_stability_landscape(size=80)

memory = np.zeros_like(field)

agents = np.random.rand(N_AGENTS, 2) * 80
velocities = np.zeros_like(agents)

trajectories = [[] for _ in range(N_AGENTS)]
visit_map = np.zeros_like(field)

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    grad_y, grad_x = np.gradient(field)

    for i in range(N_AGENTS):
        x, y = agents[i]

        gx = sample_field(grad_x, x, y)
        gy = sample_field(grad_y, x, y)

        # ----------------------------
        # FLOW (gradient descent)
        # ----------------------------
        flow = np.array([gx, gy])

        # ----------------------------
        # SWIRL (orthogonal rotation)
        # ----------------------------
        swirl = np.array([-gy, gx])

        # ----------------------------
        # MEMORY attraction
        # ----------------------------
        mem_val = sample_field(memory, x, y)
        mem_force = np.array([gx, gy]) * mem_val

        # ----------------------------
        # RESONANCE LOCK (NEW)
        # agents align to local dominant direction
        # ----------------------------
        local_dir = flow + swirl
        norm = np.linalg.norm(local_dir) + 1e-8
        resonance_dir = local_dir / norm

        # ----------------------------
        # COMBINE FORCES
        # ----------------------------
        force = (
            ALPHA_FLOW * flow +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * mem_force +
            DELTA_RESONANCE * resonance_dir
        )

        # noise
        force += np.random.randn(2) * NOISE

        # update velocity
        velocities[i] = velocities[i] * DAMPING + force * STEP_SIZE

        # update position
        agents[i] += velocities[i]

        # wrap
        agents[i] %= 80

        xi, yi = int(agents[i][0]), int(agents[i][1])
        visit_map[xi, yi] += 1
        memory[xi, yi] += 1

        trajectories[i].append(agents[i].copy())

    # decay
    memory *= MEMORY_DECAY
    field *= FIELD_DECAY

# --------------------------------------------------
# METRICS
# --------------------------------------------------

visit_norm = visit_map / (visit_map.sum() + 1e-8)

entropy = -np.sum(visit_norm * np.log(visit_norm + 1e-12))

recurrence = np.sum(visit_norm > np.percentile(visit_norm, 99)) / visit_norm.size

# --------------------------------------------------
# SAVE LOG
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

log_data = {
    "run_id": run_id,
    "config": {
        "STEP_SIZE": STEP_SIZE,
        "NOISE": NOISE,
        "DAMPING": DAMPING,
        "ALPHA_FLOW": ALPHA_FLOW,
        "BETA_SWIRL": BETA_SWIRL,
        "GAMMA_MEMORY": GAMMA_MEMORY,
        "DELTA_RESONANCE": DELTA_RESONANCE
    },
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence)
    }
}

with open(f"{LOG_DIR}/log_level19_{run_id}.json", "w") as f:
    json.dump(log_data, f, indent=2)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

plt.figure(figsize=(12, 10))

# FIELD
plt.subplot(2, 2, 1)
plt.title("Field")
plt.imshow(field)

# FLOW
plt.subplot(2, 2, 2)
plt.title("Flow")
skip = 3
plt.imshow(field, alpha=0.6)

Y, X = np.mgrid[0:80, 0:80]
plt.quiver(
    X[::skip, ::skip],
    Y[::skip, ::skip],
    grad_x[::skip, ::skip],
    grad_y[::skip, ::skip],
    color="white",
    scale=50
)

# TRAJECTORIES
plt.subplot(2, 2, 3)
plt.title("Resonance Trajectories")

for traj in trajectories:
    traj = np.array(traj)
    plt.plot(traj[:, 1], traj[:, 0], alpha=0.4)

# RECURRENCE
plt.subplot(2, 2, 4)
plt.title("Recurrence Map")
plt.imshow(visit_norm)

plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/navigation_level19_{run_id}.png", dpi=200)
plt.show()
plt.close()

print("Run complete:", run_id)

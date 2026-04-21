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
STEPS = 360

STEP_SIZE = 0.24
NOISE = 0.008
DAMPING = 0.92

ALPHA_FLOW = 0.75
BETA_SWIRL = 0.70
GAMMA_MEMORY = 0.40
DELTA_RESONANCE = 0.22

# --- NEW: PHASE SYSTEM ---
KAPPA_PHASE = 0.18
PHASE_RADIUS = 10.0
OMEGA_MEAN = 0.06
OMEGA_STD = 0.015

FIELD_DECAY = 0.988
MEMORY_DECAY = 0.996

SAVE_DIR = "ENGINE/visuals/navigation_level20"
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
# INIT
# --------------------------------------------------

field = generate_stability_landscape(size=SIZE)

memory = np.zeros_like(field)

agents = np.random.rand(N_AGENTS, 2) * SIZE
vel = np.zeros_like(agents)

# --- PHASE VARIABLES ---
theta = np.random.rand(N_AGENTS) * 2 * np.pi
omega = np.random.normal(OMEGA_MEAN, OMEGA_STD, N_AGENTS)

trajectories = [[] for _ in range(N_AGENTS)]
visit_map = np.zeros_like(field)

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    grad_y, grad_x = np.gradient(field)
    mem_y, mem_x = np.gradient(memory)

    # --------------------------------------------------
    # PHASE COUPLING (Kuramoto)
    # --------------------------------------------------

    new_theta = theta.copy()

    for i in range(N_AGENTS):

        xi, yi = agents[i]

        coupling_sum = 0.0
        count = 0

        for j in range(N_AGENTS):
            if i == j:
                continue

            xj, yj = agents[j]

            dist = np.linalg.norm(agents[i] - agents[j])

            if dist < PHASE_RADIUS:
                coupling_sum += np.sin(theta[j] - theta[i])
                count += 1

        if count > 0:
            coupling = (KAPPA_PHASE / count) * coupling_sum
        else:
            coupling = 0.0

        new_theta[i] = theta[i] + omega[i] + coupling

    theta = new_theta

    # --------------------------------------------------
    # AGENT UPDATE
    # --------------------------------------------------

    for i in range(N_AGENTS):

        x, y = agents[i]

        gx = sample_field(grad_x, x, y)
        gy = sample_field(grad_y, x, y)

        flow = np.array([gx, gy])
        swirl = np.array([-gy, gx])

        mem_val = sample_field(memory, x, y)
        mem_force = flow * mem_val

        # --- RESONANCE DIRECTION ---
        local_dir = flow + swirl
        norm = np.linalg.norm(local_dir) + 1e-8
        resonance_dir = local_dir / norm

        # --- PHASE FORCE (NEW) ---
        phase_force = np.array([
            np.cos(theta[i]),
            np.sin(theta[i])
        ])

        # --------------------------------------------------
        # TOTAL FORCE
        # --------------------------------------------------

        force = (
            ALPHA_FLOW * flow +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * mem_force +
            DELTA_RESONANCE * resonance_dir +
            0.35 * phase_force   # <- phase influence
        )

        force += np.random.randn(2) * NOISE

        vel[i] = vel[i] * DAMPING + force * STEP_SIZE
        agents[i] += vel[i]

        agents[i] %= SIZE

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

# phase coherence (Kuramoto order parameter)
R = np.abs(np.mean(np.exp(1j * theta)))

recurrence = np.sum(visit_norm > np.percentile(visit_norm, 99)) / visit_norm.size

# --------------------------------------------------
# SAVE LOG
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

log_data = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence),
        "phase_coherence": float(R)
    }
}

with open(f"{LOG_DIR}/log_level20_{run_id}.json", "w") as f:
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

Y, X = np.mgrid[0:SIZE, 0:SIZE]
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
plt.title("Phase-Synchronized Trajectories")

for traj in trajectories:
    traj = np.array(traj)
    plt.plot(traj[:, 1], traj[:, 0], alpha=0.25)

# RECURRENCE / MEMORY
plt.subplot(2, 2, 4)
plt.title("Memory / Recurrence")
plt.imshow(visit_norm, cmap="magma")

plt.tight_layout()

plt.savefig(f"{SAVE_DIR}/navigation_level20_{run_id}.png", dpi=200)

plt.show()

print("\nRun complete:", run_id)
print("Entropy:", entropy)
print("Recurrence:", recurrence)
print("Phase coherence:", R)

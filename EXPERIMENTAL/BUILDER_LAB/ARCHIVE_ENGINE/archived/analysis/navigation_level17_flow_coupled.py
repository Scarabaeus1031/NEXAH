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
STEPS = 260

STEP_SIZE = 0.32
NOISE = 0.018
DAMPING = 0.90

ALPHA_FLOW = 0.95      # gradient flow
BETA_SWIRL = 0.55      # orthogonal rotation
GAMMA_MEMORY = 0.35    # memory attraction

FIELD_DECAY = 0.985
MEMORY_DECAY = 0.995

SAVE_DIR = "ENGINE/visuals/navigation_level17"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD SAMPLING
# --------------------------------------------------

def sample_field(field, x, y):
    h, w = field.shape
    x = int(np.clip(x, 0, h - 1))
    y = int(np.clip(y, 0, w - 1))
    return field[x, y]

# --------------------------------------------------
# GRADIENT
# --------------------------------------------------

def compute_gradient(field):
    gx, gy = np.gradient(field)
    return gx, gy

# --------------------------------------------------
# SWIRL (orthogonal rotation)
# --------------------------------------------------

def orthogonal(vx, vy):
    return -vy, vx

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(size=80)
gx, gy = compute_gradient(field)

memory = np.zeros_like(field)

agents = np.random.rand(N_AGENTS, 2) * field.shape[0]
vel = np.zeros_like(agents)

trajectories = [[] for _ in range(N_AGENTS)]

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        x, y = agents[i]

        # --- sample gradient ---
        fx = sample_field(gx, x, y)
        fy = sample_field(gy, x, y)

        # --- swirl ---
        sx, sy = orthogonal(fx, fy)

        # --- memory gradient ---
        mx, my = np.gradient(memory)
        memx = sample_field(mx, x, y)
        memy = sample_field(my, x, y)

        # --- combined force ---
        force_x = (
            ALPHA_FLOW * fx +
            BETA_SWIRL * sx +
            GAMMA_MEMORY * memx
        )

        force_y = (
            ALPHA_FLOW * fy +
            BETA_SWIRL * sy +
            GAMMA_MEMORY * memy
        )

        # --- noise ---
        force_x += np.random.randn() * NOISE
        force_y += np.random.randn() * NOISE

        # --- velocity update ---
        vel[i, 0] = DAMPING * vel[i, 0] + STEP_SIZE * force_x
        vel[i, 1] = DAMPING * vel[i, 1] + STEP_SIZE * force_y

        # --- position update ---
        agents[i, 0] += vel[i, 0]
        agents[i, 1] += vel[i, 1]

        # --- clamp ---
        agents[i, 0] = np.clip(agents[i, 0], 0, field.shape[0] - 1)
        agents[i, 1] = np.clip(agents[i, 1], 0, field.shape[1] - 1)

        # --- store trajectory ---
        trajectories[i].append(agents[i].copy())

        # --- update memory ---
        xi, yi = int(agents[i, 0]), int(agents[i, 1])
        memory[xi, yi] += 1.0

    # decay
    field *= FIELD_DECAY
    memory *= MEMORY_DECAY

# --------------------------------------------------
# RECURRENCE MAP
# --------------------------------------------------

recurrence = memory / (memory.max() + 1e-8)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

entropy = -np.sum((memory / memory.sum() + 1e-12) * np.log(memory / memory.sum() + 1e-12))

# --------------------------------------------------
# SAVE LOG
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

log_data = {
    "run_id": run_id,
    "config": {
        "N_AGENTS": N_AGENTS,
        "STEPS": STEPS,
        "STEP_SIZE": STEP_SIZE,
        "NOISE": NOISE,
        "DAMPING": DAMPING,
        "ALPHA_FLOW": ALPHA_FLOW,
        "BETA_SWIRL": BETA_SWIRL,
        "GAMMA_MEMORY": GAMMA_MEMORY
    },
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(np.mean(recurrence))
    }
}

with open(f"{LOG_DIR}/log_level17_{run_id}.json", "w") as f:
    json.dump(log_data, f, indent=2)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# --- Field ---
axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Base Field")

# --- Flow ---
skip = 3
X, Y = np.meshgrid(np.arange(0, field.shape[0], skip),
                   np.arange(0, field.shape[1], skip))

U = gx[::skip, ::skip]
V = gy[::skip, ::skip]

axs[0, 1].imshow(field, cmap="viridis", alpha=0.6)
axs[0, 1].quiver(X, Y, U, V, color="white")
axs[0, 1].set_title("Flow Field")

# --- Trajectories ---
for traj in trajectories:
    traj = np.array(traj)
    axs[1, 0].plot(traj[:, 1], traj[:, 0], alpha=0.2)

axs[1, 0].set_title("Agent Trajectories")

# --- Recurrence ---
axs[1, 1].imshow(recurrence, cmap="magma")
axs[1, 1].set_title("Recurrence Map")

plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/level17_{run_id}.png", dpi=150)
plt.show()

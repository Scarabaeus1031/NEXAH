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
STEPS = 300

STEP_SIZE = 0.30
NOISE = 0.015
DAMPING = 0.90

ALPHA_FLOW = 0.9
BETA_SWIRL = 0.6
GAMMA_MEMORY = 0.4

RESONANCE_THRESHOLD = 0.6
RESONANCE_GAIN = 1.5

FIELD_DECAY = 0.985
MEMORY_DECAY = 0.995

SAVE_DIR = "ENGINE/visuals/navigation_level18"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD
# --------------------------------------------------

def sample_field(field, x, y):
    h, w = field.shape
    x = int(np.clip(x, 0, h - 1))
    y = int(np.clip(y, 0, w - 1))
    return field[x, y]

def compute_gradient(field):
    gx, gy = np.gradient(field)
    return gx, gy

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

    mx, my = np.gradient(memory)

    for i in range(N_AGENTS):

        x, y = agents[i]

        fx = sample_field(gx, x, y)
        fy = sample_field(gy, x, y)

        sx, sy = orthogonal(fx, fy)

        memx = sample_field(mx, x, y)
        memy = sample_field(my, x, y)

        # --- base force ---
        force = np.array([
            ALPHA_FLOW * fx + BETA_SWIRL * sx + GAMMA_MEMORY * memx,
            ALPHA_FLOW * fy + BETA_SWIRL * sy + GAMMA_MEMORY * memy
        ])

        # --- normalize ---
        f_norm = np.linalg.norm(force) + 1e-9
        force = force / f_norm

        # --------------------------------------------------
        # 🔥 RESONANCE LOCK
        # --------------------------------------------------

        grad_vec = np.array([fx, fy])
        g_norm = np.linalg.norm(grad_vec) + 1e-9
        grad_vec = grad_vec / g_norm

        vel_vec = vel[i]
        v_norm = np.linalg.norm(vel_vec) + 1e-9
        vel_dir = vel_vec / v_norm

        alignment = np.dot(vel_dir, grad_vec)

        if alignment > RESONANCE_THRESHOLD:
            force *= RESONANCE_GAIN

        # --------------------------------------------------

        # noise
        force += NOISE * np.random.randn(2)

        # update velocity
        vel[i] = DAMPING * vel[i] + STEP_SIZE * force

        # update position
        agents[i] += vel[i]

        agents[i, 0] = np.clip(agents[i, 0], 0, field.shape[0] - 1)
        agents[i, 1] = np.clip(agents[i, 1], 0, field.shape[1] - 1)

        trajectories[i].append(agents[i].copy())

        xi, yi = int(agents[i, 0]), int(agents[i, 1])
        memory[xi, yi] += 1.0

    field *= FIELD_DECAY
    memory *= MEMORY_DECAY

# --------------------------------------------------
# METRICS
# --------------------------------------------------

memory_norm = memory / (memory.sum() + 1e-12)
entropy = -np.sum(memory_norm * np.log(memory_norm + 1e-12))

recurrence = np.mean(memory / (memory.max() + 1e-9))

# --------------------------------------------------
# LOG
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

log_data = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence)
    }
}

with open(f"{LOG_DIR}/log_level18_{run_id}.json", "w") as f:
    json.dump(log_data, f, indent=2)

# --------------------------------------------------
# VISUAL
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# field
axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

# flow
skip = 3
X, Y = np.meshgrid(np.arange(0, field.shape[0], skip),
                   np.arange(0, field.shape[1], skip))

axs[0, 1].imshow(field, alpha=0.6)
axs[0, 1].quiver(X, Y, gx[::skip, ::skip], gy[::skip, ::skip], color="white")
axs[0, 1].set_title("Flow")

# trajectories
for traj in trajectories:
    traj = np.array(traj)
    axs[1, 0].plot(traj[:, 1], traj[:, 0], alpha=0.2)

axs[1, 0].set_title("Resonance Trajectories")

# recurrence
axs[1, 1].imshow(memory, cmap="magma")
axs[1, 1].set_title("Memory / Recurrence")

plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/level18_{run_id}.png", dpi=150)
plt.show()

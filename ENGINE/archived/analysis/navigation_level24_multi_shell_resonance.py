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
CENTER = np.array([SIZE / 2, SIZE / 2], dtype=float)

N_AGENTS = 120
STEPS = 460

STEP_SIZE = 0.20
NOISE = 0.005
DAMPING = 0.94

ALPHA_FLOW = 0.55
BETA_SWIRL = 0.55
GAMMA_MEMORY = 0.22
DELTA_RESONANCE = 0.42

FIELD_DECAY = 0.992
MEMORY_DECAY = 0.996

# --------------------------------------------------
# MULTI-SHELL SYSTEM
# --------------------------------------------------

TARGET_RADII = np.array([10.0, 18.0, 28.0], dtype=float)
SHELL_STRENGTH = 0.42
SHELL_TANGENTIAL_GAIN = 0.38
SHELL_WIDTH = 3.5

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

SAVE_DIR = "ENGINE/visuals/navigation_level24"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE))

agents = np.random.rand(N_AGENTS, 2) * SIZE
vel = np.zeros((N_AGENTS, 2))

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def sample_field(field, x, y):
    h, w = field.shape
    xi = int(np.clip(x, 0, h - 1))
    yi = int(np.clip(y, 0, w - 1))
    return field[xi, yi]

def compute_gradient(field):
    gx, gy = np.gradient(field)
    return gx, gy

def nearest_shell(dist):
    return TARGET_RADII[np.argmin(np.abs(TARGET_RADII - dist))]

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

trajectories = []
recurrence = np.zeros((SIZE, SIZE))

gx, gy = compute_gradient(field)

for step in range(STEPS):

    field *= FIELD_DECAY
    memory *= MEMORY_DECAY

    for i in range(N_AGENTS):

        pos = agents[i]
        v = vel[i]

        x, y = pos

        # ------------------------------
        # FLOW (Gradient)
        # ------------------------------
        g = np.array([
            gx[int(np.clip(x, 0, SIZE-1)), int(np.clip(y, 0, SIZE-1))],
            gy[int(np.clip(x, 0, SIZE-1)), int(np.clip(y, 0, SIZE-1))]
        ])

        # ------------------------------
        # SWIRL (Orthogonal)
        # ------------------------------
        swirl = np.array([-g[1], g[0]])

        # ------------------------------
        # MEMORY
        # ------------------------------
        mem = sample_field(memory, x, y)
        mem_vec = np.random.randn(2) * mem

        # ------------------------------
        # MULTI-SHELL LOGIC
        # ------------------------------
        rel = pos - CENTER
        dist = np.linalg.norm(rel) + 1e-8
        dir_radial = rel / dist

        target_r = nearest_shell(dist)

        # radial force toward shell
        radial_force = -(dist - target_r) * dir_radial

        # tangential motion along shell
        tangent = np.array([-dir_radial[1], dir_radial[0]])

        shell_weight = np.exp(-((dist - target_r) ** 2) / (2 * SHELL_WIDTH ** 2))

        shell_force = (
            SHELL_STRENGTH * radial_force +
            SHELL_TANGENTIAL_GAIN * tangent
        ) * shell_weight

        # ------------------------------
        # COMBINE FORCES
        # ------------------------------
        total = (
            ALPHA_FLOW * g +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * mem_vec +
            DELTA_RESONANCE * shell_force +
            NOISE * np.random.randn(2)
        )

        # ------------------------------
        # UPDATE
        # ------------------------------
        v = DAMPING * v + STEP_SIZE * total
        pos = pos + v

        pos = np.clip(pos, 0, SIZE - 1)

        agents[i] = pos
        vel[i] = v

        xi, yi = int(pos[0]), int(pos[1])
        memory[xi, yi] += 1
        recurrence[xi, yi] += 1

        trajectories.append(pos.copy())

# --------------------------------------------------
# METRICS
# --------------------------------------------------

prob = recurrence / np.sum(recurrence)
entropy = -np.sum(prob * np.log(prob + 1e-12))
recurrence_score = np.mean(recurrence > np.percentile(recurrence, 95))

# --------------------------------------------------
# SAVE LOG
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence_score)
    }
}

with open(f"{LOG_DIR}/log_level24_{run_id}.json", "w") as f:
    json.dump(log, f, indent=2)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

# Field
axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

# Flow
axs[0, 1].quiver(gx, gy)
axs[0, 1].set_title("Flow")

# Trajectories
traj = np.array(trajectories)
axs[1, 0].plot(traj[:, 1], traj[:, 0], linewidth=0.3, alpha=0.6)
axs[1, 0].set_title("Multi-Shell Trajectories")

# Memory
axs[1, 1].imshow(memory, cmap="magma")
axs[1, 1].set_title("Memory / Shell Density")

for ax in axs.flat:
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()
plt.savefig(f"{SAVE_DIR}/level24_{run_id}.png", dpi=150)
plt.close()

print("Run complete:", run_id)
print("Entropy:", entropy)
print("Recurrence:", recurrence_score)

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
STEPS = 750

STEP_SIZE = 0.12
NOISE = 0.002
DAMPING = 0.96

ALPHA_FLOW = 0.18
BETA_SWIRL = 0.28
GAMMA_MEMORY = 0.65
DELTA_RESONANCE = 0.22

FIELD_DECAY = 0.992
MEMORY_DECAY = 0.998

# --------------------------------------------------
# GRID / CRYSTALLIZATION
# --------------------------------------------------

GRID_SIZE = 6.0
GRID_STRENGTH = 0.35
MEMORY_QUANT = 0.25
AXIS_LOCK = 0.18

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

SAVE_DIR = "ENGINE/visuals/navigation_level28"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

agents = np.random.rand(N_AGENTS, 2) * SIZE
vel = np.zeros((N_AGENTS, 2), dtype=float)

frames = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def sample(arr, x, y):
    xi = int(np.clip(x, 0, SIZE - 1))
    yi = int(np.clip(y, 0, SIZE - 1))
    return arr[xi, yi]

def grad(arr, x, y):
    xi = int(x) % SIZE
    yi = int(y) % SIZE
    dx = arr[(xi + 1) % SIZE, yi] - arr[(xi - 1) % SIZE, yi]
    dy = arr[xi, (yi + 1) % SIZE] - arr[xi, (yi - 1) % SIZE]
    return np.array([dx, dy], dtype=float)

def normalize(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros_like(v)
    return v / n

def grid_pull(pos):
    gx = np.round(pos[0] / GRID_SIZE) * GRID_SIZE
    gy = np.round(pos[1] / GRID_SIZE) * GRID_SIZE
    target = np.array([gx, gy])
    return (target - pos)

def axis_projection(v):
    return np.array([
        v[0] * (1 - AXIS_LOCK) + np.sign(v[0]) * AXIS_LOCK,
        v[1] * (1 - AXIS_LOCK) + np.sign(v[1]) * AXIS_LOCK
    ])

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for step in range(STEPS):

    for i in range(N_AGENTS):

        pos = agents[i]

        # field + memory gradient
        g_field = grad(field, pos[0], pos[1])
        g_mem = grad(memory, pos[0], pos[1])

        # combined dynamics
        v = (
            ALPHA_FLOW * g_field +
            GAMMA_MEMORY * g_mem +
            BETA_SWIRL * np.array([-g_field[1], g_field[0]])
        )

        # grid pull
        v += GRID_STRENGTH * grid_pull(pos)

        # axis alignment
        v = axis_projection(v)

        # noise
        v += np.random.randn(2) * NOISE

        # normalize + damping
        v = normalize(v)
        vel[i] = vel[i] * DAMPING + v * STEP_SIZE

        agents[i] += vel[i]

        # wrap
        agents[i] %= SIZE

        # update memory (quantized)
        xi, yi = int(agents[i][0]), int(agents[i][1])
        memory[xi, yi] += MEMORY_QUANT

    # decay
    memory *= MEMORY_DECAY
    field *= FIELD_DECAY

    frames.append(agents.copy())

# --------------------------------------------------
# METRICS
# --------------------------------------------------

entropy = -np.sum(memory * np.log(memory + 1e-8))
recurrence = np.mean(memory > np.percentile(memory, 95))

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field (Crystallized)")

axs[0, 1].imshow(memory, cmap="inferno")
axs[0, 1].set_title("Memory (Quantized Grid)")

for traj in frames[-200:]:
    axs[1, 0].plot(traj[:, 0], traj[:, 1], alpha=0.02)

axs[1, 0].set_title("Grid-Aligned Trajectories")

axs[1, 1].imshow(memory > np.percentile(memory, 85), cmap="gray")
axs[1, 1].set_title("Emergent Grid Nodes")

# save
run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
img_path = os.path.join(SAVE_DIR, f"level28_{run_id}.png")
plt.savefig(img_path)
plt.close()

# --------------------------------------------------
# LOG
# --------------------------------------------------

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence)
    }
}

with open(os.path.join(LOG_DIR, f"level28_{run_id}.json"), "w") as f:
    json.dump(log, f, indent=2)

print("Run complete:", run_id)

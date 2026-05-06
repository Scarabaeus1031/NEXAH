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
STEPS = 850

STEP_SIZE = 0.10
NOISE = 0.0018
DAMPING = 0.965

ALPHA_FLOW = 0.15
BETA_SWIRL = 0.22
GAMMA_MEMORY = 0.75
DELTA_RESONANCE = 0.18

FIELD_DECAY = 0.991
MEMORY_DECAY = 0.999

# --------------------------------------------------
# SYMBOL SYSTEM
# --------------------------------------------------

CLUSTER_RADIUS = 2.5
SYMBOL_THRESHOLD = 4.0
SYMBOL_STRENGTH = 0.6
ALIGNMENT_GAIN = 0.25

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

SAVE_DIR = "ENGINE/visuals/navigation_level29"
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

def detect_clusters(memory):
    coords = np.argwhere(memory > SYMBOL_THRESHOLD)
    clusters = []

    for c in coords:
        close = []
        for d in coords:
            if np.linalg.norm(c - d) < CLUSTER_RADIUS:
                close.append(d)
        if len(close) > 3:
            clusters.append(np.mean(close, axis=0))

    return clusters

def alignment_force(pos, clusters):
    force = np.zeros(2)
    for c in clusters:
        direction = c - pos
        dist = np.linalg.norm(direction)
        if dist < 15:
            force += normalize(direction)
    return force

# --------------------------------------------------
# MAIN LOOP
# --------------------------------------------------

for step in range(STEPS):

    clusters = detect_clusters(memory)

    for i in range(N_AGENTS):

        pos = agents[i]

        g_field = grad(field, pos[0], pos[1])
        g_mem = grad(memory, pos[0], pos[1])

        v = (
            ALPHA_FLOW * g_field +
            GAMMA_MEMORY * g_mem +
            BETA_SWIRL * np.array([-g_field[1], g_field[0]])
        )

        # symbol alignment
        v += ALIGNMENT_GAIN * alignment_force(pos, clusters)

        # noise
        v += np.random.randn(2) * NOISE

        v = normalize(v)
        vel[i] = vel[i] * DAMPING + v * STEP_SIZE

        agents[i] += vel[i]
        agents[i] %= SIZE

        xi, yi = int(agents[i][0]), int(agents[i][1])
        memory[xi, yi] += 1.0

    memory *= MEMORY_DECAY
    field *= FIELD_DECAY

    frames.append(agents.copy())

# --------------------------------------------------
# METRICS
# --------------------------------------------------

entropy = -np.sum(memory * np.log(memory + 1e-8))
recurrence = np.mean(memory > np.percentile(memory, 95))
cluster_count = len(detect_clusters(memory))

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(10, 10))

axs[0, 0].imshow(field, cmap="viridis")
axs[0, 0].set_title("Field")

axs[0, 1].imshow(memory, cmap="inferno")
axs[0, 1].set_title("Symbol Memory")

for traj in frames[-200:]:
    axs[1, 0].plot(traj[:, 0], traj[:, 1], alpha=0.02)

axs[1, 0].set_title("Symbol Trajectories")

binary = memory > SYMBOL_THRESHOLD
axs[1, 1].imshow(binary, cmap="gray")
axs[1, 1].set_title("Detected Symbols")

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
img_path = os.path.join(SAVE_DIR, f"level29_{run_id}.png")
plt.savefig(img_path)
plt.close()

# --------------------------------------------------
# LOG
# --------------------------------------------------

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence),
        "clusters": int(cluster_count)
    }
}

with open(os.path.join(LOG_DIR, f"level29_{run_id}.json"), "w") as f:
    json.dump(log, f, indent=2)

print("Run complete:", run_id)

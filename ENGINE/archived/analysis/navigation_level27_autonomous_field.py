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
STEPS = 700

STEP_SIZE = 0.14
NOISE = 0.0025
DAMPING = 0.955

ALPHA_FLOW = 0.22
BETA_SWIRL = 0.34
GAMMA_MEMORY = 0.55
DELTA_RESONANCE = 0.28

# --------------------------------------------------
# AUTONOMOUS FIELD
# --------------------------------------------------

BASE_FIELD_BLEND = 0.08
MEMORY_FIELD_BLEND = 0.92
MEMORY_GRAD_GAIN = 0.60

FIELD_DECAY = 0.991
MEMORY_DECAY = 0.999

# self-excitation (very important)
MEMORY_SELF_EXCITE = 0.015
FIELD_REINFORCE = 0.02

# controlled instability (Mode C)
INSTABILITY_PROB = 0.003
INSTABILITY_STRENGTH = 0.6

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

SAVE_DIR = "ENGINE/visuals/navigation_level27"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# INIT
# --------------------------------------------------

base_field = generate_stability_landscape(SIZE)
field = base_field.copy()
memory = np.zeros((SIZE, SIZE), dtype=float)

agents = np.random.rand(N_AGENTS, 2) * SIZE
vel = np.zeros((N_AGENTS, 2), dtype=float)

frames = []

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def normalize(v):
    n = np.linalg.norm(v)
    if n < 1e-12:
        return np.zeros_like(v)
    return v / n

def grad(arr, x, y):
    xi = int(x) % SIZE
    yi = int(y) % SIZE
    dx = arr[(xi+1)%SIZE, yi] - arr[(xi-1)%SIZE, yi]
    dy = arr[xi, (yi+1)%SIZE] - arr[xi, (yi-1)%SIZE]
    return np.array([dx, dy], dtype=float)

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    # --------------------------------------------------
    # AUTONOMOUS FIELD GENERATION
    # --------------------------------------------------

    memory_norm = memory / (np.max(memory) + 1e-8)

    field = (
        BASE_FIELD_BLEND * base_field +
        MEMORY_FIELD_BLEND * memory_norm
    )

    # reinforce field from memory
    field += FIELD_REINFORCE * memory_norm

    new_positions = []

    for i in range(N_AGENTS):

        x, y = agents[i]

        # --------------------------
        # FLOW + SWIRL
        # --------------------------
        g = grad(field, x, y)
        flow = normalize(g)

        swirl = np.array([-flow[1], flow[0]])

        # --------------------------
        # MEMORY FORCE
        # --------------------------
        mg = grad(memory, x, y)
        mem_force = MEMORY_GRAD_GAIN * normalize(mg)

        # --------------------------
        # ORBITAL STRUCTURE
        # --------------------------
        rel = agents[i] - CENTER
        r = np.linalg.norm(rel) + 1e-8

        radial = -normalize(rel) * (r - 22.0) * 0.03

        tangent = np.array([-rel[1], rel[0]])
        tangent = normalize(tangent)

        orbit = tangent * np.sin(step * 0.008 + i * 0.01)

        # --------------------------
        # CONTROLLED INSTABILITY
        # --------------------------
        instability = np.zeros(2)

        if np.random.rand() < INSTABILITY_PROB:
            instability = np.random.randn(2) * INSTABILITY_STRENGTH

        # --------------------------
        # TOTAL FORCE
        # --------------------------
        total = (
            ALPHA_FLOW * flow +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * mem_force +
            DELTA_RESONANCE * orbit +
            radial +
            instability
        )

        vel[i] = DAMPING * vel[i] + STEP_SIZE * total
        vel[i] += np.random.randn(2) * NOISE

        agents[i] += vel[i]
        agents[i] = np.clip(agents[i], 0, SIZE - 1)

        xi, yi = int(agents[i][0]), int(agents[i][1])

        # memory deposition + self-excitation
        memory[xi, yi] += 1.0 + MEMORY_SELF_EXCITE * memory[xi, yi]

        new_positions.append(agents[i].copy())

    # decay
    memory *= MEMORY_DECAY
    field *= FIELD_DECAY

    frames.append(np.array(new_positions))

# --------------------------------------------------
# METRICS
# --------------------------------------------------

prob = memory / (np.sum(memory) + 1e-12)
entropy = -np.sum(prob * np.log(prob + 1e-12))
recurrence = np.mean(memory > np.percentile(memory, 95))

alignment = np.corrcoef(field.flatten(), memory.flatten())[0,1]

# autonomy score (NEW)
autonomy_score = np.mean(memory > np.mean(memory))

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Field
axs[0,0].imshow(field, cmap="viridis")
axs[0,0].set_title("Autonomous Field")

# Flow
gx, gy = np.gradient(field)
axs[0,1].quiver(gx, gy)
axs[0,1].set_title("Flow")

# Trajectories
for traj in frames[::20]:
    axs[1,0].plot(traj[:,0], traj[:,1], alpha=0.25, linewidth=0.7)

axs[1,0].set_title("Autonomous Trajectories")

# Memory
axs[1,1].imshow(memory, cmap="magma")
axs[1,1].set_title("Self-Sustained Memory")

for ax in axs.flat:
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
img_path = f"{SAVE_DIR}/level27_{run_id}.png"
plt.savefig(img_path, dpi=200)
plt.close()

# --------------------------------------------------
# LOG
# --------------------------------------------------

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence),
        "alignment": float(alignment),
        "autonomy_score": float(autonomy_score)
    }
}

with open(f"{LOG_DIR}/log_level27_{run_id}.json", "w") as f:
    json.dump(log, f, indent=2)

print("Run complete:", run_id)
print("Entropy:", entropy)
print("Recurrence:", recurrence)
print("Alignment:", alignment)
print("Autonomy Score:", autonomy_score)

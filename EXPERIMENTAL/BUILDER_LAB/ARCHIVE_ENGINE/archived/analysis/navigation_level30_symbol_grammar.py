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
STEPS = 600

STEP_SIZE = 0.12
NOISE = 0.002
DAMPING = 0.96

ALPHA_FLOW = 0.20
BETA_SWIRL = 0.25
GAMMA_MEMORY = 0.65
DELTA_RESONANCE = 0.30

# Symbol Grammar
SYMBOL_THRESHOLD = 0.015
SEQUENCE_LENGTH = 6
SEQUENCE_TOL = 2.5

MEMORY_DECAY = 0.996

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

SAVE_DIR = "ENGINE/visuals/navigation_level30"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# INIT
# --------------------------------------------------

field = generate_stability_landscape(SIZE)
memory = np.zeros((SIZE, SIZE), dtype=float)

agents = np.random.rand(N_AGENTS, 2) * SIZE
vel = np.zeros((N_AGENTS, 2))

trajectories = [[] for _ in range(N_AGENTS)]

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def gradient(arr, x, y):
    xi = int(x) % SIZE
    yi = int(y) % SIZE
    dx = arr[(xi + 1) % SIZE, yi] - arr[(xi - 1) % SIZE, yi]
    dy = arr[xi, (yi + 1) % SIZE] - arr[xi, (yi - 1) % SIZE]
    return np.array([dx, dy])

def normalize(v):
    n = np.linalg.norm(v)
    return v / n if n > 1e-8 else np.zeros_like(v)

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    memory *= MEMORY_DECAY

    for i in range(N_AGENTS):

        x, y = agents[i]

        grad = gradient(field, x, y)
        mem_grad = gradient(memory, x, y)

        flow = normalize(grad)
        swirl = np.array([-flow[1], flow[0]])

        v = (
            ALPHA_FLOW * flow +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * normalize(mem_grad)
        )

        v += np.random.randn(2) * NOISE
        vel[i] = DAMPING * vel[i] + v

        agents[i] += vel[i] * STEP_SIZE
        agents[i] %= SIZE

        xi, yi = int(agents[i][0]), int(agents[i][1])
        memory[xi, yi] += DELTA_RESONANCE

        trajectories[i].append((agents[i][0], agents[i][1]))

# --------------------------------------------------
# SYMBOL DETECTION
# --------------------------------------------------

symbol_mask = memory > SYMBOL_THRESHOLD

# --------------------------------------------------
# SEQUENCE DETECTION (Grammar)
# --------------------------------------------------

sequences = []

for traj in trajectories:
    if len(traj) < SEQUENCE_LENGTH:
        continue

    for i in range(len(traj) - SEQUENCE_LENGTH):
        segment = traj[i:i+SEQUENCE_LENGTH]

        start = np.array(segment[0])
        end = np.array(segment[-1])

        # straightness measure
        dist = np.linalg.norm(end - start)

        path_len = sum(
            np.linalg.norm(np.array(segment[j+1]) - np.array(segment[j]))
            for j in range(SEQUENCE_LENGTH - 1)
        )

        if abs(path_len - dist) < SEQUENCE_TOL:
            sequences.append(segment)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

entropy = -np.sum(memory * np.log(memory + 1e-12))
recurrence = np.mean(memory > SYMBOL_THRESHOLD)
grammar_density = len(sequences)

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

# --------------------------------------------------
# PLOT
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Field
axs[0, 0].imshow(field, origin="lower")
axs[0, 0].set_title("Field")

# Symbol Memory
axs[0, 1].imshow(memory, origin="lower")
axs[0, 1].set_title("Symbol Memory")

# Trajectories
for traj in trajectories:
    xs, ys = zip(*traj)
    axs[1, 0].plot(xs, ys, alpha=0.15)
axs[1, 0].set_title("Symbol Trajectories")

# Grammar Sequences
axs[1, 1].imshow(symbol_mask, origin="lower", cmap="gray")

for seq in sequences[:150]:
    xs, ys = zip(*seq)
    axs[1, 1].plot(xs, ys, linewidth=1.2)

axs[1, 1].set_title("Symbol Grammar (Sequences)")

plt.tight_layout()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

img_path = os.path.join(SAVE_DIR, f"level30_{run_id}.png")
plt.savefig(img_path)
plt.close()

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence),
        "grammar_sequences": int(grammar_density)
    }
}

with open(os.path.join(LOG_DIR, f"level30_{run_id}.json"), "w") as f:
    json.dump(log, f, indent=2)

print("Run complete:", run_id)
print("Entropy:", entropy)
print("Recurrence:", recurrence)
print("Grammar sequences:", grammar_density)

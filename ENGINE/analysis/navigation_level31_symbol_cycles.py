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
STEPS = 700

STEP_SIZE = 0.11
NOISE = 0.002
DAMPING = 0.965

ALPHA_FLOW = 0.18
BETA_SWIRL = 0.22
GAMMA_MEMORY = 0.72

MEMORY_DECAY = 0.997

# Symbol detection
SYMBOL_THRESHOLD = 0.02
CLUSTER_RADIUS = 3.5
MAX_SYMBOLS = 30

# Cycle detection
MAX_HISTORY = 20
CYCLE_TOL = 2.5
MIN_CYCLE_LENGTH = 3
MAX_CYCLE_LENGTH = 8

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

SAVE_DIR = "ENGINE/visuals/navigation_level31"
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

agent_histories = [[] for _ in range(N_AGENTS)]

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

def detect_symbols(memory):
    coords = np.argwhere(memory > SYMBOL_THRESHOLD)
    if len(coords) == 0:
        return []

    coords = sorted(coords, key=lambda c: memory[c[0], c[1]], reverse=True)

    nodes = []
    for c in coords:
        c = np.array(c, dtype=float)
        keep = True
        for n in nodes:
            if np.linalg.norm(c - n) < CLUSTER_RADIUS:
                keep = False
                break
        if keep:
            nodes.append(c)
        if len(nodes) >= MAX_SYMBOLS:
            break

    return nodes

def nearest_symbol(pos, nodes):
    if len(nodes) == 0:
        return None
    dists = [np.linalg.norm(pos - n) for n in nodes]
    idx = int(np.argmin(dists))
    if dists[idx] < CLUSTER_RADIUS * 2:
        return idx
    return None

def detect_cycles(history):
    cycles = []

    n = len(history)
    for length in range(MIN_CYCLE_LENGTH, MAX_CYCLE_LENGTH + 1):
        if n < 2 * length:
            continue

        seq1 = history[-length:]
        seq2 = history[-2*length:-length]

        if seq1 == seq2:
            cycles.append(seq1)

    return cycles

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

for step in range(STEPS):

    memory *= MEMORY_DECAY
    nodes = detect_symbols(memory)

    for i in range(N_AGENTS):

        x, y = agents[i]

        grad_f = gradient(field, x, y)
        grad_m = gradient(memory, x, y)

        flow = normalize(grad_f)
        swirl = np.array([-flow[1], flow[0]])

        v = (
            ALPHA_FLOW * flow +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * normalize(grad_m)
        )

        v += np.random.randn(2) * NOISE

        vel[i] = DAMPING * vel[i] + v
        agents[i] += vel[i] * STEP_SIZE
        agents[i] %= SIZE

        xi, yi = int(agents[i][0]), int(agents[i][1])
        memory[xi, yi] += 1.0

        sid = nearest_symbol(agents[i], nodes)

        if sid is not None:
            hist = agent_histories[i]

            if len(hist) == 0 or hist[-1] != sid:
                hist.append(sid)

            if len(hist) > MAX_HISTORY:
                hist.pop(0)

# --------------------------------------------------
# CYCLE ANALYSIS
# --------------------------------------------------

all_cycles = []

for hist in agent_histories:
    cycles = detect_cycles(hist)
    all_cycles.extend(cycles)

# count frequency
cycle_dict = {}

for c in all_cycles:
    key = tuple(c)
    cycle_dict[key] = cycle_dict.get(key, 0) + 1

# sort cycles
sorted_cycles = sorted(cycle_dict.items(), key=lambda x: x[1], reverse=True)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

entropy = -np.sum(memory * np.log(memory + 1e-12))
recurrence = np.mean(memory > SYMBOL_THRESHOLD)

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Memory
axs[0, 0].imshow(memory, cmap="inferno", origin="lower")
axs[0, 0].set_title("Symbol Memory")

# Symbols
nodes = detect_symbols(memory)
axs[0, 1].imshow(memory > SYMBOL_THRESHOLD, cmap="gray", origin="lower")
axs[0, 1].set_title("Detected Symbols")

for i, n in enumerate(nodes):
    axs[0, 1].scatter(n[1], n[0], s=25, c="cyan")
    axs[0, 1].text(n[1]+1, n[0]+1, str(i), color="white", fontsize=7)

# Cycle Visualization
axs[1, 0].imshow(memory, cmap="magma", origin="lower")
axs[1, 0].set_title("Cycle Paths")

top_cycles = sorted_cycles[:10]

for cyc, freq in top_cycles:
    if len(cyc) < 2:
        continue

    pts = [nodes[i] for i in cyc if i < len(nodes)]
    for a, b in zip(pts[:-1], pts[1:]):
        axs[1, 0].plot([a[1], b[1]], [a[0], b[0]],
                       color="cyan", alpha=0.6)

# Cycle histogram
lengths = [len(c[0]) for c in sorted_cycles]

axs[1, 1].hist(lengths, bins=range(1, MAX_CYCLE_LENGTH+2))
axs[1, 1].set_title("Cycle Length Distribution")

plt.tight_layout()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

img_path = os.path.join(SAVE_DIR, f"level31_{run_id}.png")
plt.savefig(img_path)
plt.close()

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence),
        "cycles_detected": int(len(all_cycles)),
        "unique_cycles": int(len(sorted_cycles))
    }
}

with open(os.path.join(LOG_DIR, f"level31_{run_id}.json"), "w") as f:
    json.dump(log, f, indent=2)

print("Run complete:", run_id)
print("Entropy:", entropy)
print("Recurrence:", recurrence)
print("Cycles detected:", len(all_cycles))
print("Unique cycles:", len(sorted_cycles))

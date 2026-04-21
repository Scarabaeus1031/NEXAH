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
STEPS = 750

STEP_SIZE = 0.11
NOISE = 0.002
DAMPING = 0.967

ALPHA_FLOW = 0.16
BETA_SWIRL = 0.20
GAMMA_MEMORY = 0.88

MEMORY_DECAY = 0.999

# symbol detection
SYMBOL_THRESHOLD = 0.02
CLUSTER_RADIUS = 3.5
MAX_SYMBOLS = 32

# cycle detection
MAX_HISTORY = 28
MIN_CYCLE_LENGTH = 3
MAX_CYCLE_LENGTH = 8

# locked dynamics
SYMBOL_LOCK_PROB = 0.88
SYMBOL_ATTRACTION = 0.95

# semantics
SEMANTIC_DISTANCE_THRESHOLD = 14.0
TOP_CYCLES_TO_CLUSTER = 24

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------

MODE = "semantics"

SAVE_DIR = "ENGINE/visuals/navigation_level32"
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

agent_histories = [[] for _ in range(N_AGENTS)]

# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def gradient(arr, x, y):
    xi = int(x) % SIZE
    yi = int(y) % SIZE
    dx = arr[(xi + 1) % SIZE, yi] - arr[(xi - 1) % SIZE, yi]
    dy = arr[xi, (yi + 1) % SIZE] - arr[xi, (yi - 1) % SIZE]
    return np.array([dx, dy], dtype=float)

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
        seq2 = history[-2 * length:-length]

        if seq1 == seq2:
            cycles.append(seq1)

    return cycles

def cycle_centroid(cycle, nodes):
    pts = [nodes[i] for i in cycle if i < len(nodes)]
    if len(pts) == 0:
        return None
    return np.mean(np.array(pts), axis=0)

def cycle_signature(cycle, nodes):
    pts = [nodes[i] for i in cycle if i < len(nodes)]
    if len(pts) < 2:
        return None

    pts = np.array(pts)
    center = np.mean(pts, axis=0)

    radii = np.linalg.norm(pts - center, axis=1)
    mean_radius = float(np.mean(radii))
    var_radius = float(np.var(radii))
    length = len(cycle)

    return np.array([length, mean_radius, var_radius], dtype=float)

def semantic_distance(sig1, sig2, c1, c2):
    if sig1 is None or sig2 is None or c1 is None or c2 is None:
        return np.inf

    ds = np.linalg.norm(sig1 - sig2)
    dc = np.linalg.norm(c1 - c2)
    return ds + 0.35 * dc

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
        swirl = np.array([-flow[1], flow[0]], dtype=float)

        v = (
            ALPHA_FLOW * flow +
            BETA_SWIRL * swirl +
            GAMMA_MEMORY * normalize(grad_m)
        )

        sid = nearest_symbol(agents[i], nodes)
        if sid is not None:
            target = nodes[sid]
            if np.random.rand() < SYMBOL_LOCK_PROB:
                direction = normalize(target - agents[i])
                v += direction * SYMBOL_ATTRACTION

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

cycle_dict = {}
for c in all_cycles:
    key = tuple(c)
    cycle_dict[key] = cycle_dict.get(key, 0) + 1

sorted_cycles = sorted(cycle_dict.items(), key=lambda x: x[1], reverse=True)
top_cycles = sorted_cycles[:TOP_CYCLES_TO_CLUSTER]

nodes = detect_symbols(memory)

# --------------------------------------------------
# SEMANTIC CLUSTERING
# --------------------------------------------------

semantic_groups = []
cycle_to_group = {}

for idx, (cyc, count) in enumerate(top_cycles):
    centroid = cycle_centroid(cyc, nodes)
    signature = cycle_signature(cyc, nodes)

    assigned = False
    for g_idx, group in enumerate(semantic_groups):
        d = semantic_distance(signature, group["signature"], centroid, group["centroid"])
        if d < SEMANTIC_DISTANCE_THRESHOLD:
            group["cycles"].append((cyc, count))
            group["members"].append(idx)
            # update centroid/signature as running average
            group["centroid"] = 0.5 * group["centroid"] + 0.5 * centroid
            group["signature"] = 0.5 * group["signature"] + 0.5 * signature
            cycle_to_group[cyc] = g_idx
            assigned = True
            break

    if not assigned:
        semantic_groups.append({
            "cycles": [(cyc, count)],
            "members": [idx],
            "centroid": centroid,
            "signature": signature
        })
        cycle_to_group[cyc] = len(semantic_groups) - 1

# --------------------------------------------------
# METRICS
# --------------------------------------------------

prob = memory / (np.sum(memory) + 1e-12)
entropy = -np.sum(prob * np.log(prob + 1e-12))
recurrence = np.mean(memory > np.percentile(memory, 95))

semantic_sizes = [len(g["cycles"]) for g in semantic_groups]

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

fig, axs = plt.subplots(2, 2, figsize=(12, 10))

# Memory
axs[0, 0].imshow(memory, cmap="inferno", origin="lower")
axs[0, 0].set_title("Symbol Memory")

# Detected symbols
binary = memory > SYMBOL_THRESHOLD
axs[0, 1].imshow(binary, cmap="gray", origin="lower")
axs[0, 1].set_title("Detected Symbols")
for i, n in enumerate(nodes):
    axs[0, 1].scatter(n[1], n[0], s=22, c="cyan")
    axs[0, 1].text(n[1] + 1, n[0] + 1, str(i), color="white", fontsize=7)

# Semantic groups overlay
axs[1, 0].imshow(memory, cmap="magma", origin="lower")
axs[1, 0].set_title("Semantic Groups")

colors = plt.cm.tab10(np.linspace(0, 1, max(1, len(semantic_groups))))

for g_idx, group in enumerate(semantic_groups):
    color = colors[g_idx % len(colors)]
    for cyc, count in group["cycles"]:
        pts = [nodes[i] for i in cyc if i < len(nodes)]
        if len(pts) < 2:
            continue
        pts = np.array(pts)
        axs[1, 0].plot(pts[:, 1], pts[:, 0], color=color, alpha=0.75, linewidth=1.2)
        # close loop visually
        axs[1, 0].plot([pts[-1, 1], pts[0, 1]], [pts[-1, 0], pts[0, 0]],
                       color=color, alpha=0.75, linewidth=1.2)
    c = group["centroid"]
    axs[1, 0].scatter(c[1], c[0], s=60, c=[color], edgecolors="white")

# Group size histogram
axs[1, 1].bar(range(len(semantic_sizes)), semantic_sizes)
axs[1, 1].set_title("Semantic Group Sizes")
axs[1, 1].set_xlabel("group")
axs[1, 1].set_ylabel("cycles")

for ax in axs[:, :].flat:
    if ax is not axs[1, 1]:
        ax.set_xticks([])
        ax.set_yticks([])

plt.tight_layout()

# --------------------------------------------------
# SAVE
# --------------------------------------------------

run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

img_path = os.path.join(SAVE_DIR, f"level32_{MODE}_{run_id}.png")
plt.savefig(img_path, dpi=180)
plt.close()

log = {
    "run_id": run_id,
    "metrics": {
        "entropy": float(entropy),
        "recurrence": float(recurrence),
        "cycles_detected": int(len(all_cycles)),
        "unique_cycles": int(len(sorted_cycles)),
        "semantic_groups": int(len(semantic_groups)),
        "semantic_sizes": [int(x) for x in semantic_sizes]
    }
}

with open(os.path.join(LOG_DIR, f"level32_{MODE}_{run_id}.json"), "w") as f:
    json.dump(log, f, indent=2)

print("Run complete:", run_id)
print("Mode:", MODE)
print("Entropy:", entropy)
print("Recurrence:", recurrence)
print("Cycles detected:", len(all_cycles))
print("Unique cycles:", len(sorted_cycles))
print("Semantic groups:", len(semantic_groups))
print("Semantic sizes:", semantic_sizes)

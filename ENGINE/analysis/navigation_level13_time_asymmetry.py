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
STEPS = 220

STEP_SIZE = 0.45
NOISE = 0.05
DAMPING = 0.92

ALPHA_FIELD = 0.6
BETA_TARGET = 1.2
GAMMA_MEMORY = 0.6

FIELD_DECAY = 0.985
MEMORY_DECAY = 0.992
FEEDBACK_GAIN = 0.22

SAVE_DIR = "ENGINE/visuals/navigation_level13"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD SAMPLING
# --------------------------------------------------

def sample_field(field, x, y):
    SIZE = field.shape[0]

    x = x % SIZE
    y = y % SIZE

    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    x1 = (x0 + 1) % SIZE
    y1 = (y0 + 1) % SIZE

    dx = x - x0
    dy = y - y0

    return (
        field[x0, y0] * (1 - dx) * (1 - dy) +
        field[x1, y0] * dx * (1 - dy) +
        field[x0, y1] * (1 - dx) * dy +
        field[x1, y1] * dx * dy
    )

# --------------------------------------------------
# GRADIENT
# --------------------------------------------------

def compute_gradient(field, x, y):
    eps = 1.0

    gx = (sample_field(field, x+eps, y) - sample_field(field, x-eps, y)) / (2*eps)
    gy = (sample_field(field, x, y+eps) - sample_field(field, x, y-eps)) / (2*eps)

    return np.array([gx, gy])

# --------------------------------------------------
# TARGETS
# --------------------------------------------------

def find_targets(field, k=3):
    flat = np.argsort(field.flatten())[::-1]
    SIZE = field.shape[0]

    targets = []
    for idx in flat:
        x = idx // SIZE
        y = idx % SIZE

        if all(np.linalg.norm(np.array([x,y]) - t) > 6 for t in targets):
            targets.append(np.array([x,y], dtype=float))

        if len(targets) >= k:
            break

    return targets

# --------------------------------------------------
# AGENT (FORWARD / BACKWARD)
# --------------------------------------------------

def run_agent(field, memory, targets, reverse=False):

    SIZE = field.shape[0]

    pos = np.array([
        np.random.uniform(0, SIZE),
        np.random.uniform(0, SIZE)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]

    target = targets[np.random.randint(len(targets))]

    for _ in range(STEPS):

        grad_field = compute_gradient(field, pos[0], pos[1])
        grad_memory = compute_gradient(memory, pos[0], pos[1])

        target_vec = target - pos
        target_vec /= (np.linalg.norm(target_vec) + 1e-6)

        grad_field /= (np.linalg.norm(grad_field) + 1e-6)
        grad_memory /= (np.linalg.norm(grad_memory) + 1e-6)

        direction = (
            ALPHA_FIELD * grad_field +
            BETA_TARGET * target_vec +
            GAMMA_MEMORY * grad_memory
        )

        direction /= (np.linalg.norm(direction) + 1e-6)

        # 🔥 REVERSAL
        if reverse:
            direction = -direction

        vel = DAMPING * vel + STEP_SIZE * direction
        vel += NOISE * np.random.randn(2)

        pos = (pos + vel) % SIZE
        path.append(pos.copy())

    return np.array(path)

# --------------------------------------------------
# MEMORY
# --------------------------------------------------

def update_memory(memory, paths):
    SIZE = memory.shape[0]
    new = np.zeros_like(memory)

    for path in paths:
        for p in path:
            x = int(p[0]) % SIZE
            y = int(p[1]) % SIZE
            new[x, y] += 1

    new = new / (np.max(new) + 1e-6)

    memory = MEMORY_DECAY * memory + FEEDBACK_GAIN * new
    memory = memory / (np.max(memory) + 1e-6)

    return memory

# --------------------------------------------------
# METRICS
# --------------------------------------------------

def compute_entropy(field):
    p = field / (np.sum(field) + 1e-12)
    p[p <= 0] = 1e-12
    return float(-np.sum(p * np.log(p)))

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def run_simulation():

    base = generate_stability_landscape()
    field = base.copy()
    memory = np.zeros_like(field)

    targets = find_targets(field)

    forward_paths = []
    backward_paths = []

    for _ in range(N_AGENTS):
        forward_paths.append(run_agent(field, memory, targets, reverse=False))
        backward_paths.append(run_agent(field, memory, targets, reverse=True))

    return base, field, memory, targets, forward_paths, backward_paths

# --------------------------------------------------
# VISUAL
# --------------------------------------------------

def plot_results(base, field, memory, targets, f_paths, b_paths):

    plt.figure(figsize=(15,5))

    # FIELD
    plt.subplot(1,3,1)
    plt.title("Field")
    plt.imshow(field, origin="lower")

    for t in targets:
        plt.scatter(t[0], t[1], s=120)

    plt.axis("off")

    # FORWARD
    plt.subplot(1,3,2)
    plt.title("Forward Paths")
    plt.imshow(field, origin="lower")

    for p in f_paths[:60]:
        plt.plot(p[:,0], p[:,1], alpha=0.2)

    plt.axis("off")

    # BACKWARD
    plt.subplot(1,3,3)
    plt.title("Backward Paths")
    plt.imshow(field, origin="lower")

    for p in b_paths[:60]:
        plt.plot(p[:,0], p[:,1], alpha=0.2)

    plt.axis("off")

    path = os.path.join(SAVE_DIR, "time_reversal.png")
    plt.savefig(path, dpi=200)

    print(f"\nSaved → {path}")
    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    base, field, memory, targets, f_paths, b_paths = run_simulation()

    metrics = {
        "entropy": compute_entropy(field)
    }

    config = {
        "STEP_SIZE": STEP_SIZE,
        "NOISE": NOISE,
        "DAMPING": DAMPING
    }

    log_path = os.path.join(LOG_DIR, "level13.json")

    with open(log_path, "w") as f:
        json.dump({
            "config": config,
            "metrics": metrics
        }, f, indent=2)

    print(f"Saved log → {log_path}")

    plot_results(base, field, memory, targets, f_paths, b_paths)

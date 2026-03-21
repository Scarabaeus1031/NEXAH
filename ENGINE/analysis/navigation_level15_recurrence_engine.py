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

STEP_SIZE = 0.42
NOISE = 0.03
DAMPING = 0.93

ALPHA_FIELD = 0.6
BETA_TARGET = 1.1
GAMMA_MEMORY = 0.65

FIELD_DECAY = 0.985
MEMORY_DECAY = 0.992
FEEDBACK_GAIN = 0.2

LOOP_THRESHOLD = 1.5  # distance for recurrence detection

SAVE_DIR = "ENGINE/visuals/navigation_level15"
LOG_DIR = "ENGINE/logs"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD SAMPLING
# --------------------------------------------------

def sample_field(field, x, y):
    h, w = field.shape

    x = x % h
    y = y % w

    x0 = int(np.floor(x))
    y0 = int(np.floor(y))

    x1 = (x0 + 1) % h
    y1 = (y0 + 1) % w

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

    fx1 = sample_field(field, x + eps, y)
    fx2 = sample_field(field, x - eps, y)
    fy1 = sample_field(field, x, y + eps)
    fy2 = sample_field(field, x, y - eps)

    return np.array([
        (fx1 - fx2) / (2 * eps),
        (fy1 - fy2) / (2 * eps)
    ])

# --------------------------------------------------
# AGENT (WITH MEMORY)
# --------------------------------------------------

def run_agent(field, memory_field, targets):

    h, w = field.shape

    pos = np.array([
        np.random.uniform(0, h),
        np.random.uniform(0, w)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]

    for _ in range(STEPS):

        grad = compute_gradient(field, pos[0], pos[1])
        grad /= (np.linalg.norm(grad) + 1e-6)

        mem_grad = compute_gradient(memory_field, pos[0], pos[1])
        mem_grad /= (np.linalg.norm(mem_grad) + 1e-6)

        target = targets[np.random.randint(len(targets))]
        t_vec = target - pos
        t_vec /= (np.linalg.norm(t_vec) + 1e-6)

        direction = (
            ALPHA_FIELD * grad +
            BETA_TARGET * t_vec +
            GAMMA_MEMORY * mem_grad
        )

        direction /= (np.linalg.norm(direction) + 1e-6)

        vel = DAMPING * vel + STEP_SIZE * direction
        vel += NOISE * np.random.randn(2)

        pos = (pos + vel) % np.array([h, w])
        path.append(pos.copy())

    return np.array(path)

# --------------------------------------------------
# RESPONSE
# --------------------------------------------------

def compute_response(paths, shape):
    response = np.zeros(shape)

    for path in paths:
        for p in path:
            x = int(p[0]) % shape[0]
            y = int(p[1]) % shape[1]
            response[x, y] += 1

    return response / (np.max(response) + 1e-6)

# --------------------------------------------------
# LOOP / RECURRENCE METRIC
# --------------------------------------------------

def compute_recurrence(paths):

    loop_count = 0
    total = 0

    for path in paths:
        start = path[0]

        for p in path[50:]:  # ignore early noise
            dist = np.linalg.norm(p - start)
            total += 1
            if dist < LOOP_THRESHOLD:
                loop_count += 1

    return loop_count / (total + 1e-6)

# --------------------------------------------------
# ENTROPY
# --------------------------------------------------

def compute_entropy(field):
    f = field.flatten()
    f = f / (np.sum(f) + 1e-12)
    f = f[f > 0]
    return -np.sum(f * np.log(f))

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def run_simulation():

    base = generate_stability_landscape()
    field = base.copy()
    memory = np.zeros_like(field)

    h, w = field.shape

    # detect top 3 attractors
    flat_idx = np.argsort(field.flatten())[::-1][:3]
    targets = [np.array([i // w, i % w]) for i in flat_idx]

    paths = []

    for _ in range(N_AGENTS):
        p = run_agent(field, memory, targets)
        paths.append(p)

    response = compute_response(paths, field.shape)

    field = FIELD_DECAY * field + FEEDBACK_GAIN * response
    field /= (np.max(field) + 1e-6)

    memory = MEMORY_DECAY * memory + response
    memory /= (np.max(memory) + 1e-6)

    # metrics
    entropy = compute_entropy(response)
    recurrence = compute_recurrence(paths)

    return base, field, memory, paths, entropy, recurrence

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, field, memory, paths):

    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    plt.subplot(1, 3, 2)
    plt.title("Final Field")
    plt.imshow(field, origin="lower")

    for p in paths[:80]:
        plt.plot(p[:, 0], p[:, 1], alpha=0.2)

    plt.axis("off")

    plt.subplot(1, 3, 3)
    plt.title("Memory Field")
    plt.imshow(memory, origin="lower")
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "level15_result.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# LOGGING
# --------------------------------------------------

def save_log(entropy, recurrence):

    data = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "metrics": {
            "entropy": float(entropy),
            "recurrence": float(recurrence)
        }
    }

    path = os.path.join(LOG_DIR, f"log_level15_{data['run_id']}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Log saved → {path}")

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    base, field, memory, paths, entropy, recurrence = run_simulation()

    plot_results(base, field, memory, paths)
    save_log(entropy, recurrence)

    print("\n--- RESULTS ---")
    print(f"Entropy     : {entropy:.4f}")
    print(f"Recurrence  : {recurrence:.6f}")

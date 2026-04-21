import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

N_AGENTS = 100
STEPS = 360

STEP_SIZE = 0.38
NOISE = 0.025
DAMPING = 0.94

ALPHA_FIELD = 0.55
BETA_TARGET = 1.15
GAMMA_MEMORY = 0.55

FIELD_DECAY = 0.988
MEMORY_DECAY = 0.994
FEEDBACK_GAIN = 0.16

# 🔴 NEW: PHASE SYSTEM
PHASE_SPEED = 0.045
PHASE_RADIUS = 6.0

SAVE_DIR = "ENGINE/visuals/navigation_level16"
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

    gx = (sample_field(field, x + eps, y) - sample_field(field, x - eps, y)) / (2 * eps)
    gy = (sample_field(field, x, y + eps) - sample_field(field, x, y - eps)) / (2 * eps)

    return np.array([gx, gy])

# --------------------------------------------------
# TARGET EXTRACTION
# --------------------------------------------------

def find_targets(field, k=3):
    h, w = field.shape
    flat = np.argsort(field.flatten())[::-1][:k]
    return [np.array([i // w, i % w], dtype=float) for i in flat]

# --------------------------------------------------
# PHASE ROTATION (L2⁴ CORE)
# --------------------------------------------------

def rotate_targets(targets, t, center):

    rotated = []
    angle = PHASE_SPEED * t

    for i, target in enumerate(targets):

        # each target gets its own phase offset
        a = angle + i * (2 * np.pi / len(targets))

        offset = np.array([
            PHASE_RADIUS * np.cos(a),
            PHASE_RADIUS * np.sin(a)
        ])

        rotated.append(center + offset)

    return rotated

# --------------------------------------------------
# AGENT
# --------------------------------------------------

def run_agent(field, memory, targets):

    h, w = field.shape

    pos = np.array([
        np.random.uniform(0, h),
        np.random.uniform(0, w)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]

    center = np.array([h/2, w/2])

    for t in range(STEPS):

        grad = compute_gradient(field, pos[0], pos[1])
        grad /= (np.linalg.norm(grad) + 1e-6)

        mem_grad = compute_gradient(memory, pos[0], pos[1])
        mem_grad /= (np.linalg.norm(mem_grad) + 1e-6)

        # 🔴 rotating targets
        phase_targets = rotate_targets(targets, t, center)
        target = phase_targets[np.random.randint(len(phase_targets))]

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

    resp = np.zeros(shape)

    for path in paths:
        for p in path:
            x = int(p[0]) % shape[0]
            y = int(p[1]) % shape[1]
            resp[x, y] += 1

    return resp / (np.max(resp) + 1e-6)

# --------------------------------------------------
# METRICS
# --------------------------------------------------

def compute_entropy(field):
    f = field.flatten()
    f = f / (np.sum(f) + 1e-12)
    f = f[f > 0]
    return float(-np.sum(f * np.log(f)))

def compute_recurrence(paths):

    loops = 0
    total = 0

    for path in paths:
        start = path[0]

        for p in path[80:]:
            d = np.linalg.norm(p - start)
            total += 1
            if d < 1.5:
                loops += 1

    return loops / (total + 1e-6)

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def run_simulation():

    base = generate_stability_landscape()
    field = base.copy()
    memory = np.zeros_like(field)

    targets = find_targets(field)

    paths = [run_agent(field, memory, targets) for _ in range(N_AGENTS)]

    response = compute_response(paths, field.shape)

    field = FIELD_DECAY * field + FEEDBACK_GAIN * response
    field /= (np.max(field) + 1e-6)

    memory = MEMORY_DECAY * memory + response
    memory /= (np.max(memory) + 1e-6)

    entropy = compute_entropy(response)
    recurrence = compute_recurrence(paths)

    return base, field, memory, paths, entropy, recurrence

# --------------------------------------------------
# VISUAL
# --------------------------------------------------

def plot_results(base, field, memory, paths):

    plt.figure(figsize=(15,5))

    plt.subplot(1,3,1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    plt.subplot(1,3,2)
    plt.title("Phase Navigation Field")
    plt.imshow(field, origin="lower")

    for p in paths[:80]:
        plt.plot(p[:,0], p[:,1], alpha=0.15)

    plt.axis("off")

    plt.subplot(1,3,3)
    plt.title("Memory Field")
    plt.imshow(memory, origin="lower")
    plt.axis("off")

    out = os.path.join(SAVE_DIR, "level16_phase.png")
    plt.savefig(out, dpi=220)
    print(f"Saved → {out}")
    plt.show()

# --------------------------------------------------
# LOG
# --------------------------------------------------

def save_log(entropy, recurrence):

    data = {
        "run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "metrics": {
            "entropy": entropy,
            "recurrence": recurrence
        }
    }

    path = os.path.join(LOG_DIR, f"log_level16_{data['run_id']}.json")

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

    print("\n--- LEVEL 16 ---")
    print(f"Entropy    : {entropy:.4f}")
    print(f"Recurrence : {recurrence:.6f}")

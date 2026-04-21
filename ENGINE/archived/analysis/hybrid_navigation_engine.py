import numpy as np
import matplotlib.pyplot as plt
import os
import json
import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

N_AGENTS = 140
STEPS = 260

STEP_SIZE = 0.42
NOISE = 0.045
DAMPING = 0.90

ALPHA_FIELD = 0.65   # Feldgradient
BETA_TARGET = 0.95   # Zielvektor
GAMMA_MEMORY = 0.75  # Memory influence

FIELD_DECAY = 0.985
MEMORY_DECAY = 0.992
FEEDBACK_GAIN = 0.22

SAVE_DIR = "ENGINE/visuals/navigation_hybrid"
LOG_DIR = "ENGINE/logs/level11"

os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --------------------------------------------------
# LOGGING
# --------------------------------------------------

def create_run_id():
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def save_run(config, metrics):
    run_id = create_run_id()

    data = {
        "run_id": run_id,
        "config": config,
        "metrics": metrics
    }

    path = os.path.join(LOG_DIR, f"level11_{run_id}.json")

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"✔ Run saved → {path}")

# --------------------------------------------------
# METRICS
# --------------------------------------------------

def compute_metrics(field, memory):

    field_norm = field / (np.max(field) + 1e-9)

    entropy = -np.sum(field_norm * np.log(field_norm + 1e-9))
    peak = np.max(field_norm)
    spread = np.std(field_norm)
    memory_strength = np.sum(memory)

    return {
        "entropy": float(entropy),
        "peak": float(peak),
        "spread": float(spread),
        "memory": float(memory_strength)
    }

# --------------------------------------------------
# FIELD SAMPLING (FIXED!)
# --------------------------------------------------

def sample_field(field, x, y):
    SIZE = field.shape[0]

    # wrap FIRST → dann floor!
    x = x % SIZE
    y = y % SIZE

    x0 = int(np.floor(x))
    y0 = int(np.floor(y))
    x1 = (x0 + 1) % SIZE
    y1 = (y0 + 1) % SIZE

    dx = x - x0
    dy = y - y0

    val = (
        field[x0, y0] * (1 - dx) * (1 - dy) +
        field[x1, y0] * dx * (1 - dy) +
        field[x0, y1] * (1 - dx) * dy +
        field[x1, y1] * dx * dy
    )

    return val

# --------------------------------------------------
# GRADIENT
# --------------------------------------------------

def compute_gradient(field, x, y):
    eps = 1.0

    fx1 = sample_field(field, x + eps, y)
    fx2 = sample_field(field, x - eps, y)
    fy1 = sample_field(field, x, y + eps)
    fy2 = sample_field(field, x, y - eps)

    gx = (fx1 - fx2) / (2 * eps)
    gy = (fy1 - fy2) / (2 * eps)

    return np.array([gx, gy])

# --------------------------------------------------
# FIND TARGET
# --------------------------------------------------

def find_target(field):
    idx = np.argmax(field)
    SIZE = field.shape[0]
    return np.array([idx // SIZE, idx % SIZE], dtype=float)

# --------------------------------------------------
# AGENT (HYBRID)
# --------------------------------------------------

def run_agent(field, memory, target):

    SIZE = field.shape[0]

    pos = np.array([
        np.random.uniform(0, SIZE),
        np.random.uniform(0, SIZE)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]

    for _ in range(STEPS):

        grad_field = compute_gradient(field, pos[0], pos[1])
        grad_memory = compute_gradient(memory, pos[0], pos[1])

        # target vector
        target_vec = target - pos
        target_vec = target_vec / (np.linalg.norm(target_vec) + 1e-6)

        # normalize gradients
        grad_field /= (np.linalg.norm(grad_field) + 1e-6)
        grad_memory /= (np.linalg.norm(grad_memory) + 1e-6)

        # combined direction
        direction = (
            ALPHA_FIELD * grad_field +
            BETA_TARGET * target_vec +
            GAMMA_MEMORY * grad_memory
        )

        direction /= (np.linalg.norm(direction) + 1e-6)

        # update velocity
        vel = DAMPING * vel + STEP_SIZE * direction

        # noise
        vel += NOISE * np.random.randn(2)

        # move
        pos = pos + vel
        pos = pos % SIZE  # torus

        path.append(pos.copy())

    return np.array(path)

# --------------------------------------------------
# MEMORY UPDATE
# --------------------------------------------------

def update_memory(memory, paths):
    SIZE = memory.shape[0]

    new_memory = np.zeros_like(memory)

    for path in paths:
        for p in path:
            x = int(p[0]) % SIZE
            y = int(p[1]) % SIZE
            new_memory[x, y] += 1

    new_memory = new_memory / (np.max(new_memory) + 1e-6)

    memory = MEMORY_DECAY * memory + FEEDBACK_GAIN * new_memory
    memory = memory / (np.max(memory) + 1e-6)

    return memory

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def run_simulation(iterations=5):

    base_field = generate_stability_landscape()
    field = base_field.copy()
    memory = np.zeros_like(field)

    history = []
    all_paths = []

    for it in range(iterations):

        target = find_target(field)

        paths = []
        for _ in range(N_AGENTS):
            p = run_agent(field, memory, target)
            paths.append(p)

        memory = update_memory(memory, paths)

        # field update
        field = FIELD_DECAY * field + FEEDBACK_GAIN * memory
        field = field / (np.max(field) + 1e-6)

        history.append((field.copy(), memory.copy()))
        all_paths.append(paths)

        print(f"Iteration {it+1} done")

    return base_field, history, all_paths

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, history, paths_all):

    final_field, final_memory = history[-1]
    final_paths = paths_all[-1]

    plt.figure(figsize=(15,5))

    plt.subplot(1,3,1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    plt.subplot(1,3,2)
    plt.title("Hybrid Navigation Field")
    plt.imshow(final_field, origin="lower")

    for path in final_paths[:80]:
        plt.plot(path[:,0], path[:,1], alpha=0.2)

    plt.axis("off")

    plt.subplot(1,3,3)
    plt.title("Memory Field (Y)")
    plt.imshow(final_memory, origin="lower")
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "level11_hybrid.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":

    base, history, paths = run_simulation(iterations=5)
    plot_results(base, history, paths)

    final_field, final_memory = history[-1]

    config = {
        "N_AGENTS": N_AGENTS,
        "STEPS": STEPS,
        "STEP_SIZE": STEP_SIZE,
        "NOISE": NOISE,
        "DAMPING": DAMPING,
        "ALPHA_FIELD": ALPHA_FIELD,
        "BETA_TARGET": BETA_TARGET,
        "GAMMA_MEMORY": GAMMA_MEMORY
    }

    metrics = compute_metrics(final_field, final_memory)

    save_run(config, metrics)

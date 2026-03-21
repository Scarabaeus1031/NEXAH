import numpy as np
import matplotlib.pyplot as plt
import os

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

SWITCH_PROB = 0.02   # Zielwechsel

FIELD_DECAY = 0.985
MEMORY_DECAY = 0.992
FEEDBACK_GAIN = 0.22

SAVE_DIR = "ENGINE/visuals/navigation_level12"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD SAMPLING (SAFE)
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
# FIND MULTIPLE TARGETS
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
# AGENT (DECISION!)
# --------------------------------------------------

def run_agent(field, memory, targets):

    SIZE = field.shape[0]

    pos = np.array([
        np.random.uniform(0, SIZE),
        np.random.uniform(0, SIZE)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]

    # initial target
    current_target = targets[np.random.randint(len(targets))]

    for _ in range(STEPS):

        # occasional target switch
        if np.random.rand() < SWITCH_PROB:
            current_target = targets[np.random.randint(len(targets))]

        grad_field = compute_gradient(field, pos[0], pos[1])
        grad_memory = compute_gradient(memory, pos[0], pos[1])

        # target direction
        target_vec = current_target - pos
        target_vec /= (np.linalg.norm(target_vec) + 1e-6)

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

        # velocity update
        vel = DAMPING * vel + STEP_SIZE * direction
        vel += NOISE * np.random.randn(2)

        pos = (pos + vel) % SIZE

        path.append(pos.copy())

    return np.array(path)

# --------------------------------------------------
# MEMORY UPDATE
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
# SIMULATION
# --------------------------------------------------

def run_simulation(iterations=5):

    base = generate_stability_landscape()
    field = base.copy()
    memory = np.zeros_like(field)

    history = []
    all_paths = []

    for it in range(iterations):

        targets = find_targets(field, k=3)

        paths = []
        for _ in range(N_AGENTS):
            p = run_agent(field, memory, targets)
            paths.append(p)

        memory = update_memory(memory, paths)

        field = FIELD_DECAY * field + FEEDBACK_GAIN * memory
        field /= (np.max(field) + 1e-6)

        history.append((field.copy(), memory.copy(), targets))
        all_paths.append(paths)

        print(f"Iteration {it+1} done")

    return base, history, all_paths

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, history, paths_all):

    field, memory, targets = history[-1]
    paths = paths_all[-1]

    plt.figure(figsize=(15,5))

    # base
    plt.subplot(1,3,1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    # navigation
    plt.subplot(1,3,2)
    plt.title("Decision Navigation Field")
    plt.imshow(field, origin="lower")

    for path in paths[:80]:
        plt.plot(path[:,0], path[:,1], alpha=0.2)

    # plot targets
    for i, t in enumerate(targets):
        plt.scatter(t[0], t[1], s=120, label=f"T{i}")

    plt.legend()
    plt.axis("off")

    # memory
    plt.subplot(1,3,3)
    plt.title("Memory Field")
    plt.imshow(memory, origin="lower")
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "level12_decision.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    base, history, paths = run_simulation(iterations=5)
    plot_results(base, history, paths)

import numpy as np
import matplotlib.pyplot as plt
import os

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
GAMMA_MEMORY = 0.75  # Memory / gelernte Route

FIELD_DECAY = 0.985
MEMORY_DECAY = 0.992
FEEDBACK_GAIN = 0.22

SAVE_DIR = "ENGINE/visuals/navigation_hybrid"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD INTERPOLATION (TORUS SAFE)
# --------------------------------------------------

def sample_field(field, x, y):
    size = field.shape[0]

    x = x % size
    y = y % size

    x0 = int(np.floor(x))
    y0 = int(np.floor(y))

    x1 = (x0 + 1) % size
    y1 = (y0 + 1) % size

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

    gx = (fx1 - fx2) / (2 * eps)
    gy = (fy1 - fy2) / (2 * eps)

    return np.array([gx, gy])

# --------------------------------------------------
# MEMORY FIELD (Y)
# --------------------------------------------------

def compute_memory(paths, size):
    memory = np.zeros((size, size))

    for path in paths:
        for p in path:
            x = int(p[0]) % size
            y = int(p[1]) % size
            memory[x, y] += 1

    memory /= (np.max(memory) + 1e-6)
    return memory

# --------------------------------------------------
# TARGET (X)
# --------------------------------------------------

def find_target(field):
    idx = np.argmax(field)
    size = field.shape[0]
    return np.array([idx // size, idx % size])

# --------------------------------------------------
# AGENT (HYBRID NAVIGATION)
# --------------------------------------------------

def run_agent(field, memory, target):

    size = field.shape[0]

    pos = np.array([
        np.random.uniform(0, size),
        np.random.uniform(0, size)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]

    for _ in range(STEPS):

        grad = compute_gradient(field, pos[0], pos[1])
        grad_norm = np.linalg.norm(grad) + 1e-6
        grad = grad / grad_norm

        mem_grad = compute_gradient(memory, pos[0], pos[1])
        mem_norm = np.linalg.norm(mem_grad) + 1e-6
        mem_grad = mem_grad / mem_norm

        target_vec = target - pos
        target_vec = target_vec / (np.linalg.norm(target_vec) + 1e-6)

        direction = (
            ALPHA_FIELD * grad +
            BETA_TARGET * target_vec +
            GAMMA_MEMORY * mem_grad
        )

        direction = direction / (np.linalg.norm(direction) + 1e-6)

        vel = DAMPING * vel + STEP_SIZE * direction
        vel += NOISE * np.random.randn(2)

        pos = pos + vel
        pos = pos % size

        path.append(pos.copy())

    return np.array(path)

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def run_simulation(iterations=5):

    base_field = generate_stability_landscape()
    size = base_field.shape[0]

    field = base_field.copy()
    memory = np.zeros_like(field)

    history = []
    memory_history = []
    all_paths = []

    for it in range(iterations):

        target = find_target(field)

        paths = []
        for _ in range(N_AGENTS):
            p = run_agent(field, memory, target)
            paths.append(p)

        response = compute_memory(paths, size)

        # Update field + memory
        field = FIELD_DECAY * field + FEEDBACK_GAIN * response
        field /= (np.max(field) + 1e-6)

        memory = MEMORY_DECAY * memory + response
        memory /= (np.max(memory) + 1e-6)

        history.append(field.copy())
        memory_history.append(memory.copy())
        all_paths.append(paths)

        print(f"Iteration {it+1} done")

    return base_field, history, memory_history, all_paths

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, history, memory_history, paths_all):

    final_field = history[-1]
    final_memory = memory_history[-1]
    final_paths = paths_all[-1]

    plt.figure(figsize=(15,5))

    # Base
    plt.subplot(1,3,1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    # Learned field
    plt.subplot(1,3,2)
    plt.title("Hybrid Navigation Field")
    plt.imshow(final_field, origin="lower")

    for path in final_paths[:60]:
        plt.plot(path[:,0], path[:,1], alpha=0.15)

    plt.axis("off")

    # Memory field
    plt.subplot(1,3,3)
    plt.title("Memory Field (Y)")
    plt.imshow(final_memory, origin="lower")
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "navigation_hybrid.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    base, history, memory, paths = run_simulation(iterations=6)
    plot_results(base, history, memory, paths)

import numpy as np
import matplotlib.pyplot as plt
import os

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

N_AGENTS = 120
STEPS = 220

STEP_SIZE = 0.6
NOISE = 0.08
DAMPING = 0.95

SAVE_DIR = "ENGINE/visuals/navigation_continuous"
os.makedirs(SAVE_DIR, exist_ok=True)

# --------------------------------------------------
# FIELD INTERPOLATION
# --------------------------------------------------

def sample_field(field, x, y):
    """Bilinear interpolation with correct dimensions"""

    H, W = field.shape  # 🔥 wichtig!

    x0 = int(np.floor(x)) % H
    y0 = int(np.floor(y)) % W
    x1 = (x0 + 1) % H
    y1 = (y0 + 1) % W

    dx = x - np.floor(x)
    dy = y - np.floor(y)

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
# AGENT
# --------------------------------------------------

def run_agent(field):

    H, W = field.shape

    pos = np.array([
        np.random.uniform(0, H),
        np.random.uniform(0, W)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]

    for _ in range(STEPS):

        grad = compute_gradient(field, pos[0], pos[1])

        norm = np.linalg.norm(grad) + 1e-6
        grad = grad / norm

        vel = DAMPING * vel + STEP_SIZE * grad
        vel += NOISE * np.random.randn(2)

        pos = pos + vel

        # torus wrap (korrekt für beide Achsen)
        pos[0] = pos[0] % H
        pos[1] = pos[1] % W

        path.append(pos.copy())

    return np.array(path)

# --------------------------------------------------
# FIELD RESPONSE
# --------------------------------------------------

def compute_response(paths, field_shape):

    H, W = field_shape
    response = np.zeros((H, W))

    for path in paths:
        for p in path:
            x = int(p[0]) % H
            y = int(p[1]) % W
            response[x, y] += 1

    response = response / (np.max(response) + 1e-6)
    return response

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def run_simulation(iterations=4):

    base_field = generate_stability_landscape()
    field = base_field.copy()

    history = []
    all_paths = []

    for it in range(iterations):

        paths = []

        for _ in range(N_AGENTS):
            p = run_agent(field)
            paths.append(p)

        response = compute_response(paths, field.shape)

        field = 0.97 * field + 0.3 * response
        field = field / (np.max(field) + 1e-6)

        history.append(field.copy())
        all_paths.append(paths)

        print(f"Iteration {it+1} done")

    return base_field, history, all_paths

# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def plot_results(base, history, paths_all):

    final_field = history[-1]
    final_paths = paths_all[-1]

    plt.figure(figsize=(10,5))

    plt.subplot(1,2,1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    plt.subplot(1,2,2)
    plt.title("Continuous Navigation Field")
    plt.imshow(final_field, origin="lower")

    for path in final_paths[:80]:
        plt.plot(path[:,0], path[:,1], alpha=0.2)

    plt.axis("off")

    path = os.path.join(SAVE_DIR, "continuous_navigation.png")
    plt.savefig(path, dpi=200)
    print(f"\nSaved → {path}")

    plt.show()

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    base, history, paths = run_simulation(iterations=5)
    plot_results(base, history, paths)

import numpy as np
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

N_AGENTS = 140
STEPS = 240

STEP_SIZE = 0.45
NOISE = 0.05
DAMPING = 0.92

ALPHA_FIELD = 0.6
BETA_TARGET = 1.2

SAVE_DIR = "ENGINE/visuals/navigation_level14"
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
        field[x0, y0]*(1-dx)*(1-dy) +
        field[x1, y0]*dx*(1-dy) +
        field[x0, y1]*(1-dx)*dy +
        field[x1, y1]*dx*dy
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
    h, w = field.shape

    targets = []
    for idx in flat:
        x = idx // w
        y = idx % w
        p = np.array([x, y], dtype=float)

        if all(np.linalg.norm(p - t) > 6 for t in targets):
            targets.append(p)

        if len(targets) >= k:
            break

    return targets

# --------------------------------------------------
# AGENT
# --------------------------------------------------

def run_agent(field, targets, reverse=False):
    h, w = field.shape

    pos = np.array([
        np.random.uniform(0, h),
        np.random.uniform(0, w)
    ])

    vel = np.zeros(2)
    path = [pos.copy()]
    target = targets[np.random.randint(len(targets))]

    for _ in range(STEPS):

        grad = compute_gradient(field, pos[0], pos[1])
        grad /= (np.linalg.norm(grad) + 1e-9)

        target_vec = target - pos
        target_vec /= (np.linalg.norm(target_vec) + 1e-9)

        direction = ALPHA_FIELD * grad + BETA_TARGET * target_vec
        direction /= (np.linalg.norm(direction) + 1e-9)

        if reverse:
            direction = -direction

        vel = DAMPING * vel + STEP_SIZE * direction
        vel += NOISE * np.random.randn(2)

        pos = (pos + vel) % h
        path.append(pos.copy())

    return np.array(path)

# --------------------------------------------------
# MAPS
# --------------------------------------------------

def density_map(paths, shape):
    h, w = shape
    m = np.zeros((h, w))

    for path in paths:
        for p in path:
            x = int(p[0]) % h
            y = int(p[1]) % w
            m[x, y] += 1

    return m / (np.max(m) + 1e-9)

def endpoint_map(paths, shape):
    h, w = shape
    m = np.zeros((h, w))

    for path in paths:
        x = int(path[-1,0]) % h
        y = int(path[-1,1]) % w
        m[x, y] += 1

    return m / (np.max(m) + 1e-9)

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def run():

    base = generate_stability_landscape()
    base /= (np.max(base) + 1e-9)

    targets = find_targets(base)

    forward = [run_agent(base, targets, False) for _ in range(N_AGENTS)]
    backward = [run_agent(base, targets, True) for _ in range(N_AGENTS)]

    f_visit = density_map(forward, base.shape)
    b_visit = density_map(backward, base.shape)

    f_end = endpoint_map(forward, base.shape)
    b_end = endpoint_map(backward, base.shape)

    # ASYMMETRY
    asym_visit = np.abs(f_visit - b_visit)
    asym_end = np.abs(f_end - b_end)

    core = asym_visit + 0.8 * asym_end
    core /= (np.max(core) + 1e-9)

    # --------------------------------------------------
    # VISUAL
    # --------------------------------------------------

    plt.figure(figsize=(14,8))

    plt.subplot(2,2,1)
    plt.title("Base Field")
    plt.imshow(base, origin="lower")
    plt.axis("off")

    plt.subplot(2,2,2)
    plt.title("Visit Asymmetry")
    plt.imshow(asym_visit, origin="lower", cmap="inferno")
    plt.axis("off")

    plt.subplot(2,2,3)
    plt.title("Endpoint Asymmetry")
    plt.imshow(asym_end, origin="lower", cmap="inferno")
    plt.axis("off")

    plt.subplot(2,2,4)
    plt.title("TIME CORE")
    plt.imshow(core, origin="lower", cmap="magma")
    plt.axis("off")

    path = os.path.join(SAVE_DIR, "level14_core.png")
    plt.savefig(path, dpi=220)
    print(f"Saved → {path}")

    plt.show()

    # --------------------------------------------------
    # LOG
    # --------------------------------------------------

    metrics = {
        "visit_asymmetry": float(np.mean(asym_visit)),
        "endpoint_asymmetry": float(np.mean(asym_end))
    }

    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    with open(os.path.join(LOG_DIR, f"{run_id}_lvl14.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print("Saved log")

# --------------------------------------------------

if __name__ == "__main__":
    run()

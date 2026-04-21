# ENGINE/analysis/navigation_level50_persistent_return_field.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

try:
    from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape
    HAS_EXTERNAL_FIELD = True
except Exception:
    HAS_EXTERNAL_FIELD = False


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80

N_PARTICLES = 120
STEPS = 800

STEP_SIZE = 0.20
DRIFT_STRENGTH = 0.035
ROTATION_STRENGTH = 0.34
RETURN_STRENGTH = 0.11
MEMORY_DECAY = 0.996

SMOOTH_SIGMA = 1.2
DENSITY_SMOOTH = 1.2

OUTPUT_DIR = "ENGINE/visuals"


# --------------------------------------------------
# FIELD
# --------------------------------------------------

def build_field():
    if HAS_EXTERNAL_FIELD:
        field = generate_stability_landscape(size=SIZE)
    else:
        x = np.linspace(0, SIZE - 1, SIZE)
        y = np.linspace(0, SIZE - 1, SIZE)
        X, Y = np.meshgrid(x, y)

        g1 = np.exp(-((X - 25)**2 + (Y - 30)**2) / 200)
        g2 = np.exp(-((X - 55)**2 + (Y - 60)**2) / 220)

        field = g1 + g2

    field = gaussian_filter(field, sigma=SMOOTH_SIGMA)
    field /= np.max(field) + 1e-6

    return field


# --------------------------------------------------
# GRADIENT
# --------------------------------------------------

def compute_gradient(field):
    gy, gx = np.gradient(field)
    return gx, gy


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def simulate(field):

    gx, gy = compute_gradient(field)

    particles = np.random.rand(N_PARTICLES, 2) * SIZE

    memory = np.zeros((SIZE, SIZE))
    density = np.zeros((SIZE, SIZE))

    for step in range(STEPS):

        new_particles = []

        for (x, y) in particles:

            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            fx = gx[iy, ix]
            fy = gy[iy, ix]

            # Rotation
            rx = -fy
            ry = fx

            # Drift
            dx = DRIFT_STRENGTH
            dy = DRIFT_STRENGTH * 0.5

            # Memory Return
            m = memory[iy, ix]

            vx = (
                STEP_SIZE * fx
                + ROTATION_STRENGTH * rx
                + dx
                + RETURN_STRENGTH * m
            )

            vy = (
                STEP_SIZE * fy
                + ROTATION_STRENGTH * ry
                + dy
                + RETURN_STRENGTH * m
            )

            nx = (x + vx) % SIZE
            ny = (y + vy) % SIZE

            new_particles.append((nx, ny))

            ix2 = int(nx)
            iy2 = int(ny)

            density[iy2, ix2] += 1.0
            memory[iy2, ix2] += 1.0

        particles = np.array(new_particles)

        memory *= MEMORY_DECAY

    density = gaussian_filter(density, sigma=DENSITY_SMOOTH)
    density /= np.max(density) + 1e-6

    return density


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def save_output(field, density):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # 👉 richtiger Zielordner wie bei deinen anderen Levels
    run_dir = os.path.join(OUTPUT_DIR, f"level50_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    # IMAGE
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].set_title("Field")
    axs[0].imshow(field, cmap="viridis")

    axs[1].set_title("Persistent Torus (Level 50)")
    axs[1].imshow(density, cmap="viridis")

    for ax in axs:
        ax.axis("off")

    img_path = os.path.join(run_dir, "persistent_return_field.png")
    plt.savefig(img_path, dpi=150)
    plt.close()

    # JSON
    data = {
        "num_particles": int(N_PARTICLES),
        "steps": int(STEPS),
        "config": {
            "step_size": STEP_SIZE,
            "drift": DRIFT_STRENGTH,
            "rotation": ROTATION_STRENGTH,
            "return": RETURN_STRENGTH,
            "memory_decay": MEMORY_DECAY
        }
    }

    json_path = os.path.join(run_dir, "persistent_return_field.json")

    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)

    print("Saved:", img_path)
    print("Saved:", json_path)

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    field = build_field()
    density = simulate(field)

    save_output(field, density)


if __name__ == "__main__":
    main()

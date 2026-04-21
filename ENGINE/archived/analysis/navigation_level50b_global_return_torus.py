# ENGINE/analysis/navigation_level50b_global_return_torus.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80

N_PARTICLES = 120
STEPS = 800

STEP_SIZE = 0.18
ROTATION_STRENGTH = 0.42
RETURN_STRENGTH = 0.18
DRIFT_STRENGTH = 0.0   # ❗ bewusst aus → kein shear mehr

SMOOTH_SIGMA = 1.2
DENSITY_SMOOTH = 1.3

OUTPUT_DIR = "ENGINE/visuals"


# --------------------------------------------------
# FIELD
# --------------------------------------------------

def build_field():
    x = np.linspace(0, SIZE - 1, SIZE)
    y = np.linspace(0, SIZE - 1, SIZE)
    X, Y = np.meshgrid(x, y)

    g1 = np.exp(-((X - 30)**2 + (Y - 35)**2) / 180)
    g2 = np.exp(-((X - 55)**2 + (Y - 60)**2) / 200)

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
# GLOBAL CENTER (🔥 entscheidend)
# --------------------------------------------------

def compute_center(density):
    total = np.sum(density)

    if total < 1e-6:
        return SIZE / 2, SIZE / 2

    y_idx, x_idx = np.indices(density.shape)

    cx = np.sum(x_idx * density) / total
    cy = np.sum(y_idx * density) / total

    return cx, cy


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def simulate(field):

    gx, gy = compute_gradient(field)

    particles = np.random.rand(N_PARTICLES, 2) * SIZE
    density = np.zeros((SIZE, SIZE))

    for step in range(STEPS):

        cx, cy = compute_center(density)

        new_particles = []

        for (x, y) in particles:

            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            # FIELD
            fx = gx[iy, ix]
            fy = gy[iy, ix]

            # ROTATION
            rx = -fy
            ry = fx

            # ------------------------------------------
            # GLOBAL RETURN (🔥 DER FIX)
            # ------------------------------------------
            dx = x - cx
            dy = y - cy

            ret_x = -RETURN_STRENGTH * dx
            ret_y = -RETURN_STRENGTH * dy

            # ------------------------------------------
            # COMBINE
            # ------------------------------------------
            vx = STEP_SIZE * fx + ROTATION_STRENGTH * rx + ret_x
            vy = STEP_SIZE * fy + ROTATION_STRENGTH * ry + ret_y

            nx = (x + vx) % SIZE
            ny = (y + vy) % SIZE

            new_particles.append((nx, ny))

            ix2 = int(nx)
            iy2 = int(ny)

            density[iy2, ix2] += 1.0

        particles = np.array(new_particles)

    density = gaussian_filter(density, sigma=DENSITY_SMOOTH)
    density /= np.max(density) + 1e-6

    return density


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def save_output(field, density):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    run_dir = os.path.join(OUTPUT_DIR, f"level50b_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].set_title("Field")
    axs[0].imshow(field, cmap="viridis")

    axs[1].set_title("Global Return Torus (Level 50b)")
    axs[1].imshow(density, cmap="viridis")

    for ax in axs:
        ax.axis("off")

    img_path = os.path.join(run_dir, "global_return_torus.png")
    plt.savefig(img_path, dpi=150)
    plt.close()

    data = {
        "num_particles": N_PARTICLES,
        "steps": STEPS,
        "config": {
            "rotation": ROTATION_STRENGTH,
            "return": RETURN_STRENGTH,
            "step": STEP_SIZE
        }
    }

    json_path = os.path.join(run_dir, "global_return_torus.json")

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

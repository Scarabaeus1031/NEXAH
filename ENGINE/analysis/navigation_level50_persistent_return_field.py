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

        # zwei Gauss-Hügel → wie deine bisherigen Felder
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
    velocities = np.zeros_like(particles)

    # 🔥 MEMORY FIELD
    memory = np.zeros((SIZE, SIZE))

    density = np.zeros((SIZE, SIZE))

    for step in range(STEPS):

        new_particles = []

        for i, (x, y) in enumerate(particles):

            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            # ------------------------------------------
            # FIELD FORCE
            # ------------------------------------------
            fx = gx[iy, ix]
            fy = gy[iy, ix]

            # ------------------------------------------
            # ROTATION (orthogonal)
            # ------------------------------------------
            rx = -fy
            ry = fx

            # ------------------------------------------
            # DRIFT (global bias)
            # ------------------------------------------
            dx = DRIFT_STRENGTH
            dy = DRIFT_STRENGTH * 0.5

            # ------------------------------------------
            # RETURN FIELD (Memory Attraction)
            # ------------------------------------------
            mx = 0.0
            my = 0.0

            if memory.sum() > 0:
                mx = memory[iy, ix]
                my = memory[iy, ix]

            # ------------------------------------------
            # COMBINE FORCES
            # ------------------------------------------
            vx = (
                STEP_SIZE * fx
                + ROTATION_STRENGTH * rx
                + dx
                + RETURN_STRENGTH * mx
            )

            vy = (
                STEP_SIZE * fy
                + ROTATION_STRENGTH * ry
                + dy
                + RETURN_STRENGTH * my
            )

            # ------------------------------------------
            # UPDATE POSITION
            # ------------------------------------------
            nx = (x + vx) % SIZE
            ny = (y + vy) % SIZE

            new_particles.append((nx, ny))

            # ------------------------------------------
            # WRITE TO DENSITY
            # ------------------------------------------
            ix2 = int(nx)
            iy2 = int(ny)

            density[iy2, ix2] += 1.0

            # ------------------------------------------
            # UPDATE MEMORY
            # ------------------------------------------
            memory[iy2, ix2] += 1.0

        particles = np.array(new_particles)

        # ------------------------------------------
        # DECAY MEMORY
        # ------------------------------------------
        memory *= MEMORY_DECAY

    density = gaussian_filter(density, sigma=DENSITY_SMOOTH)
    density /= np.max(density) + 1e-6

    return density


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def save_output(field, density):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    os.makedirs("ENGINE/output", exist_ok=True)

    # IMAGE
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].set_title("Field")
    axs[0].imshow(field, cmap="viridis")

    axs[1].set_title("Persistent Torus (Level 50)")
    axs[1].imshow(density, cmap="viridis")

    for ax in axs:
        ax.axis("off")

    img_path = f"ENGINE/output/level50_{timestamp}.png"
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

    json_path = f"ENGINE/output/level50_{timestamp}.json"

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

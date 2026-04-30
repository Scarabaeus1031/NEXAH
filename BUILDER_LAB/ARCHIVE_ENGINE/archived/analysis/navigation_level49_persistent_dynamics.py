# ENGINE/analysis/navigation_level49_persistent_dynamics.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape


# --------------------------------------------------
# CONFIG
# --------------------------------------------------

SIZE = 80

N_PARTICLES = 120
STEPS = 600

STEP_SIZE = 0.35
DRIFT_STRENGTH = 0.12
ROTATION_STRENGTH = 0.25

SMOOTH_SIGMA = 1.2


# --------------------------------------------------
# FIELD
# --------------------------------------------------

def build_field():
    field = generate_stability_landscape(size=SIZE)
    field = gaussian_filter(field, sigma=SMOOTH_SIGMA)
    return field


# --------------------------------------------------
# PARTICLE SYSTEM
# --------------------------------------------------

def run_particles(field):

    gx, gy = np.gradient(field)

    particles = np.random.rand(N_PARTICLES, 2) * SIZE

    trajectories = []

    for p in particles:

        path = []

        x, y = p

        for t in range(STEPS):

            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            dx = gx[iy, ix]
            dy = gy[iy, ix]

            # --------------------------------------------------
            # ROTATION (Torus-Komponente)
            # --------------------------------------------------

            rx = -dy
            ry = dx

            # --------------------------------------------------
            # DRIFT (wichtig!)
            # --------------------------------------------------

            drift_x = DRIFT_STRENGTH * np.sin(0.05 * t + x * 0.1)
            drift_y = DRIFT_STRENGTH * np.cos(0.05 * t + y * 0.1)

            # --------------------------------------------------
            # UPDATE
            # --------------------------------------------------

            x += STEP_SIZE * (dx + ROTATION_STRENGTH * rx) + drift_x
            y += STEP_SIZE * (dy + ROTATION_STRENGTH * ry) + drift_y

            # Wrap → Torus Topologie
            x %= SIZE
            y %= SIZE

            path.append((x, y))

        trajectories.append(path)

    return trajectories


# --------------------------------------------------
# DENSITY MAP
# --------------------------------------------------

def build_density(trajectories):

    density = np.zeros((SIZE, SIZE))

    for path in trajectories:
        for (x, y) in path:
            ix = int(x)
            iy = int(y)
            density[iy, ix] += 1

    density = gaussian_filter(density, sigma=1.2)

    max_val = np.max(density)
    if max_val > 0:
        density /= max_val

    return density


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def run():

    field = build_field()

    trajectories = run_particles(field)

    density = build_density(trajectories)

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    out_dir = "ENGINE/analysis/output_level49"
    os.makedirs(out_dir, exist_ok=True)

    # save trajectories (optional)
    with open(f"{out_dir}/trajectories_{ts}.json", "w") as f:
        json.dump({
            "num_particles": len(trajectories),
            "steps": STEPS
        }, f, indent=2)

    # --------------------------------------------------
    # VISUAL
    # --------------------------------------------------

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(field)
    axs[0].set_title("Field")

    axs[1].imshow(density)
    axs[1].set_title("Persistent Torus (Level 49)")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/persistent_{ts}.png")
    plt.close()

    print("Done. Trajectories:", len(trajectories))


if __name__ == "__main__":
    run()

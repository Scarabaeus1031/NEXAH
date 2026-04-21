# ENGINE/analysis/navigation_level49c_persistent_torus_refined.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter

# optional import (falls vorhanden)
try:
    from ENGINE.analysis.stability_landscape_generator import generate_stability_landscape
    HAS_EXTERNAL_FIELD = True
except:
    HAS_EXTERNAL_FIELD = False


# --------------------------------------------------
# CONFIG (REFINED SWEET SPOT)
# --------------------------------------------------

SIZE = 80

N_PARTICLES = 120
STEPS = 600

STEP_SIZE = 0.22
DRIFT_STRENGTH = 0.045
ROTATION_STRENGTH = 0.38

SMOOTH_SIGMA = 1.2


# --------------------------------------------------
# FIELD
# --------------------------------------------------

def build_field():

    if HAS_EXTERNAL_FIELD:
        field = generate_stability_landscape(size=SIZE)
    else:
        # stabiler Fallback (2 gekoppelte Attraktoren)
        x = np.linspace(0, SIZE-1, SIZE)
        y = np.linspace(0, SIZE-1, SIZE)
        X, Y = np.meshgrid(x, y)

        cx1, cy1 = SIZE * 0.35, SIZE * 0.35
        cx2, cy2 = SIZE * 0.65, SIZE * 0.65

        field = (
            np.exp(-((X-cx1)**2 + (Y-cy1)**2) / 180)
            + 0.8 * np.exp(-((X-cx2)**2 + (Y-cy2)**2) / 200)
        )

    field = gaussian_filter(field, sigma=SMOOTH_SIGMA)

    field -= field.min()
    field /= (field.max() + 1e-8)

    return field


# --------------------------------------------------
# PARTICLES
# --------------------------------------------------

def run_particles(field):

    gy, gx = np.gradient(field)

    particles = np.random.rand(N_PARTICLES, 2) * SIZE

    trajectories = []

    for p in particles:

        x, y = p
        path = []

        for t in range(STEPS):

            ix = int(np.clip(x, 0, SIZE-1))
            iy = int(np.clip(y, 0, SIZE-1))

            dx = gx[iy, ix]
            dy = gy[iy, ix]

            # Rotation → Ringbildung
            rx = -dy
            ry = dx

            # Drift → verhindert Wiederholung
            drift_x = DRIFT_STRENGTH * np.sin(0.05 * t + x * 0.1)
            drift_y = DRIFT_STRENGTH * np.cos(0.05 * t + y * 0.1)

            # Update
            x += STEP_SIZE * (dx + ROTATION_STRENGTH * rx) + drift_x
            y += STEP_SIZE * (dy + ROTATION_STRENGTH * ry) + drift_y

            # Torus-Wrap
            x %= SIZE
            y %= SIZE

            path.append((x, y))

        trajectories.append(path)

    return trajectories


# --------------------------------------------------
# DENSITY
# --------------------------------------------------

def build_density(trajectories):

    density = np.zeros((SIZE, SIZE))

    for path in trajectories:
        for (x, y) in path:
            ix = int(x)
            iy = int(y)
            density[iy, ix] += 1

    density = gaussian_filter(density, sigma=1.2)

    if np.max(density) > 0:
        density /= np.max(density)

    return density


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def run():

    field = build_field()
    trajectories = run_particles(field)
    density = build_density(trajectories)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    out_dir = "ENGINE/analysis/output_level49c"
    os.makedirs(out_dir, exist_ok=True)

    # Save config + meta
    with open(f"{out_dir}/meta_{ts}.json", "w") as f:
        json.dump({
            "num_particles": N_PARTICLES,
            "steps": STEPS,
            "config": {
                "step": STEP_SIZE,
                "drift": DRIFT_STRENGTH,
                "rotation": ROTATION_STRENGTH
            }
        }, f, indent=2)

    # Plot
    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].imshow(field)
    axs[0].set_title("Field")

    axs[1].imshow(density)
    axs[1].set_title("Persistent Torus (Level 49c Refined)")

    plt.tight_layout()
    plt.savefig(f"{out_dir}/persistent_{ts}.png")
    plt.close()

    print("DONE:", ts)


if __name__ == "__main__":
    run()

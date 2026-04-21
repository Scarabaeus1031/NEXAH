# ENGINE/analysis/navigation_level53_resonant_split_bridge.py

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

N_PARTICLES = 140
STEPS = 1000

STEP_SIZE = 0.18
ROTATION_STRENGTH = 0.38
RETURN_STRENGTH = 0.14
SPLIT_STRENGTH = 0.22
REJOIN_STRENGTH = 0.18

PENTAGON_BIAS = 5
ANGLE_OFFSET = 0.0

MEMORY_DECAY = 0.995
DENSITY_SMOOTH = 1.2
FIELD_SMOOTH = 1.2

OUTPUT_DIR = "ENGINE/visuals"


# --------------------------------------------------
# FIELD
# --------------------------------------------------

def build_field():
    x = np.linspace(0, SIZE - 1, SIZE)
    y = np.linspace(0, SIZE - 1, SIZE)
    X, Y = np.meshgrid(x, y)

    g1 = np.exp(-((X - 25)**2 + (Y - 30)**2) / 180)
    g2 = np.exp(-((X - 55)**2 + (Y - 60)**2) / 200)

    field = g1 + g2
    field = gaussian_filter(field, sigma=FIELD_SMOOTH)
    field /= np.max(field) + 1e-6

    return field


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def quantize_angle(theta):
    sector = 2 * np.pi / PENTAGON_BIAS
    return np.round(theta / sector) * sector


def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def simulate(field):

    gy, gx = np.gradient(field)

    particles = np.random.rand(N_PARTICLES, 2) * SIZE

    memory = np.zeros((SIZE, SIZE))
    density = np.zeros((SIZE, SIZE))

    cx, cy = SIZE / 2, SIZE / 2

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

            # Center vector
            dx = x - cx
            dy = y - cy

            r = np.sqrt(dx**2 + dy**2) + 1e-6
            theta = np.arctan2(dy, dx)

            # Pentagon Split
            theta_q = quantize_angle(theta + ANGLE_OFFSET)
            phase_error = wrap_angle(theta_q - theta)

            tx = -np.sin(theta)
            ty = np.cos(theta)

            split_force = SPLIT_STRENGTH * phase_error * np.array([tx, ty])

            # Rejoin (center attraction)
            rejoin_force = -REJOIN_STRENGTH * np.array([dx, dy]) / r

            # Memory
            m = memory[iy, ix]

            # Combine
            vx = (
                STEP_SIZE * fx +
                ROTATION_STRENGTH * rx +
                split_force[0] +
                rejoin_force[0] +
                RETURN_STRENGTH * m
            )

            vy = (
                STEP_SIZE * fy +
                ROTATION_STRENGTH * ry +
                split_force[1] +
                rejoin_force[1] +
                RETURN_STRENGTH * m
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

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].set_title("Field")
    axs[0].imshow(field, cmap="viridis")

    axs[1].set_title("Resonant Split Bridge (Level 53)")
    axs[1].imshow(density, cmap="inferno")

    for ax in axs:
        ax.axis("off")

    img_path = os.path.join(OUTPUT_DIR, f"level53_{timestamp}.png")
    plt.savefig(img_path, dpi=150)
    plt.close()

    data = {
        "num_particles": int(N_PARTICLES),
        "steps": int(STEPS),
        "config": {
            "step_size": STEP_SIZE,
            "rotation": ROTATION_STRENGTH,
            "return": RETURN_STRENGTH,
            "split": SPLIT_STRENGTH,
            "rejoin": REJOIN_STRENGTH,
            "pentagon": PENTAGON_BIAS
        }
    }

    json_path = os.path.join(OUTPUT_DIR, f"level53_{timestamp}.json")

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

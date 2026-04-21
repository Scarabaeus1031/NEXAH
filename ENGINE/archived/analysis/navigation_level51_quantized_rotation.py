# ENGINE/analysis/navigation_level51_quantized_rotation.py

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
STEPS = 900

STEP_SIZE = 0.18
RETURN_STRENGTH = 0.16
ROTATION_STRENGTH = 0.40

N_RAYS = 7                     # 🔥 diskrete 7er-Symmetrie
ANGLE_OFFSET = 0.0             # später rotierbar (RATH tuning)

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

    # einfache Dual-Struktur (stabil genug für Pattern)
    g1 = np.exp(-((X - 25)**2 + (Y - 30)**2) / 200)
    g2 = np.exp(-((X - 55)**2 + (Y - 60)**2) / 220)

    field = g1 + g2

    field = gaussian_filter(field, sigma=FIELD_SMOOTH)
    field /= np.max(field) + 1e-6

    return field


# --------------------------------------------------
# GRADIENT
# --------------------------------------------------

def compute_gradient(field):
    gy, gx = np.gradient(field)
    return gx, gy


# --------------------------------------------------
# QUANTIZED ROTATION (🔥 KERN!)
# --------------------------------------------------

def quantize_vector(fx, fy):
    angle = np.arctan2(fy, fx) + ANGLE_OFFSET

    # Mapping → 0 bis 1
    norm_angle = (angle + np.pi) / (2 * np.pi)

    # Diskrete Ray-Zuordnung
    sector = int(norm_angle * N_RAYS) % N_RAYS

    quant_angle = sector * (2 * np.pi / N_RAYS)

    return np.cos(quant_angle), np.sin(quant_angle)


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def simulate(field):

    gx, gy = compute_gradient(field)

    particles = np.random.rand(N_PARTICLES, 2) * SIZE

    density = np.zeros((SIZE, SIZE))

    cx = SIZE / 2
    cy = SIZE / 2

    for step in range(STEPS):

        new_particles = []

        for (x, y) in particles:

            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            fx = gx[iy, ix]
            fy = gy[iy, ix]

            # 🔥 Quantisierte Richtung
            qx, qy = quantize_vector(fx, fy)

            # Rotation (orthogonal)
            rx = -qy
            ry = qx

            # Global Return (Zentrum)
            dx = cx - x
            dy = cy - y

            vx = (
                STEP_SIZE * qx
                + ROTATION_STRENGTH * rx
                + RETURN_STRENGTH * dx * 0.01
            )

            vy = (
                STEP_SIZE * qy
                + ROTATION_STRENGTH * ry
                + RETURN_STRENGTH * dy * 0.01
            )

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

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].set_title("Field")
    axs[0].imshow(field, cmap="viridis")

    axs[1].set_title("Quantized Torus (Level 51)")
    axs[1].imshow(density, cmap="inferno")

    for ax in axs:
        ax.axis("off")

    img_path = os.path.join(OUTPUT_DIR, f"level51_{timestamp}.png")
    plt.savefig(img_path, dpi=150)
    plt.close()

    data = {
        "num_particles": int(N_PARTICLES),
        "steps": int(STEPS),
        "config": {
            "step_size": STEP_SIZE,
            "rotation": ROTATION_STRENGTH,
            "return": RETURN_STRENGTH,
            "rays": N_RAYS,
            "angle_offset": ANGLE_OFFSET
        }
    }

    json_path = os.path.join(OUTPUT_DIR, f"level51_{timestamp}.json")

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

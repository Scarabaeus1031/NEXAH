# ENGINE/analysis/navigation_level51b_quantized_orbit_lock.py

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
STEPS = 1000

STEP_SIZE = 0.18
ROTATION_STRENGTH = 0.42

RETURN_STRENGTH = 0.12
ORBIT_LOCK_STRENGTH = 0.18   # 🔥 neu!

N_RAYS = 7

OUTPUT_DIR = "ENGINE/visuals"


# --------------------------------------------------
# FIELD
# --------------------------------------------------

def build_field():
    x = np.linspace(0, SIZE - 1, SIZE)
    y = np.linspace(0, SIZE - 1, SIZE)
    X, Y = np.meshgrid(x, y)

    g1 = np.exp(-((X - 25)**2 + (Y - 30)**2) / 200)
    g2 = np.exp(-((X - 55)**2 + (Y - 60)**2) / 220)

    field = g1 + g2
    field = gaussian_filter(field, sigma=1.2)
    field /= np.max(field) + 1e-6

    return field


# --------------------------------------------------
# GRADIENT
# --------------------------------------------------

def compute_gradient(field):
    gy, gx = np.gradient(field)
    return gx, gy


# --------------------------------------------------
# QUANTIZATION
# --------------------------------------------------

def quantize_vector(fx, fy):
    angle = np.arctan2(fy, fx)

    norm = (angle + np.pi) / (2 * np.pi)
    sector = int(norm * N_RAYS) % N_RAYS

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

    TARGET_RADIUS = SIZE * 0.22   # 🔥 Orbit-Zielradius

    for step in range(STEPS):

        new_particles = []

        for (x, y) in particles:

            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            fx = gx[iy, ix]
            fy = gy[iy, ix]

            qx, qy = quantize_vector(fx, fy)

            # Rotation
            rx = -qy
            ry = qx

            # ------------------------------------------
            # 🔥 ORBIT LOCK (der entscheidende Schritt)
            # ------------------------------------------

            dx = x - cx
            dy = y - cy

            r = np.sqrt(dx**2 + dy**2) + 1e-6

            # Differenz zum Zielradius
            dr = TARGET_RADIUS - r

            # radialer Rückzug / Expansion
            ox = (dx / r) * dr * ORBIT_LOCK_STRENGTH
            oy = (dy / r) * dr * ORBIT_LOCK_STRENGTH

            # leichte Zentrumskorrektur
            retx = -dx * RETURN_STRENGTH * 0.01
            rety = -dy * RETURN_STRENGTH * 0.01

            vx = STEP_SIZE * qx + ROTATION_STRENGTH * rx + ox + retx
            vy = STEP_SIZE * qy + ROTATION_STRENGTH * ry + oy + rety

            nx = (x + vx) % SIZE
            ny = (y + vy) % SIZE

            new_particles.append((nx, ny))

            density[int(ny), int(nx)] += 1

        particles = np.array(new_particles)

    density = gaussian_filter(density, sigma=1.2)
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

    axs[1].set_title("Quantized Orbit Lock (51b)")
    axs[1].imshow(density, cmap="inferno")

    for ax in axs:
        ax.axis("off")

    path = os.path.join(OUTPUT_DIR, f"level51b_{timestamp}.png")
    plt.savefig(path, dpi=150)
    plt.close()

    print("Saved:", path)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    field = build_field()
    density = simulate(field)

    save_output(field, density)


if __name__ == "__main__":
    main()

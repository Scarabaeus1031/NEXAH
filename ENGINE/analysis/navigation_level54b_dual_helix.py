# ENGINE/analysis/navigation_level54b_dual_helix.py

import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter


# --------------------------------------------------
# CONFIG (leichter & stabiler)
# --------------------------------------------------

SIZE = 80

N_PARTICLES = 120
STEPS = 900

STEP_SIZE = 0.16

ROTATION_STRENGTH = 0.32
RETURN_STRENGTH = 0.08
REJOIN_STRENGTH = 0.14
ORBIT_STRENGTH = 0.22

R_TARGET = SIZE * 0.24

HELIX_STRENGTH = 0.30
PHASE_DRIFT = 0.05

MEMORY_DECAY = 0.996

FIELD_SMOOTH = 1.2
DENSITY_SMOOTH = 1.3

OUTPUT_DIR = "ENGINE/visuals"


# --------------------------------------------------
# FIELD
# --------------------------------------------------

def build_field():
    x = np.linspace(0, SIZE - 1, SIZE)
    y = np.linspace(0, SIZE - 1, SIZE)
    X, Y = np.meshgrid(x, y)

    g1 = np.exp(-((X - 24)**2 + (Y - 30)**2) / 180)
    g2 = np.exp(-((X - 56)**2 + (Y - 60)**2) / 220)

    field = g1 + g2
    field = gaussian_filter(field, sigma=FIELD_SMOOTH)
    field /= np.max(field) + 1e-8

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

    # 🔥 Dual branches (entscheidend!)
    branch = np.random.choice([-1.0, 1.0], size=N_PARTICLES)

    # eigene Phase pro Partikel
    phase = np.random.uniform(0, 2*np.pi, size=N_PARTICLES)

    density = np.zeros((SIZE, SIZE))
    memory = np.zeros((SIZE, SIZE))

    cx = SIZE / 2
    cy = SIZE / 2

    for step in range(STEPS):

        new_particles = []

        for i, (x, y) in enumerate(particles):

            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            fx = gx[iy, ix]
            fy = gy[iy, ix]

            # Rotation
            rx = -fy
            ry = fx

            # Zentrum
            dx = x - cx
            dy = y - cy

            r = np.sqrt(dx**2 + dy**2) + 1e-8
            theta = np.arctan2(dy, dx)

            # Orbit Stabilisierung
            radial_error = R_TARGET - r
            radial_force = np.array([dx, dy]) / r * radial_error * ORBIT_STRENGTH

            # Rejoin
            rejoin = -REJOIN_STRENGTH * np.array([dx, dy]) / r

            # Tangentialrichtung
            tx = -np.sin(theta)
            ty = np.cos(theta)

            # 🔥 Dual Helix Phase
            phase[i] += PHASE_DRIFT * branch[i]

            helix = HELIX_STRENGTH * np.cos(phase[i]) * np.array([tx, ty]) * branch[i]

            # Memory
            m = memory[iy, ix]

            vx = (
                STEP_SIZE * fx
                + ROTATION_STRENGTH * rx
                + radial_force[0]
                + rejoin[0]
                + helix[0]
                + RETURN_STRENGTH * m
            )

            vy = (
                STEP_SIZE * fy
                + ROTATION_STRENGTH * ry
                + radial_force[1]
                + rejoin[1]
                + helix[1]
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
    density /= np.max(density) + 1e-8

    return density


# --------------------------------------------------
# SAVE
# --------------------------------------------------

def save_output(field, density):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = os.path.join(OUTPUT_DIR, f"level54b_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    fig, axs = plt.subplots(1, 2, figsize=(10, 5))

    axs[0].set_title("Field")
    axs[0].imshow(field, cmap="viridis")

    axs[1].set_title("Dual Helix (Level 54b)")
    axs[1].imshow(density, cmap="inferno")

    for ax in axs:
        ax.axis("off")

    img_path = os.path.join(run_dir, "dual_helix.png")
    plt.savefig(img_path, dpi=150)
    plt.close()

    print("Saved:", img_path)


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    field = build_field()
    density = simulate(field)
    save_output(field, density)


if __name__ == "__main__":
    main()

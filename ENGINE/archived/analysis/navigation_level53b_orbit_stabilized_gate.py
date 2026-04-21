# ENGINE/analysis/navigation_level53b_orbit_stabilized_gate.py

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
STEPS = 1100

STEP_SIZE = 0.18

ROTATION_STRENGTH = 0.38
RETURN_STRENGTH = 0.14

SPLIT_STRENGTH = 0.22
REJOIN_STRENGTH = 0.18

ORBIT_STRENGTH = 0.28       # 🔥 NEW (entscheidend)
R_TARGET = SIZE * 0.22

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
# SIMULATION
# --------------------------------------------------

def simulate(field):

    gx, gy = compute_gradient(field)

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

            # ------------------------
            # Rotation
            # ------------------------
            rx = -fy
            ry = fx

            # ------------------------
            # Memory
            # ------------------------
            m = memory[iy, ix]

            # ------------------------
            # Split (diagonal axis)
            # ------------------------
            split = (x - y) * SPLIT_STRENGTH

            # ------------------------
            # Rejoin (center attraction)
            # ------------------------
            rejoin_x = (cx - x) * REJOIN_STRENGTH
            rejoin_y = (cy - y) * REJOIN_STRENGTH

            # ------------------------
            # 🔥 ORBIT STABILIZATION (NEU)
            # ------------------------
            dx = x - cx
            dy = y - cy

            r = np.sqrt(dx**2 + dy**2) + 1e-8
            radial_error = R_TARGET - r

            radial_force = np.array([dx, dy]) / r * radial_error * ORBIT_STRENGTH

            # ------------------------
            # FINAL VELOCITY
            # ------------------------
            vx = (
                STEP_SIZE * fx
                + ROTATION_STRENGTH * rx
                + rejoin_x
                + RETURN_STRENGTH * m
                + split
                + radial_force[0]
            )

            vy = (
                STEP_SIZE * fy
                + ROTATION_STRENGTH * ry
                + rejoin_y
                + RETURN_STRENGTH * m
                - split
                + radial_force[1]
            )

            nx = (x + vx) % SIZE
            ny = (y + vy) % SIZE

            new_particles.append((nx, ny))

            ix2 = int(nx)
            iy2 = int(ny)

            density[iy2, ix2] += 1.0
            memory[iy2, ix2] += 1.0

        particles = np.array(new_particles)
        memory *= 0.996

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
    axs[0].imshow(field)

    axs[1].set_title("Orbit Stabilized Gate (53b)")
    axs[1].imshow(density)

    for ax in axs:
        ax.axis("off")

    img_path = os.path.join(OUTPUT_DIR, f"level53b_{timestamp}.png")
    plt.savefig(img_path, dpi=150)
    plt.close()

    data = {
        "particles": N_PARTICLES,
        "steps": STEPS,
        "orbit_strength": ORBIT_STRENGTH,
        "r_target": R_TARGET
    }

    json_path = os.path.join(OUTPUT_DIR, f"level53b_{timestamp}.json")

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

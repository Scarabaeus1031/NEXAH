# ENGINE/analysis/navigation_level54_helical_lock_engine.py

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

N_PARTICLES = 160
STEPS = 1400

STEP_SIZE = 0.16

ROTATION_STRENGTH = 0.34
RETURN_STRENGTH = 0.10
REJOIN_STRENGTH = 0.16
ORBIT_STRENGTH = 0.24

R_TARGET = SIZE * 0.23

HELIX_STRENGTH = 0.28
PHASE_DRIFT = 0.055
PHASE_COUPLING = 0.12

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

    g1 = np.exp(-((X - 24)**2 + (Y - 28)**2) / 180)
    g2 = np.exp(-((X - 56)**2 + (Y - 58)**2) / 220)

    field = g1 + g2
    field = gaussian_filter(field, sigma=FIELD_SMOOTH)
    field /= np.max(field) + 1e-8
    return field


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def compute_gradient(field):
    gy, gx = np.gradient(field)
    return gx, gy


def wrap_angle(a):
    return (a + np.pi) % (2 * np.pi) - np.pi


# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def simulate(field):
    gx, gy = compute_gradient(field)

    particles = np.random.rand(N_PARTICLES, 2) * SIZE
    phases = np.random.uniform(0, 2 * np.pi, size=N_PARTICLES)
    branch = np.random.choice([-1.0, 1.0], size=N_PARTICLES)

    density = np.zeros((SIZE, SIZE), dtype=float)
    memory = np.zeros((SIZE, SIZE), dtype=float)

    cx = SIZE / 2
    cy = SIZE / 2

    for step in range(STEPS):
        new_particles = []

        global_phase = step * PHASE_DRIFT

        for i, (x, y) in enumerate(particles):
            ix = int(np.clip(x, 0, SIZE - 1))
            iy = int(np.clip(y, 0, SIZE - 1))

            fx = gx[iy, ix]
            fy = gy[iy, ix]

            # Lokale Feldrotation
            rx = -fy
            ry = fx

            # Zentrum / Orbit
            dx = x - cx
            dy = y - cy
            r = np.sqrt(dx**2 + dy**2) + 1e-8
            theta = np.arctan2(dy, dx)

            radial_error = R_TARGET - r
            radial_force = np.array([dx, dy]) / r * radial_error * ORBIT_STRENGTH

            # Rejoin zur Mitte
            rejoin_force = -REJOIN_STRENGTH * np.array([dx, dy]) / r

            # Tangentiale Richtung
            tx = -np.sin(theta)
            ty = np.cos(theta)

            # Duale Helix-Phase
            phases[i] += PHASE_DRIFT * branch[i]
            local_phase = phases[i] + global_phase * branch[i]

            helix_force = HELIX_STRENGTH * np.cos(local_phase) * np.array([tx, ty])
            lift_force = PHASE_COUPLING * np.sin(local_phase) * np.array([tx, ty]) * branch[i]

            # Memory
            m = memory[iy, ix]

            vx = (
                STEP_SIZE * fx
                + ROTATION_STRENGTH * rx
                + radial_force[0]
                + rejoin_force[0]
                + helix_force[0]
                + lift_force[0]
                + RETURN_STRENGTH * m
            )

            vy = (
                STEP_SIZE * fy
                + ROTATION_STRENGTH * ry
                + radial_force[1]
                + rejoin_force[1]
                + helix_force[1]
                + lift_force[1]
                + RETURN_STRENGTH * m
            )

            nx = (x + vx) % SIZE
            ny = (y + vy) % SIZE

            new_particles.append((nx, ny))

            ix2 = int(np.clip(nx, 0, SIZE - 1))
            iy2 = int(np.clip(ny, 0, SIZE - 1))

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
    run_dir = os.path.join(OUTPUT_DIR, f"level54_{timestamp}")
    os.makedirs(run_dir, exist_ok=True)

    fig, axs = plt.subplots(1, 2, figsize=(11, 5))

    axs[0].set_title("Field")
    axs[0].imshow(field, cmap="viridis")
    axs[0].axis("off")

    axs[1].set_title("Helical Lock Engine (Level 54)")
    axs[1].imshow(density, cmap="inferno")
    axs[1].axis("off")

    img_path = os.path.join(run_dir, "helical_lock_engine.png")
    plt.tight_layout()
    plt.savefig(img_path, dpi=180)
    plt.close()

    data = {
        "num_particles": N_PARTICLES,
        "steps": STEPS,
        "config": {
            "step_size": STEP_SIZE,
            "rotation": ROTATION_STRENGTH,
            "return": RETURN_STRENGTH,
            "rejoin": REJOIN_STRENGTH,
            "orbit_strength": ORBIT_STRENGTH,
            "r_target": R_TARGET,
            "helix_strength": HELIX_STRENGTH,
            "phase_drift": PHASE_DRIFT,
            "phase_coupling": PHASE_COUPLING
        }
    }

    json_path = os.path.join(run_dir, "helical_lock_engine.json")
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

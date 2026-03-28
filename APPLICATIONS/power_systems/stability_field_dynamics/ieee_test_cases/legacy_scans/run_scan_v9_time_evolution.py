from .ieee_loader import load_ieee14
from .stability_landscape_v2 import run_2d_stability_scan_v2
from .current_field_v8 import compute_current_field, normalize_field
from .boundary_dynamics_v2 import extract_dynamic_boundary
from .time_dynamics_v9 import (
    seed_particles_from_boundary,
    advect_particles,
    build_density_map,
)

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


# =========================
# BASE FIELD
# =========================
def plot_base(field):
    plt.figure()
    img = plt.imshow(field, cmap="viridis", origin="lower")
    plt.title("Voltage Field (Potential)")
    plt.colorbar(img)
    plt.show()


# =========================
# TRAJECTORIES
# =========================
def plot_trajectories(field, boundary, trajectories):
    plt.figure(figsize=(8, 6))
    plt.imshow(field, cmap="viridis", origin="lower", alpha=0.6)
    plt.contour(boundary, levels=[0.5], colors="red", linewidths=2)

    for traj in trajectories:
        plt.plot(traj[:, 0], traj[:, 1], linewidth=1, alpha=0.5)

    plt.title("Particle Trajectories (Time Evolution)")
    plt.xlabel("Axis A")
    plt.ylabel("Axis B")
    plt.show()


# =========================
# DENSITY MAP
# =========================
def plot_density(field, density):
    plt.figure(figsize=(8, 6))
    plt.imshow(field, cmap="viridis", origin="lower", alpha=0.4)
    img = plt.imshow(density, cmap="inferno", origin="lower", alpha=0.9)

    plt.title("Flow Density / Memory")
    plt.colorbar(img, label="Normalized density")
    plt.show()


# =========================
# ANIMATION
# =========================
def animate_particles(field, boundary, trajectories):
    fig, ax = plt.subplots(figsize=(8, 6))

    ax.imshow(field, cmap="viridis", origin="lower", alpha=0.6)
    ax.contour(boundary, levels=[0.5], colors="red", linewidths=2)

    scat = ax.scatter([], [], s=10, c="white")

    max_len = max(len(t) for t in trajectories) if trajectories else 0

    def update(frame):
        xs, ys = [], []

        for traj in trajectories:
            if frame < len(traj):
                xs.append(traj[frame, 0])
                ys.append(traj[frame, 1])
            else:
                xs.append(traj[-1, 0])
                ys.append(traj[-1, 1])

        if xs:
            scat.set_offsets(np.column_stack([xs, ys]))
        else:
            scat.set_offsets(np.empty((0, 2)))

        return (scat,)

    anim = FuncAnimation(fig, update, frames=max_len, interval=60, blit=True)

    plt.title("Flow Animation (Level 9)")
    plt.show()


# =========================
# MAIN
# =========================
def main():
    net = load_ieee14()

    print("\n--- V9 Time Evolution ---")

    load_bus = int(net.load["bus"].values[2])

    fx, fy, field = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=3.8,
        steps=60
    )

    Ix, Iy, speed = compute_current_field(field)
    speed = normalize_field(speed)

    boundary = extract_dynamic_boundary(field, threshold=0.7)

    particles = seed_particles_from_boundary(boundary, n_particles=80)

    trajectories = advect_particles(
        Ix, Iy,
        particles,
        dt=0.5,
        steps=120,
        damping=0.97
    )

    density = build_density_map(field.shape, trajectories)

    plot_base(field)
    plot_trajectories(field, boundary, trajectories)
    plot_density(field, density)
    animate_particles(field, boundary, trajectories)


if __name__ == "__main__":
    main()

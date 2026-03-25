from .ieee_loader import load_ieee14
from .stability_landscape_v2 import run_2d_stability_scan_v2
from .boundary_dynamics_v2 import extract_dynamic_boundary
from .current_field_v8 import compute_current_field
from .time_dynamics_v9 import (
    seed_particles_from_boundary,
    advect_particles
)

from .recurrence_analysis_v10 import (
    detect_loops,
    compute_recurrence_map
)

from .markov_transition_v10 import (
    build_transition_counts,
    normalize_transition_matrix,
    compute_transition_entropy
)

import matplotlib.pyplot as plt
import numpy as np


# =========================
# PLOTTING
# =========================
def plot_v10(field, trajectories, recurrence, entropy, loops):
    plt.figure(figsize=(12, 10))

    # ===== FIELD =====
    plt.subplot(2, 2, 1)
    plt.imshow(field, cmap="viridis", origin="lower")
    plt.title("Field")

    # ===== TRAJECTORIES =====
    plt.subplot(2, 2, 2)
    for traj in trajectories:
        traj = np.array(traj)
        if len(traj) > 1:
            plt.plot(traj[:, 0], traj[:, 1], alpha=0.15)
    plt.title("Trajectories")

    # ===== RECURRENCE =====
    plt.subplot(2, 2, 3)
    plt.imshow(recurrence, cmap="inferno", origin="lower")
    plt.title("Recurrence Map")

    # ===== ENTROPY =====
    plt.subplot(2, 2, 4)
    plt.imshow(entropy, cmap="plasma", origin="lower")
    plt.title("Transition Entropy")

    plt.tight_layout()
    plt.show()

    # ===== LOOPS =====
    if len(loops) > 0:
        plt.figure()
        for loop in loops:
            loop = np.array(loop)
            if len(loop) > 1:
                plt.plot(loop[:, 0], loop[:, 1])
        plt.title("Detected Loops")
        plt.show()


# =========================
# MAIN
# =========================
def main():
    net = load_ieee14()

    print("\n--- V10 Recurrence + Markov ---")

    # ===== FIELD =====
    load_bus = int(net.load["bus"].values[2])

    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=3.8,
        steps=60
    )

    # ===== BOUNDARY =====
    boundary = extract_dynamic_boundary(landscape, threshold=0.7)

    # ===== CURRENT FIELD (FIXED) =====
    Ix, Iy, mag = compute_current_field(landscape)

    # ===== PARTICLES =====
    particles = seed_particles_from_boundary(boundary, n_particles=120)

    trajectories = advect_particles(
        Ix, Iy,
        particles,
        dt=0.6,
        steps=120
    )

    # ===== RECURRENCE =====
    recurrence = compute_recurrence_map(
        trajectories,
        landscape.shape
    )

    loops = detect_loops(trajectories)

    # ===== MARKOV =====
    counts = build_transition_counts(
        trajectories,
        landscape.shape
    )

    probs = normalize_transition_matrix(counts)

    entropy = compute_transition_entropy(
        probs,
        landscape.shape
    )

    # ===== PLOT =====
    plot_v10(
        landscape,
        trajectories,
        recurrence,
        entropy,
        loops
    )


if __name__ == "__main__":
    main()

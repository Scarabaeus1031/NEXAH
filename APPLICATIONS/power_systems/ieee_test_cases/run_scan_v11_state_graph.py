from .ieee_loader import load_ieee14
from .stability_landscape_v2 import run_2d_stability_scan_v2
from .boundary_dynamics_v2 import compute_gradient_field, extract_dynamic_boundary
from .current_field_v8 import compute_current_field
from .time_dynamics_v9 import seed_particles_from_boundary, advect_particles
from .recurrence_analysis_v10 import compute_recurrence_map
from .state_clustering_v11 import extract_states_from_recurrence
from .state_graph_v11 import build_state_transition_graph

import matplotlib.pyplot as plt
import numpy as np


def plot_states(M, states):
    plt.figure()
    plt.imshow(M, cmap="inferno")

    for s in states:
        cy, cx = s["center"]
        plt.scatter(cx, cy, c="cyan", s=50)

    plt.title("Detected States (Attractors)")
    plt.show()


def plot_state_graph(states, transitions):
    plt.figure()

    for s in states:
        cy, cx = s["center"]
        plt.scatter(cx, cy, c="yellow", s=80)
        plt.text(cx + 1, cy + 1, f"S{s['id']}")

    for (a, b), w in transitions.items():
        sa = next((s for s in states if s["id"] == a), None)
        sb = next((s for s in states if s["id"] == b), None)

        if sa is None or sb is None:
            continue

        y1, x1 = sa["center"]
        y2, x2 = sb["center"]

        plt.plot([x1, x2], [y1, y2], alpha=0.5)

    plt.title("State Transition Graph")
    plt.show()


def main():
    print("\n--- V11 State Graph ---")

    net = load_ieee14()

    # ===== FIELD =====
    load_bus = int(net.load["bus"].values[2])

    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=3.8,
        steps=60
    )

    gx, gy, _ = compute_gradient_field(landscape)
    boundary = extract_dynamic_boundary(landscape, threshold=0.7)

    Ix, Iy, _ = compute_current_field(landscape)

    # ===== PARTICLES =====
    particles = seed_particles_from_boundary(boundary)
    trajectories = advect_particles(Ix, Iy, particles)

    # ===== RECURRENCE =====
    M = compute_recurrence_map(trajectories, landscape.shape)

    # ===== STATES =====
    states, labeled = extract_states_from_recurrence(M, threshold=0.3)

    # ===== GRAPH =====
    transitions = build_state_transition_graph(trajectories, labeled)

    # ===== PLOTS =====
    plot_states(M, states)
    plot_state_graph(states, transitions)


if __name__ == "__main__":
    main()

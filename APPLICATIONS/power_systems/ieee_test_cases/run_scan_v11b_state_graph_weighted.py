from .ieee_loader import load_ieee14
from .stability_landscape_v2 import run_2d_stability_scan_v2
from .boundary_dynamics_v2 import compute_gradient_field, extract_dynamic_boundary
from .current_field_v8 import compute_current_field
from .time_dynamics_v9 import seed_particles_from_boundary, advect_particles
from .recurrence_analysis_v10 import compute_recurrence_map
from .state_clustering_v11 import extract_states_from_recurrence
from .state_graph_v11b import build_weighted_transition_graph, compute_state_entropy

import matplotlib.pyplot as plt
import numpy as np


# 🔁 NEW: mirror seeding
def seed_bipolar(boundary):
    p1 = seed_particles_from_boundary(boundary)

    # mirror horizontally
    h, w = boundary.shape
    p2 = p1.copy()
    p2[:, 0] = w - p2[:, 0]

    return np.vstack([p1, p2])


def plot_states(M, states):
    plt.figure()
    plt.imshow(M, cmap="inferno")

    for s in states:
        cy, cx = s["center"]
        plt.scatter(cx, cy, c="cyan", s=60)

    plt.title("Detected States (Bipolar)")
    plt.show()


def plot_graph(states, probs, entropy):
    plt.figure()

    for s in states:
        cy, cx = s["center"]

        e = entropy.get(s["id"], 0)
        size = 50 + 200 * e

        plt.scatter(cx, cy, s=size, c="yellow")
        plt.text(cx + 1, cy + 1, f"S{s['id']}")

    for (a, b), p in probs.items():
        if p < 0.05:
            continue

        sa = next((s for s in states if s["id"] == a), None)
        sb = next((s for s in states if s["id"] == b), None)

        if sa is None or sb is None:
            continue

        y1, x1 = sa["center"]
        y2, x2 = sb["center"]

        plt.plot([x1, x2], [y1, y2], alpha=p)

    plt.title("Weighted State Graph")
    plt.show()


def main():
    print("\n--- V11b Weighted State Graph ---")

    net = load_ieee14()

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

    # 🔥 KEY CHANGE
    particles = seed_bipolar(boundary)

    trajectories = advect_particles(Ix, Iy, particles)

    M = compute_recurrence_map(trajectories, landscape.shape)

    states, labeled = extract_states_from_recurrence(M, threshold=0.25)

    transitions, probs, counts = build_weighted_transition_graph(
        trajectories, labeled
    )

    entropy = compute_state_entropy(probs)

    print(f"States: {len(states)}")
    print(f"Transitions: {len(transitions)}")

    plot_states(M, states)
    plot_graph(states, probs, entropy)


if __name__ == "__main__":
    main()

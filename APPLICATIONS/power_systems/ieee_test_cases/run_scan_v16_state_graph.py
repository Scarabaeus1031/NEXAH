# APPLICATIONS/power_systems/ieee_test_cases/run_scan_v16_state_graph.py

from .ieee_loader import load_ieee14
from .stability_landscape_v2 import run_2d_stability_scan_v2
from .boundary_dynamics_v2 import (
    compute_gradient_field,
    extract_dynamic_boundary
)
from .time_dynamics_v9 import (
    seed_particles_from_boundary,
    advect_particles
)
from .recurrence_analysis_v10 import (
    detect_loops,
    compute_recurrence_map
)
from .state_clustering_v11 import extract_states_from_recurrence
from .dynamic_flow_v12 import compute_dynamic_flow
from .closure_feedback_v13 import apply_closure_feedback
from .neon_rotation_v13b import inject_neon_rotation
from .dual_resonance_v15b import apply_dual_resonance_stabilized
from .state_graph_v16 import (
    build_state_graph,
    classify_loops_by_state
)

import matplotlib.pyplot as plt
import numpy as np


def seed_bipolar(boundary, n_particles=100):
    p1 = seed_particles_from_boundary(boundary, n_particles=n_particles)

    if len(p1) == 0:
        return p1

    h, w = boundary.shape
    p2 = p1.copy()
    p2[:, 0] = (w - 1) - p2[:, 0]

    return np.vstack([p1, p2])


def plot_states(M, states):
    plt.figure(figsize=(8, 6))
    plt.imshow(M, cmap="inferno", origin="lower")

    for i, s in enumerate(states):
        cy, cx = s["center"]
        plt.scatter(cx, cy, c="cyan", s=80)
        plt.text(cx + 0.8, cy + 0.8, f"S{i}", color="white")

    plt.title("Detected States")
    plt.show()


def plot_state_graph(M, states, edge_counts):
    plt.figure(figsize=(8, 6))
    plt.imshow(M, cmap="inferno", origin="lower")

    # plot nodes
    for i, s in enumerate(states):
        cy, cx = s["center"]
        plt.scatter(cx, cy, c="cyan", s=90, zorder=3)
        plt.text(cx + 0.8, cy + 0.8, f"S{i}", color="white", zorder=4)

    # plot edges
    max_w = max(edge_counts.values()) if len(edge_counts) > 0 else 1

    for (a, b), w in edge_counts.items():
        cya, cxa = states[a]["center"]
        cyb, cxb = states[b]["center"]

        alpha = 0.2 + 0.8 * (w / max_w)
        lw = 1 + 4 * (w / max_w)

        plt.plot([cxa, cxb], [cya, cyb], color="lime", alpha=alpha, linewidth=lw)

    plt.title("State Graph / Interface Coupling")
    plt.show()


def plot_loop_classes(classified):
    plt.figure(figsize=(10, 8))

    colors = {
        "local": "cyan",
        "bridging": "orange",
        "interface": "magenta"
    }

    for label, loops in classified.items():
        for loop in loops:
            loop = np.array(loop)
            if len(loop) > 1:
                plt.plot(loop[:, 0], loop[:, 1], alpha=0.7, color=colors[label])

    plt.title("Loop Topology: local / bridging / interface")
    plt.show()


def main():
    print("\n--- V16 State Graph / Loop Topology / Interface Coupling ---")

    net = load_ieee14()
    load_bus = int(net.load["bus"].values[2])

    # ===== FIELD =====
    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=3.8,
        steps=60
    )

    boundary = extract_dynamic_boundary(landscape, threshold=0.7)

    # ===== FLOW =====
    gx, gy, _ = compute_gradient_field(landscape)

    Fx, Fy = compute_dynamic_flow(
        gx, gy,
        strength=0.6,
        rotation=0.5,
        noise=0.02
    )

    Fx, Fy = apply_closure_feedback(
        landscape,
        Fx,
        Fy
    )

    Fx, Fy = inject_neon_rotation(
        Fx, Fy,
        strength=0.35
    )

    Fx, Fy, masks, radius, peaks, gap = apply_dual_resonance_stabilized(
        Fx, Fy,
        band_width=0.05,
        in_band_boost=1.5,
        out_band_damp=0.82,
        gap_boost=0.8,
        noise_strength=0.02,
        top_k=2
    )

    print("Detected peaks:", peaks)
    print("Gap:", gap)

    # ===== PARTICLES =====
    particles = seed_bipolar(boundary, n_particles=120)

    trajectories = advect_particles(
        Fx, Fy,
        particles,
        dt=0.6,
        steps=240,
        damping=0.975
    )

    # ===== ANALYSIS =====
    M = compute_recurrence_map(trajectories, landscape.shape)

    states, labeled = extract_states_from_recurrence(
        M,
        threshold=0.08
    )

    loops = detect_loops(
        trajectories,
        eps=2.0,
        min_length=10
    )

    node_counts, edge_counts = build_state_graph(
        trajectories,
        states,
        max_dist=6.0
    )

    classified = classify_loops_by_state(
        loops,
        states,
        max_dist=6.0
    )

    print(f"States: {len(states)}")
    print(f"Loops: {len(loops)}")
    print("Node counts:", node_counts)
    print("Edge counts:", edge_counts)
    print(
        "Loop classes:",
        {k: len(v) for k, v in classified.items()}
    )

    # ===== PLOTS =====
    plot_states(M, states)
    plot_state_graph(M, states, edge_counts)
    plot_loop_classes(classified)


if __name__ == "__main__":
    main()

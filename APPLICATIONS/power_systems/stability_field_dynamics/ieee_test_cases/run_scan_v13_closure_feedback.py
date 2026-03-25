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
from .state_graph_v11b import (
    build_weighted_transition_graph,
    compute_state_entropy
)
from .dynamic_flow_v12 import compute_dynamic_flow
from .closure_feedback_v13 import apply_closure_feedback

import matplotlib.pyplot as plt
import numpy as np


# =========================
# BIPOLAR SEEDING
# =========================
def seed_bipolar(boundary, n_particles=80):
    p1 = seed_particles_from_boundary(boundary, n_particles=n_particles)

    if len(p1) == 0:
        return p1

    h, w = boundary.shape
    p2 = p1.copy()
    p2[:, 0] = (w - 1) - p2[:, 0]

    return np.vstack([p1, p2])


# =========================
# PLOTS
# =========================
def plot_flow(landscape, Fx, Fy):
    plt.figure(figsize=(8, 6))
    plt.imshow(landscape, cmap="viridis", origin="lower", alpha=0.75)

    X, Y = np.meshgrid(np.arange(landscape.shape[1]), np.arange(landscape.shape[0]))
    plt.quiver(
        X[::3, ::3], Y[::3, ::3],
        Fx[::3, ::3], Fy[::3, ::3],
        color="white", alpha=0.8
    )

    plt.title("Closure Feedback Flow Field")
    plt.show()


def plot_states(M, states):
    plt.figure(figsize=(8, 6))
    plt.imshow(M, cmap="inferno", origin="lower")

    for s in states:
        cy, cx = s["center"]
        plt.scatter(cx, cy, c="cyan", s=60)

    plt.title("Detected States (Closure Feedback)")
    plt.show()


def plot_loops(loops):
    plt.figure(figsize=(8, 6))
    for loop in loops:
        loop = np.array(loop)
        if len(loop) > 1:
            plt.plot(loop[:, 0], loop[:, 1], alpha=0.7)

    plt.title("Detected Loops")
    plt.show()


# =========================
# MAIN
# =========================
def main():
    print("\n--- V13 Closure Feedback / Resonance Lock ---")

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

    # ===== BASE FLOW =====
    gx, gy, _ = compute_gradient_field(landscape)

    Fx, Fy = compute_dynamic_flow(
        gx, gy,
        strength=0.6,
        rotation=0.5,
        noise=0.02
    )

    # 🔥 FIX: positional args (kein keyword!)
    Fx, Fy = apply_closure_feedback(
        landscape,
        Fx,
        Fy
    )

    # ===== PARTICLES =====
    particles = seed_bipolar(boundary, n_particles=80)

    trajectories = advect_particles(
        Fx, Fy,
        particles,
        dt=0.6,
        steps=180,
        damping=0.97
    )

    # ===== ANALYSIS =====
    M = compute_recurrence_map(trajectories, landscape.shape)

    states, labeled = extract_states_from_recurrence(M, threshold=0.15)

    loops = detect_loops(trajectories, eps=1.5, min_length=12)

    print(f"States: {len(states)}")
    print(f"Loops: {len(loops)}")

    # ===== PLOTS =====
    plot_flow(landscape, Fx, Fy)
    plot_states(M, states)
    plot_loops(loops)


if __name__ == "__main__":
    main()

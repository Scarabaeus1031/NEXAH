# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/run_scan_v17_coupling.py

import matplotlib.pyplot as plt
import numpy as np

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
from .dynamic_flow_v12 import compute_dynamic_flow
from .closure_feedback_v13 import apply_closure_feedback
from .neon_rotation_v13b import inject_neon_rotation
from .dual_resonance_v15b import apply_dual_resonance_stabilized

from .coupling_metric_v17 import compute_coupling_metric


# =========================
# BIPOLAR SEEDING
# =========================
def seed_bipolar(boundary, n_particles=120):
    p1 = seed_particles_from_boundary(boundary, n_particles=n_particles)

    if len(p1) == 0:
        return p1

    h, w = boundary.shape
    p2 = p1.copy()
    p2[:, 0] = (w - 1) - p2[:, 0]

    return np.vstack([p1, p2])


# =========================
# MAIN
# =========================
def main():
    print("\n--- V17 Coupling Metric ---")

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

    Fx, Fy = apply_closure_feedback(landscape, Fx, Fy)
    Fx, Fy = inject_neon_rotation(Fx, Fy, strength=0.35)

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

    loops = detect_loops(
        trajectories,
        eps=2.0,
        min_length=10
    )

    # ===== COUPLING METRIC =====
    result = compute_coupling_metric(
        Fx, Fy, M, loops, len(particles)
    )

    print("\n--- Coupling Metric ---")
    print(f"C (total): {result['C']:.6f}")
    print(f"P (flow persistence): {result['P']:.4f}")
    print(f"R (recurrence concentration): {result['R']:.4f}")
    print(f"L (loop density): {result['L']:.4f}")

    # ===== VISUAL =====
    plt.figure(figsize=(8, 6))
    plt.imshow(M, cmap="inferno", origin="lower")
    plt.title("Recurrence Map (M)")
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    main()

# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/run_scan_v17b_coupling_heatmap.py

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
from .coupling_heatmap_v17b import compute_coupling_heatmap


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
# PLOTTING
# =========================
def plot_heatmaps(maps):
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    ax = axes[0, 0]
    im = ax.imshow(maps["P_local"], cmap="Blues", origin="lower")
    ax.set_title("Flow Persistence P(x,y)")
    plt.colorbar(im, ax=ax)

    ax = axes[0, 1]
    im = ax.imshow(maps["R_local"], cmap="Oranges", origin="lower")
    ax.set_title("Recurrence R(x,y)")
    plt.colorbar(im, ax=ax)

    ax = axes[1, 0]
    im = ax.imshow(maps["L_local"], cmap="Greens", origin="lower")
    ax.set_title("Loop Density L(x,y)")
    plt.colorbar(im, ax=ax)

    ax = axes[1, 1]
    im = ax.imshow(maps["C_local"], cmap="inferno", origin="lower")
    ax.set_title("Coupling Heatmap C(x,y)")
    plt.colorbar(im, ax=ax)

    plt.tight_layout()
    plt.show()


def plot_overlay(landscape, C):
    plt.figure(figsize=(8, 6))
    plt.imshow(landscape, cmap="viridis", origin="lower", alpha=0.4)
    im = plt.imshow(C, cmap="inferno", origin="lower", alpha=0.9)
    plt.title("Coupling Birth Zones (Overlay)")
    plt.colorbar(im)
    plt.show()


# =========================
# MAIN
# =========================
def main():
    print("\n--- V17b Coupling Heatmap ---")

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

    print(f"Loops: {len(loops)}")

    # ===== COUPLING MAP =====
    maps = compute_coupling_heatmap(Fx, Fy, M, loops)

    # ===== PLOTS =====
    plot_heatmaps(maps)
    plot_overlay(landscape, maps["C_local"])


if __name__ == "__main__":
    main()

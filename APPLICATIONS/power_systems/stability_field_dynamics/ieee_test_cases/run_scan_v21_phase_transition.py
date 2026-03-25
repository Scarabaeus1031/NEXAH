# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/run_scan_v21_phase_transition.py

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
from .state_clustering_v11 import extract_states_from_recurrence
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
# SINGLE RUN
# =========================
def run_single_coupling(base_load, steps=60, n_particles=120):
    net = load_ieee14()
    load_bus = int(net.load["bus"].values[2])

    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=base_load,
        steps=steps
    )

    boundary = extract_dynamic_boundary(landscape, threshold=0.7)
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

    particles = seed_bipolar(boundary, n_particles=n_particles)

    trajectories = advect_particles(
        Fx, Fy,
        particles,
        dt=0.6,
        steps=240,
        damping=0.975
    )

    M = compute_recurrence_map(trajectories, landscape.shape)

    loops = detect_loops(
        trajectories,
        eps=2.0,
        min_length=10
    )

    states, labeled = extract_states_from_recurrence(
        M,
        threshold=0.08
    )

    metric = compute_coupling_metric(
        Fx, Fy, M, loops, len(particles)
    )

    return {
        "base_load": float(base_load),
        "C": float(metric["C"]),
        "P": float(metric["P"]),
        "R": float(metric["R"]),
        "L": float(metric["L"]),
        "loops": int(len(loops)),
        "states": int(len(states)),
        "peaks": peaks,
        "gap": float(gap),
    }


# =========================
# PLOTS
# =========================
def plot_phase_transition(results):
    x = [r["base_load"] for r in results]
    C = [r["C"] for r in results]
    P = [r["P"] for r in results]
    R = [r["R"] for r in results]
    L = [r["L"] for r in results]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))

    axes[0, 0].plot(x, C, marker="o")
    axes[0, 0].set_title("Coupling C vs Base Load")
    axes[0, 0].set_xlabel("Base Load")
    axes[0, 0].set_ylabel("C")

    axes[0, 1].plot(x, P, marker="o", label="P")
    axes[0, 1].plot(x, R, marker="o", label="R")
    axes[0, 1].plot(x, L, marker="o", label="L")
    axes[0, 1].set_title("P / R / L vs Base Load")
    axes[0, 1].set_xlabel("Base Load")
    axes[0, 1].legend()

    loops = [r["loops"] for r in results]
    states = [r["states"] for r in results]

    axes[1, 0].plot(x, loops, marker="o")
    axes[1, 0].set_title("Loop Count vs Base Load")
    axes[1, 0].set_xlabel("Base Load")
    axes[1, 0].set_ylabel("Loops")

    axes[1, 1].plot(x, states, marker="o")
    axes[1, 1].set_title("State Count vs Base Load")
    axes[1, 1].set_xlabel("Base Load")
    axes[1, 1].set_ylabel("States")

    plt.tight_layout()
    plt.show()


def plot_gap_and_peaks(results):
    x = [r["base_load"] for r in results]
    gap = [r["gap"] for r in results]
    peak_a = [r["peaks"][0] if len(r["peaks"]) > 0 else np.nan for r in results]
    peak_b = [r["peaks"][-1] if len(r["peaks"]) > 0 else np.nan for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(x, peak_a, marker="o", label="Peak A")
    plt.plot(x, peak_b, marker="o", label="Peak B")
    plt.plot(x, gap, marker="o", label="Gap")
    plt.title("Peaks / Gap vs Base Load")
    plt.xlabel("Base Load")
    plt.legend()
    plt.show()


# =========================
# MAIN
# =========================
def main():
    print("\n--- V21 Phase Transition Scan ---")

    # deliberately modest range first
    load_values = np.linspace(3.4, 4.2, 7)

    results = []

    for base_load in load_values:
        print(f"\nScanning base_load = {base_load:.3f}")
        try:
            result = run_single_coupling(
                base_load=base_load,
                steps=60,
                n_particles=120
            )
            results.append(result)

            print(
                f"C={result['C']:.6f}, "
                f"P={result['P']:.4f}, "
                f"R={result['R']:.4f}, "
                f"L={result['L']:.4f}, "
                f"states={result['states']}, "
                f"loops={result['loops']}, "
                f"gap={result['gap']:.4f}"
            )

        except Exception as e:
            print(f"Failed at base_load={base_load:.3f}: {e}")

    if len(results) == 0:
        print("No valid runs.")
        return

    print("\n--- Summary ---")
    for r in results:
        print(
            f"base_load={r['base_load']:.3f} | "
            f"C={r['C']:.6f} | "
            f"states={r['states']} | "
            f"loops={r['loops']} | "
            f"gap={r['gap']:.4f}"
        )

    plot_phase_transition(results)
    plot_gap_and_peaks(results)


if __name__ == "__main__":
    main()

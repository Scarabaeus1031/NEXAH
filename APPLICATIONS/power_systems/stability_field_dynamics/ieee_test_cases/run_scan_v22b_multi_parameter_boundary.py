# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/run_scan_v22b_multi_parameter_boundary.py

import numpy as np
import matplotlib.pyplot as plt

from .run_scan_v21_phase_transition import run_single_coupling


# =========================
# REGIME CLASSIFICATION
# =========================
def classify_regime(C, loops, states, c_eps=1e-4):
    if loops == 0 and states == 0 and C <= c_eps:
        return 0  # diffuse
    if loops > 0 and states > 0 and C > c_eps:
        return 2  # coupled
    return 1  # transition


# =========================
# MAIN
# =========================
def main():
    print("\n--- V22b Multi-Parameter Boundary ---")

    base_load_values = np.linspace(1.0, 4.0, 8)
    noise_values = np.linspace(0.0, 0.5, 10)

    regime_map = np.zeros((len(base_load_values), len(noise_values)))
    coupling_map = np.zeros_like(regime_map)

    for i, base_load in enumerate(base_load_values):
        for j, noise in enumerate(noise_values):

            print(f"Load={base_load:.2f}, Noise={noise:.3f}")

            try:
                r = run_single_coupling(
                    base_load=base_load,
                    steps=60,
                    n_particles=120,
                    noise_strength=noise  # key parameter
                )

                regime = classify_regime(
                    r["C"],
                    r["loops"],
                    r["states"]
                )

                regime_map[i, j] = regime
                coupling_map[i, j] = r["C"]

                print(
                    f"C={r['C']:.6f}, loops={r['loops']}, "
                    f"states={r['states']} → regime={regime}"
                )

            except Exception as e:
                print("failed:", e)
                regime_map[i, j] = -1

    # =========================
    # PLOT REGIME MAP
    # =========================
    plt.figure(figsize=(8, 6))
    plt.imshow(
        regime_map,
        origin="lower",
        aspect="auto",
        extent=[
            noise_values[0], noise_values[-1],
            base_load_values[0], base_load_values[-1]
        ]
    )
    plt.colorbar(label="Regime (0=diffuse, 1=transition, 2=coupled)")
    plt.xlabel("Noise Strength")
    plt.ylabel("Base Load")
    plt.title("Phase Diagram (Load vs Noise)")
    plt.show()

    # =========================
    # PLOT COUPLING MAP
    # =========================
    plt.figure(figsize=(8, 6))
    plt.imshow(
        coupling_map,
        origin="lower",
        aspect="auto",
        extent=[
            noise_values[0], noise_values[-1],
            base_load_values[0], base_load_values[-1]
        ]
    )
    plt.colorbar(label="Coupling C")
    plt.xlabel("Noise Strength")
    plt.ylabel("Base Load")
    plt.title("Coupling Strength Map")
    plt.show()


if __name__ == "__main__":
    main()

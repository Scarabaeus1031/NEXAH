# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/run_scan_v21b_phase_transition.py

import matplotlib.pyplot as plt
import numpy as np

from .run_scan_v21_phase_transition import run_single_coupling


# =========================
# REGIME DETECTION
# =========================
def classify_regime(C, loops, states, eps=1e-4):
    if loops == 0 and states == 0:
        return "diffuse"

    if C > eps and loops > 0:
        return "coupled"

    return "transition"


def detect_plateau(values, tol=1e-5):
    diffs = np.abs(np.diff(values))
    return np.all(diffs < tol)


# =========================
# PLOTS
# =========================
def plot_results(results):
    x = [r["base_load"] for r in results]
    C = [r["C"] for r in results]
    loops = [r["loops"] for r in results]
    states = [r["states"] for r in results]

    regimes = [r["regime"] for r in results]

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, C, marker="o", label="Coupling C")

    # mark regimes
    for i, r in enumerate(results):
        color = {
            "diffuse": "gray",
            "transition": "orange",
            "coupled": "green"
        }[r["regime"]]

        ax.scatter(x[i], C[i], color=color, s=80)

    ax.set_title("Phase Transition (C vs Base Load)")
    ax.set_xlabel("Base Load")
    ax.set_ylabel("C")
    ax.legend()

    plt.show()

    # loops / states
    plt.figure(figsize=(10, 5))
    plt.plot(x, loops, marker="o", label="Loops")
    plt.plot(x, states, marker="o", label="States")
    plt.title("Loops / States vs Base Load")
    plt.xlabel("Base Load")
    plt.legend()
    plt.show()


# =========================
# MAIN
# =========================
def main():
    print("\n--- V21b Wide Phase Transition Scan ---")

    # WICHTIG: großer Bereich!
    load_values = np.linspace(1.5, 6.0, 15)

    results = []

    for base_load in load_values:
        print(f"\nScanning base_load = {base_load:.3f}")

        try:
            r = run_single_coupling(base_load)

            regime = classify_regime(
                r["C"],
                r["loops"],
                r["states"]
            )

            r["regime"] = regime
            results.append(r)

            print(
                f"C={r['C']:.6f}, "
                f"loops={r['loops']}, "
                f"states={r['states']}, "
                f"gap={r['gap']:.4f}, "
                f"→ {regime}"
            )

        except Exception as e:
            print(f"Failed at {base_load:.3f}: {e}")

    if len(results) == 0:
        print("No valid runs.")
        return

    # =========================
    # ANALYSIS
    # =========================
    C_vals = [r["C"] for r in results]

    print("\n--- Regime Summary ---")
    for r in results:
        print(
            f"{r['base_load']:.3f} → {r['regime']} "
            f"(C={r['C']:.6f}, loops={r['loops']})"
        )

    if detect_plateau(C_vals):
        print("\nDetected: Stable Plateau Region")
    else:
        print("\nNo global plateau — possible transitions present")

    plot_results(results)


if __name__ == "__main__":
    main()

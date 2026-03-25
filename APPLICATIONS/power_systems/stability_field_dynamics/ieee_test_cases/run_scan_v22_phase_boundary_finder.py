# APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/run_scan_v22_phase_boundary.py

import matplotlib.pyplot as plt
import numpy as np

from .run_scan_v21_phase_transition import run_single_coupling


# =========================
# REGIME CLASSIFICATION
# =========================
def classify_regime(C, loops, states, c_eps=1e-4):
    """
    Simple regime classifier.
    """
    if loops == 0 and states == 0 and C <= c_eps:
        return "diffuse"

    if loops > 0 and states > 0 and C > c_eps:
        return "coupled"

    return "transition"


def find_boundaries(results):
    """
    Find rough regime boundaries by scanning adjacent changes.
    """
    boundaries = []

    for a, b in zip(results[:-1], results[1:]):
        if a["regime"] != b["regime"]:
            boundaries.append({
                "from": a["regime"],
                "to": b["regime"],
                "load_left": a["base_load"],
                "load_right": b["base_load"],
            })

    return boundaries


# =========================
# PLOTS
# =========================
def plot_phase_boundary(results):
    x = [r["base_load"] for r in results]
    C = [r["C"] for r in results]
    loops = [r["loops"] for r in results]
    states = [r["states"] for r in results]

    colors = {
        "diffuse": "gray",
        "transition": "orange",
        "coupled": "green"
    }

    plt.figure(figsize=(10, 6))
    plt.plot(x, C, marker="o", color="black", linewidth=1.5, alpha=0.8)

    for r in results:
        plt.scatter(
            r["base_load"],
            r["C"],
            s=90,
            color=colors[r["regime"]],
            zorder=3
        )

    plt.title("Phase Boundary Finder — Coupling C vs Base Load")
    plt.xlabel("Base Load")
    plt.ylabel("Coupling C")
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(x, loops, marker="o", label="Loops")
    plt.plot(x, states, marker="o", label="States")
    plt.title("Loops / States vs Base Load")
    plt.xlabel("Base Load")
    plt.legend()
    plt.show()


def plot_prl(results):
    x = [r["base_load"] for r in results]
    P = [r["P"] for r in results]
    R = [r["R"] for r in results]
    L = [r["L"] for r in results]

    plt.figure(figsize=(10, 6))
    plt.plot(x, P, marker="o", label="P")
    plt.plot(x, R, marker="o", label="R")
    plt.plot(x, L, marker="o", label="L")
    plt.title("P / R / L vs Base Load")
    plt.xlabel("Base Load")
    plt.legend()
    plt.show()


# =========================
# MAIN
# =========================
def main():
    print("\n--- V22 Phase Boundary Finder ---")

    # much wider scan
    load_values = np.linspace(0.6, 6.0, 19)

    results = []

    for base_load in load_values:
        print(f"\nScanning base_load = {base_load:.3f}")

        try:
            r = run_single_coupling(
                base_load=base_load,
                steps=60,
                n_particles=120
            )

            r["regime"] = classify_regime(
                r["C"],
                r["loops"],
                r["states"]
            )

            results.append(r)

            print(
                f"C={r['C']:.6f}, "
                f"P={r['P']:.4f}, "
                f"R={r['R']:.4f}, "
                f"L={r['L']:.4f}, "
                f"states={r['states']}, "
                f"loops={r['loops']}, "
                f"gap={r['gap']:.4f}, "
                f"regime={r['regime']}"
            )

        except Exception as e:
            print(f"Failed at base_load={base_load:.3f}: {e}")

    if len(results) == 0:
        print("No valid runs.")
        return

    boundaries = find_boundaries(results)

    print("\n--- Summary ---")
    for r in results:
        print(
            f"base_load={r['base_load']:.3f} | "
            f"C={r['C']:.6f} | "
            f"states={r['states']} | "
            f"loops={r['loops']} | "
            f"gap={r['gap']:.4f} | "
            f"regime={r['regime']}"
        )

    print("\n--- Detected Regime Boundaries ---")
    if len(boundaries) == 0:
        print("No regime changes detected in scanned interval.")
    else:
        for b in boundaries:
            print(
                f"{b['from']} -> {b['to']} "
                f"between load {b['load_left']:.3f} and {b['load_right']:.3f}"
            )

    plot_phase_boundary(results)
    plot_prl(results)


if __name__ == "__main__":
    main()

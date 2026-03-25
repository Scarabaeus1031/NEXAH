from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .stability_landscape import run_2d_stability_scan

import matplotlib.pyplot as plt


# =========================
# 1D PLOT
# =========================
def plot_results(results):
    factors = [f for f, s in results]
    stability = [1 if s else 0 for f, s in results]

    plt.figure()
    plt.plot(factors, stability, marker="o")
    plt.xlabel("Load Factor")
    plt.ylabel("Stability (1=stable, 0=unstable)")
    plt.title("IEEE 14-bus Stability Scan")
    plt.grid()
    plt.axvline(x=4.2, linestyle="--", label="Collapse boundary")
    plt.legend()
    plt.show()


# =========================
# 2D LANDSCAPE PLOT
# =========================
def plot_landscape(factors, landscape):
    plt.figure()
    plt.imshow(
        landscape,
        origin="lower",
        extent=[factors[0], factors[-1], factors[0], factors[-1]],
        aspect="auto"
    )

    plt.xlabel("Load factor (Bus A)")
    plt.ylabel("Load factor (Bus B)")
    plt.title("IEEE 14-bus Stability Landscape")
    plt.colorbar(label="Stability (1=stable, 0=unstable)")
    plt.show()


# =========================
# MAIN
# =========================
def main():

    net = load_ieee14()

    # ===== 1D SCAN =====
    results = run_stability_scan(
        net,
        min_factor=3.8,
        max_factor=4.4,
        steps=40
    )

    print("\n--- 1D Stability Scan ---")
    for factor, stable in results:
        status = "Stable" if stable else "Unstable"
        print(f"Load factor: {factor:.2f} → {status}")

    plot_results(results)

    # ===== 2D LANDSCAPE =====
    print("\n--- 2D Stability Landscape ---")

    factors, landscape = run_2d_stability_scan(
        net,
        bus_a=3,
        bus_b=9,
        min_factor=3.0,
        max_factor=4.5,
        steps=30
    )

    plot_landscape(factors, landscape)


if __name__ == "__main__":
    main()

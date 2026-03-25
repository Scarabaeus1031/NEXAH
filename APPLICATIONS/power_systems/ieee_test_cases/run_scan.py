from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .stability_landscape import run_2d_stability_scan

import matplotlib.pyplot as plt


def plot_results(results):
    factors = [f for f, s in results]
    stability = [1 if s else 0 for f, s in results]

    plt.figure()
    plt.plot(factors, stability, marker="o")
    plt.xlabel("Load Factor")
    plt.ylabel("Stability (1=stable, 0=unstable)")
    plt.title("IEEE 14-bus Stability Scan")
    plt.grid()

    collapse = next((f for f, s in results if not s), None)
    if collapse:
        plt.axvline(x=collapse, linestyle="--", label=f"Collapse ~ {collapse:.2f}")
        plt.legend()

    plt.show()


def plot_landscape(factors, landscape):
    plt.figure()

    plt.imshow(
        landscape,
        origin="lower",
        extent=[factors[0], factors[-1], factors[0], factors[-1]],
        aspect="auto",
        cmap="viridis"
    )

    plt.contour(
        landscape,
        levels=[0.5],
        colors="red",
        linewidths=1,
        extent=[factors[0], factors[-1], factors[0], factors[-1]]
    )

    plt.xlabel("Load factor (Bus A)")
    plt.ylabel("Load factor (Bus B)")
    plt.title("IEEE 14-bus Stability Landscape")
    plt.colorbar(label="Stability (1=stable, 0=unstable)")
    plt.show()


def main():
    net = load_ieee14()

    print("\n--- 1D Stability Scan ---")
    results = run_stability_scan(
        net,
        min_factor=3.8,
        max_factor=4.4,
        steps=40
    )

    for factor, stable in results:
        status = "Stable" if stable else "Unstable"
        print(f"Load factor: {factor:.2f} → {status}")

    plot_results(results)

    print("\n--- 2D Stability Landscape ---")

    load_buses = net.load["bus"].values
    bus_a = int(load_buses[0])
    bus_b = int(load_buses[1])

    factors, landscape = run_2d_stability_scan(
        net,
        bus_a=bus_a,
        bus_b=bus_b,
        min_factor=3.5,
        max_factor=4.5,
        steps=40
    )

    plot_landscape(factors, landscape)


if __name__ == "__main__":
    main()

from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan

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
    plt.axvline(x=4.2, linestyle="--", label="Collapse boundary")
    plt.legend()
    plt.show()


def main():
    net = load_ieee14()
    results = run_stability_scan(net, min_factor=3.8, max_factor=4.4, steps=40)

    for factor, stable in results:
        status = "Stable" if stable else "Unstable"
        print(f"Load factor: {factor:.2f} → {status}")

    plot_results(results)


if __name__ == "__main__":
    main()

from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .stability_landscape_v2 import run_2d_stability_scan_v2
from .boundary_dynamics_v2 import (
    compute_gradient_field,
    extract_dynamic_boundary,
    compute_boundary_strength
)
from .field_mirror_v1 import mirror_field, combine_fields

import matplotlib.pyplot as plt
import numpy as np


# =========================
# 1D
# =========================
def plot_results(results):
    factors = [f for f, s in results]
    stability = [1 if s else 0 for f, s in results]

    plt.figure()
    plt.plot(factors, stability, marker="o")
    plt.grid()

    collapse = next((f for f, s in results if not s), None)
    if collapse:
        plt.axvline(x=collapse, linestyle="--", label=f"Collapse ~ {collapse:.2f}")
        plt.legend()

    plt.title("1D Stability Scan")
    plt.show()


# =========================
# 2D FIELD
# =========================
def plot_landscape(factors_x, factors_y, landscape):
    plt.figure()

    img = plt.imshow(
        landscape,
        origin="lower",
        extent=[factors_x[0], factors_x[-1],
                factors_y[0], factors_y[-1]],
        aspect="auto",
        cmap="viridis"
    )

    if np.unique(landscape).size > 1:
        plt.colorbar(img, label="Min Voltage (pu)")

    plt.xlabel("Load Axis A")
    plt.ylabel("Load Axis B")
    plt.title("2D Stability Field")

    plt.show()


# =========================
# FLOW FIELD
# =========================
def plot_flow_field(factors_x, factors_y, gx, gy):
    plt.figure()

    X, Y = np.meshgrid(factors_x, factors_y)

    plt.quiver(
        X, Y,
        gx, gy,
        color="white",
        scale=30
    )

    plt.title("Flow Field (Gradient)")
    plt.xlabel("Axis A")
    plt.ylabel("Axis B")

    plt.show()


# =========================
# BOUNDARY
# =========================
def plot_boundary(boundary, strength):
    plt.figure()

    plt.subplot(1, 2, 1)
    plt.imshow(boundary, cmap="gray")
    plt.title("Boundary")

    plt.subplot(1, 2, 2)
    plt.imshow(strength, cmap="inferno")
    plt.title("Boundary Strength")

    plt.show()


# =========================
# MIRROR + INTERACTION
# =========================
def plot_mirror_and_interaction(landscape):
    mirrored = mirror_field(landscape)
    combined = combine_fields(landscape, mirrored, mode="difference")

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(landscape, cmap="viridis")
    plt.title("Original Field")

    plt.subplot(1, 3, 2)
    plt.imshow(mirrored, cmap="viridis")
    plt.title("Mirrored Field")

    plt.subplot(1, 3, 3)
    plt.imshow(combined, cmap="coolwarm")
    plt.title("Interaction (Difference)")
    plt.colorbar()

    plt.tight_layout()
    plt.show()


# =========================
# MAIN
# =========================
def main():
    net = load_ieee14()

    # ===== 1D =====
    print("\n--- 1D Stability Scan ---")

    results = run_stability_scan(
        net,
        min_factor=3.8,
        max_factor=4.4,
        steps=40
    )

    plot_results(results)

    # ===== 2D =====
    print("\n--- 2D Stability Field ---")

    load_bus = int(net.load["bus"].values[2])

    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=3.8,
        steps=60
    )

    plot_landscape(fx, fy, landscape)

    # ===== FLOW =====
    gx, gy, grad_mag = compute_gradient_field(landscape)
    plot_flow_field(fx, fy, gx, gy)

    # ===== BOUNDARY =====
    boundary = extract_dynamic_boundary(landscape, threshold=0.7)
    strength = compute_boundary_strength(grad_mag, boundary)
    plot_boundary(boundary, strength)

    # ===== MIRROR SYSTEM =====
    plot_mirror_and_interaction(landscape)


if __name__ == "__main__":
    main()

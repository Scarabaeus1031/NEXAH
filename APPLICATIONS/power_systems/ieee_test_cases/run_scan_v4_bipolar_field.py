from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .stability_landscape_v2 import run_2d_stability_scan_v2
from .boundary_dynamics_v3 import (
    compute_gradient_field,
    extract_dynamic_boundary,
    compute_boundary_strength,
    compute_signed_boundary_field,
    normalize_field,
    mirror_field_vertical,
    combine_fields,
)

import matplotlib.pyplot as plt
import numpy as np


# =========================
# 1D STABILITY PLOT
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

    plt.xlabel("Load Factor")
    plt.ylabel("Stability (1=stable, 0=unstable)")
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
        extent=[factors_x[0], factors_x[-1], factors_y[0], factors_y[-1]],
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
def plot_flow_field(factors_x, factors_y, gx, gy, stride=4):
    plt.figure()

    X, Y = np.meshgrid(factors_x, factors_y)

    plt.quiver(
        X[::stride, ::stride],
        Y[::stride, ::stride],
        gx[::stride, ::stride],
        gy[::stride, ::stride],
        color="white",
        scale=15
    )

    plt.xlabel("Axis A")
    plt.ylabel("Axis B")
    plt.title("Flow Field (Gradient)")
    plt.show()


# =========================
# BOUNDARY
# =========================
def plot_boundary(boundary, strength):
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.imshow(boundary, cmap="gray")
    plt.title("Boundary")

    plt.subplot(1, 2, 2)
    plt.imshow(strength, cmap="inferno")
    plt.title("Boundary Strength")

    plt.tight_layout()
    plt.show()


# =========================
# SIGNED FIELD
# =========================
def plot_signed_field(field, title="Signed Boundary Field"):
    plt.figure()

    img = plt.imshow(field, cmap="coolwarm", origin="lower")
    plt.colorbar(img, label="Signed distance to boundary")
    plt.title(title)
    plt.show()


# =========================
# BIPOLAR / MIRROR FIELD
# =========================
def plot_bipolar_fields(original_signed, mirrored_signed, combined):
    plt.figure(figsize=(15, 4))

    plt.subplot(1, 3, 1)
    img1 = plt.imshow(original_signed, cmap="coolwarm", origin="lower")
    plt.title("Original Signed Field")
    plt.colorbar(img1, fraction=0.046, pad=0.04)

    plt.subplot(1, 3, 2)
    img2 = plt.imshow(mirrored_signed, cmap="coolwarm", origin="lower")
    plt.title("Mirrored Signed Field")
    plt.colorbar(img2, fraction=0.046, pad=0.04)

    plt.subplot(1, 3, 3)
    img3 = plt.imshow(combined, cmap="PuOr", origin="lower")
    plt.title("Bipolar Combined Field")
    plt.colorbar(img3, fraction=0.046, pad=0.04)

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

    # ===== V3: BOUNDARY DYNAMICS =====
    print("\n--- V3 Boundary Dynamics ---")

    gx, gy, grad_mag = compute_gradient_field(landscape)
    boundary = extract_dynamic_boundary(landscape, threshold=0.7, band=0.02)
    strength = compute_boundary_strength(grad_mag, boundary)

    plot_flow_field(fx, fy, gx, gy)
    plot_boundary(boundary, strength)

    # ===== V4: BIPOLAR FIELD =====
    print("\n--- V4 Bipolar Field ---")

    signed = compute_signed_boundary_field(landscape, threshold=0.7)
    signed = normalize_field(signed)

    mirrored = mirror_field_vertical(signed)
    combined = combine_fields(signed, mirrored, mode="difference")
    combined = normalize_field(combined)

    plot_signed_field(signed, title="Signed Boundary Field")
    plot_bipolar_fields(signed, mirrored, combined)


if __name__ == "__main__":
    main()

from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .stability_landscape_v2 import run_2d_stability_scan_v2

from .boundary_dynamics_v2 import (
    compute_gradient_field,
    extract_dynamic_boundary,
    compute_boundary_strength
)

from .phase_dynamics_v4 import (
    compute_curl_field,
    compute_phase_field,
    compute_vorticity_strength
)

from .eigenmode_dynamics_v6 import (
    extract_boundary_points,
    compute_pca_axes,
    compute_hessian_like_curvature,
    normalize_field
)

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # noqa


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

    plt.xlabel("Load Factor")
    plt.ylabel("Stability")
    plt.title("1D Stability Scan")
    plt.show()


# =========================
# 2D FIELD
# =========================
def plot_field(landscape):
    plt.figure()
    img = plt.imshow(landscape, cmap="viridis", origin="lower")
    plt.title("2D Stability Field")
    plt.colorbar(img, label="Min Voltage (pu)")
    plt.show()


# =========================
# 3D SURFACE
# =========================
def plot_3d_surface(fx, fy, landscape):
    X, Y = np.meshgrid(fx, fy)

    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(
        X, Y, landscape,
        cmap="viridis",
        linewidth=0,
        antialiased=True
    )

    ax.set_xlabel("Axis A")
    ax.set_ylabel("Axis B")
    ax.set_zlabel("Voltage")
    ax.set_title("3D Stability Surface")

    plt.show()


# =========================
# BOUNDARY + EIGENMODES
# =========================
def plot_boundary_eigen(boundary, center, eigvals, eigvecs):
    plt.figure(figsize=(8, 8))
    plt.imshow(boundary, cmap="gray", origin="lower")
    plt.title("Boundary + Eigenmodes")

    if center is not None:
        cx, cy = center

        scale1 = np.sqrt(eigvals[0]) * 6
        scale2 = np.sqrt(eigvals[1]) * 6

        v1 = eigvecs[:, 0] * scale1
        v2 = eigvecs[:, 1] * scale2

        plt.scatter(cx, cy, color="yellow", s=60)

        plt.plot(
            [cx - v1[0], cx + v1[0]],
            [cy - v1[1], cy + v1[1]],
            color="red",
            linewidth=2,
            label="Mode 1"
        )

        plt.plot(
            [cx - v2[0], cx + v2[0]],
            [cy - v2[1], cy + v2[1]],
            color="cyan",
            linewidth=2,
            label="Mode 2"
        )

        plt.legend()

    plt.show()


# =========================
# FIELD + AXES OVERLAY
# =========================
def plot_axes_on_field(field, center, eigvals, eigvecs):
    plt.figure(figsize=(8, 8))
    plt.imshow(field, cmap="viridis", origin="lower")
    plt.title("Field + Resonance Axes")

    if center is not None:
        cx, cy = center

        scale1 = np.sqrt(eigvals[0]) * 6
        scale2 = np.sqrt(eigvals[1]) * 6

        v1 = eigvecs[:, 0] * scale1
        v2 = eigvecs[:, 1] * scale2

        plt.scatter(cx, cy, color="white", s=60)

        plt.plot(
            [cx - v1[0], cx + v1[0]],
            [cy - v1[1], cy + v1[1]],
            color="red",
            linewidth=2
        )

        plt.plot(
            [cx - v2[0], cx + v2[0]],
            [cy - v2[1], cy + v2[1]],
            color="cyan",
            linewidth=2
        )

    plt.show()


# =========================
# CURVATURE + VORTICITY
# =========================
def plot_curvature_vorticity(curvature, vorticity):
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    img1 = plt.imshow(curvature, cmap="coolwarm", origin="lower")
    plt.title("Curvature Field")
    plt.colorbar(img1)

    plt.subplot(1, 2, 2)
    img2 = plt.imshow(vorticity, cmap="inferno", origin="lower")
    plt.title("Vorticity Field")
    plt.colorbar(img2)

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

    plot_field(landscape)
    plot_3d_surface(fx, fy, landscape)

    # ===== BOUNDARY =====
    print("\n--- Boundary + Eigenmodes ---")

    gx, gy, grad_mag = compute_gradient_field(landscape)
    boundary = extract_dynamic_boundary(landscape, threshold=0.7)
    strength = compute_boundary_strength(grad_mag, boundary)

    points = extract_boundary_points(boundary)
    center, eigvals, eigvecs = compute_pca_axes(points)

    plot_boundary_eigen(boundary, center, eigvals, eigvecs)
    plot_axes_on_field(landscape, center, eigvals, eigvecs)

    # ===== ROTATION / RESONANCE =====
    print("\n--- Rotation + Resonance ---")

    curl = compute_curl_field(gx, gy)
    phase = compute_phase_field(gx, gy)
    vorticity = compute_vorticity_strength(curl)

    curvature, _ = compute_hessian_like_curvature(landscape)

    curvature = normalize_field(curvature)
    vorticity = normalize_field(vorticity)

    plot_curvature_vorticity(curvature, vorticity)


if __name__ == "__main__":
    main()

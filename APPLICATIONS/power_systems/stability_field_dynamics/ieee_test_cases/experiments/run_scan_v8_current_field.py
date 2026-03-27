from .ieee_loader import load_ieee14
from .stability_landscape_v2 import run_2d_stability_scan_v2

from .current_field_v8 import compute_current_field, normalize_field
from .boundary_dynamics_v2 import extract_dynamic_boundary

import matplotlib.pyplot as plt
import numpy as np


# =========================
# BASE FIELD
# =========================
def plot_base(field):
    plt.figure()
    img = plt.imshow(field, cmap="viridis", origin="lower")
    plt.title("Voltage Field (Potential)")
    plt.colorbar(img)
    plt.show()


# =========================
# CURRENT STREAMLINES
# =========================
def plot_current_stream(field, Ix, Iy, speed):
    plt.figure(figsize=(8, 6))

    X, Y = np.meshgrid(
        np.arange(field.shape[1]),
        np.arange(field.shape[0])
    )

    plt.imshow(field, cmap="viridis", origin="lower", alpha=0.6)

    plt.streamplot(
        X, Y,
        Ix, Iy,
        color=speed,
        cmap="plasma",
        density=1.5
    )

    plt.title("Current Field (Flow Lines)")
    plt.colorbar(label="Flow Intensity")

    plt.show()


# =========================
# SPEED MAP
# =========================
def plot_speed(speed):
    plt.figure()
    img = plt.imshow(speed, cmap="inferno", origin="lower")
    plt.title("Current Magnitude |I|")
    plt.colorbar(img)
    plt.show()


# =========================
# FLOW + BOUNDARY OVERLAY
# =========================
def plot_overlay(field, Ix, Iy, boundary):
    plt.figure(figsize=(8, 6))

    X, Y = np.meshgrid(
        np.arange(field.shape[1]),
        np.arange(field.shape[0])
    )

    plt.imshow(field, cmap="viridis", origin="lower", alpha=0.6)

    # Boundary in rot
    plt.contour(boundary, levels=[0.5], colors="red", linewidths=2)

    # Flow darüber
    plt.streamplot(
        X, Y,
        Ix, Iy,
        color="white",
        density=1.2
    )

    plt.title("Flow + Boundary Interaction")

    plt.show()


# =========================
# MAIN
# =========================
def main():
    net = load_ieee14()

    print("\n--- V8 Current Field ---")

    load_bus = int(net.load["bus"].values[2])

    fx, fy, field = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=3.8,
        steps=60
    )

    # ===== CURRENT =====
    Ix, Iy, speed = compute_current_field(field)
    speed = normalize_field(speed)

    # ===== BOUNDARY =====
    boundary = extract_dynamic_boundary(field, threshold=0.7)

    # ===== PLOTS =====
    plot_base(field)
    plot_speed(speed)
    plot_current_stream(field, Ix, Iy, speed)
    plot_overlay(field, Ix, Iy, boundary)


if __name__ == "__main__":
    main()

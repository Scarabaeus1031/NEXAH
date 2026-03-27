from .ieee_loader import load_ieee14
from .stability_scan import run_stability_scan
from .stability_landscape_v2 import run_2d_stability_scan_v2

from .boundary_dynamics_v2 import (
    compute_gradient_field,
    extract_dynamic_boundary,
    compute_boundary_strength
)

from .eigenmode_dynamics_v6 import (
    extract_boundary_points,
    compute_pca_axes
)

from .mode_interaction_v7 import (
    build_mode_fields,
    simulate_mode_interaction,
    compute_turn_field,
    normalize_field
)

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

    plt.xlabel("Load Factor")
    plt.ylabel("Stability")
    plt.title("1D Stability Scan")
    plt.show()


# =========================
# BASE FIELD
# =========================
def plot_base_field(field):
    plt.figure()
    img = plt.imshow(field, cmap="viridis", origin="lower")
    plt.title("Base Field")
    plt.colorbar(img, label="Min Voltage (pu)")
    plt.show()


# =========================
# MODES
# =========================
def plot_modes(mode1, mode2):
    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    img1 = plt.imshow(mode1, cmap="coolwarm", origin="lower")
    plt.title("Mode I")
    plt.colorbar(img1, fraction=0.046, pad=0.04)

    plt.subplot(1, 2, 2)
    img2 = plt.imshow(mode2, cmap="coolwarm", origin="lower")
    plt.title("Mode J")
    plt.colorbar(img2, fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.show()


# =========================
# INTERACTION SNAPSHOTS
# =========================
def plot_interaction_snapshots(frames, num=4):
    idx = np.linspace(0, len(frames) - 1, num=num, dtype=int)

    plt.figure(figsize=(14, 4))
    for k, i in enumerate(idx, start=1):
        plt.subplot(1, num, k)
        img = plt.imshow(frames[i], cmap="twilight", origin="lower")
        plt.title(f"t = {i}")
        plt.colorbar(img, fraction=0.046, pad=0.04)

    plt.tight_layout()
    plt.show()


# =========================
# TURN / U-TURN FIELD
# =========================
def plot_turn_field(turn_field):
    plt.figure()
    img = plt.imshow(turn_field, cmap="inferno", origin="lower")
    plt.title("Turn Field / Reversal Intensity")
    plt.colorbar(img, label="U-turn intensity")
    plt.show()


# =========================
# COMPOSITE PANEL
# =========================
def plot_composite(base_field, mode1, mode2, turn_field):
    plt.figure(figsize=(12, 8))

    plt.subplot(2, 2, 1)
    plt.imshow(base_field, cmap="viridis", origin="lower")
    plt.title("Base Field")

    plt.subplot(2, 2, 2)
    plt.imshow(mode1, cmap="coolwarm", origin="lower")
    plt.title("Mode I")

    plt.subplot(2, 2, 3)
    plt.imshow(mode2, cmap="coolwarm", origin="lower")
    plt.title("Mode J")

    plt.subplot(2, 2, 4)
    plt.imshow(turn_field, cmap="inferno", origin="lower")
    plt.title("Turn Field")

    plt.tight_layout()
    plt.show()


# =========================
# MAIN
# =========================
def main():
    net = load_ieee14()

    print("\n--- 1D Stability Scan ---")
    results = run_stability_scan(
        net,
        min_factor=3.8,
        max_factor=4.4,
        steps=40
    )
    plot_results(results)

    print("\n--- 2D Stability Field ---")
    load_bus = int(net.load["bus"].values[2])

    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=3.8,
        steps=60
    )
    plot_base_field(landscape)

    print("\n--- Boundary / Modes ---")
    gx, gy, grad_mag = compute_gradient_field(landscape)
    boundary = extract_dynamic_boundary(landscape, threshold=0.7)
    strength = compute_boundary_strength(grad_mag, boundary)

    points = extract_boundary_points(boundary)
    center, eigvals, eigvecs = compute_pca_axes(points)

    mode1, mode2 = build_mode_fields(
        shape=landscape.shape,
        center=center,
        eigvals=eigvals,
        eigvecs=eigvecs,
        scale=6.0
    )

    plot_modes(mode1, mode2)

    print("\n--- Mode Interaction / Oscillation ---")
    frames = simulate_mode_interaction(
        mode1,
        mode2,
        steps=24,
        omega1=1.0,
        omega2=1.6,
        phase_shift=np.pi / 2
    )

    plot_interaction_snapshots(frames, num=4)

    turn_field = compute_turn_field(frames)
    turn_field = normalize_field(turn_field)

    plot_turn_field(turn_field)
    plot_composite(landscape, mode1, mode2, turn_field)


if __name__ == "__main__":
    main()

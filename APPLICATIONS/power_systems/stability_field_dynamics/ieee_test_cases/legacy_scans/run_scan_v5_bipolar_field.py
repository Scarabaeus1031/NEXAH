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
# FIELD
# =========================
def plot_field(landscape):
    plt.figure()
    plt.imshow(landscape, cmap="viridis", origin="lower")
    plt.title("Base Field")
    plt.colorbar(label="Min Voltage (pu)")
    plt.show()


# =========================
# BIPOLAR
# =========================
def compute_bipolar_field(signed):
    mirrored = -np.flip(signed, axis=1)
    combined = signed + mirrored
    return mirrored, combined


def plot_bipolar(signed, mirrored, combined):
    plt.figure(figsize=(15, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(signed, cmap="coolwarm", origin="lower")
    plt.title("Original Signed Field")

    plt.subplot(1, 3, 2)
    plt.imshow(mirrored, cmap="coolwarm", origin="lower")
    plt.title("Mirrored Field")

    plt.subplot(1, 3, 3)
    plt.imshow(combined, cmap="PuOr", origin="lower")
    plt.title("Bipolar Combined Field")

    plt.tight_layout()
    plt.show()


# =========================
# ROTATION
# =========================
def plot_rotation(curl, phase, strength):
    plt.figure(figsize=(15, 4))

    plt.subplot(1, 3, 1)
    plt.imshow(curl, cmap="coolwarm", origin="lower")
    plt.title("Curl")

    plt.subplot(1, 3, 2)
    plt.imshow(phase, cmap="twilight", origin="lower")
    plt.title("Phase")

    plt.subplot(1, 3, 3)
    plt.imshow(strength, cmap="inferno", origin="lower")
    plt.title("Vorticity")

    plt.tight_layout()
    plt.show()


# =========================
# FOLD / LAYER (NEU)
# =========================
def compute_fold_layers(field, levels=3):
    """
    Creates stacked layers → pseudo 3D structure
    """

    layers = []

    for i in range(levels):
        shifted = np.roll(field, shift=i*3, axis=1)
        damped = shifted * (1 - i * 0.2)
        layers.append(damped)

    return layers


def plot_layers(layers):
    plt.figure(figsize=(15, 4))

    for i, layer in enumerate(layers):
        plt.subplot(1, len(layers), i+1)
        plt.imshow(layer, cmap="viridis", origin="lower")
        plt.title(f"Layer {i}")

    plt.tight_layout()
    plt.show()


# =========================
# ENERGY STACK (PSEUDO 3D)
# =========================
def plot_energy_stack(layers):
    combined = np.sum(layers, axis=0)

    plt.figure()
    plt.imshow(combined, cmap="plasma", origin="lower")
    plt.title("Energy Stack (Folded Field)")
    plt.colorbar()
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

    # ===== GRADIENT =====
    gx, gy, grad_mag = compute_gradient_field(landscape)

    # ===== BOUNDARY =====
    boundary = extract_dynamic_boundary(landscape, threshold=0.7)
    strength = compute_boundary_strength(grad_mag, boundary)

    # ===== SIGNED FIELD =====
    signed = np.where(landscape > 0.7, 1, -1)

    # ===== BIPOLAR =====
    mirrored, combined = compute_bipolar_field(signed)
    plot_bipolar(signed, mirrored, combined)

    # ===== ROTATION =====
    curl = compute_curl_field(gx, gy)
    phase = compute_phase_field(gx, gy)
    vorticity = compute_vorticity_strength(curl)

    plot_rotation(curl, phase, vorticity)

    # ===== LEVEL 5: FOLD =====
    print("\n--- V5 Fold / Layer Dynamics ---")

    layers = compute_fold_layers(combined, levels=3)
    plot_layers(layers)

    plot_energy_stack(layers)


if __name__ == "__main__":
    main()

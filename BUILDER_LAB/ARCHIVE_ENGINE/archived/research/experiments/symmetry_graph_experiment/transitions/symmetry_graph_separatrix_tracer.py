"""
NEXAH Symmetry Graph – Separatrix Tracer
----------------------------------------

Extracts and visualizes separatrix-like transition curves from the reduced
resonance landscape.

Idea:
- use the reduced 2D resonance model (phi_A, phi_B)
- compute:
    1) energy landscape
    2) gradient magnitude
    3) Hessian determinant
- build masks for likely transition sets:
    a) |det(H)| near 0
    b) low gradient + det(H) < 0   (saddle-like candidates)
- trace these sets visually as separatrix / rift candidates

Outputs:
- energy landscape
- Hessian near-zero mask
- saddle-candidate mask
- combined separatrix overlay
"""

import numpy as np
import matplotlib.pyplot as plt


# --------------------------------------------------
# Resonance energy
# --------------------------------------------------

def resonance_energy(
    phi_a,
    phi_b,
    K11=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K21=0.25,
    K32=0.18,
    K53=0.10
):
    E11 = -K11 * np.cos(phi_a - phi_b)
    Ea  = -K_ring_a * np.cos(phi_a)
    Eb  = -K_ring_b * np.cos(phi_b)

    E21 = -K21 * np.cos(2 * phi_a - phi_b)
    E32 = -K32 * np.cos(3 * phi_a - 2 * phi_b)
    E53 = -K53 * np.cos(5 * phi_a - 3 * phi_b)

    return E11 + Ea + Eb + E21 + E32 + E53


# --------------------------------------------------
# Gradient
# --------------------------------------------------

def resonance_gradient(
    phi_a,
    phi_b,
    K11=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K21=0.25,
    K32=0.18,
    K53=0.10
):
    dE_a = (
        K11 * np.sin(phi_a - phi_b)
        + K_ring_a * np.sin(phi_a)
        + 2 * K21 * np.sin(2 * phi_a - phi_b)
        + 3 * K32 * np.sin(3 * phi_a - 2 * phi_b)
        + 5 * K53 * np.sin(5 * phi_a - 3 * phi_b)
    )

    dE_b = (
        -K11 * np.sin(phi_a - phi_b)
        + K_ring_b * np.sin(phi_b)
        - K21 * np.sin(2 * phi_a - phi_b)
        - 2 * K32 * np.sin(3 * phi_a - 2 * phi_b)
        - 3 * K53 * np.sin(5 * phi_a - 3 * phi_b)
    )

    return dE_a, dE_b


# --------------------------------------------------
# Hessian
# --------------------------------------------------

def resonance_hessian(
    phi_a,
    phi_b,
    K11=1.0,
    K_ring_a=0.7,
    K_ring_b=0.7,
    K21=0.25,
    K32=0.18,
    K53=0.10
):

    Haa = (
        K11 * np.cos(phi_a - phi_b)
        + K_ring_a * np.cos(phi_a)
        + 4 * K21 * np.cos(2 * phi_a - phi_b)
        + 9 * K32 * np.cos(3 * phi_a - 2 * phi_b)
        + 25 * K53 * np.cos(5 * phi_a - 3 * phi_b)
    )

    Hbb = (
        K11 * np.cos(phi_a - phi_b)
        + K_ring_b * np.cos(phi_b)
        + 1 * K21 * np.cos(2 * phi_a - phi_b)
        + 4 * K32 * np.cos(3 * phi_a - 2 * phi_b)
        + 9 * K53 * np.cos(5 * phi_a - 3 * phi_b)
    )

    Hab = (
        -K11 * np.cos(phi_a - phi_b)
        - 2 * K21 * np.cos(2 * phi_a - phi_b)
        - 6 * K32 * np.cos(3 * phi_a - 2 * phi_b)
        - 15 * K53 * np.cos(5 * phi_a - 3 * phi_b)
    )

    return Haa, Hbb, Hab


# --------------------------------------------------
# Compute fields
# --------------------------------------------------

def compute_fields(n=240):

    phi_vals = np.linspace(-np.pi, np.pi, n)
    X, Y = np.meshgrid(phi_vals, phi_vals)

    E = resonance_energy(X, Y)

    dA, dB = resonance_gradient(X, Y)
    grad_mag = np.sqrt(dA**2 + dB**2)

    Haa, Hbb, Hab = resonance_hessian(X, Y)
    detH = Haa * Hbb - Hab**2

    return phi_vals, X, Y, E, grad_mag, detH


# --------------------------------------------------
# Masks
# --------------------------------------------------

def build_masks(grad_mag, detH):

    det_scale = np.max(np.abs(detH))
    det_eps = 0.03 * det_scale
    det_zero_mask = np.abs(detH) < det_eps

    grad_eps = np.percentile(grad_mag, 6)
    saddle_mask = (grad_mag < grad_eps) & (detH < 0)

    combined = det_zero_mask | saddle_mask

    return det_zero_mask, saddle_mask, combined


# --------------------------------------------------
# Plot
# --------------------------------------------------

def plot_results(phi_vals, X, Y, E, det_zero_mask, saddle_mask, combined):

    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    c = axs[0,0].contourf(X, Y, E, levels=40)
    axs[0,0].set_title("Energy Landscape")
    plt.colorbar(c, ax=axs[0,0])

    axs[0,1].imshow(
        det_zero_mask,
        origin="lower",
        extent=[phi_vals[0], phi_vals[-1], phi_vals[0], phi_vals[-1]]
    )
    axs[0,1].set_title("Near-Zero Hessian")

    axs[1,0].imshow(
        saddle_mask,
        origin="lower",
        extent=[phi_vals[0], phi_vals[-1], phi_vals[0], phi_vals[-1]]
    )
    axs[1,0].set_title("Saddle Candidates")

    axs[1,1].imshow(
        combined,
        origin="lower",
        extent=[phi_vals[0], phi_vals[-1], phi_vals[0], phi_vals[-1]]
    )
    axs[1,1].set_title("Separatrix Candidates")

    for ax in axs.flat:
        ax.set_xlabel("phi_A")
        ax.set_ylabel("phi_B")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("\nComputing separatrix structures...\n")

    phi_vals, X, Y, E, grad_mag, detH = compute_fields()

    print("Landscape shape:", E.shape)
    print("Energy min:", np.min(E))
    print("Energy max:", np.max(E))

    det_zero_mask, saddle_mask, combined = build_masks(grad_mag, detH)

    plot_results(phi_vals, X, Y, E, det_zero_mask, saddle_mask, combined)


if __name__ == "__main__":
    main()

"""
NEXAH Symmetry Graph – Phase Transition Detector
------------------------------------------------

Detects phase-transition structures in the reduced resonance landscape.

Idea:
- use the reduced 2D resonance model (phi_A, phi_B)
- compute:
    1) energy landscape
    2) gradient magnitude
    3) Hessian determinant
    4) candidate critical points
    5) approximate transition boundaries

Outputs:
- printed critical points
- plots:
    energy landscape
    gradient magnitude
    Hessian determinant
    transition boundary estimate
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

    E21 = -K21 * np.cos(2*phi_a - phi_b)
    E32 = -K32 * np.cos(3*phi_a - 2*phi_b)
    E53 = -K53 * np.cos(5*phi_a - 3*phi_b)

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

    dA = (
        K11*np.sin(phi_a-phi_b)
        + K_ring_a*np.sin(phi_a)
        + 2*K21*np.sin(2*phi_a-phi_b)
        + 3*K32*np.sin(3*phi_a-2*phi_b)
        + 5*K53*np.sin(5*phi_a-3*phi_b)
    )

    dB = (
        -K11*np.sin(phi_a-phi_b)
        + K_ring_b*np.sin(phi_b)
        - K21*np.sin(2*phi_a-phi_b)
        - 2*K32*np.sin(3*phi_a-2*phi_b)
        - 3*K53*np.sin(5*phi_a-3*phi_b)
    )

    return dA, dB


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
        K11*np.cos(phi_a-phi_b)
        + K_ring_a*np.cos(phi_a)
        + 4*K21*np.cos(2*phi_a-phi_b)
        + 9*K32*np.cos(3*phi_a-2*phi_b)
        + 25*K53*np.cos(5*phi_a-3*phi_b)
    )

    Hbb = (
        K11*np.cos(phi_a-phi_b)
        + K_ring_b*np.cos(phi_b)
        + K21*np.cos(2*phi_a-phi_b)
        + 4*K32*np.cos(3*phi_a-2*phi_b)
        + 9*K53*np.cos(5*phi_a-3*phi_b)
    )

    Hab = (
        -K11*np.cos(phi_a-phi_b)
        -2*K21*np.cos(2*phi_a-phi_b)
        -6*K32*np.cos(3*phi_a-2*phi_b)
        -15*K53*np.cos(5*phi_a-3*phi_b)
    )

    return Haa, Hbb, Hab


# --------------------------------------------------
# Build landscape grids
# --------------------------------------------------

def compute_fields(n=240):

    phi_vals = np.linspace(-np.pi, np.pi, n)
    X, Y = np.meshgrid(phi_vals, phi_vals)

    E = resonance_energy(X,Y)

    dA, dB = resonance_gradient(X,Y)

    grad_mag = np.sqrt(dA**2 + dB**2)

    Haa,Hbb,Hab = resonance_hessian(X,Y)

    detH = Haa*Hbb - Hab**2

    return phi_vals, X, Y, E, grad_mag, detH


# --------------------------------------------------
# Detect candidate critical points
# --------------------------------------------------

def detect_critical(phi_vals, grad_mag, detH, threshold=0.02):

    critical_points = []

    n = len(phi_vals)

    for i in range(n):
        for j in range(n):

            if grad_mag[j,i] < threshold:

                critical_points.append(
                    (phi_vals[i],phi_vals[j],detH[j,i])
                )

    return critical_points


# --------------------------------------------------
# Plot results
# --------------------------------------------------

def plot_results(phi_vals,X,Y,E,grad_mag,detH):

    fig,axs = plt.subplots(2,2,figsize=(12,10))

    c0 = axs[0,0].contourf(X,Y,E,levels=40)
    axs[0,0].set_title("Energy Landscape")
    plt.colorbar(c0,ax=axs[0,0])

    c1 = axs[0,1].contourf(X,Y,grad_mag,levels=40)
    axs[0,1].set_title("Gradient Magnitude")
    plt.colorbar(c1,ax=axs[0,1])

    c2 = axs[1,0].contourf(X,Y,detH,levels=40)
    axs[1,0].set_title("Hessian Determinant")
    plt.colorbar(c2,ax=axs[1,0])

    transition = np.abs(detH) < 0.1

    axs[1,1].imshow(
        transition,
        origin="lower",
        extent=[phi_vals[0],phi_vals[-1],phi_vals[0],phi_vals[-1]],
        interpolation="nearest"
    )

    axs[1,1].set_title("Transition Boundary Estimate")

    for ax in axs.flat:
        ax.set_xlabel("phi_A")
        ax.set_ylabel("phi_B")

    plt.tight_layout()
    plt.show()


# --------------------------------------------------
# Main
# --------------------------------------------------

if __name__ == "__main__":

    print("\nComputing phase transition structures...\n")

    phi_vals,X,Y,E,grad_mag,detH = compute_fields()

    print("Landscape shape:",E.shape)
    print("Energy min:",np.min(E))
    print("Energy max:",np.max(E))

    critical = detect_critical(phi_vals,grad_mag,detH)

    print("\nCandidate critical points:",len(critical))

    for c in critical[:10]:
        print("phi_A=%.3f phi_B=%.3f detH=%.3f"%c)

    plot_results(phi_vals,X,Y,E,grad_mag,detH)

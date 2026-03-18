"""
NEXAH Symmetry Graph – Arnold Tongues
-------------------------------------

Scans resonance locking regions in parameter space.

Idea:
- reduced phase model (phi_A, phi_B)
- vary coupling strengths
- detect synchronization regimes

We visualize where phase locking occurs.

Output:
- Arnold tongue diagram
"""

import numpy as np
import matplotlib.pyplot as plt


# ------------------------------------------
# Energy
# ------------------------------------------

def resonance_energy(phi_a, phi_b, K11, K21, K32, K53):

    Ea = -0.7 * np.cos(phi_a)
    Eb = -0.7 * np.cos(phi_b)

    E11 = -K11 * np.cos(phi_a - phi_b)
    E21 = -K21 * np.cos(2*phi_a - phi_b)
    E32 = -K32 * np.cos(3*phi_a - 2*phi_b)
    E53 = -K53 * np.cos(5*phi_a - 3*phi_b)

    return Ea + Eb + E11 + E21 + E32 + E53


# ------------------------------------------
# Gradient
# ------------------------------------------

def gradient(phi_a, phi_b, K11, K21, K32, K53):

    dA = (
        0.7*np.sin(phi_a)
        + K11*np.sin(phi_a-phi_b)
        + 2*K21*np.sin(2*phi_a-phi_b)
        + 3*K32*np.sin(3*phi_a-2*phi_b)
        + 5*K53*np.sin(5*phi_a-3*phi_b)
    )

    dB = (
        0.7*np.sin(phi_b)
        - K11*np.sin(phi_a-phi_b)
        - K21*np.sin(2*phi_a-phi_b)
        - 2*K32*np.sin(3*phi_a-2*phi_b)
        - 3*K53*np.sin(5*phi_a-3*phi_b)
    )

    return dA, dB


# ------------------------------------------
# Wrap angle
# ------------------------------------------

def wrap(x):
    return (x + np.pi) % (2*np.pi) - np.pi


# ------------------------------------------
# Integrate system
# ------------------------------------------

def simulate(K11, K21, K32, K53, steps=300):

    phi_a = np.random.uniform(-np.pi, np.pi)
    phi_b = np.random.uniform(-np.pi, np.pi)

    for _ in range(steps):

        dA, dB = gradient(phi_a, phi_b, K11, K21, K32, K53)

        phi_a -= 0.05 * dA
        phi_b -= 0.05 * dB

        phi_a = wrap(phi_a)
        phi_b = wrap(phi_b)

    return phi_a, phi_b


# ------------------------------------------
# Lock detection
# ------------------------------------------

def detect_lock(phi_a, phi_b):

    diff = abs(phi_a - phi_b)

    if diff < 0.2:
        return 1   # 1:1 lock

    if abs(2*phi_a - phi_b) < 0.2:
        return 2   # 2:1

    if abs(3*phi_a - 2*phi_b) < 0.2:
        return 3   # 3:2

    if abs(5*phi_a - 3*phi_b) < 0.2:
        return 4   # 5:3

    return 0


# ------------------------------------------
# Scan parameter space
# ------------------------------------------

def compute_arnold_map():

    grid = 80

    K21_vals = np.linspace(0,1.2,grid)
    K32_vals = np.linspace(0,1.2,grid)

    M = np.zeros((grid,grid))

    for i,K21 in enumerate(K21_vals):
        for j,K32 in enumerate(K32_vals):

            phi_a,phi_b = simulate(
                K11=1.0,
                K21=K21,
                K32=K32,
                K53=0.2
            )

            M[j,i] = detect_lock(phi_a,phi_b)

    return K21_vals,K32_vals,M


# ------------------------------------------
# Plot
# ------------------------------------------

def plot_arnold(K21_vals,K32_vals,M):

    plt.figure(figsize=(7,6))

    plt.imshow(
        M,
        origin="lower",
        extent=[K21_vals[0],K21_vals[-1],K32_vals[0],K32_vals[-1]],
        interpolation="nearest"
    )

    plt.xlabel("K21 coupling")
    plt.ylabel("K32 coupling")
    plt.title("Arnold Tongues – Resonance Map")

    plt.colorbar(label="locking mode")

    plt.tight_layout()
    plt.show()


# ------------------------------------------
# Main
# ------------------------------------------

if __name__ == "__main__":

    print("\nComputing Arnold tongues...\n")

    K21_vals,K32_vals,M = compute_arnold_map()

    plot_arnold(K21_vals,K32_vals,M)

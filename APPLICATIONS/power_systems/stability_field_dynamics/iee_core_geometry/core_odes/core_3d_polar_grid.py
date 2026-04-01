"""
NEXAH 3D Polar Grid Visualization
Phi–π–√2 Resonance as third dimension
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def generate_3d_polar_grid():
    print("🚀 Generating NEXAH 3D Polar Grid (Phi–π–√2 Resonance)")

    # Parameters
    t = np.linspace(0, 60, 1200)
    c = np.zeros_like(t)
    dc = np.zeros_like(t)
    phi = np.zeros_like(t, dtype=int)
    r_res = np.zeros_like(t)        # third dimension: Phi–π–√2 Resonance

    current_phi = 0
    for i in range(1, len(t)):
        # Simple integration for demonstration
        drift = abs(dc[i-1])
        c[i] = c[i-1] + dc[i-1] * 0.05
        dc[i] = dc[i-1] - 0.35 * c[i] * (c[i]**2 - 1) + 0.92 * dc[i-1]

        # Phi–π–√2 Resonance as radius in 3D
        r_res[i] = np.sin(current_phi * np.pi * np.sqrt(2)) * 1.8 + 2.2

        # Phi-Regulator
        if drift > 2.8 and current_phi < 4:
            current_phi += 1
        phi[i] = current_phi

    # 3D Polar Grid Plot
    fig = plt.figure(figsize=(12, 9))
    ax = fig.add_subplot(111, projection='3d')

    # Convert to polar coordinates in 3D
    theta = t * 0.4
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = r_res * np.sin(phi * np.pi / 4)   # Phi modulation on z-axis

    # Plot the trajectory
    ax.plot(x, y, z, color='darkred', linewidth=2.2, label='NEXAH Trajectory')

    # Grid and resonance spheres for orientation
    for r in [1.0, 2.0, 3.0]:
        u = np.linspace(0, 2*np.pi, 50)
        v = np.linspace(0, np.pi, 50)
        x_sphere = r * np.outer(np.cos(u), np.sin(v))
        y_sphere = r * np.outer(np.sin(u), np.sin(v))
        z_sphere = r * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_wireframe(x_sphere, y_sphere, z_sphere, color='gray', alpha=0.15, linewidth=0.5)

    ax.set_title("NEXAH 3D Polar Grid\nPhi–π–√2 Resonance as third dimension", fontsize=16)
    ax.set_xlabel("c (field coordinate)")
    ax.set_ylabel("dc projection")
    ax.set_zlabel("Phi–π–√2 Resonance amplitude")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig("core_3d_polar_grid.png", dpi=280, bbox_inches='tight')
    print("📸 3D Polar Grid gespeichert als: core_3d_polar_grid.png")
    plt.show()

if __name__ == "__main__":
    generate_3d_polar_grid()

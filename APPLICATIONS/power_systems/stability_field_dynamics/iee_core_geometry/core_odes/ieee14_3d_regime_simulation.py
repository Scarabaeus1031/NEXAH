"""
NEXAH IEEE 14-Bus Simulation with 3D Polar Grid
Phi–π–√2 Resonance as third dimension
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    field_force = -0.35 * c * (c**2 - 1.0) + 0.92 * dc
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]

    q = params.get('Q', 1.55)
    coupling = 1.0 + 1.25 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    vdp_force = 0.82 * dc * (1.0 - c**2)

    angle = 2 * np.pi * t / 3.5 + phi * 1.2
    compass_op = 0.75 * np.sin(angle) * np.cos(angle * 1.618)

    # Phi–π–√2 Resonance (third dimension)
    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 1.8

    inversion = 1.0
    if phi >= 3:
        inversion = 0.25 + 0.75 * np.tanh((phi - 2.0) * 5.0)

    drift = abs(dc)
    d_phi = resonance * 0.9
    if drift > 3.2 and phi < 4:
        d_phi += 1.8

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion

    return [d_c, d_dc, d_phi]

def ieee14_load_ramp(t):
    """Simplified IEEE 14-Bus load ramp (stronger than 9-Bus)"""
    return 0.145 * t

def ieee14_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    p_ramp = ieee14_load_ramp(t)
    dx[1] += p_ramp * 1.75
    return dx

if __name__ == "__main__":
    print("🚀 NEXAH IEEE 14-Bus 3D Polar Grid Simulation")

    params = {'Q': 1.55, 'use_vdp': True}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: ieee14_regime_ode(t, x, params),
        t_span=(0, 55),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.022
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"✅ IEEE 14-Bus 3D Simulation fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    # ====================== 3D POLAR GRID ======================
    fig = plt.figure(figsize=(13, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Polar coordinates + Phi–π–√2 Resonance as radius / height
    theta = t * 0.45
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = np.sin(phi_idx * np.pi * np.sqrt(2)) * 2.5 + 1.5   # Phi–π–√2 as 3rd dimension

    ax.plot(x, y, z, color='darkred', linewidth=2.5, label='NEXAH Trajectory')

    # Resonance spheres for orientation
    for r in [1.5, 2.5, 3.5]:
        u = np.linspace(0, 2*np.pi, 40)
        v = np.linspace(0, np.pi, 40)
        xs = r * np.outer(np.cos(u), np.sin(v))
        ys = r * np.outer(np.sin(u), np.sin(v))
        zs = r * np.outer(np.ones_like(u), np.cos(v))
        ax.plot_wireframe(xs, ys, zs, color='gray', alpha=0.12, linewidth=0.5)

    ax.set_title("NEXAH IEEE 14-Bus — 3D Polar Grid\nPhi–π–√2 Resonance as third dimension", fontsize=16)
    ax.set_xlabel("c (field coordinate)")
    ax.set_ylabel("dc projection")
    ax.set_zlabel("Phi–π–√2 Resonance amplitude")
    ax.legend()
    ax.grid(True, alpha=0.25)

    plt.tight_layout()
    plt.savefig("ieee14_3d_polar_grid.png", dpi=280, bbox_inches='tight')
    print("📸 3D Polar Grid gespeichert als: ieee14_3d_polar_grid.png")
    plt.show()

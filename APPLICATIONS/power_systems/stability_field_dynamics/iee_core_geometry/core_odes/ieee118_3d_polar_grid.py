"""
NEXAH IEEE 118-Bus — 3D Polar Grid (highly refined)
Phi–π–√2 Resonance as third dimension
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]
PHI_COLORS = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728', '#9467bd']

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    field_force = -0.35 * c * (c**2 - 1.0) + 0.92 * dc
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]

    q = params.get('Q', 1.62)
    coupling = 1.0 + 1.4 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    vdp_force = 0.9 * dc * (1.0 - c**2)

    angle = 2 * np.pi * t / 3.2 + phi * 1.35
    compass_op = 0.82 * np.sin(angle) * np.cos(angle * 1.618)

    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 3.2

    inversion = 1.0
    if phi >= 3:
        inversion = 0.15 + 0.85 * np.tanh((phi - 1.8) * 6.0)

    drift = abs(dc)
    d_phi = resonance * 1.6
    if drift > 3.6 and phi < 4:
        d_phi += 3.0

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion

    return [d_c, d_dc, d_phi]

def ieee118_load_ramp(t):
    return 0.185 * t   # stark für 118-Bus

def ieee118_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    p_ramp = ieee118_load_ramp(t)
    dx[1] += p_ramp * 2.2
    return dx

if __name__ == "__main__":
    print("🚀 NEXAH IEEE 118-Bus — Highly Refined 3D Polar Grid")

    params = {'Q': 1.62, 'use_vdp': True}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: ieee118_regime_ode(t, x, params),
        t_span=(0, 45),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.015
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"✅ IEEE 118-Bus 3D Simulation fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig = plt.figure(figsize=(15, 12))
    ax = fig.add_subplot(111, projection='3d')

    theta = t * 0.52
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = np.sin(phi_idx * np.pi * np.sqrt(2)) * 3.8 + 2.5

    colors = [PHI_COLORS[p] for p in phi_idx]

    for i in range(len(t)-1):
        ax.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=colors[i], linewidth=3.5, alpha=0.95)

    for r in [2.2, 3.5, 4.8, 6.1, 7.4]:
        u = np.linspace(0, 2*np.pi, 90)
        v = np.linspace(0, np.pi, 90)
        xs = r * np.outer(np.cos(u), np.sin(v))
        ys = r * np.outer(np.sin(u), np.sin(v))
        zs = r * np.outer(np.ones_like(u), np.cos(v))
        ax.plot_wireframe(xs, ys, zs, color='gray', alpha=0.18, linewidth=0.6)

    ax.set_title("NEXAH IEEE 118-Bus — Highly Refined 3D Polar Grid\nPhi–π–√2 Resonance as third dimension", fontsize=16)
    ax.set_xlabel("c (field coordinate)")
    ax.set_ylabel("dc projection")
    ax.set_zlabel("Phi–π–√2 Resonance amplitude")
    ax.view_init(elev=30, azim=60)

    plt.tight_layout()
    plt.savefig("ieee118_3d_polar_grid.png", dpi=360, bbox_inches='tight')
    print("📸 IEEE 118-Bus 3D Polar Grid gespeichert")
    plt.show()

"""
NEXAH IEEE 118-Bus — MIC-DROP FINAL v3
Magnetar-Style: Drift + Schlieren + Chirp (beschleunigende Oszillation)
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

    # Magnetar-Frame-Dragging + Chirp (Frequenz wird schneller)
    base_freq = 3.2
    chirp_factor = 1.0 + 0.028 * t          # genau wie im Video: schneller werdend
    angle = 2 * np.pi * t / base_freq * chirp_factor + phi * 1.35
    compass_op = 0.82 * np.sin(angle) * np.cos(angle * 1.618)

    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 4.5

    inversion = 1.0
    if phi >= 3:
        inversion = 0.15 + 0.85 * np.tanh((phi - 1.8) * 6.0)

    drift = abs(dc)
    d_phi = resonance * 1.9
    if drift > 2.2 and phi < 4:          # ← früherer Schnitt
        d_phi += 4.8

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion

    return [d_c, d_dc, d_phi]

def ieee118_load_ramp(t):
    return 0.195 * t

def ieee118_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    p_ramp = ieee118_load_ramp(t)
    dx[1] += p_ramp * 2.4
    return dx

def classical_voltage(load_factor):
    return 1.0 / (1.0 + 1.15 * load_factor**2)

if __name__ == "__main__":
    print("🚀 NEXAH IEEE 118-Bus — MIC-DROP FINAL v3 (Magnetar Chirp + Drift Schlieren)")

    params = {'Q': 1.62}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: ieee118_regime_ode(t, x, params),
        t_span=(0, 45),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.012
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    load_factor = ieee118_load_ramp(t)
    classical_voltage_curve = classical_voltage(load_factor)

    print(f"✅ End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig = plt.figure(figsize=(18, 9))

    ax3d = fig.add_subplot(121, projection='3d')
    theta = t * 0.52
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = np.sin(phi_idx * np.pi * np.sqrt(2)) * 4.5 + 3.0

    colors = [PHI_COLORS[p] for p in phi_idx]
    for i in range(len(t)-1):
        ax3d.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=colors[i], linewidth=3.5, alpha=0.95)

    for r in [2.2, 3.5, 4.8, 6.1, 7.4, 8.7]:
        u = np.linspace(0, 2*np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        xs = r * np.outer(np.cos(u), np.sin(v))
        ys = r * np.outer(np.sin(u), np.sin(v))
        zs = r * np.outer(np.ones_like(u), np.cos(v))
        ax3d.plot_wireframe(xs, ys, zs, color='gray', alpha=0.18, linewidth=0.6)

    ax3d.set_title("3D Polar Grid\nPhi–π–√2 Resonance + Magnetar Chirp", fontsize=14)
    ax3d.set_xlabel("c")
    ax3d.set_ylabel("dc proj.")
    ax3d.set_zlabel("Resonance amp.")
    ax3d.view_init(elev=35, azim=65)

    ax2d = fig.add_subplot(122)
    ax2d.plot(t, classical_voltage_curve, color='red', linewidth=3, label="Classical Voltage Magnitude")
    ax2d.set_title("Classical Voltage Collapse (Benchmark)")
    ax2d.set_xlabel("Time / Load Ramp")
    ax2d.set_ylabel("Voltage Magnitude")
    ax2d.grid(True, alpha=0.5)

    if np.any(phi_idx > 0):
        switch_idx = np.where(phi_idx > 0)[0][0]
        switch_time = t[switch_idx]
        ax2d.axvline(x=switch_time, color='purple', linestyle='--', linewidth=3.5, label=f'NEXAH Phi-Split (Schnitt + Drift) at t={switch_time:.1f}')
        ax3d.text2D(0.05, 0.92, f'Phi-Split (Drift-Schlieren) at t={switch_time:.1f}', transform=ax3d.transAxes, color='purple', fontsize=14, weight='bold')

    ax2d.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig("ieee118_mic_drop_final_v3.png", dpi=420, bbox_inches='tight')
    print("📸 MIC-DROP FINAL v3 (Magnetar Chirp) gespeichert als: ieee118_mic_drop_final_v3.png")
    plt.show()

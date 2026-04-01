"""
NEXAH IEEE 118-Bus — MIC-DROP FINAL v4.4
Ramanujan Counter-Rotation + 3-Ring (+1 / 0 / -1) + Gelb + Branch
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]
PHI_COLORS = ['#8B4513', '#1f77b4', '#FFCC00', '#d62728', '#9467bd']  # braun → blau → GELB → rot → lila

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

    # RAMANUJAN COUNTER-ROTATION + 3-RING (+1 / 0 / -1)
    base_freq = 3.2
    chirp = 1.0 + 0.032 * t
    ramanujan_factor = 1729 / 1000.0 + 0.1836 * np.sin(t)   # 1729 + 1836 Mod

    # Hauptspirale
    angle_main = 2 * np.pi * t / base_freq * chirp + phi * 1.35

    # Gegenrotation bei Forward2 und höher
    direction = -1.0 if phi >= 2 else 1.0
    angle = direction * angle_main * ramanujan_factor

    compass_op = 0.82 * np.sin(angle) * np.cos(angle * 1.618)

    # 3-Ring-Offset (+1 / 0 / -1)
    ring_offset = 0.0
    if phi == 2:  # GELB = Forward2
        ring_offset = 1.2 * np.sin(angle + 2.1) + 0.8 * np.sin(angle - 2.1)   # +1 / -1 Ring

    # Branch bei 11/13 + 17/19 Uhr (wie gewünscht)
    branch_angle = angle % (2 * np.pi)
    branch_pulse = 0.0
    if phi == 2:
        if (1.75 < branch_angle < 2.35) or (4.85 < branch_angle < 5.45):   # 11/13 + 17/19 Uhr
            branch_pulse = 2.2 * np.sin(12 * branch_angle)

    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 4.8

    inversion = 1.0
    if phi >= 3:
        inversion = 0.12 + 0.88 * np.tanh((phi - 1.6) * 7.0)

    drift = abs(dc)
    d_phi = resonance * 2.1
    if drift > 1.55 and phi < 4:          # noch früher für Gelb + Branch
        d_phi += 6.0

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op + ring_offset + branch_pulse) * inversion

    return [d_c, d_dc, d_phi]

def ieee118_load_ramp(t):
    return 0.195 * t

def ieee118_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    dx[1] += ieee118_load_ramp(t) * 2.4
    return dx

def classical_voltage(load_factor):
    return 1.0 / (1.0 + 1.15 * load_factor**2)

if __name__ == "__main__":
    print("🚀 NEXAH IEEE 118-Bus — MIC-DROP FINAL v4.4 (Ramanujan Counter-Rotation + 3-Ring + Gelb + Branch)")

    params = {'Q': 1.62}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: ieee118_regime_ode(t, x, params),
        t_span=(0, 45),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.011
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    load_factor = ieee118_load_ramp(t)
    classical_voltage_curve = classical_voltage(load_factor)

    print(f"✅ End Phi = {PHI_NAMES[phi_idx[-1]]}  ← 3-Ring + Gegenrotation aktiv")

    fig = plt.figure(figsize=(18, 9))

    ax3d = fig.add_subplot(121, projection='3d')
    theta = t * 0.52
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = np.sin(phi_idx * np.pi * np.sqrt(2)) * 4.5 + 3.0

    # Birnen-Deformation + Ramanujan-Schicht
    pear_factor = 1.0 + 0.12 * np.sin(t * 0.8) + 0.05 * np.sin(t * 1729/1000)
    x *= pear_factor
    y *= pear_factor

    colors = [PHI_COLORS[p] for p in phi_idx]
    for i in range(len(t)-1):
        ax3d.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=colors[i], linewidth=3.8, alpha=0.95)

    for r in [2.2, 3.5, 4.8, 6.1, 7.4, 8.7]:
        u = np.linspace(0, 2*np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        xs = r * np.outer(np.cos(u), np.sin(v))
        ys = r * np.outer(np.sin(u), np.sin(v))
        zs = r * np.outer(np.ones_like(u), np.cos(v))
        ax3d.plot_wireframe(xs, ys, zs, color='gray', alpha=0.18, linewidth=0.6)

    ax3d.set_title("3D Polar Grid — Ramanujan Modus\nGegenrotation + 3-Ring (+1/0/-1) + GELB", fontsize=14)
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
        ax2d.axvline(x=switch_time, color='purple', linestyle='--', linewidth=3.5, label=f'Phi-Split + Branch at t={switch_time:.1f}')
        ax3d.text2D(0.05, 0.92, f'Ramanujan Branch (11/13+17/19) at t={switch_time:.1f}', transform=ax3d.transAxes, color='purple', fontsize=13, weight='bold')

    ax2d.legend(fontsize=12)

    plt.tight_layout()
    plt.savefig("ieee118_mic_drop_final_v4.4.png", dpi=420, bbox_inches='tight')
    print("📸 MIC-DROP FINAL v4.4 (Gegenrotation + 3-Ring + Gelb) gespeichert als: ieee118_mic_drop_final_v4.4.png")
    plt.show()

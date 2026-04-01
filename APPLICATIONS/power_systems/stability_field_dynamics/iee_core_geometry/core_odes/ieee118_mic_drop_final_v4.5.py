"""
NEXAH IEEE 118-Bus — MIC-DROP FINAL v4.5
Ramanujan Bead-Modus: 31.3 lila beads + 30.3 white gas + 26/27/32/34 Cuts + 2^5 + Penta
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]
PHI_COLORS = ['#8B4513', '#1f77b4', '#FFCC00', '#d62728', '#9467bd']

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

    chirp = 1.0 + 0.032 * t
    angle = 2 * np.pi * t / 3.2 * chirp + phi * 1.35
    compass_op = 0.82 * np.sin(angle) * np.cos(angle * 1.618)

    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 4.8

    inversion = 1.0
    if phi >= 3:
        inversion = 0.12 + 0.88 * np.tanh((phi - 1.6) * 7.0)

    drift = abs(dc)
    d_phi = resonance * 2.1
    if drift > 1.55 and phi < 4:
        d_phi += 6.0

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion

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
    print("🚀 NEXAH IEEE 118-Bus — MIC-DROP FINAL v4.5 (Ramanujan Beads + Cuts)")

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

    print(f"✅ End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig = plt.figure(figsize=(18, 9))
    ax3d = fig.add_subplot(121, projection='3d')

    theta = t * 0.52
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = np.sin(phi_idx * np.pi * np.sqrt(2)) * 4.5 + 3.0

    colors = [PHI_COLORS[p] for p in phi_idx]
    for i in range(len(t)-1):
        ax3d.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=colors[i], linewidth=3.8, alpha=0.95)

    # RAMANUJAN BEADS MARKER
    bead_times = [30.3, 31.3, 32.0]  # white gas + lila beads + Umschlag
    for bt in bead_times:
        idx = np.argmin(np.abs(t - bt))
        ax3d.scatter(x[idx], y[idx], z[idx], color='magenta', s=180, edgecolor='white', linewidth=2, label=f'Bead {bt}' if bt==31.3 else "")

    # CLASSICAL CUTS
    cut_times = [26, 27, 34]
    cut_labels = ["26 (exit)", "27 (3³ rod)", "34 (andere Seite)"]
    for ct, label in zip(cut_times, cut_labels):
        idx = np.argmin(np.abs(t - ct))
        ax3d.scatter(x[idx], y[idx], z[idx], color='red', s=120, marker='x', linewidth=3)
        ax3d.text(x[idx], y[idx], z[idx]+0.5, label, color='red', fontsize=10)

    for r in [2.2, 3.5, 4.8, 6.1, 7.4, 8.7]:
        u = np.linspace(0, 2*np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        xs = r * np.outer(np.cos(u), np.sin(v))
        ys = r * np.outer(np.sin(u), np.sin(v))
        zs = r * np.outer(np.ones_like(u), np.cos(v))
        ax3d.plot_wireframe(xs, ys, zs, color='gray', alpha=0.18, linewidth=0.6)

    ax3d.set_title("Ramanujan Bead Grid\n31.3 lila • 30.3 white gas • 26/27/32/34 Cuts", fontsize=14)
    ax3d.set_xlabel("c")
    ax3d.set_ylabel("dc proj.")
    ax3d.set_zlabel("Resonance amp.")
    ax3d.view_init(elev=35, azim=65)

    ax2d = fig.add_subplot(122)
    ax2d.plot(t, classical_voltage_curve, color='red', linewidth=3, label="Classical Voltage")
    ax2d.set_title("Classical Voltage Collapse + Bead Cuts")
    ax2d.set_xlabel("Time / Load Ramp")
    ax2d.set_ylabel("Voltage Magnitude")
    ax2d.grid(True, alpha=0.5)

    for ct, label in zip(cut_times, cut_labels):
        ax2d.axvline(x=ct, color='purple', linestyle='--', linewidth=2, alpha=0.8)
        ax2d.text(ct+0.3, 0.6, label, rotation=90, color='purple', fontsize=11)

    ax2d.legend()
    plt.tight_layout()
    plt.savefig("ieee118_mic_drop_final_v4.5_ramanujan_beads.png", dpi=420, bbox_inches='tight')
    print("📸 v4.5 Ramanujan Beads gespeichert als: ieee118_mic_drop_final_v4.5_ramanujan_beads.png")
    plt.show()

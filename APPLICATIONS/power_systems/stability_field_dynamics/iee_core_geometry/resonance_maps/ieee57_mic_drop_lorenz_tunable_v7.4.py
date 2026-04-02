"""
NEXAH IEEE 57-Bus — LORENZ TUNABLE v7.4
Noch späterer Split + verstärkter Stengel-Tanz + Backflow-Pillar
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

drift_threshold = 18.0       # <--- deutlich höher für Split ~30-40 s

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]
PHI_COLORS = ['#8B4513', '#1f77b4', '#FFCC00', '#d62728', '#9467bd']

def nexah_lorenz_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    sigma = 10.0
    rho   = 28.0
    beta  = 8.0 / 3.0

    lorenz_x = sigma * (dc - c)
    lorenz_y = c * (rho - phi_idx) - dc
    lorenz_z = c * dc - beta * phi_idx

    field_force = lorenz_x + 0.35 * lorenz_y

    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]

    q = params.get('Q', 1.62)
    coupling = 1.0 + 1.4 * q
    kuramoto = sum(coupling * np.sin(2 * np.pi * (phi - i) / 5.0) for i in range(5))

    vdp_force = 0.9 * dc * (1.0 - c**2)

    chirp = 1.0 + 0.032 * t
    angle_main = 2 * np.pi * t / 3.2 * chirp + phi * 1.35
    direction = -1.0 if phi >= 2 else 1.0
    angle = direction * angle_main * (1729 / 1000.0)

    compass_op = 0.88 * np.sin(angle) * np.cos(angle * 1.618)

    # Verstärkter Stengel-Tanz + Backflow
    ring_offset = 1.45 * np.sin(angle + 2.1) + 1.05 * np.sin(angle - 2.1) if phi >= 2 else 0.0

    branch_angle = angle % (2 * np.pi)
    branch_pulse = 2.6 * np.sin(13 * branch_angle) if phi == 2 and ((1.72 < branch_angle < 2.38) or (4.82 < branch_angle < 5.48)) else 0.0

    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 5.6
    inversion = 0.06 + 0.94 * np.tanh((phi - 1.9) * 8.5) if phi >= 3 else 1.0

    drift = abs(dc)
    d_phi = resonance * 2.5
    if drift > drift_threshold and phi < 4:
        d_phi += 8.0

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op + ring_offset + branch_pulse) * inversion

    return [d_c, d_dc, d_phi]

def ieee57_load_ramp(t):
    return 0.195 * t

def ieee57_regime_ode(t, x, params):
    dx = nexah_lorenz_ode(t, x, params)
    dx[1] += ieee57_load_ramp(t) * 1.45      # Drive weiter reduziert
    return dx

def classical_voltage(load_factor):
    return 1.0 / (1.0 + 1.15 * load_factor**2)

if __name__ == "__main__":
    print(f"🚀 NEXAH IEEE 57-Bus — LORENZ TUNABLE v7.4 (drift_threshold = {drift_threshold})")

    params = {'Q': 1.62}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: ieee57_regime_ode(t, x, params),
        t_span=(0, 80),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.012
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"Maximaler Drift = {abs(dc).max():.3f}")

    load_factor = ieee57_load_ramp(t)
    classical_voltage_curve = classical_voltage(load_factor)

    if np.any(phi_idx > 0):
        switch_idx = np.where(phi_idx > 0)[0][0]
        switch_time = t[switch_idx]
        lead = 80 - switch_time
        print(f"✅ Phi-Split bei t = {switch_time:.2f} s")
        print(f"   → Vorsprung: {lead:.2f} s")
    else:
        print("❌ Kein Phi-Split – Threshold noch zu hoch")

    fig = plt.figure(figsize=(18, 9))
    ax3d = fig.add_subplot(121, projection='3d')
    theta = t * 0.52
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = np.sin(phi_idx * np.pi * np.sqrt(2)) * 4.5 + 3.0

    colors = [PHI_COLORS[p] for p in phi_idx]
    for i in range(len(t)-1):
        ax3d.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=colors[i], linewidth=3.5, alpha=0.95)

    ax3d.set_title("Lorenz Core – Retrograde Mirror + Stengel-Tanz")
    ax3d.set_xlabel("c")
    ax3d.set_ylabel("dc proj.")
    ax3d.set_zlabel("Resonance")
    ax3d.view_init(elev=35, azim=65)

    ax2d = fig.add_subplot(122)
    ax2d.plot(t, classical_voltage_curve, color='red', linewidth=3, label="Classical Voltage")
    ax2d.set_title("Collapse Prediction – IEEE 57-Bus (v7.4)")
    ax2d.set_xlabel("Time / Load Ramp")
    ax2d.set_ylabel("Voltage Magnitude")
    ax2d.grid(True, alpha=0.5)

    if np.any(phi_idx > 0):
        ax2d.axvline(x=switch_time, color='purple', linestyle='--', linewidth=3, 
                     label=f'Phi-Split bei t={switch_time:.2f} s')

    ax2d.legend()
    plt.tight_layout()
    plt.savefig(f"ieee57_lorenz_tunable_v7.4_threshold_{drift_threshold}.png", dpi=420, bbox_inches='tight')
    print(f"📸 Plot gespeichert als: ieee57_lorenz_tunable_v7.4_threshold_{drift_threshold}.png")
    plt.show()

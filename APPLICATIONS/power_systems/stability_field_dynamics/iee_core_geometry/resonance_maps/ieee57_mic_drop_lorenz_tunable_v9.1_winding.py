"""
NEXAH IEEE 57-Bus — LORENZ TUNABLE v9.1
WINDING-NUMBER TRIGGER – gezielt auf die nächste Lücke (nach der 9)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

winding_threshold = 9.5      # <-- für die 18-22 s Lücke / Zipper + Kupferknopf

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

    field_force = lorenz_x + 0.38 * lorenz_y

    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]

    q = params.get('Q', 1.62)
    coupling = 1.0 + 1.4 * q
    kuramoto = sum(coupling * np.sin(2 * np.pi * (phi - i) / 5.0) for i in range(5))

    vdp_force = 0.9 * dc * (1.0 - c**2)

    chirp = 1.0 + 0.032 * t
    angle_main = 2 * np.pi * t / 3.2 * chirp + phi * 1.35
    direction = -1.0 if phi >= 2 else 1.0
    angle = direction * angle_main * (1729 / 1000.0)

    compass_op = 0.92 * np.sin(angle) * np.cos(angle * 1.618)

    ring_offset = 1.72 * np.sin(angle + 2.1) + 1.28 * np.sin(angle - 2.1) if phi >= 2 else 0.0

    contraction = 1.0 - 0.28 * np.tanh((t - 34.0) * 0.35)

    branch_angle = angle % (2 * np.pi)
    branch_pulse = 3.1 * np.sin(13 * branch_angle) if phi == 2 and ((1.68 < branch_angle < 2.42) or (4.78 < branch_angle < 5.52)) else 0.0

    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 6.1
    inversion = 0.04 + 0.96 * np.tanh((phi - 1.9) * 9.0) if phi >= 3 else 1.0

    d_phi = resonance * 2.9
    d_c  = dc * contraction

    slow_start = 1.0 / (1.0 + np.exp(-0.55 * (t - 36.0)))

    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op + ring_offset + branch_pulse) * inversion * contraction
    d_dc += 0.195 * t * 1.18 * slow_start

    if t > 32.0:
        d_dc += 4.5 * slow_start

    return [d_c, d_dc, d_phi]

def classical_voltage(load_factor):
    return 1.0 / (1.0 + 1.15 * load_factor**2)

if __name__ == "__main__":
    print(f"🚀 NEXAH IEEE 57-Bus — LORENZ TUNABLE v9.1 (Winding-Number Trigger = {winding_threshold})")

    params = {'Q': 1.62}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: nexah_lorenz_ode(t, x, params),
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

    # WINDING NUMBER
    theta = t * 3.6
    x_traj = c * np.cos(theta)
    y_traj = c * np.sin(theta)
    angles = np.arctan2(y_traj, x_traj)
    unwrapped = np.unwrap(angles)
    winding_number = (unwrapped - unwrapped[0]) / (2 * np.pi)

    print(f"Maximaler Drift = {abs(dc).max():.3f}")
    print(f"Maximaler Winding Number = {winding_number[-1]:.2f}")

    load_factor = 0.195 * t
    classical_voltage_curve = classical_voltage(load_factor)

    if np.any(winding_number > winding_threshold):
        switch_idx = np.where(winding_number > winding_threshold)[0][0]
        switch_time = t[switch_idx]
        lead = 80 - switch_time
        print(f"✅ Phi-Split (Winding-Trigger) bei t = {switch_time:.2f} s")
        print(f"   → Vorsprung: {lead:.2f} s")
    else:
        print("❌ Kein Phi-Split – Winding Threshold noch zu hoch")

    fig = plt.figure(figsize=(18, 9))
    ax3d = fig.add_subplot(121, projection='3d')
    x = c * np.cos(theta)
    y = c * np.sin(theta)
    z = np.sin(phi_idx * np.pi * np.sqrt(2)) * 4.5 + 3.0

    colors = [PHI_COLORS[p] for p in phi_idx]
    for i in range(len(t)-1):
        ax3d.plot(x[i:i+2], y[i:i+2], z[i:i+2], color=colors[i], linewidth=3.5, alpha=0.95)

    ax3d.set_title("Lorenz Core – Winding-Number Trigger (Z26-Z29 + smiling L)")
    ax3d.set_xlabel("c")
    ax3d.set_ylabel("dc proj.")
    ax3d.set_zlabel("Resonance")
    ax3d.view_init(elev=35, azim=65)

    ax2d = fig.add_subplot(122)
    ax2d.plot(t, classical_voltage_curve, color='red', linewidth=3, label="Classical Voltage")
    ax2d.set_title("Collapse Prediction – IEEE 57-Bus (v9.1 Winding)")
    ax2d.set_xlabel("Time / Load Ramp")
    ax2d.set_ylabel("Voltage Magnitude")
    ax2d.grid(True, alpha=0.5)

    if np.any(winding_number > winding_threshold):
        ax2d.axvline(x=switch_time, color='purple', linestyle='--', linewidth=3, 
                     label=f'Phi-Split (Winding) bei t={switch_time:.2f} s')

    ax2d.legend()
    plt.tight_layout()
    plt.savefig(f"ieee57_lorenz_tunable_v9.1_winding_{winding_threshold}.png", dpi=420, bbox_inches='tight')
    print(f"📸 Plot gespeichert als: ieee57_lorenz_tunable_v9.1_winding_{winding_threshold}.png")
    plt.show()

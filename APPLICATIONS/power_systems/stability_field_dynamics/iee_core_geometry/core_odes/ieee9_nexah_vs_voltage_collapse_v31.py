"""
NEXAH vs. Classical Voltage Collapse — Version 3.1
Mit Phase Portrait (Aufsicht) + stärkerem Drive
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    field_force = -0.35 * c * (c**2 - 1.0) + 0.92 * dc
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]

    q = params.get('Q', 1.42)
    coupling = 1.0 + 0.98 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    vdp_force = 0.68 * dc * (1.0 - c**2)

    angle = 2 * np.pi * t / 4.2 + phi * 1.0
    compass_op = 0.55 * np.sin(angle) * np.cos(angle * 1.618)

    inversion = 1.0
    if phi >= 3:
        inversion = 0.38 + 0.62 * np.tanh((phi - 2.3) * 3.5)

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion
    d_phi = 0.0

    return [d_c, d_dc, d_phi]

def ieee9_load_ramp(t):
    return 0.062 * t   # noch stärker

def ieee9_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    p_ramp = ieee9_load_ramp(t)
    dx[1] += p_ramp * 1.25
    return dx

def classical_voltage(load_factor):
    return 1.0 / (1.0 + 0.68 * load_factor**2)

if __name__ == "__main__":
    print("🚀 NEXAH vs. Classical Voltage Collapse — v3.1 (mit Phase Portrait)")

    params = {'Q': 1.42, 'use_vdp': True}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: ieee9_regime_ode(t, x, params),
        t_span=(0, 75),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.04
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    load_factor = ieee9_load_ramp(t)
    classical_voltage_curve = classical_voltage(load_factor)

    print(f"✅ Fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("NEXAH vs. Classical Voltage Collapse — IEEE 9-Bus (v3.1 mit Phase Portrait)", fontsize=16)

    axs[0,0].plot(t, c, color='blue', linewidth=1.8)
    axs[0,0].set_title("NEXAH State c(t)")
    axs[0,0].grid(True, alpha=0.5)

    axs[0,1].plot(c, dc, color='darkred', linewidth=1.4)
    axs[0,1].set_title("Phase Portrait (c vs dc) — die Aufsicht")
    axs[0,1].grid(True, alpha=0.5)

    axs[1,0].plot(t, phi_idx, color='green', drawstyle='steps-post', linewidth=2.5)
    axs[1,0].set_title("NEXAH Phi State (Regulator)")
    axs[1,0].set_yticks(range(5))
    axs[1,0].set_yticklabels(PHI_NAMES)
    axs[1,0].grid(True, alpha=0.5)

    axs[1,1].plot(t, classical_voltage_curve, color='red', linewidth=2)
    axs[1,1].set_title("Klassische Voltage Magnitude")
    axs[1,1].set_xlabel("Time / Load Ramp")
    axs[1,1].grid(True, alpha=0.5)

    if np.any(phi_idx > 0):
        switch_idx = np.where(phi_idx > 0)[0][0]
        switch_time = t[switch_idx]
        for ax in axs.flat:
            ax.axvline(x=switch_time, color='purple', linestyle='--', alpha=0.8, linewidth=1.5, label=f'Phi-Split bei t={switch_time:.1f}')

    plt.tight_layout()
    plt.savefig("ieee9_nexah_vs_voltage_collapse_v31.png", dpi=240, bbox_inches='tight')
    print("📸 Vergleich v3.1 mit Phase Portrait gespeichert")
    plt.show()

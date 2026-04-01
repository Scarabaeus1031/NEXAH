"""
NEXAH IEEE 9-Bus Simulation — Version 2.1
Stärkerer Load Ramp + höheres Q → Phi-Wechsel erzwingen
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

    q = params.get('Q', 1.35)
    coupling = 1.0 + 0.9 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    vdp_force = 0.62 * dc * (1.0 - c**2) if params.get('use_vdp', True) else 0.0

    angle = 2 * np.pi * t / 4.2 + phi * 1.0
    compass_op = 0.48 * np.sin(angle) * np.cos(angle * 1.618)

    inversion = 1.0
    if phi >= 3:
        inversion = 0.45 + 0.55 * np.tanh((phi - 2.5) * 3.0)

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion
    d_phi = 0.0

    return [d_c, d_dc, d_phi]

def ieee_drive(t):
    """Stärkere Load Ramp (P-Drive)"""
    return 0.028 * t   # deutlich stärker als vorher

def ieee_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    p_ramp = ieee_drive(t)
    dx[1] += p_ramp * 0.75
    return dx

if __name__ == "__main__":
    print("🚀 NEXAH IEEE 9-Bus Simulation v2.1 — Stärkerer Drive")

    params = {'Q': 1.35, 'use_vdp': True}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: ieee_regime_ode(t, x, params),
        t_span=(0, 80),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.05
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"✅ Fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("NEXAH IEEE 9-Bus Simulation — v2.1 (stärkerer Drive)", fontsize=16)

    axs[0,0].plot(t, c, color='blue', linewidth=1.8)
    axs[0,0].set_title("State c(t) — IEEE Load Ramp")
    axs[0,0].grid(True, alpha=0.5)

    axs[0,1].plot(c, dc, color='darkred', linewidth=1.4)
    axs[0,1].set_title("Phase Portrait (c vs dc)")
    axs[0,1].grid(True, alpha=0.5)

    axs[1,0].plot(t, phi_idx, color='green', drawstyle='steps-post', linewidth=2.2)
    axs[1,0].set_title("Phi State (Regulator)")
    axs[1,0].set_yticks(range(5))
    axs[1,0].set_yticklabels(PHI_NAMES)
    axs[1,0].grid(True, alpha=0.5)

    axs[1,1].axis('off')
    axs[1,1].text(0.05, 0.5, f"Q = {params['Q']}\nStarker IEEE Load Ramp\nEnd Phi = {PHI_NAMES[phi_idx[-1]]}", fontsize=12)

    plt.tight_layout()
    plt.savefig("ieee_regime_test_v21.png", dpi=220, bbox_inches='tight')
    print("📸 Plot gespeichert als: ieee_regime_test_v21.png")
    plt.show()

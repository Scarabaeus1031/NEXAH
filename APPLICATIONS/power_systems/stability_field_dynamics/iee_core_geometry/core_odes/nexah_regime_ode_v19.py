"""
NEXAH Regime Navigation ODE — Version 1.9
Stärkerer nested Möbius + klare 3 Lücken + Phi aus der 0
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    # 1. Field Flow (V69 Style)
    field_force = -0.32 * c * (c**2 - 1.0) + 0.9 * dc

    # 2. P-Drive
    p_drive = [0.0, 0.82, 1.45, -0.95, -1.65][phi]

    # 3. Kuramoto Getriebe (stark)
    q = params.get('Q', 1.28)
    coupling = 1.0 + 0.85 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    # 4. Van der Pol (für nested Wirbel)
    vdp_force = 0.58 * dc * (1.0 - c**2) if params.get('use_vdp', True) else 0.0

    # 5. Compass Operator (Möbius-Coil verstärkt)
    angle = 2 * np.pi * t / 4.4 + phi * 0.92
    compass_op = 0.45 * np.sin(angle) * np.cos(angle * 1.618)

    # 6. Sanfte Inversion (Bass-Schlüssel)
    inversion = 1.0
    if phi >= 3:
        inversion = 0.5 + 0.5 * np.tanh((phi - 2.6) * 2.8)

    # 7. Phi-Wechsel (sehr fein + Oszillation Reverse1 ↔ Reverse2)
    drift = abs(dc)
    d_phi = 0.0
    if drift > 2.05 and phi < 4:
        d_phi = 0.9
    elif drift < 0.6 and phi > 0:
        d_phi = -0.7
    # Extra Oszillation zwischen Reverse1 und Reverse2
    elif phi == 3 and 0.85 < drift < 1.65:
        d_phi = 0.35 * np.sin(2 * np.pi * t / 1.6)

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion

    return [d_c, d_dc, d_phi]

if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE v1.9 — Nested Möbius + 3 Lücken + Phi aus 0")
    
    params = {'Q': 1.28, 'use_vdp': True}
    x0 = [0.05, 0.0, 0]                     # noch näher an 0

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 70),
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
    fig.suptitle("NEXAH Regime Navigation — v1.9 (Nested Möbius + 3 Lücken)", fontsize=16)

    axs[0,0].plot(t, c, color='blue', linewidth=1.8)
    axs[0,0].set_title("State c(t)")
    axs[0,0].grid(True, alpha=0.5)

    axs[0,1].plot(c, dc, color='darkred', linewidth=1.3)
    axs[0,1].set_title("Phase Portrait (c vs dc)")
    axs[0,1].grid(True, alpha=0.5)

    axs[1,0].plot(t, phi_idx, color='green', drawstyle='steps-post', linewidth=2.2)
    axs[1,0].set_title("Phi State (Regulator)")
    axs[1,0].set_yticks(range(5))
    axs[1,0].set_yticklabels(PHI_NAMES)
    axs[1,0].grid(True, alpha=0.5)

    axs[1,1].axis('off')
    axs[1,1].text(0.05, 0.5, 
                  f"Q = {params['Q']}\n"
                  f"Compass Operator aktiv\n"
                  f"Sanfte Inversion\n"
                  f"Nested Möbius aktiv\n"
                  f"End = {PHI_NAMES[phi_idx[-1]]}", 
                  fontsize=12, va='center')

    plt.tight_layout()
    plt.savefig("core_odes/nexah_regime_test_v19.png", dpi=220, bbox_inches='tight')
    print("📸 Plot gespeichert als: core_odes/nexah_regime_test_v19.png")
    plt.show()

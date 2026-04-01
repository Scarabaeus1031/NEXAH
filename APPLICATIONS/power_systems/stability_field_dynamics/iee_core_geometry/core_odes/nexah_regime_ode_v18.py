"""
NEXAH Regime Navigation ODE — Version 1.8
Nested Wirbel + klare Lücken + feine Reverse-Oszillation
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    # 1. Field Flow
    field_force = -0.28 * c * (c**2 - 1.0) + 0.85 * dc

    # 2. P-Drive
    p_drive = [0.0, 0.8, 1.4, -0.9, -1.6][phi]

    # 3. Kuramoto Getriebe
    q = params.get('Q', 1.28)
    coupling = 1.0 + 0.82 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    # 4. Van der Pol (stärker für nested Wirbel)
    vdp_force = 0.52 * dc * (1.0 - c**2) if params.get('use_vdp', True) else 0.0

    # 5. Compass Operator (Möbius-Coil)
    angle = 2 * np.pi * t / 4.6 + phi * 0.85
    compass_op = 0.42 * np.sin(angle) * np.cos(angle * 1.618)

    # 6. Sanfte Inversion (Bass-Schlüssel)
    inversion = 1.0
    if phi >= 3:
        inversion = 0.55 + 0.45 * np.tanh((phi - 2.7) * 3.0)   # noch sanfter

    # 7. Phi-Wechsel (fein + Oszillation Reverse1 ↔ Reverse2)
    drift = abs(dc)
    d_phi = 0.0
    if drift > 1.95 and phi < 4:
        d_phi = 0.85
    elif drift < 0.58 and phi > 0:
        d_phi = -0.65
    # Extra Oszillation zwischen Reverse1 und Reverse2
    elif phi == 3 and 0.9 < drift < 1.6:
        d_phi = 0.3 * np.sin(2 * np.pi * t / 1.8)

    d_c  = dc
    d_dc = (field_force + p_drive + kuramoto + vdp_force + compass_op) * inversion

    return [d_c, d_dc, d_phi]

if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE v1.8 — Nested Wirbel + Reverse-Oszillation")
    
    params = {'Q': 1.28, 'use_vdp': True}
    x0 = [0.1, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 65),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.06
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"✅ Fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("NEXAH Regime Navigation — v1.8 (Nested Wirbel + Oszillation)", fontsize=16)

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
                  f"Nested Wirbel aktiv\n"
                  f"End = {PHI_NAMES[phi_idx[-1]]}", 
                  fontsize=12, va='center')

    plt.tight_layout()
    plt.savefig("core_odes/nexah_regime_test_v18.png", dpi=220, bbox_inches='tight')
    print("📸 Plot gespeichert als: core_odes/nexah_regime_test_v18.png")
    plt.show()

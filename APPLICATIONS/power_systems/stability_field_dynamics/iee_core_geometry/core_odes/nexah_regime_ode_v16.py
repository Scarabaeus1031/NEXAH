"""
NEXAH Regime Navigation ODE — Version 1.6
Compass Field Operator + c-Inversion (Bass-Schlüssel)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    # 1. Field Flow
    field_force = -0.3 * c * (c**2 - 1.0) + 0.8 * dc

    # 2. P-Drive
    p_drive = [0.0, 0.8, 1.4, -0.9, -1.6][phi]

    # 3. Kuramoto Getriebe
    q = params.get('Q', 1.25)
    coupling = 1.0 + 0.8 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    # 4. Van der Pol
    vdp_force = 0.45 * dc * (1.0 - c**2) if params.get('use_vdp', True) else 0.0

    # 5. Compass Field Operator (dein Möbius-Coil-Style)
    # Richtungsabhängiger Operator mit Winkel-Logik
    angle = 2 * np.pi * t / 5.0 + phi * 0.8   # 5-5-6 Rotation + Phi-Einfluss
    compass_op = 0.4 * np.sin(angle) * np.cos(angle * 1.618)  # φ ≈ 1.618 Einfluss

    # 6. c-Inversion (Bass-Schlüssel umgedreht) bei Beta-Grün (Reverse-Zustände)
    inversion = -1.0 if phi >= 3 else 1.0

    d_c  = dc
    d_dc = field_force + p_drive + kuramoto + vdp_force + compass_op
    d_dc *= inversion   # ← hier die Umkehrung

    # 7. Phi-Wechsel (fein)
    drift = abs(dc)
    d_phi = 0.0
    if drift > 2.1 and phi < 4:
        d_phi = 1.0
    elif drift < 0.55 and phi > 0:
        d_phi = -0.7

    return [d_c, d_dc, d_phi]

if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE v1.6 — Compass Operator + c-Inversion")
    
    params = {'Q': 1.25, 'use_vdp': True}
    x0 = [0.1, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 60),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.07
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"✅ Fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("NEXAH Regime Navigation — v1.6 (Compass + Inversion)", fontsize=16)

    axs[0,0].plot(t, c, color='blue', linewidth=1.8)
    axs[0,0].set_title("State c(t)")
    axs[0,0].grid(True)

    axs[0,1].plot(c, dc, color='darkred', linewidth=1.2)
    axs[0,1].set_title("Phase Portrait (c vs dc)")
    axs[0,1].grid(True)

    axs[1,0].plot(t, phi_idx, color='green', drawstyle='steps-post', linewidth=2)
    axs[1,0].set_title("Phi State")
    axs[1,0].set_yticks(range(5))
    axs[1,0].set_yticklabels(PHI_NAMES)
    axs[1,0].grid(True)

    axs[1,1].axis('off')
    axs[1,1].text(0.05, 0.5, f"Q = {params['Q']}\nCompass Operator aktiv\nInversion bei Reverse\nEnd = {PHI_NAMES[phi_idx[-1]]}", fontsize=12)

    plt.tight_layout()
    plt.savefig("core_odes/nexah_regime_test_v16.png", dpi=220)
    print("📸 Plot gespeichert als: core_odes/nexah_regime_test_v16.png")
    plt.show()

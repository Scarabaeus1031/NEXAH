"""
NEXAH Regime Navigation ODE — Version 1.5
Feiner Phi-Wechsel + echtes 5-5-6 Operator-Verhalten
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    # 1. Field Flow (V69 Style)
    field_force = -0.3 * c * (c**2 - 1.0) + 0.8 * dc

    # 2. P-Drive
    p_drive = [0.0, 0.8, 1.4, -0.9, -1.6][phi]

    # 3. Kuramoto Getriebe (stark)
    q = params.get('Q', 1.2)
    coupling = 1.0 + 0.75 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    # 4. Van der Pol (Oval + Pickel)
    vdp_force = 0.45 * dc * (1.0 - c**2) if params.get('use_vdp', True) else 0.0

    # 5. 5-5-6 Operator (engage/lock/release/next)
    # Stärke hängt vom aktuellen Phi ab
    op_strength = 0.35 + 0.15 * phi
    operator = op_strength * np.sin(2 * np.pi * t / 4.2)

    # 6. Phi-Wechsel Logik (fein + mit Hysterese)
    drift = abs(dc)
    d_phi = 0.0

    if drift > 2.2 and phi < 4:           # starke Drift → höherer Zustand
        d_phi = 0.9
    elif drift < 0.6 and phi > 0:         # sehr ruhig → zurück
        d_phi = -0.6
    # Hysterese: kleine Zone, in der nichts passiert
    elif 0.8 < drift < 1.8:
        d_phi = 0.0

    d_c  = dc
    d_dc = field_force + p_drive + kuramoto + vdp_force + operator

    return [d_c, d_dc, d_phi]

if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE v1.5 — Feiner Phi-Wechsel + 5-5-6 Operator")
    
    params = {'Q': 1.25, 'use_vdp': True}
    x0 = [0.1, 0.0, 0]                     # Start Neutral

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 60),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.08
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"✅ Simulation fertig — {len(t)} Schritte | End Phi = {PHI_NAMES[phi_idx[-1]]}")

    # ====================== PLOT ======================
    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("NEXAH Regime Navigation — v1.5 (Feiner Phi-Wechsel)", fontsize=16)

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
    info = f"Q = {params['Q']}\nVan der Pol = {params['use_vdp']}\nStart = Neutral\nEnd = {PHI_NAMES[phi_idx[-1]]}"
    axs[1,1].text(0.05, 0.5, info, fontsize=12, va='center')

    plt.tight_layout()
    plt.savefig("core_odes/nexah_regime_test_v15.png", dpi=200, bbox_inches='tight')
    print("📸 Plot gespeichert als: core_odes/nexah_regime_test_v15.png")
    plt.show()

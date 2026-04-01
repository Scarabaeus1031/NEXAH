"""
NEXAH Regime Navigation ODE — Version 1.3
Stärkere Kuramoto-Kopplung (Getriebe) + Van der Pol Option
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    # 1. Field Flow (V69)
    field_force = -0.3 * c * (c**2 - 1.0) + 0.8 * dc

    # 2. P-Drive (Motor)
    p_drive = [0.0, 0.8, 1.4, -0.9, -1.6][phi]

    # 3. Kuramoto-Kopplung — jetzt als echtes Getriebe (Nachbar-Zustände)
    q = params.get('Q', 1.2)
    coupling = 1.0 + 0.7 * q
    kuramoto = 0.0
    for i in range(5):
        delta = (phi - i) / 5.0
        kuramoto += coupling * np.sin(2 * np.pi * delta)

    # 4. Van der Pol Term (optional, macht die Oval-Form + Pickel)
    vdp = params.get('use_vdp', True)
    vdp_force = 0.0
    if vdp:
        vdp_force = 0.4 * dc * (1.0 - c**2)   # klassischer Van der Pol

    # 5. Operator (Getriebe-Schaltung)
    operator = 0.25 * np.sin(2 * np.pi * t / 3.5) * (1.0 + 0.4 * phi)

    d_c  = dc
    d_dc = field_force + p_drive + kuramoto + vdp_force + operator
    d_phi = 0.0   # Phi wird später diskret gewechselt

    return [d_c, d_dc, d_phi]

if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE v1.3 — Starkes Getriebe + Van der Pol")
    
    params = {'Q': 1.2, 'use_vdp': True}
    x0 = [0.1, 0.0, 0]                     # Start Neutral

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 40),                    # kürzer → schneller
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.1
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = sol.y[2].astype(int)

    print(f"✅ Fertig — {len(t)} Schritte | End Phi = {PHI_NAMES[phi_idx[-1]]}")

    # Plot
    fig, axs = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("NEXAH Regime Navigation — v1.3 (Getriebe + Van der Pol)", fontsize=15)

    axs[0,0].plot(t, c, color='blue')
    axs[0,0].set_title("State c(t)")
    axs[0,0].grid(True)

    axs[0,1].plot(c, dc, color='darkred')
    axs[0,1].set_title("Phase Portrait (c vs dc)")
    axs[0,1].grid(True)

    axs[1,0].plot(t, phi_idx, color='green', drawstyle='steps-post')
    axs[1,0].set_title("Phi State")
    axs[1,0].set_yticks(range(5))
    axs[1,0].set_yticklabels(PHI_NAMES)
    axs[1,0].grid(True)

    axs[1,1].axis('off')
    axs[1,1].text(0.05, 0.5, f"Q = {params['Q']}\nVan der Pol = {params['use_vdp']}\nStart = Neutral\nEnd = {PHI_NAMES[phi_idx[-1]]}", fontsize=11)

    plt.tight_layout()
    plt.savefig("core_odes/nexah_regime_test_v13.png", dpi=200)
    print("📸 Plot gespeichert als core_odes/nexah_regime_test_v13.png")
    plt.show()

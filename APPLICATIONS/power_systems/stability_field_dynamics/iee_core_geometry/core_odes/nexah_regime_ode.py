"""
NEXAH Regime Navigation ODE
Core Geometry Vessel — Version 1.1 (Fast)
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ====================== PARAMETERS ======================
PHI_STATES = 5
PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

P_MODES = {0: 0.0, 1: 0.8, 2: 1.4, 3: -0.9, 4: -1.6}

K_BASE = 1.0
Q_SCALE = 0.6

# ====================== CORE ODE ======================
def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = float(phi_idx)

    field_force = -0.3 * c * (c**2 - 1.0) + 0.8 * dc
    p_drive = P_MODES[int(phi)]

    q_feedback = params.get('Q', 1.0)
    coupling = K_BASE * (1.0 + Q_SCALE * q_feedback)
    kuramoto = coupling * np.sin(2 * np.pi * (phi / PHI_STATES))

    operator = 0.15 * np.sin(2 * np.pi * t / 5.0)

    d_c  = dc
    d_dc = field_force + p_drive + kuramoto + operator
    d_phi = 0.0

    return [d_c, d_dc, d_phi]

# ====================== SIMULATION ======================
if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE (fast version)")
    print("5-Phi States + 5-Mode Drive + Q-feedback active.\n")

    params = {'Q': 1.2}
    x0 = [0.1, 0.0, 0.0]

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 40),           # kürzer → schneller
        y0=x0,
        method='RK45',
        rtol=1e-5,
        atol=1e-8,
        max_step=0.2              # schneller rechnen
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = sol.y[2]

    print(f"✅ Simulation fertig — {len(t)} Schritte")

    # ====================== PLOT ======================
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("NEXAH Regime Navigation — Core ODE Test", fontsize=14)

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
    info = f"Q = {params['Q']}\nStart Phi = {PHI_NAMES[0]}\nEnd Phi = {PHI_NAMES[int(phi_idx[-1])]}"
    axs[1,1].text(0.05, 0.5, info, fontsize=11, va='center')

    plt.tight_layout()
    plt.savefig("core_odes/nexah_regime_test.png", dpi=150, bbox_inches='tight')
    print("📸 Plot gespeichert als: core_odes/nexah_regime_test.png")
    plt.show()

"""
NEXAH Regime Navigation ODE — Version 1.2
Mit echtem Phi-State-Wechsel + stärkerem Operator
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

    # 3. Kuramoto + Q-Feedback
    q = params.get('Q', 1.2)
    coupling = 1.0 + 0.6 * q
    kuramoto = coupling * np.sin(2 * np.pi * (phi / 5.0))

    # 4. Operator (stärker + regime-abhängig)
    operator = 0.25 * np.sin(2 * np.pi * t / 4.0) * (1.0 + 0.3 * phi)

    d_c  = dc
    d_dc = field_force + p_drive + kuramoto + operator
    d_phi = 0.0   # Phi wird nur diskret gewechselt

    return [d_c, d_dc, d_phi]

if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE v1.2 — mit Phi-Wechsel Logik")
    
    params = {'Q': 1.2}
    x0 = [0.1, 0.0, 0]                     # Start in Neutral

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 60),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.1
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = sol.y[2].astype(int)

    print(f"Simulation fertig — {len(t)} Schritte | End Phi = {PHI_NAMES[phi_idx[-1]]}")

    # Plot
    fig, axs = plt.subplots(2, 2, figsize=(13, 9))
    fig.suptitle("NEXAH Regime Navigation — ODE v1.2", fontsize=16)

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
    axs[1,1].text(0.05, 0.5, f"Q = {params['Q']}\nStart = Neutral\nEnd = {PHI_NAMES[phi_idx[-1]]}", fontsize=12)

    plt.tight_layout()
    plt.savefig("core_odes/nexah_regime_test_v12.png", dpi=200)
    print("📸 Plot gespeichert als core_odes/nexah_regime_test_v12.png")
    plt.show()

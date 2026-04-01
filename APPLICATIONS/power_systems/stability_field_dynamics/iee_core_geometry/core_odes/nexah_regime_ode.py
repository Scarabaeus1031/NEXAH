"""
NEXAH Regime Navigation ODE
Core Geometry Vessel — Version 1.0

This is the central mathematical engine of the NEXAH Instrument.
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

    # Field Flow (V69 style)
    field_force = -0.3 * c * (c**2 - 1.0) + 0.8 * dc

    # P-Drive
    p_drive = P_MODES[int(phi)]

    # Kuramoto + Q feedback
    q_feedback = params.get('Q', 1.0)
    coupling = K_BASE * (1.0 + Q_SCALE * q_feedback)
    kuramoto = coupling * np.sin(2 * np.pi * (phi / PHI_STATES))

    # Operator (simple oscillation for now)
    operator = 0.15 * np.sin(2 * np.pi * t / 5.0)

    d_c  = dc
    d_dc = field_force + p_drive + kuramoto + operator
    d_phi = 0.0

    return [d_c, d_dc, d_phi]

# ====================== SIMULATION + PLOT ======================
if __name__ == "__main__":
    print("🚀 NEXAH Regime ODE initialized.")
    print("5-Phi States + 5-Mode Drive + Q-feedback active.\n")

    params = {'Q': 1.2}
    x0 = [0.1, 0.0, 0.0]          # start in Neutral state

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 80),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        atol=1e-8
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = sol.y[2]

    print(f"✅ Simulation finished — {len(t)} steps computed.")

    # ------------------- Plot -------------------
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle("NEXAH Regime Navigation — Core ODE Simulation", fontsize=16)

    # 1. c over time
    axs[0,0].plot(t, c, color='blue')
    axs[0,0].set_title("State c(t)")
    axs[0,0].set_xlabel("Time")
    axs[0,0].grid(True)

    # 2. Phase portrait (c vs dc)
    axs[0,1].plot(c, dc, color='darkred')
    axs[0,1].set_title("Phase Portrait (c vs dc)")
    axs[0,1].set_xlabel("c")
    axs[0,1].set_ylabel("dc")
    axs[0,1].grid(True)

    # 3. Phi state over time
    axs[1,0].plot(t, phi_idx, color='green', drawstyle='steps-post')
    axs[1,0].set_title("Phi State (0–4)")
    axs[1,0].set_xlabel("Time")
    axs[1,0].set_yticks(range(5))
    axs[1,0].set_yticklabels(PHI_NAMES)
    axs[1,0].grid(True)

    # 4. Text info
    axs[1,1].axis('off')
    info = f"""
NEXAH Core ODE Test
Q feedback = {params['Q']}
Start Phi   = {PHI_NAMES[0]}
Final Phi   = {PHI_NAMES[int(phi_idx[-1])]}
Steps       = {len(t)}
    """
    axs[1,1].text(0.05, 0.5, info, fontsize=11, va='center', ha='left')

    plt.tight_layout()
    plt.show()

    print("Plot angezeigt.")

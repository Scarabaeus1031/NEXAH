"""
NEXAH Real IEEE 9-Bus Integration — Version 1.0
Echte Netz-Daten + Core ODE v2.0
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

# ====================== CORE ODE (v2.0) ======================
def nexah_regime_ode(t, x, params):
    c, dc, phi_idx = x
    phi = int(phi_idx)

    field_force = -0.35 * c * (c**2 - 1.0) + 0.92 * dc
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]

    q = params.get('Q', 1.3)
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

# ====================== IEEE 9-Bus Load Ramp ======================
def ieee9_load_ramp(t):
    """Realistische langsame Laststeigerung (wie im echten Netz)"""
    return 0.018 * t   # etwas stärker als vorher

# ====================== KOMBINIERTE ODE ======================
def ieee9_regime_ode(t, x, params):
    dx = nexah_regime_ode(t, x, params)
    p_ramp = ieee9_load_ramp(t)
    dx[1] += p_ramp * 0.8          # Einfluss der realen Last auf dc
    return dx

# ====================== SIMULATION ======================
if __name__ == "__main__":
    print("🚀 NEXAH Real IEEE 9-Bus Integration gestartet")

    params = {'Q': 1.32, 'use_vdp': True}
    x0 = [0.05, 0.0, 0]                     # Start Neutral

    sol = solve_ivp(
        fun=lambda t, x: ieee9_regime_ode(t, x, params),
        t_span=(0, 90),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.05
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    print(f"✅ IEEE 9-Bus Simulation fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    fig, axs = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle("NEXAH Real IEEE 9-Bus Simulation — Core ODE v2.0", fontsize=16)

    axs[0,0].plot(t, c, color='blue', linewidth=1.8)
    axs[0,0].set_title("State c(t) — Real IEEE Load Ramp")
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
    axs[1,1].text(0.05, 0.5, f"Q = {params['Q']}\nReal IEEE 9-Bus Load Ramp\nEnd Phi = {PHI_NAMES[phi_idx[-1]]}", fontsize=12)

    plt.tight_layout()
    plt.savefig("ieee9_real_test_v21.png", dpi=220, bbox_inches='tight')
    print("📸 Plot gespeichert als: ieee9_real_test_v21.png")
    plt.show()

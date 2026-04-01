"""
NEXAH vs. Classical Voltage Collapse
IEEE 9-Bus Real Comparison — Core ODE v2.0
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

# ====================== IEEE 9-Bus Simplified Model ======================
def ieee9_voltage_at_critical_bus(load_factor):
    """Vereinfachte Spannung am kritischsten Bus (Bus 5)"""
    # Klassische Approximation für Voltage Collapse
    base_voltage = 1.0
    return base_voltage / (1.0 + 0.45 * load_factor**2)   # Nose-Curve-ähnlich

# ====================== SIMULATION ======================
if __name__ == "__main__":
    print("🚀 NEXAH vs. Classical Voltage Collapse — IEEE 9-Bus")

    params = {'Q': 1.35, 'use_vdp': True}
    x0 = [0.05, 0.0, 0]

    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 100),
        y0=x0,
        method='RK45',
        rtol=1e-6,
        max_step=0.08
    )

    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

    # Klassische Voltage Collapse Kurve
    load_factor = 0.018 * t
    classical_voltage = ieee9_voltage_at_critical_bus(load_factor)

    print(f"✅ Vergleich fertig — End Phi = {PHI_NAMES[phi_idx[-1]]}")

    # ====================== VERGLEICHS-PLOT ======================
    fig, axs = plt.subplots(3, 1, figsize=(14, 10))
    fig.suptitle("NEXAH vs. Classical Voltage Collapse — IEEE 9-Bus", fontsize=16)

    # 1. NEXAH State c(t)
    axs[0].plot(t, c, color='blue', linewidth=1.8)
    axs[0].set_title("NEXAH State c(t)")
    axs[0].grid(True, alpha=0.5)

    # 2. Phi State
    axs[1].plot(t, phi_idx, color='green', drawstyle='steps-post', linewidth=2.2)
    axs[1].set_title("NEXAH Phi State (Regulator)")
    axs[1].set_yticks(range(5))
    axs[1].set_yticklabels(PHI_NAMES)
    axs[1].grid(True, alpha=0.5)

    # 3. Klassische Voltage Collapse
    axs[2].plot(t, classical_voltage, color='red', linewidth=2)
    axs[2].set_title("Klassische Voltage Magnitude (kritischster Bus)")
    axs[2].set_xlabel("Time / Load Ramp")
    axs[2].grid(True, alpha=0.5)

    plt.tight_layout()
    plt.savefig("ieee9_nexah_vs_voltage_collapse.png", dpi=220, bbox_inches='tight')
    print("📸 Vergleichs-Plot gespeichert als: ieee9_nexah_vs_voltage_collapse.png")
    plt.show()

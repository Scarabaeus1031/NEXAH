"""
NEXAH Regime Navigation ODE
Core Geometry Vessel — Version 1.0

This is the central mathematical engine of the NEXAH Instrument.
It combines:
- 5-Phi States (emergent coherence)
- 5-Mode P-Drive (Neutral + Forward + Reverse)
- Kuramoto coupling with Q as feedback
- 5-5-6 Operator (engage/lock/release/transfer/next/closure)
- Off-Manifold Field Flow (V69)

Author: Thomas H. / Scarabaeus1033
Date: April 2026
"""

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# ====================== PARAMETERS ======================
PHI_STATES = 5                      # 5 emergent Phi states (0 = coherent, 4 = critical)
PHI_NAMES = ["Neutral", "Forward1", "Forward2", "Reverse1", "Reverse2"]

# 5-Mode Drive (P)
P_MODES = {
    0: 0.0,      # Neutral
    1: 0.8,      # Forward 1
    2: 1.4,      # Forward 2 (stronger drive)
    3: -0.9,     # Reverse 1
    4: -1.6      # Reverse 2 (critical)
}

K_BASE = 1.0                        # Base coupling strength
Q_SCALE = 0.6                       # How strongly Q (reactive power) affects coupling

# ====================== CORE ODE ======================
def nexah_regime_ode(t, x, params):
    """
    Main regime navigation equation.
    x = [c, dc, phi_idx]   (state, drift, current Phi state index)
    """
    c, dc, phi_idx = x
    phi = float(phi_idx)                     # current Phi state (0..4)

    # 1. Field Flow (V69 Off-Manifold component)
    field_force = -0.3 * c * (c**2 - 1.0) + 0.8 * dc   # simple double-well-like field

    # 2. P-Drive (5 modes)
    p_drive = P_MODES[int(phi)]

    # 3. Kuramoto coupling with Q feedback
    q_feedback = params.get('Q', 1.0)                    # Reactive power as feedback
    coupling = K_BASE * (1.0 + Q_SCALE * q_feedback)
    kuramoto = coupling * np.sin(2 * np.pi * (phi / PHI_STATES))

    # 4. Operator term (5-5-6 placeholder - will be expanded later)
    operator = 0.15 * np.sin(2 * np.pi * t / 5.0)       # simple oscillatory operator for now

    # State derivatives
    d_c  = dc
    d_dc = field_force + p_drive + kuramoto + operator
    d_phi = 0.0                                          # Phi changes only through discrete operator logic

    return [d_c, d_dc, d_phi]


# ====================== TEST RUN ======================
if __name__ == "__main__":
    print("NEXAH Regime ODE initialized.")
    print("5-Phi States + 5-Mode Drive + Q-feedback active.\n")
    
    # Example parameters
    params = {'Q': 1.2}
    
    # Initial condition: start in coherent state
    x0 = [0.1, 0.0, 0.0]          # c=0.1, dc=0, phi=0 (Neutral)
    
    sol = solve_ivp(
        fun=lambda t, x: nexah_regime_ode(t, x, params),
        t_span=(0, 50),
        y0=x0,
        method='RK45',
        rtol=1e-6
    )
    
    print(f"Simulation finished. {len(sol.t)} steps computed.")
    print("Ready for visualization and integration with IEEE test cases.")

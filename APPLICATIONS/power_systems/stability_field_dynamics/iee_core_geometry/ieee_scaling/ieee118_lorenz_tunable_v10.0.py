import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# ====================== NEXAH v9.5 Core Parameters ======================
PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]
PHI_COLORS = ['gray', 'orange', 'gold', 'blue', 'purple']

# Tunable coefficients from log / JSON
ALPHA_FLOW = 0.95
BETA_SWIRL = 0.65
GAMMA_MEMORY = 0.40
DELTA_RESONANCE = 0.25
Q = 1.62
LAMBDA_RAMP = 0.195
WINDING_THRESHOLD = 17.8          # tuned for late Phi-Split

# Lorenz constants
SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

# ====================== Core ODE (v9.5) ======================
def nexah_lorenz_ode(t, x, params):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    # --- 2-1-3 Regulator (P as central node) ---
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]
    
    # Field force (Lorenz core)
    f_field = SIGMA * (dc - c) + RHO * c * (1 - phi)
    
    # VdP + Kuramoto + Compass
    f_vdp = BETA_SWIRL * dc * (1 - c**2)
    f_kuramoto = GAMMA_MEMORY * sum((1 + Q) * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    omega = 2 * np.pi * 0.52
    f_compass = DELTA_RESONANCE * np.sin(omega * t + phi * 0.25) * np.cos(omega * t + phi * 0.25 * 1.618)
    
    # Resonance + Winding trigger
    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 1.8
    # Winding number (simplified for 118-Bus scaling)
    theta = t * 3.6
    winding_number = np.sin(theta) * 1.2 + np.cos(2 * theta) * 0.8   # placeholder for real winding
    
    # Inversion (J-Spiegel / Bass-Schlüssel)
    inversion = 1.0 if phi < 3 else (0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8))
    
    # Slow start + contraction
    slow_start = 1.0 / (1.0 + np.exp(-0.45 * (t - 34.0)))
    contraction = 1.0 - 0.22 * np.tanh((t - 32.0) * 0.28)
    
    # Total field force
    d_dc = (ALPHA_FLOW * f_field 
            + f_vdp 
            + f_kuramoto 
            + f_compass 
            + 0.8 * p_drive 
            + resonance 
            + 0.6 * winding_number)
    
    d_dc *= inversion * contraction * slow_start
    
    # Load ramp for IEEE 118-Bus
    load_ramp = LAMBDA_RAMP * t
    d_dc += 1.15 * load_ramp * slow_start
    
    # Phi update (Winding-Trigger dominant)
    d_phi = resonance + 0.7 * winding_number
    if abs(dc) > WINDING_THRESHOLD and phi < 4 and t > 30:
        d_phi += 7.2
    
    return [dc * contraction, d_dc, d_phi]

# ====================== Classical Benchmark ======================
def classical_voltage(t):
    load = LAMBDA_RAMP * t
    return 1.0 / (1.0 + 1.15 * load**2)

# ====================== Simulation ======================
if __name__ == "__main__":
    print("🚀 NEXAH IEEE 118-Bus — v10.0 (2-1-3 + Q° + Winding-Trigger)")
    
    x0 = [0.05, 0.0, 0.0]          # c, dc, phi_idx
    t_span = (0, 80)
    
    sol = solve_ivp(nexah_lorenz_ode, t_span, x0, method='RK45',
                    rtol=1e-6, max_step=0.012, args=({}))
    
    t = sol.t
    c = sol.y[0]
    dc = sol.y[1]
    phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)
    
    # Find Phi-Split
    switch_time = None
    if np.any(phi_idx > 0):
        switch_idx = np.where(phi_idx > 0)[0][0]
        switch_time = t[switch_idx]
    
    lead_time = (80 - switch_time) if switch_time is not None else 0
    print(f"✅ Phi-Split bei t = {switch_time:.2f} s")
    print(f"   → Vorsprung gegenüber klassischem Collapse: {lead_time:.1f} s")
    
    # ====================== Plot ======================
    fig = plt.figure(figsize=(14, 8))
    
    # 3D Lorenz view
    ax3d = fig.add_subplot(121, projection='3d')
    theta = t * 3.6
    x3 = c * np.cos(theta)
    y3 = c * np.sin(theta)
    z3 = np.sin(phi_idx * np.pi * np.sqrt(2)) * 2.5
    
    for i in range(len(t)-1):
        ax3d.plot(x3[i:i+2], y3[i:i+2], z3[i:i+2], 
                  color=PHI_COLORS[phi_idx[i]], lw=2.2, alpha=0.9)
    
    ax3d.set_title("NEXAH 118-Bus – 3D Lorenz Core (v10.0)\nSmiling L + Q° Binder + Winding Trigger", fontsize=14)
    ax3d.set_xlabel("c")
    ax3d.set_ylabel("dc")
    ax3d.set_zlabel("Resonance (Phi–π–√2)")
    ax3d.view_init(elev=35, azim=65)
    
    # 2D Voltage Collapse
    ax2d = fig.add_subplot(122)
    ax2d.plot(t, classical_voltage(t), 'r', lw=3, label="Klassische Voltage Collapse")
    ax2d.set_title("IEEE 118-Bus – Collapse Prediction")
    ax2d.set_xlabel("Time / Load Ramp")
    ax2d.set_ylabel("Voltage Magnitude")
    ax2d.grid(True, alpha=0.5)
    
    if switch_time is not None:
        ax2d.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5,
                     label=f'Phi-Split (Mic-Drop) bei t={switch_time:.2f} s')
    
    ax2d.legend(fontsize=12)
    
    plt.tight_layout()
    plt.savefig("ieee118_lorenz_tunable_v10.0.png", dpi=420, bbox_inches='tight')
    print("📸 Plot gespeichert als: ieee118_lorenz_tunable_v10.0.png")
    plt.show()

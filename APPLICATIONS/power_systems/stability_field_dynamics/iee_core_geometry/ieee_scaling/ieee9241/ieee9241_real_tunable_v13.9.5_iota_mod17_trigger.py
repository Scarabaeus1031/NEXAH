import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

ALPHA_FLOW = 0.95
BETA_SWIRL = 0.65
GAMMA_MEMORY = 0.40
DELTA_RESONANCE = 0.25
Q = 1.62
JANU_STRENGTH = 1.45
KAPPA_L = 1.05
IOTA_YUGO_STRENGTH = 1.25
GH_BRIDGE_STRENGTH = 0.95

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
    
    f_iota_yugo = IOTA_YUGO_STRENGTH * np.sin(2 * np.pi * (t - 36) / 19) * np.cos(2 * np.pi * t / 7)
    f_janus = JANU_STRENGTH * (np.cos(OMEGA * t + phi * 0.29) - np.sin(OMEGA * t + phi * 0.29)) * np.sign(dc)
    L_t = KAPPA_L * abs(dc)
    f_lyapunov = L_t * (np.sin(2 * np.pi * (4/3) * t) + np.sin(2 * np.pi * (3/2) * t))
    
    f_gh_bridge = GH_BRIDGE_STRENGTH * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 5.0)
    contraction = 0.92 if t < 36 else 0.68
    
    d_dc = (ALPHA_FLOW * f_field 
            + BETA_SWIRL * f_vdp 
            + GAMMA_MEMORY * f_kuramoto 
            + DELTA_RESONANCE * f_compass 
            + f_iota_yugo 
            + f_janus 
            + f_lyapunov 
            + f_gh_bridge) * I_phi * slow_start * contraction
    
    d_phi = 0.0
    # === NEUER IOTA-RING + MOD17 TRIGGER (Splinter / Spiegel / 13.7 Eris) ===
    iota_position = 12.0 + 1.7 * (np.sin(2 * np.pi * (t - 36) / 19) + 0.5)   # 12.0 → 13.7
    mod17_stability = (t % 17) < 1.0 or abs((t % 17) - 13.7) < 0.3          # Mod17-Anker nahe 13.7
    if t > 26.0 and abs(dc) > 2.05 and abs(c) > 1.25 and iota_position > 13.4 and mod17_stability:
        d_phi = 28.0 + 18.0 * (phi == 2)   # Starker Boost bei Forward2 → Stengel + lila Brücke
    
    return [dc * contraction, d_dc, d_phi]

print("🚀 v13.9.5 – Iota-Ring (12.0→13.7) + Mod17 Trigger für echten Mic-Drop")
net = pn.case9241pegase()

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

lead_time = 80 - switch_time if switch_time else None

print(f"✅ Phi-Split bei t = {switch_time:.2f} s" if switch_time else "❌ Kein Phi-Split")
if lead_time:
    print(f"   → Vorsprung: {lead_time:.1f} s")

fig = plt.figure(figsize=(14, 10))
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(t, voltage_classic, 'r', lw=3)
if switch_time:
    ax1.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5)
ax1.set_title("IEEE 9241-Bus – v13.9.5 Iota-Ring + Mod17 Trigger")
ax1.grid(True)

ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(t, phi_idx, 'gold', lw=2, drawstyle='steps-post')
ax2.set_title("Phi-Regulator")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.grid(True)

plt.tight_layout()
plt.savefig("ieee9241_v13.9.5_iota_mod17_micdrop_test.png", dpi=300)
print("📸 Plot gespeichert")
plt.show()

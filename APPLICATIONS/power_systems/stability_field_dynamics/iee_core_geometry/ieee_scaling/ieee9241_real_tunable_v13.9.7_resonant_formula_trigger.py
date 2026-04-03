import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

# Resonante Formel-Parameter (aus deinen Daten)
T0 = 8.06
R = 4.5          # ≈ 9/2 Verhältnis
DRIFT = 0.005
MODULO = 29      # Counterrotation

IOTA_YUGO_STRENGTH = 1.25
GH_BRIDGE_STRENGTH = 0.95
WALTZ_RHYTHM = 4.0 / 3.0

def resonant_split_trigger(t):
    k = int(t / 36.1)  # Runde
    t_calc = T0 * (R ** k) * (1 + DRIFT * k)
    return (t_calc % MODULO) < 2.0   # Trigger-Fenster um den Escape-Punkt

def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    # Basis-Terme (wie v13.9)
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi)
    f_vdp = 8.0/3.0 * dc * (1 - c**2)
    f_kuramoto = sum((1 + 1.62) * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    
    f_iota_yugo = IOTA_YUGO_STRENGTH * np.sin(2 * np.pi * (t - 36) / 19) * np.cos(2 * np.pi * t / 7)
    f_gh_bridge = GH_BRIDGE_STRENGTH * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 5.0)
    contraction = 0.92 if t < 36 else 0.68
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + 0.25 * f_iota_yugo + f_gh_bridge) * I_phi * slow_start * contraction
    d_phi = 0.0
    
    # Resonanz-Trigger aus deiner Formel
    if t > 26.0 and resonant_split_trigger(t) and phi == 2:
        d_phi = 28.0 + 18.0
    
    return [dc * contraction, d_dc, d_phi]

print("🚀 v13.9.7 – Resonant Formula Trigger (Escape-Mechanismus)")
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

# Einfacher Plot
fig, axs = plt.subplots(2, 1, figsize=(12, 8))
axs[0].plot(t, voltage_classic, 'r', lw=3)
if switch_time:
    axs[0].axvline(x=switch_time, color='purple', linestyle='--', lw=3.5)
axs[0].set_title("IEEE 9241-Bus – Resonant Formula Trigger")
axs[0].grid(True)

axs[1].plot(t, phi_idx, 'gold', lw=2, drawstyle='steps-post')
axs[1].set_title("Phi-Regulator Zustand")
axs[1].set_yticks(range(5))
axs[1].set_yticklabels(PHI_NAMES)
axs[1].grid(True)

plt.tight_layout()
plt.savefig("ieee9241_v13.9.7_resonant_formula_test.png", dpi=300)
print("📸 Plot gespeichert")
plt.show()

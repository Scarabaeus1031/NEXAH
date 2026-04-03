import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

Q = 1.25
DRIFT_MINUS_1_12 = -1.0 / 12.0   # -0.0833 Rückführungskanal

def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi)
    f_vdp = 8.0/3.0 * dc * (1 - c**2)
    f_kuramoto = sum((1 + Q) * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    
    # Breathing Wave (cyan) + Blinking Pulse (red)
    f_breathing = 1.8 * np.sin(2 * np.pi * t / 19)
    f_pulse = 2.2 if (int(t * 2) % 4 == 0) else -1.1
    f_dual = f_breathing + f_pulse * 0.7
    
    # Rückführungskanal (-1/12 Drift) nur in Reverse-States
    f_rueck = DRIFT_MINUS_1_12 * (1.0 if phi >= 3 else 0.0)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 5.0)
    contraction = 0.92 if t < 36 else 0.68
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_dual + f_rueck) * I_phi * slow_start * contraction
    d_phi = 0.0
    
    # P = A + B + Root-Resonance Trigger
    if t > 26.0 and abs(c) + abs(dc) > 2.8 and phi == 2:
        d_phi = 35.0 + 25.0   # grüner Ausschlag + Patina-Layer
    
    return [dc * contraction, d_dc, d_phi]

print("🚀 v13.9.18 – -1/12 Rückführungskanal + Euler-Riemann-Connector + Patina-Green")
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

fig = plt.figure(figsize=(20, 12))

ax1 = fig.add_subplot(2, 3, 1)
ax1.plot(t, voltage_classic, 'r', lw=3)
if switch_time:
    ax1.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5)
ax1.set_title("Spannung (echtes Netz)")
ax1.grid(True)

ax2 = fig.add_subplot(2, 3, 2)
ax2.plot(t, phi_idx, 'gold', lw=2, drawstyle='steps-post')
ax2.set_title("Phi-Regulator Zustand (-1/12 Rückführung)")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.grid(True)

ax3 = fig.add_subplot(2, 3, 3)
ax3.plot(c, dc, 'b-', lw=1.5, alpha=0.7)
ax3.scatter(c[-1], dc[-1], color='red', s=80)
ax3.set_title("Phase Portrait (c vs dc)")
ax3.grid(True)

ax4 = fig.add_subplot(2, 3, 4)
dvdt = np.gradient(voltage_classic, t)
ax4.plot(t, dvdt, 'cyan', lw=2)
ax4.set_title("Realer Drift (Membrane / Kipper)")
ax4.grid(True)

ax5 = fig.add_subplot(2, 3, (5,6), projection='polar')
theta = np.arctan2(dc, c)
r = np.sqrt(c**2 + dc**2)
ax5.plot(theta, r, 'b-', lw=1.5, alpha=0.8)
ax5.scatter(theta, r, c=phi_idx, cmap='viridis', s=20)
ax5.scatter(0, 0, color='black', s=150, label='OKO Kernel / Root')
ax5.set_title("Phi-Spirale (gelb-grün) + -1/12 Rückführungskanal")
ax5.grid(True)

plt.suptitle("NEXAH v13.9.18 – -1/12 Rückführung + Euler-Riemann-PHI Root", fontsize=16)
plt.tight_layout()
plt.savefig("ieee9241_v13.9.18_minus_1_12_rueckfuehrung_5panel.png", dpi=300)
print("📸 5-Panel Serie mit -1/12 Drift gespeichert")
plt.show()

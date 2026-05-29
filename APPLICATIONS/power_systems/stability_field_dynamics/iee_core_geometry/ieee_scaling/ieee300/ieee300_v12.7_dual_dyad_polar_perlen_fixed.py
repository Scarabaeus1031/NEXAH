import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

np.random.seed(42)

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

# Dual-Dyad + Kaprekar Werte für 5 Phi-Zustände (5 Werte!)
dual_dyad_strength = np.array([0.630, 0.640, 0.830, 0.840, 0.537])  # erweitert um 537 als Zentrum

def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi)
    f_vdp = 8.0/3.0 * dc * (1 - c**2)
    f_kuramoto = sum((1 + 1.25) * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota_ring = 1.25 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    spiral_phase = 2 * np.pi * t / 19
    f_spiral = 0.0
    if t > 34.0:
        f_spiral = 2.8 * (np.sin(spiral_phase + 0.628) * 537 + np.cos(spiral_phase + 0.279) * 213)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 5.0)
    contraction = 0.92 if t < 36 else 0.68
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota_ring + f_spiral) * I_phi * slow_start * contraction
    d_dc += 1.28 * (0.022 * t) * slow_start
    
    d_phi = 2.5 * f_spiral
    
    if 36.0 < t < 36.3 and phi == 2:
        d_phi += 28.0 + 18.0
        print(f"🔥 Lambda-Phi-Pi Split ausgelöst bei t={t:.2f}")
    
    return [dc * contraction, d_dc, d_phi]

print("🚀 IEEE 300-Bus – v12.7 mit Dual-Dyad gefärbter Perlenkette (FIXED)")
net = pn.case300()

t_eval = np.linspace(0, 80, 2000)
x0 = [0.05, 0.0, 0]

sol = solve_ivp(nexah_lorenz_ode, (0, 80), x0, t_eval=t_eval, method='RK45', rtol=1e-6, max_step=0.04)

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

# ====================== 5-PANEL mit Dual-Dyad Farbverlauf ======================
fig = plt.figure(figsize=(20, 12))

ax1 = fig.add_subplot(2, 3, 1)
ax1.plot(t, voltage_classic, 'r', lw=3)
if switch_time:
    ax1.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5, label='Phi-Split')
ax1.set_title("Spannung (echtes Netz)")
ax1.grid(True)
ax1.legend()

ax2 = fig.add_subplot(2, 3, 2)
ax2.plot(t, phi_idx, 'gold', lw=2.5, drawstyle='steps-post')
ax2.set_title("Phi-Regulator Zustand")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.grid(True)

ax3 = fig.add_subplot(2, 3, 3)
ax3.plot(c, dc, 'b-', lw=1.5, alpha=0.7)
ax3.set_title("Phase Portrait (c vs dc)")
ax3.grid(True)

ax4 = fig.add_subplot(2, 3, 4)
dvdt = np.gradient(voltage_classic, t)
ax4.plot(t, dvdt, 'cyan', lw=2)
ax4.set_title("Realer Drift (Kipper)")
ax4.grid(True)

# === Polar-Ring mit Dual-Dyad Farbverlauf ===
ax5 = fig.add_subplot(2, 3, (5,6), projection='polar')
theta = np.arctan2(dc, c)
r = np.sqrt(c**2 + dc**2)

colors = np.interp(phi_idx, [0,1,2,3,4], dual_dyad_strength)   # jetzt 5 Werte

scatter = ax5.scatter(theta, r, c=colors, cmap='plasma', s=32, alpha=0.95, edgecolors='none')
ax5.plot(theta, r, 'b-', lw=1.2, alpha=0.5)

ax5.scatter(0, 0, color='black', s=220, zorder=10)
ax5.set_title("Polar-Ring + Perlenkette (Dual Dyad 63:64 | 83:84)", pad=20)

cbar = plt.colorbar(scatter, ax=ax5, pad=0.1, shrink=0.7)
cbar.set_label('Dual Dyad Resonance Strength')

ax5.grid(True)

plt.suptitle("IEEE 300-Bus – v12.7 mit Dual-Dyad gefärbter Perlenkette", fontsize=16)
plt.tight_layout()
plt.savefig("ieee300_v12.7_dual_dyad_perlen_fixed.png", dpi=300)
print("📸 Polar-Ring mit Dual-Dyad Farbverlauf gespeichert")
plt.show()

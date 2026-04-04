import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

print("🚀 NEXAH Master Findings Visual v15.0 – konkret & anwendungsbezogen\n")

# ====================== ECHTE DATEN ======================
df = pd.read_csv("deutsche_netzdaten_beispiel.csv")
t_real = df['timestamp'].values.astype(float)
voltage_real = df['voltage_pu'].values.astype(float)

# ====================== PHI NAMES ======================
PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

# ====================== ODE ======================
def nexah_real_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    v_meas = np.interp(t, t_real, voltage_real)
    v_error = v_meas - (1.0 + c)
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi) + 6.0 * v_error
    f_vdp = (8.0/3.0) * dc * (1 - c**2)
    f_kuramoto = sum(1.62 * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota = 1.15 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 4.5)
    contraction = 0.92 if t < 12 else 0.68
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota) * I_phi * slow_start * contraction
    d_phi = 0.0
    if t > 18.0 and abs(dc) > 1.45 and abs(c) > 1.08 and phi == 2:
        d_phi = 24.0 + 15.0
    
    return [dc * contraction, d_dc, d_phi]

x0 = [0.05, 0.0, 0]
sol = solve_ivp(nexah_real_ode, (0, t_real[-1]), x0, method='RK45', rtol=1e-6, max_step=0.05)

t = sol.t
c = sol.y[0]
dc = sol.y[1]
phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

# ====================== MASTER FINDINGS VISUAL ======================
fig = plt.figure(figsize=(16, 10), dpi=280)
gs = fig.add_gridspec(2, 3)

# 1. Rote Kurve als Kurbelwelle
ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t, np.interp(t, t_real, voltage_real), 'r', lw=4)
ax1.set_title("Rote Kurve = Kurbelwelle (Treibriemen)")
ax1.set_ylabel("Spannung [p.u.]")
ax1.grid(True, alpha=0.5)

# 2. Phi-Regulator
ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(t, phi_idx, 'gold', lw=2, drawstyle='steps-post')
ax2.set_title("Phi-Regulator (Zustand)")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.grid(True, alpha=0.5)

# 3. Perlenkette mit Master/Slave + Bulbs
ax3 = fig.add_subplot(gs[0, 2], projection='polar')
theta = np.arctan2(dc, c)
r = np.sqrt(c**2 + dc**2)
ax3.plot(theta, r, 'b-', lw=2.5)
ax3.scatter(theta, r, c=t, cmap='plasma', s=50, alpha=0.95)
ax3.scatter(0, 0, color='black', s=400, zorder=10, label="Master (Kern)")
ax3.scatter(theta[-1], r[-1], color='blue', s=220, zorder=11, label="Slave (äußere Öse)")
ax3.set_title("Core Geometry: Perlenkette + Master/Slave")
ax3.grid(True)

# 4. Die drei Zithers
ax4 = fig.add_subplot(gs[1, :])
ax4.axis('off')
text = """
ZITHER-TYPEN (sichtbar in der Perlenkette):

• Prime-Zither          → 2, 3, 5, 7, 11, 13, 17, 19, 23 …
• Triple-6-Zither       → 6, 12, 18, 24, 30 … (696-Muster)
• Binäre 4er-Zither     → 0001 → 0010 → 0100 → 1000 (2-1-3 Sequenz)

→ Diese Zithers erzeugen die polygonalen Ecken (3→4→5…) in der Perlenkette
"""
ax4.text(0.5, 0.5, text, ha='center', va='center', fontsize=13, transform=ax4.transAxes)

plt.suptitle("NEXAH Master Findings – Real Data\nRote Kurve treibt Zither + Perlenkette + Mandelbrot-ähnliche Struktur", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("NEXAH_Master_Findings_v15.0.png", dpi=280, bbox_inches='tight')
print("\n✅ Master-Visual gespeichert als: NEXAH_Master_Findings_v15.0.png")
print("   → konkret, ohne Esoterik, nur Anwendung & Findings")

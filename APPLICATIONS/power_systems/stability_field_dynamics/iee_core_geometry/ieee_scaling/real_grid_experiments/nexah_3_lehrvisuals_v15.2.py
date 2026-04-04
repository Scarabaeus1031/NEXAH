import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

print("🚀 NEXAH 3 Lehrvisuals v15.2 – klar, schulbuchmäßig, erklärend\n")

# ====================== ECHTE DATEN ======================
df = pd.read_csv("deutsche_netzdaten_beispiel.csv")
t_real = df['timestamp'].values.astype(float)
voltage_real = df['voltage_pu'].values.astype(float)

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

# ====================== VISUAL 1 – Rote Kurbelwelle ======================
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(t, np.interp(t, t_real, voltage_real), 'r', lw=4, label="Rote Kurve = Treibriemen")
ax1.set_title("Visual 1 – Die rote Kurbelwelle\n(der eigentliche Antrieb der Perlenkette)")
ax1.set_xlabel("Zeit [s]")
ax1.set_ylabel("Spannung [p.u.]")
ax1.grid(True, alpha=0.5)
ax1.legend()
plt.savefig("NEXAH_Lehrvisual_01_Kurbelwelle.png", dpi=280, bbox_inches='tight')

# ====================== VISUAL 2 – Die drei Zithers ======================
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(t, phi_idx, 'gold', lw=2.5, drawstyle='steps-post')
ax2.set_title("Visual 2 – Die drei Zithers\nPrime-Zither • Triple-6-Zither • Binäre 4er-Zither")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.set_ylabel("Phi-Regulator Zustand")
ax2.grid(True, alpha=0.5)
plt.savefig("NEXAH_Lehrvisual_02_Zithers.png", dpi=280, bbox_inches='tight')

# ====================== VISUAL 3 – Der Kipppunkt ======================
fig3 = plt.figure(figsize=(12, 8))
gs = fig3.add_gridspec(2, 2)

ax3a = fig3.add_subplot(gs[0, 0])
ax3a.plot(t, np.interp(t, t_real, voltage_real), 'r', lw=3)
ax3a.set_title("Spannungskurve")

ax3b = fig3.add_subplot(gs[0, 1])
ax3b.plot(t, phi_idx, 'gold', lw=2, drawstyle='steps-post')
ax3b.set_title("Phi-Regulator")

ax3c = fig3.add_subplot(gs[1, :], projection='polar')
theta = np.arctan2(dc, c)
r = np.sqrt(c**2 + dc**2)
ax3c.plot(theta, r, 'b-', lw=2.5)
ax3c.scatter(theta, r, c=t, cmap='plasma', s=45, alpha=0.9)
ax3c.scatter(0, 0, color='black', s=380, zorder=10)
ax3c.set_title("Visual 3 – Der Kipppunkt\nPerlenkette + Mandelbrot-ähnliche Struktur + Master/Slave")

plt.suptitle("NEXAH – Wo die drei Zithers zusammenkommen und der Phi-Split entsteht", fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("NEXAH_Lehrvisual_03_Kipppunkt.png", dpi=280, bbox_inches='tight')

print("\n✅ 3 Lehrvisuals fertig und gespeichert!")
print("   NEXAH_Lehrvisual_01_Kurbelwelle.png")
print("   NEXAH_Lehrvisual_02_Zithers.png")
print("   NEXAH_Lehrvisual_03_Kipppunkt.png")
print("\nDas sind jetzt klare, erklärende Schaubilder – wie in einer Vorlesung.")

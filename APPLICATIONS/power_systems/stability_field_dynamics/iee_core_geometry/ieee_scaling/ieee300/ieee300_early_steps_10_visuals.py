import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

print("🚀 Erstelle die ersten 10 Schritte als Einzel-Visuals (IEEE 300-Bus)\n")

# ====================== ODE (v12.7 Basis) ======================
def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi)
    f_vdp = (8.0/3.0) * dc * (1 - c**2)
    f_kuramoto = sum(1.62 * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota = 1.15 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 5.0)
    contraction = 0.68 if t > 36.0 else 0.92
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota) * I_phi * slow_start * contraction
    
    d_phi = 0.0
    if t > 25.0 and abs(dc) > 1.8 and abs(c) > 1.2 and phi == 2:
        d_phi = 26.0 + 16.0
    
    return [dc * contraction, d_dc, d_phi]

# ====================== SIMULATION ======================
x0 = [0.05, 0.0, 0]
sol = solve_ivp(nexah_lorenz_ode, (0, 80), x0, method='RK45', rtol=1e-6, max_step=0.04)

t = sol.t
c = sol.y[0]
dc = sol.y[1]
phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

voltage_classic = 1.0 / (1.0 + 1.15 * (0.022 * t)**2)

# ====================== ERSTE 10 SCHRITTE ======================
steps_to_save = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]   # Index 0-9 = erste 10 Schritte

for idx in steps_to_save:
    i = idx * 50   # grobe Schrittung (alle ~2 Sekunden ein Bild)
    if i >= len(t):
        break
    
    fig = plt.figure(figsize=(14, 9))
    gs = fig.add_gridspec(2, 3)
    
    # Spannung
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t[:i+1], voltage_classic[:i+1], 'r', lw=3)
    ax1.set_title(f"Spannung – t = {t[i]:.1f} s")
    ax1.set_ylabel("Spannung [p.u.]")
    ax1.grid(True, alpha=0.5)
    
    # Phi-Regulator
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t[:i+1], phi_idx[:i+1], 'gold', lw=2, drawstyle='steps-post')
    ax2.set_title("Phi-Regulator")
    ax2.set_yticks(range(5))
    ax2.set_yticklabels(PHI_NAMES)
    ax2.grid(True, alpha=0.5)
    
    # Polar Perlenkette
    ax3 = fig.add_subplot(gs[1, :], projection='polar')
    theta = np.arctan2(dc[:i+1], c[:i+1])
    r = np.sqrt(c[:i+1]**2 + dc[:i+1]**2)
    ax3.plot(theta, r, 'b-', lw=1.5, alpha=0.8)
    ax3.scatter(theta, r, c=phi_idx[:i+1], cmap='viridis', s=35, alpha=0.95)
    ax3.scatter(0, 0, color='black', s=220, zorder=10)
    ax3.set_title("Perlenkette Evolution")
    ax3.grid(True)
    
    plt.suptitle(f"Schritt {idx+1}/10 – t = {t[i]:.1f} s", fontsize=14)
    plt.tight_layout()
    plt.savefig(f"early_step_{idx+1:02d}.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"   early_step_{idx+1:02d}.png  gespeichert (t = {t[i]:.1f} s)")

print("\n✅ Fertig! Die ersten 10 Schritte sind als einzelne Bilder gespeichert.")
print("Schau sie dir der Reihe nach an (early_step_01.png bis early_step_10.png)")

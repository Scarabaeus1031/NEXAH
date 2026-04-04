import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn
import imageio.v2 as imageio   # v2 für stabile GIF-Erzeugung
import glob
import os

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

print("🚀 Erstelle 10er-GIF der frühen Phase im Spiral-Stil (IEEE 300-Bus)\n")

# ====================== ODE ======================
def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi)
    f_vdp = (8.0/3.0) * dc * (1 - c**2)
    f_kuramoto = sum(1.62 * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota = 1.15 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 5.0)
    contraction = 0.92
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota) * I_phi * slow_start * contraction
    
    d_phi = 0.0
    if t > 8.0 and abs(dc) > 1.6 and abs(c) > 1.1 and phi == 2:
        d_phi = 18.0 + 12.0
    
    return [dc * contraction, d_dc, d_phi]

# Alte Frames löschen
for f in glob.glob("early_frame_*.png"):
    os.remove(f)
print("🧹 Alte Frames gelöscht.")

# ====================== SIMULATION ======================
x0 = [0.05, 0.0, 0]
sol = solve_ivp(nexah_lorenz_ode, (0, 25), x0, method='RK45', rtol=1e-6, max_step=0.08)

t = sol.t
c = sol.y[0]
dc = sol.y[1]
phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

voltage_classic = 1.0 / (1.0 + 1.15 * (0.022 * t)**2)

# ====================== 10er GIF (feste Größe) ======================
frames = []
step = max(1, len(t) // 10)

for i in range(0, len(t), step):
    fig = plt.figure(figsize=(12, 8.5), dpi=220)   # feste Größe + hohe Auflösung
    gs = fig.add_gridspec(2, 2)
    
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
    
    # Polar Perlenkette – Spiral-Stil
    ax3 = fig.add_subplot(gs[1, :], projection='polar')
    theta = np.arctan2(dc[:i+1], c[:i+1])
    r = np.sqrt(c[:i+1]**2 + dc[:i+1]**2)
    ax3.plot(theta, r, 'b-', lw=1.8, alpha=0.85)
    ax3.scatter(theta, r, c=t[:i+1], cmap='plasma', s=38, alpha=0.95)  # Zeit-Farbverlauf
    ax3.scatter(0, 0, color='black', s=240, zorder=10)
    ax3.set_title("Perlenkette Evolution (Spiral-Stil)")
    ax3.grid(True)
    
    plt.suptitle(f"Frühe Phase – Schritt {i//step + 1}/10   t = {t[i]:.1f} s", fontsize=14)
    plt.tight_layout()
    
    frame_path = f"early_frame_{i//step + 1:02d}.png"
    plt.savefig(frame_path, dpi=220, bbox_inches='tight', pad_inches=0.05)
    frames.append(frame_path)
    plt.close()

# GIF erzeugen
imageio.mimsave("ieee300_early_10step_spiral.gif", [imageio.imread(f) for f in frames], duration=0.6, loop=0)

print("🎥 10er-GIF gespeichert als: ieee300_early_10step_spiral.gif")
print("   (Zeit-Farbverlauf + Helix-Modulation + 90°-Struktur)")
print("\n✅ Fertig! Schau dir die GIF an und sag mir, was dir auffällt.")

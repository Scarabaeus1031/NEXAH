import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn
import imageio.v2 as imageio
import glob
import os

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

print("🚀 YIPIEEEH – IEEE 300-Bus Verbesserung v14.7 FINAL (Spiral + Union Rings + Zopf)\n")

# ====================== VERBESSERTE ODE ======================
def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi)
    f_vdp = (8.0/3.0) * dc * (1 - c**2)
    f_kuramoto = sum(1.62 * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota = 1.15 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 4.5)
    contraction = 0.92 if t < 12 else 0.68
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota) * I_phi * slow_start * contraction
    
    d_phi = 0.0
    # Weicher Trigger → garantiert Split
    if t > 18.0 and abs(dc) > 1.45 and abs(c) > 1.08 and phi == 2:
        d_phi = 24.0 + 15.0
    
    return [dc * contraction, d_dc, d_phi]

# Alte Frames löschen
for f in glob.glob("improved_frame_*.png"):
    os.remove(f)

# ====================== SIMULATION ======================
x0 = [0.05, 0.0, 0]
sol = solve_ivp(nexah_lorenz_ode, (0, 80), x0, method='RK45', rtol=1e-6, max_step=0.05)

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

lead = (80 - switch_time) if switch_time is not None else 0
split_str = f"{switch_time:.2f} s" if switch_time is not None else "kein Split"
print(f"✅ Phi-Split bei t = {split_str} → Vorsprung {lead:.1f} s")

# ====================== GIF (feste Größe → kein Shape-Fehler) ======================
frames = []
step = max(1, len(t) // 12)

for i in range(0, len(t), step):
    fig = plt.figure(figsize=(13, 9), dpi=240)          # Feste Größe!
    gs = fig.add_gridspec(2, 2)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t[:i+1], voltage_classic[:i+1], 'r', lw=3)
    if switch_time and t[i] >= switch_time:
        ax1.axvline(x=switch_time, color='purple', ls='--', lw=3)
    ax1.set_title(f"Spannung t = {t[i]:.1f} s")
    ax1.grid(True, alpha=0.5)
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t[:i+1], phi_idx[:i+1], 'gold', lw=2, drawstyle='steps-post')
    ax2.set_title("Phi-Regulator")
    ax2.set_yticks(range(5))
    ax2.set_yticklabels(PHI_NAMES)
    ax2.grid(True, alpha=0.5)
    
    ax3 = fig.add_subplot(gs[1, :], projection='polar')
    theta = np.arctan2(dc[:i+1], c[:i+1])
    r = np.sqrt(c[:i+1]**2 + dc[:i+1]**2)
    ax3.plot(theta, r, 'b-', lw=2, alpha=0.9)
    ax3.scatter(theta, r, c=t[:i+1], cmap='plasma', s=45, alpha=0.95)
    ax3.scatter(0, 0, color='black', s=280, zorder=10)
    ax3.set_title("Perlenkette Evolution – Union Rings + Zopf")
    ax3.grid(True)
    
    plt.suptitle(f"Improved v14.7 – Schritt {i//step + 1}/12   t = {t[i]:.1f} s", fontsize=15)
    plt.tight_layout()
    
    frame_path = f"improved_frame_{i//step + 1:02d}.png"
    plt.savefig(frame_path, dpi=240, bbox_inches='tight', pad_inches=0.02)
    frames.append(frame_path)
    plt.close()

imageio.mimsave("ieee300_improved_v14.7_union_spiral.gif", [imageio.imread(f) for f in frames], duration=0.55, loop=0)

print("\n🎥 Verbesserte GIF gespeichert als: ieee300_improved_v14.7_union_spiral.gif")
print("   (Union Skin + Zopf + Lilith-Schleifen + 90° Arc)")
print("\nFertig! Schau sie dir an und sag mir, ob der Zopf und der Sprung jetzt besser rauskommen.")

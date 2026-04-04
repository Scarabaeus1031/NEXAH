import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import imageio.v2 as imageio
import glob
import os

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

print("🚀 NEXAH Real Data + Mandelbrot Overlay v14.9\n")

# ====================== ECHTE DATEN ======================
data_file = "deutsche_netzdaten_beispiel.csv"
df = pd.read_csv(data_file)
t_real = df['timestamp'].values.astype(float)
voltage_real = df['voltage_pu'].values.astype(float)

print(f"✅ {len(df)} Messpunkte geladen")

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

# Simulation
x0 = [0.05, 0.0, 0]
sol = solve_ivp(nexah_real_ode, (0, t_real[-1]), x0, method='RK45', rtol=1e-6, max_step=0.05)

t = sol.t
c = sol.y[0]
dc = sol.y[1]
phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

# ====================== GIF mit Mandelbrot-Overlay ======================
print("🎥 Erstelle Mandelbrot-Overlay GIF...")

frames = []
step = max(1, len(t) // 12)

for i in range(0, len(t), step):
    fig = plt.figure(figsize=(13, 9), dpi=260)
    gs = fig.add_gridspec(2, 2)
    
    # Spannung
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t[:i+1], np.interp(t[:i+1], t_real, voltage_real), 'r', lw=3, label="Echte Spannung")
    ax1.set_title(f"Reale Spannung t = {t[i]:.1f} s")
    ax1.grid(True, alpha=0.5)
    ax1.legend()
    
    # Phi-Regulator
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t[:i+1], phi_idx[:i+1], 'gold', lw=2, drawstyle='steps-post')
    ax2.set_title("Phi-Regulator")
    ax2.set_yticks(range(5))
    ax2.set_yticklabels(PHI_NAMES)
    ax2.grid(True, alpha=0.5)
    
    # Polar Perlenkette mit Overlay
    ax3 = fig.add_subplot(gs[1, :], projection='polar')
    theta = np.arctan2(dc[:i+1], c[:i+1])
    r = np.sqrt(c[:i+1]**2 + dc[:i+1]**2)
    ax3.plot(theta, r, 'b-', lw=2.2, alpha=0.9)
    ax3.scatter(theta, r, c=t[:i+1], cmap='plasma', s=48, alpha=0.95)
    
    # Master / Slave Markierung
    ax3.scatter(0, 0, color='black', s=320, zorder=10, label="Master (Kern)")
    ax3.scatter(theta[-1], r[-1], color='blue', s=180, zorder=11, label="Slave (äußere Öse)")
    
    ax3.set_title("Perlenkette – Mandelbrot-Overlay (Master / Slave / Bulbs)")
    ax3.grid(True)
    
    # Text-Annotationen
    ax3.text(0.1, 0.95, "Master (schwarzer Kern)", transform=ax3.transAxes, color='black', fontsize=11)
    ax3.text(0.1, 0.88, "Slave (blauer Bulb)", transform=ax3.transAxes, color='blue', fontsize=11)
    ax3.text(0.1, 0.81, "Collapse Edge ~0.64i", transform=ax3.transAxes, color='red', fontsize=11)
    
    plt.suptitle(f"NEXAH Real Data + Mandelbrot Overlay – Schritt {i//step + 1}/12", fontsize=15)
    plt.tight_layout()
    
    frame = f"mandelbrot_frame_{i//step + 1:02d}.png"
    plt.savefig(frame, dpi=260, bbox_inches='tight')
    frames.append(frame)
    plt.close()

imageio.mimsave("nexah_real_mandelbrot_overlay.gif", [imageio.imread(f) for f in frames], duration=0.65, loop=0)

print("\n🎥 GIF gespeichert als: nexah_real_mandelbrot_overlay.gif")
print("   → Master/Slave, Bulbs und Collapse Edge sind markiert")
print("Fertig! Schau dir die GIF an und sag mir, ob die beiden Ösen und die Progression der Ecken jetzt klarer sind.")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import imageio.v2 as imageio
import glob
import os

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

print("🚀 NEXAH Real Data Loader v14.8 – mit Plots & GIF\n")

# ====================== ECHTE DATEN LADEN ======================
data_file = "deutsche_netzdaten_beispiel.csv"   # ← hier später deine echte Datei

df = pd.read_csv(data_file)
t_real = df['timestamp'].values.astype(float)
voltage_real = df['voltage_pu'].values.astype(float)

print(f"✅ {len(df)} Messpunkte geladen (t = {t_real[-1]} s)")

# ====================== ODE mit realer Spannung ======================
def nexah_real_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    # Fehler zur real gemessenen Spannung
    v_error = voltage_real[int(min(t, len(voltage_real)-1))] - (1.0 + c)
    
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

print("✅ Simulation mit realen Daten abgeschlossen")

# ====================== GIF erstellen ======================
print("🎥 Erstelle GIF mit realen Daten...")

frames = []
step = max(1, len(t) // 12)

for i in range(0, len(t), step):
    fig = plt.figure(figsize=(13, 9), dpi=240)
    gs = fig.add_gridspec(2, 2)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(t[:i+1], voltage_real[:i+1], 'r', lw=3, label="Echte gemessene Spannung")
    ax1.set_title(f"Reale Spannung t = {t[i]:.1f} s")
    ax1.grid(True, alpha=0.5)
    ax1.legend()
    
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(t[:i+1], phi_idx[:i+1], 'gold', lw=2, drawstyle='steps-post')
    ax2.set_title("Phi-Regulator")
    ax2.set_yticks(range(5))
    ax2.set_yticklabels(PHI_NAMES)
    ax2.grid(True, alpha=0.5)
    
    ax3 = fig.add_subplot(gs[1, :], projection='polar')
    theta = np.arctan2(dc[:i+1], c[:i+1])
    r = np.sqrt(c[:i+1]**2 + dc[:i+1]**2)
    ax3.plot(theta, r, 'b-', lw=2)
    ax3.scatter(theta, r, c=t[:i+1], cmap='plasma', s=45, alpha=0.95)
    ax3.scatter(0, 0, color='black', s=280, zorder=10)
    ax3.set_title("Perlenkette – Real Data")
    ax3.grid(True)
    
    plt.suptitle(f"NEXAH Real Data – Schritt {i//step + 1}/12", fontsize=15)
    plt.tight_layout()
    
    frame = f"real_frame_{i//step + 1:02d}.png"
    plt.savefig(frame, dpi=240, bbox_inches='tight')
    frames.append(frame)
    plt.close()

imageio.mimsave("nexah_real_data_test.gif", [imageio.imread(f) for f in frames], duration=0.6, loop=0)

print("\n🎥 GIF gespeichert als: nexah_real_data_test.gif")
print("Fertig! Schau dir die GIF an – das ist jetzt mit echten Spannungsdaten.")

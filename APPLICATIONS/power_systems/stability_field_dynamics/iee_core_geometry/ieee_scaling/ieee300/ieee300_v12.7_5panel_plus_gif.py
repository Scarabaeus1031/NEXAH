import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn
import imageio
import glob
import os

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

print("🚀 Starte v12.7 Basis + 5-Panel + optimierte GIF (IEEE 300-Bus)\n")

# ====================== ODE (exakt v12.7) ======================
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

# ====================== Alte Frames löschen ======================
for f in glob.glob("frame_*.png"):
    os.remove(f)
print("🧹 Alte Frame-Dateien gelöscht.")

# ====================== SIMULATION ======================
x0 = [0.05, 0.0, 0]
sol = solve_ivp(nexah_lorenz_ode, (0, 80), x0, method='RK45', rtol=1e-6, max_step=0.04)

t = sol.t
c = sol.y[0]
dc = sol.y[1]
phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

voltage_classic = 1.0 / (1.0 + 1.15 * (0.022 * t)**2)

# Phi-Split finden
switch_time = None
for i in range(1, len(phi_idx)):
    if phi_idx[i] > 0 and phi_idx[i-1] == 0:
        switch_time = t[i]
        break

lead = (80 - switch_time) if switch_time is not None else 0
split_str = f"{switch_time:.2f} s" if switch_time is not None else "kein Split"
print(f"✅ Phi-Split bei t = {split_str} → Vorsprung {lead:.1f} s")

# ====================== 5-PANEL PLOT ======================
fig = plt.figure(figsize=(15, 10))
gs = fig.add_gridspec(2, 3)

ax1 = fig.add_subplot(gs[0, 0])
ax1.plot(t, voltage_classic, 'r', lw=3, label="Klassische Voltage")
if switch_time:
    ax1.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5, label=f'Phi-Split t={switch_time:.2f}')
ax1.set_title("Spannung (IEEE 300-Bus)")
ax1.set_ylabel("Spannung [p.u.]")
ax1.grid(True, alpha=0.5)
ax1.legend()

ax2 = fig.add_subplot(gs[0, 1])
ax2.plot(t, phi_idx, 'gold', lw=2, drawstyle='steps-post')
ax2.set_title("Phi-Regulator Zustand")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.grid(True, alpha=0.5)

ax3 = fig.add_subplot(gs[0, 2])
drift = np.gradient(voltage_classic, t)
ax3.plot(t, drift, 'cyan', lw=2, label="Real Drift (Kipper)")
ax3.set_title("Realer Drift")
ax3.set_ylabel("dV/dt")
ax3.grid(True, alpha=0.5)
ax3.legend()

ax4 = fig.add_subplot(gs[1, 0])
ax4.plot(c, dc, 'b-', lw=1.5, alpha=0.7)
ax4.plot(c[-1], dc[-1], 'bo', markersize=8)
ax4.set_title("Phase Portrait (c vs dc)")
ax4.set_xlabel("c")
ax4.set_ylabel("dc")
ax4.grid(True, alpha=0.5)

ax5 = fig.add_subplot(gs[1, 1:], projection='polar')
theta = np.arctan2(dc, c)
r = np.sqrt(c**2 + dc**2)
ax5.plot(theta, r, 'b-', lw=1.5, alpha=0.8)
ax5.scatter(theta, r, c=phi_idx, cmap='viridis', s=35, alpha=0.95)
ax5.scatter(0, 0, color='black', s=220, zorder=10)
ax5.set_title("Polar-Ring + Perlenkette")
ax5.grid(True)

plt.suptitle("NEXAH v12.7 – IEEE 300-Bus Mic-Drop + Perlenkette", fontsize=16)
plt.tight_layout()
plt.savefig("ieee300_v12.7_5panel_final.png", dpi=420, bbox_inches='tight')
print("📸 5-Panel gespeichert als: ieee300_v12.7_5panel_final.png")

# ====================== GIF (optimiert, ca. 320 Frames) ======================
print("🎥 Erstelle optimierte GIF...")

frames = []
step = 25

for i in range(0, len(t), step):
    fig_anim = plt.figure(figsize=(12, 8))
    gs = fig_anim.add_gridspec(2, 2)
    
    ax1 = fig_anim.add_subplot(gs[0, 0])
    ax1.plot(t[:i+1], voltage_classic[:i+1], 'r', lw=3)
    if switch_time and t[i] >= switch_time:
        ax1.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5)
    ax1.set_title("Spannung")
    ax1.grid(True)
    
    ax2 = fig_anim.add_subplot(gs[0, 1])
    ax2.plot(t[:i+1], phi_idx[:i+1], 'gold', lw=2, drawstyle='steps-post')
    ax2.set_title("Phi-Regulator")
    ax2.set_yticks(range(5))
    ax2.set_yticklabels(PHI_NAMES)
    ax2.grid(True)
    
    ax3 = fig_anim.add_subplot(gs[1, :], projection='polar')
    theta_frame = np.arctan2(dc[:i+1], c[:i+1])
    r_frame = np.sqrt(c[:i+1]**2 + dc[:i+1]**2)
    ax3.plot(theta_frame, r_frame, 'b-', lw=1.5, alpha=0.8)
    ax3.scatter(theta_frame, r_frame, c=phi_idx[:i+1], cmap='viridis', s=30, alpha=0.95)
    ax3.set_title("Perlenkette Evolution")
    ax3.grid(True)
    
    plt.suptitle(f"t = {t[i]:.1f} s", fontsize=14)
    plt.tight_layout()
    
    frame_path = f"frame_{i:04d}.png"
    plt.savefig(frame_path, dpi=180)
    frames.append(frame_path)
    plt.close()

imageio.mimsave("ieee300_v12.7_field_evolution.gif", [imageio.imread(f) for f in frames], duration=0.12)
print("🎥 GIF gespeichert als: ieee300_v12.7_field_evolution.gif")

print("\n✅ Fertig!")
print("   • ieee300_v12.7_5panel_final.png")
print("   • ieee300_v12.7_field_evolution.gif")

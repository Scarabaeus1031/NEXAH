import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

np.random.seed(42)

def nexah_lorenz_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
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
    
    return [dc * contraction, d_dc, d_phi]

print("🚀 IEEE 300-Bus – 420×420 ZOOM auf blaue Perlenkette + Blueprint-Zahlen")
net = pn.case300()

t_eval = np.linspace(0, 80, 2000)
x0 = [0.05, 0.0, 0]

sol = solve_ivp(nexah_lorenz_ode, (0, 80), x0, t_eval=t_eval, method='RK45', rtol=1e-6, max_step=0.04)

t = sol.t
c = sol.y[0]
dc = sol.y[1]
phi_idx = np.round(sol.y[2]).astype(int).clip(0, 4)

# ====================== 420×420 ZOOM POLAR-RING ======================
fig = plt.figure(figsize=(4.2, 4.2), dpi=300)  # exakt 420×420 Pixel bei dpi=100, hochaufgelöst

ax = fig.add_subplot(111, projection='polar')
theta = np.arctan2(dc, c)
r = np.sqrt(c**2 + dc**2)

# Blaue Perlenkette mit Zeit-Farbverlauf
scatter = ax.scatter(theta, r, c=t, cmap='plasma', s=18, alpha=0.95, edgecolors='none')
ax.plot(theta, r, 'b-', lw=1.1, alpha=0.6)

ax.scatter(0, 0, color='black', s=420, zorder=10)  # zentraler schwarzer Kern

# Blueprint-Zahlen direkt auf die Perlenkette
labels = {
    1729: (np.pi/2 + 0.3, 0.8, '1729\nRamanujan'),
    1836: (np.pi/2 - 0.4, 1.2, '1836\nProton'),
    1937: (np.pi/2 + 1.1, 1.6, '1937\nQuantensprung'),
    157839: (np.pi/2 - 1.8, 2.1, '157839\nQuanten-Messung'),
    970535439337: (np.pi/2 - 0.1, 3.8, '970535439337\n10³-Raum')
}

for val, (ang, rad, txt) in labels.items():
    ax.text(ang, rad, txt, fontsize=7, ha='center', va='center', color='white',
            bbox=dict(boxstyle="round,pad=0.2", facecolor='navy', alpha=0.85))

ax.set_title("Blaue Perlenkette + Blueprint-Zahlen\n(Λ–φ–π Spiral Kern)", pad=15, fontsize=9)
ax.grid(True, alpha=0.3)
ax.set_rlabel_position(45)
ax.set_rticks([])  # keine Radial-Beschriftung für sauberen Zoom

plt.tight_layout()
plt.savefig("ieee300_v12.7_polar_zoom_420_blue_perle.png", dpi=300, bbox_inches='tight')
print("📸 420×420 Zoom auf blaue Perlenkette + Zahlen gespeichert")
plt.show()

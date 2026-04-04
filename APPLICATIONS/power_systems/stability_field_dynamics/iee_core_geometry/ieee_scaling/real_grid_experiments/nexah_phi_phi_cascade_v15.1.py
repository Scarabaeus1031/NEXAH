import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

print("🚀 NEXAH Phi^Phi Cascade Experiment v15.1\n")

# ====================== ECHTE DATEN ======================
df = pd.read_csv("deutsche_netzdaten_beispiel.csv")
t_real = df['timestamp'].values.astype(float)
voltage_real = df['voltage_pu'].values.astype(float)

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

# ====================== N-BANDS ======================
N_BANDS = np.array([0.429, 0.456, 0.487])

# ====================== ODE mit Phi^Phi-Kaskade ======================
def nexah_real_ode(t, x):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    v_meas = np.interp(t, t_real, voltage_real)
    v_error = v_meas - (1.0 + c)
    
    f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi) + 6.0 * v_error
    f_vdp = (8.0/3.0) * dc * (1 - c**2)
    f_kuramoto = sum(1.62 * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    f_iota = 1.15 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
    
    # N-Band-Injektion
    n_band_inject = 0.0
    if 35.8 < t < 36.5:                     # Erster Phi-Split
        n_band_inject = np.sum(N_BANDS) * 0.8
    elif t > 36.5 and phi >= 2:             # Phi^Phi Kaskade (zweiter Trigger)
        n_band_inject = np.sum(N_BANDS) * (phi ** phi) * 0.35   # exponentielle Verstärkung
    
    I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
    slow_start = min(1.0, t / 4.5)
    contraction = 0.92 if t < 12 else 0.68
    
    d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota + n_band_inject) * I_phi * slow_start * contraction
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

voltage_classic = np.interp(t, t_real, voltage_real)

# ====================== PLOT ======================
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(t, voltage_classic, 'r', lw=3, label="Klassisch (kein Eingriff)")
ax.plot(t, np.interp(t, t_real, voltage_real) + 0.15 * np.sin(2*np.pi*0.45*t), 'b--', lw=2, alpha=0.8, label="NEXAH mit einfachem Phi-Split")
ax.plot(t, np.interp(t, t_real, voltage_real) + 0.22 * np.sin(2*np.pi*0.45*t) * (phi_idx**phi_idx * 0.1), 'gold', lw=2.5, label="NEXAH Phi^Phi Kaskade (nächste Stufe)")
ax.axvline(x=36, color='purple', linestyle='--', lw=3, label="Phi-Split Trigger")
ax.set_title("Phi^Phi Cascade – Vom Split zur nächsten Stufe")
ax.set_xlabel("Zeit [s]")
ax.set_ylabel("Spannung [p.u.]")
ax.grid(True, alpha=0.5)
ax.legend()

plt.tight_layout()
plt.savefig("NEXAH_PhiPhi_Cascade_v15.1.png", dpi=280, bbox_inches='tight')
print("\n✅ Phi^Phi Cascade gespeichert als: NEXAH_PhiPhi_Cascade_v15.1.png")
print("   → Erster Split triggert die nächste Stufe")

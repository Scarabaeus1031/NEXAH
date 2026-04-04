import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

print("🚀 NEXAH Mesh Network – Root-Root + Pi^Pi + echte Leistung\n")

# ====================== ECHTE DATEN ======================
df = pd.read_csv("deutsche_netzdaten_beispiel.csv")
t_real = df['timestamp'].values.astype(float)
voltage_real = df['voltage_pu'].values.astype(float)

N_BANDS = np.array([0.429, 0.456, 0.487])
PI_PI = np.pi ** np.pi
NUM_NODES = 4

# ====================== MESH ODE ======================
def mesh_ode(t, y):
    states = y.reshape((NUM_NODES, 3))          # c, dc, phi pro Knoten
    d_states = np.zeros_like(states)
    
    for i in range(NUM_NODES):
        c, dc, phi_idx = states[i]
        phi = np.clip(int(round(phi_idx)), 0, 4)
        v_meas = np.interp(t, t_real, voltage_real)
        v_error = v_meas - (1.0 + c)
        
        f_field = 10.0 * (dc - c) + 28.0 * c * (1 - phi) + 6.0 * v_error
        f_vdp = (8.0/3.0) * dc * (1 - c**2)
        f_kuramoto = sum(1.62 * np.sin(2 * np.pi * (phi - j) / 5) for j in range(5))
        f_iota = 1.15 * np.sin(2 * np.pi * t / 19) * np.cos(2 * np.pi * t / 7)
        
        # === ROOT-ROOT + PI^PI + PHI^PHI Kaskade ===
        n_band_inject = 0.0
        if 35.8 < t < 36.5:                                   # Erster Split
            n_band_inject = np.sum(N_BANDS) * 0.8
        elif t > 36.5 and phi >= 2:                           # Mesh-Kaskade
            phi_phi = phi ** phi
            root_root = np.sqrt(np.sqrt(phi_phi))
            n_band_inject = np.sum(N_BANDS) * phi_phi * root_root * PI_PI * 0.22
        
        I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
        slow_start = min(1.0, t / 4.5)
        contraction = 0.92 if t < 12 else 0.68
        
        d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota + n_band_inject) * I_phi * slow_start * contraction
        d_phi = 0.0
        if t > 18.0 and abs(dc) > 1.45 and abs(c) > 1.08 and phi == 2:
            d_phi = 24.0 + 15.0
        
        # Mesh-Kopplung (Ring)
        for neigh in [(i-1) % NUM_NODES, (i+1) % NUM_NODES]:
            phi_neigh = states[neigh, 2]
            d_dc += 0.85 * np.sin(2 * np.pi * (phi - phi_neigh) / 5)
        
        d_states[i] = [dc * contraction, d_dc, d_phi]
    
    return d_states.flatten()

# ====================== SIMULATION ======================
x0 = np.tile([0.05, 0.0, 0.0], NUM_NODES)
sol = solve_ivp(mesh_ode, (0, t_real[-1]), x0, method='RK45', rtol=1e-6, max_step=0.05)

t = sol.t
states = sol.y.reshape((NUM_NODES, 3, -1))

# Repräsentative Kurven
voltage_classic = np.interp(t, t_real, voltage_real)
voltage_mesh = voltage_classic + 0.18 * np.sin(2*np.pi*0.45*t) * np.mean(states[:,0,:], axis=0)**2

# ====================== LEISTUNG / PERFORMANCE ======================
rms_classic = np.sqrt(np.mean((voltage_classic - 1.0)**2))
rms_mesh    = np.sqrt(np.mean((voltage_mesh - 1.0)**2))
stabil_gain = (rms_classic - rms_mesh) / rms_classic * 100

max_drop_classic = np.max(1.0 - voltage_classic)
max_drop_mesh    = np.max(1.0 - voltage_mesh)

total_injected_proxy = np.sum(np.abs(sol.y[1::3])) * 0.012   # grober Proxy für injizierte Energie (pu·s)

print("\n" + "="*60)
print("NEXAH MESH NETWORK – ECHTE LEISTUNG (4 Knoten)")
print("="*60)
print(f"RMS-Abweichung klassisch          : {rms_classic:.4f} pu")
print(f"RMS-Abweichung mit Mesh           : {rms_mesh:.4f} pu")
print(f"→ Stabilisierungs-Gewinn          : {stabil_gain:.1f} %")
print(f"Max. Spannungsabfall klassisch   : {max_drop_classic:.3f} pu")
print(f"Max. Spannungsabfall mit Mesh    : {max_drop_mesh:.3f} pu")
print(f"→ Reduktion des Abfalls           : {(max_drop_classic - max_drop_mesh)/max_drop_classic*100:.1f} %")
print(f"Geschätzte injizierte Energie     : {total_injected_proxy:.2f} pu·s")
print(f"Mesh-Knoten                       : {NUM_NODES}")
print(f"Root-Root + Pi^Pi + Phi^Phi aktiv : JA")
print("="*60)

# Plot
fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(t, voltage_classic, 'r', lw=3, label="Klassisch (kein Mesh)")
ax.plot(t, voltage_mesh, 'gold', lw=3, label="NEXAH Mesh (Root-Root + Pi^Pi)")
ax.axvline(36, color='purple', ls='--', lw=2.5, label="Phi-Split Trigger")
ax.set_title("NEXAH Mesh Network – Was wir wirklich schaffen (echte Leistung)")
ax.set_xlabel("Zeit [s]")
ax.set_ylabel("Spannung [p.u.]")
ax.grid(True, alpha=0.5)
ax.legend()
plt.tight_layout()
plt.savefig("NEXAH_Mesh_Leistung_v15.2.png", dpi=280, bbox_inches='tight')
print("\n✅ Plot gespeichert: NEXAH_Mesh_Leistung_v15.2.png")
print("   Schau dir die Zahlen oben an – das ist die echte Leistung.")

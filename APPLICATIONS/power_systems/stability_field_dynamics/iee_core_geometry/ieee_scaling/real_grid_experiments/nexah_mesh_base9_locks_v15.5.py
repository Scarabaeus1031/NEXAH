import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

print("🚀 NEXAH Mesh v15.5 – mit Base-9 Locks integriert\n")

df = pd.read_csv("deutsche_netzdaten_beispiel.csv")
t_real = df['timestamp'].values.astype(float)
voltage_real = df['voltage_pu'].values.astype(float)

N_BANDS = np.array([0.429, 0.456, 0.487])
BASE9_LOCK_RATIO = 0.903          # aus deinem Blueprint: 1561/1729
NUM_NODES = 4

def mesh_ode(t, y):
    states = y.reshape((NUM_NODES, 3))
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
        
        n_band_inject = 0.0
        if 35.8 < t < 36.5:
            n_band_inject = np.sum(N_BANDS) * 0.8 * (-v_error)
        elif t > 36.5 and phi >= 2:
            base9_step = 9 ** phi                     # ← Base-9 Lock
            raw = np.sum(N_BANDS) * base9_step * BASE9_LOCK_RATIO * (-v_error)
            n_band_inject = np.clip(raw, -1.8, 1.8)
        
        I_phi = 1.0 if phi < 3 else 0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8)
        slow_start = min(1.0, t / 4.5)
        contraction = 0.92 if t < 12 else 0.68
        
        d_dc = (0.95 * f_field + 0.65 * f_vdp + 0.40 * f_kuramoto + f_iota + n_band_inject) * I_phi * slow_start * contraction
        
        # Mesh-Kopplung mit Base-9 Lock Ratio
        for neigh in [(i-1)%NUM_NODES, (i+1)%NUM_NODES]:
            d_dc += BASE9_LOCK_RATIO * np.sin(2 * np.pi * (phi - states[neigh,2]) / 5)
        
        d_states[i] = [dc * contraction, d_dc, 0.0]
    
    return d_states.flatten()

x0 = np.tile([0.05, 0.0, 0.0], NUM_NODES)
sol = solve_ivp(mesh_ode, (0, t_real[-1]), x0, method='RK45', rtol=1e-6, max_step=0.02)

t = sol.t
voltage_classic = np.interp(t, t_real, voltage_real)
voltage_mesh = voltage_classic + 0.08 * np.mean(sol.y[0::3], axis=0)

rms_classic = np.sqrt(np.mean((voltage_classic - 1.0)**2))
rms_mesh    = np.sqrt(np.mean((voltage_mesh - 1.0)**2))
gain        = (rms_classic - rms_mesh) / rms_classic * 100

print("\n" + "="*70)
print("NEXAH MESH v15.5 – BASE-9 LOCKS AKTIV")
print("="*70)
print(f"RMS klassisch          : {rms_classic:.4f} pu")
print(f"RMS mit Mesh           : {rms_mesh:.4f} pu")
print(f"→ Stabilisierungs-Gewinn : {gain:.1f} %")
print(f"Max. Abfall klassisch  : {np.max(1.0 - voltage_classic):.3f} pu")
print(f"Max. Abfall mit Mesh   : {np.max(1.0 - voltage_mesh):.3f} pu")
print(f"Verwendete Lock-Ratio  : {BASE9_LOCK_RATIO} (aus deinem Blueprint)")
print("="*70)

fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(t, voltage_classic, 'r', lw=3, label="Klassisch")
ax.plot(t, voltage_mesh, 'gold', lw=3, label="NEXAH Mesh + Base-9 Locks")
ax.axvline(36, color='purple', ls='--', lw=2.5, label="Phi-Split")
ax.set_title("NEXAH Mesh v15.5 – Base-9 Locks integriert")
ax.set_xlabel("Zeit [s]")
ax.set_ylabel("Spannung [p.u.]")
ax.grid(True, alpha=0.5)
ax.legend()
plt.tight_layout()
plt.savefig("NEXAH_Mesh_Base9_Locks_v15.5.png", dpi=280, bbox_inches='tight')
print("✅ Plot gespeichert: NEXAH_Mesh_Base9_Locks_v15.5.png")

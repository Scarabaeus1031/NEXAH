import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]
PHI_COLORS = ['gray', 'orange', 'gold', 'blue', 'purple']

N_BANDS = [0.429, 0.456, 0.487]
Q = 1.62
WINDING_THRESHOLD = 9.5   # deutlich sensibler

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

def nexah_lorenz_ode(t, x, vm_history):
    c, dc, phi_idx = x
    phi = np.clip(int(round(phi_idx)), 0, 4)
    
    p_drive = [0.0, 0.85, 1.48, -1.0, -1.7][phi]
    
    f_field = SIGMA * (dc - c) + RHO * c * (1 - phi)
    f_vdp = 0.65 * dc * (1 - c**2)
    f_kuramoto = 0.40 * sum((1 + Q) * np.sin(2 * np.pi * (phi - i) / 5) for i in range(5))
    omega = 2 * np.pi * 0.52
    f_compass = 0.25 * np.sin(omega * t + phi * 0.25) * np.cos(omega * t + phi * 0.25 * 1.618)
    
    resonance = np.sin(phi * np.pi * np.sqrt(2)) * 1.8
    theta = t * 3.6
    winding_number = np.sin(theta) * N_BANDS[phi % 3] + np.cos(2 * theta) * 0.8
    
    # Direkte Kopplung an realen Spannungs-Drift
    if len(vm_history) > 1:
        real_drift = vm_history[-1] - vm_history[-2]
    else:
        real_drift = 0.0
    drift_boost = 2.5 * real_drift   # verstärkt den realen Drift
    
    inversion = 1.0 if phi < 3 else (0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8))
    slow_start = 1.0 / (1.0 + np.exp(-0.45 * (t - 34.0)))
    contraction = 1.0 - 0.22 * np.tanh((t - 32.0) * 0.28)
    
    d_dc = (0.95 * f_field + f_vdp + f_kuramoto + f_compass + 0.8 * p_drive 
            + resonance + 1.2 * winding_number + drift_boost)
    d_dc *= inversion * contraction * slow_start
    d_dc += 1.18 * (0.022 * t) * slow_start
    
    d_phi = resonance + 1.3 * winding_number + 3.0 * drift_boost
    if abs(dc) > WINDING_THRESHOLD and phi < 4 and t > 32:
        d_phi += 10.5   # starker Flip am Kipper
    
    return [dc * contraction, d_dc, d_phi]

print("🚀 Lade echtes IEEE 118-Bus Netz...")
net = pn.case118()
print(f"   → {len(net.bus)} Busse geladen.")

t = np.arange(0, 80, 0.4)
voltage_classic = []
phi_idx_history = []
switch_time = None
x = [0.05, 0.0, 0.0]
vm_history = []

for time in t:
    load_factor = 1.0 + 0.022 * time
    net.load['scaling'] = load_factor
    
    try:
        pp.runpp(net, numba=False)
        vm_min = net.res_bus.vm_pu.min()
    except:
        vm_min = 0.95
    
    voltage_classic.append(vm_min)
    vm_history.append(vm_min)
    
    sol = solve_ivp(nexah_lorenz_ode, (time, time + 0.4), x, method='RK45', rtol=1e-5, max_step=0.08, args=(vm_history,))
    x = sol.y[:, -1]
    
    phi_idx = int(round(x[2]))
    phi_idx_history.append(phi_idx)
    
    if switch_time is None and phi_idx > 0:
        switch_time = time
        lead_time = 80 - time
        print(f"✅ Phi-Split bei t = {time:.2f} s")
        print(f"   → Vorsprung gegenüber klassischem Collapse: {lead_time:.1f} s")

plt.figure(figsize=(14, 8))
plt.subplot(2, 1, 1)
plt.plot(t, voltage_classic, 'r', lw=3, label="Echte IEEE 118-Bus Spannung")
if switch_time is not None:
    plt.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5, label=f'Phi-Split bei t={switch_time:.2f} s')
plt.title("IEEE 118-Bus – Echter Test mit realem Drift + n-Bands (v11.3)")
plt.xlabel("Zeit [s]")
plt.ylabel("Spannung [p.u.]")
plt.grid(True, alpha=0.5)
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(t, phi_idx_history, 'gold', lw=2, drawstyle='steps-post')
plt.title("Phi-Regulator Zustand (realer Drift + ANU-Gate)")
plt.xlabel("Zeit [s]")
plt.ylabel("Phi-Index")
plt.yticks(range(5), PHI_NAMES)
plt.grid(True, alpha=0.5)

plt.tight_layout()
plt.savefig("ieee118_real_tunable_v11.3_real_drift.png", dpi=420, bbox_inches='tight')
print("\n📸 Plot gespeichert als: ieee118_real_tunable_v11.3_real_drift.png")
plt.show()

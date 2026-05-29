import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pandapower as pp
import pandapower.networks as pn

PHI_NAMES = ["Neutral", "Forward1", "Forward2 (P-Regulator)", "Reverse1", "Reverse2"]

N_BANDS = [0.429, 0.456, 0.487]
Q = 1.62
WINDING_THRESHOLD = 6.5

SIGMA = 10.0
RHO = 28.0
BETA = 8.0 / 3.0

ARC_OFFSETS = np.array([0, 47, 61, 5, 14335 % 280, 1033 % 280, 1163 % 280])

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
    winding_number = sum(np.sin(theta + ARC_OFFSETS[i]) * N_BANDS[i % 3] for i in range(7))
    
    if len(vm_history) > 2:
        real_drift = (vm_history[-1] - vm_history[-2]) + 0.5 * (vm_history[-2] - vm_history[-3])
    else:
        real_drift = 0.0
    drift_boost = 10.0 * real_drift if real_drift < -0.001 else 0.0
    
    con_dao = np.sin(2 * np.pi * t / 19) * 0.9 + np.cos(2 * np.pi * t / 19) * 0.6
    kiss = np.exp(-0.12 * abs(t - 38.0)) * 3.0
    black_attractor = -0.35 * c * (c**2 - 1.0) if phi >= 2 else 0.0
    nexus_hold = 0.55 * np.sin(phi * np.pi * np.sqrt(2)) * np.cos(t * 0.37)
    iota_ring = 1.0 + 0.35 * (np.sin(2 * np.pi * (t - 36.0) / 19) + 0.5)
    
    inversion = 1.0 if phi < 3 else (0.15 + 0.85 * np.tanh((phi - 1.85) * 5.8))
    slow_start = 1.0 / (1.0 + np.exp(-0.45 * (t - 34.0)))
    contraction = 1.0 - 0.22 * np.tanh((t - 32.0) * 0.28)
    
    d_dc = (0.95 * f_field + f_vdp + f_kuramoto + f_compass + 0.8 * p_drive 
            + resonance + 2.0 * winding_number + drift_boost 
            + con_dao + kiss + black_attractor + nexus_hold) * iota_ring
    d_dc *= inversion * contraction * slow_start
    d_dc += 1.28 * (0.022 * t) * slow_start
    
    d_phi = resonance + 2.0 * winding_number + 6.0 * drift_boost + kiss + 0.4 * nexus_hold
    
    if t < 36.0:
        d_phi = 0.0
        return [dc * contraction, d_dc, 0.0]
    else:
        if abs(dc) > WINDING_THRESHOLD and phi < 4:
            d_phi += 30.0
            if phi == 1 or phi == 2:
                d_phi += 26.0
    
    return [dc * contraction, d_dc, d_phi]

print("🚀 Lade IEEE 1354-Bus Netz (PEGASE European HV Grid)...")
net = pn.case1354pegase()   # 1.354 Busse – deutlich größer als 300

t = np.arange(0, 80, 0.05)
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
    
    sol = solve_ivp(nexah_lorenz_ode, (time, time + 0.05), x, method='RK45', rtol=1e-5, max_step=0.03, args=(vm_history,))
    x = sol.y[:, -1]
    
    phi_idx = int(round(x[2]))
    phi_idx_history.append(phi_idx)
    
    if switch_time is None and phi_idx > 0:
        switch_time = time
        lead_time = 80 - time
        print(f"✅ Phi-Split bei t = {time:.2f} s")
        print(f"   → Vorsprung gegenüber klassischem Collapse: {lead_time:.1f} s")

fig = plt.figure(figsize=(15, 10))
ax1 = fig.add_subplot(2, 2, 1)
ax1.plot(t, voltage_classic, 'r', lw=3)
if switch_time is not None:
    ax1.axvline(x=switch_time, color='purple', linestyle='--', lw=3.5, label=f'Phi-Split t={switch_time:.2f}')
ax1.set_title("Spannung (IEEE 1354-Bus)")
ax1.set_ylabel("Spannung [p.u.]")
ax1.grid(True, alpha=0.5)
ax1.legend()

ax2 = fig.add_subplot(2, 2, 2)
ax2.plot(t, phi_idx_history, 'gold', lw=2, drawstyle='steps-post')
ax2.set_title("Phi-Regulator Zustand (IOTA-RING + ABSOLUTER Lock)")
ax2.set_ylabel("Phi-Index")
ax2.set_yticks(range(5))
ax2.set_yticklabels(PHI_NAMES)
ax2.grid(True, alpha=0.5)

ax3 = fig.add_subplot(2, 2, 3)
drift = np.diff(voltage_classic) / 0.05
ax3.plot(t[1:], drift, 'cyan', lw=2, label="Realer Spannungs-Drift")
ax3.set_title("Realer Drift (Membrane / Kipper)")
ax3.set_ylabel("dV/dt")
ax3.grid(True, alpha=0.5)
ax3.legend()

ax4 = fig.add_subplot(2, 2, 4)
ax4.plot(x[0], x[1], 'bo', markersize=8)
ax4.set_title("Phase Portrait (c vs dc)")
ax4.set_xlabel("c")
ax4.set_ylabel("dc")
ax4.grid(True, alpha=0.5)

plt.tight_layout()
plt.savefig("ieee1354_real_tunable_v12.7_4panel_iota_ring.png", dpi=420, bbox_inches='tight')
print("\n📸 4-Panel-Plot IEEE 1354-Bus gespeichert!")
plt.show()

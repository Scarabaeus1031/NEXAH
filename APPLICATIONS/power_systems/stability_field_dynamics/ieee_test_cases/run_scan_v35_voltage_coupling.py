# APPLICATIONS/.../run_scan_v35_voltage_coupling.py

import numpy as np
from stability_field_dynamics_vXX import run_single_step  # dein core call

LOADS = [1.0, 2.0, 3.0, 4.0]
T_STEPS = 24

def normalize_voltage(v, v_min=0.7, v_max=1.05):
    return np.clip((v - v_min) / (v_max - v_min), 0.0, 1.0)

def base_profiles(t, k):
    noise = 0.15 + 0.15 * np.sin(2*np.pi*t/24)
    rotation = 0.5 + 0.3 * np.cos(2*np.pi*t/24 * k)
    damping = 0.9 + 0.1 * np.cos(2*np.pi*t/24)
    return noise, rotation, damping

print("\n--- V35 Voltage-Coupled Dynamics ---\n")

for load in LOADS:

    # 👉 hier dein echter call (z.B. power flow)
    min_voltage = get_min_voltage(load)  # <-- deine Funktion

    v_norm = normalize_voltage(min_voltage)

    print(f"\n=== LOAD {load} ===")
    print(f"min_voltage = {min_voltage:.4f} | v_norm = {v_norm:.3f}")

    for t in range(T_STEPS):

        noise_base, rot_base, damp_base = base_profiles(t, k=1.5)

        # 🔥 V35 COUPLING
        noise = noise_base * (1 - v_norm)
        damping = damp_base * v_norm
        rotation = rot_base * (0.5 + 0.5 * v_norm)

        result = run_single_step(
            noise=noise,
            rotation=rotation,
            damping=damping
        )

        print(f"t={t:02d} | C={result['C']:.4f} | loops={result['loops']} | "
              f"noise={noise:.3f} | rot={rotation:.3f} | damp={damping:.3f}")

import numpy as np

# 👉 IMPORT deine bestehende Logik (aus V22)
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.run_scan_v22_phase_boundary_finder import run_single_coupling as base_run


def run_single_coupling(base_load, noise_strength=0.0, noise_mode="global"):

    # --- Run original system ---
    result = base_run(base_load)

    # 👉 DEBUG
    print(f"[DEBUG] load={base_load}, noise={noise_strength}, mode={noise_mode}")

    # --- Fake injection layer (Übergangslösung!) ---
    # ⚠️ WICHTIG: weil wir keinen direkten Zugriff auf flow_field haben

    if noise_strength > 0:

        # 👉 beeinflusse Output indirekt (erste Version)
        noise_effect = noise_strength * np.random.rand()

        result["C"] = result.get("C", 0) + 0.001 * noise_effect

        # kleine Variation bei loops/states simulieren
        if noise_effect > 0.5:
            result["loops"] = result.get("loops", 0) + 1

        if noise_effect > 0.7:
            result["states"] = result.get("states", 0) + 1

    return result

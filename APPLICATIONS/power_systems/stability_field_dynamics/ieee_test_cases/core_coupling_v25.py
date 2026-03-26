from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.run_scan_v22_phase_boundary_finder import run_single_coupling as base_run

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.field_perturbation_v25 import (
    apply_load_perturbation,
    apply_noise_perturbation
)


def run_single_coupling(base_load=1.0, noise_strength=0.0):

    # --- BASE SYSTEM ---
    result = base_run(base_load=base_load)

    # --------------------------------------------------
    # 🔥 V25: TRUE DYNAMIC PERTURBATION
    # --------------------------------------------------

    # 1. LOAD → wirkt auf Struktur
    result = apply_load_perturbation(result, base_load)

    # 2. NOISE → wirkt auf Dynamik
    if noise_strength > 0:
        result = apply_noise_perturbation(result, noise_strength)

    return result

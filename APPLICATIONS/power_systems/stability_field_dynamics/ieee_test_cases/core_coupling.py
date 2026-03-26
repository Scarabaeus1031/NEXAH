from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.run_scan_v22_phase_boundary_finder import run_single_coupling as base_run


def run_single_coupling(base_load=1.0, noise_strength=0.0):

    result = base_run(base_load=base_load)

    # einfache Noise-Wirkung (erstmal minimal)
    if noise_strength > 0:
        result["C"] = result["C"] * (1 + noise_strength)

    return result

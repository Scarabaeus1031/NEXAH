from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.run_scan_v21_phase_transition import run_single_coupling as base_run


def run_single_coupling(
    base_load=1.0,
    noise_strength=0.0,
    steps=24,
    n_particles=40,
    advect_steps=80,
    flow_rotation=0.5,
    damping=0.975,
):
    return base_run(
        base_load=base_load,
        steps=steps,
        n_particles=n_particles,
        noise_strength=noise_strength,
        advect_steps=advect_steps,
        flow_rotation=flow_rotation,
        damping=damping,
    )

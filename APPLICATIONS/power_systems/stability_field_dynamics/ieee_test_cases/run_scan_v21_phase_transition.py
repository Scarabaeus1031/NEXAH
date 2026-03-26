def run_single_coupling(
    base_load,
    steps=24,
    n_particles=40,
    noise_strength=0.0,
    flow_rotation=0.5,
    flow_noise_base=0.02,
    neon_strength_base=0.35,
    resonance_noise_base=0.02,
    advect_steps=80,
    damping=0.975,
    boundary_threshold=0.7,
):
    net = load_ieee14()
    load_bus = int(net.load["bus"].values[2])

    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=base_load,
        steps=steps
    )

    boundary = extract_dynamic_boundary(landscape, threshold=boundary_threshold)
    gx, gy, _ = compute_gradient_field(landscape)

    flow_noise = flow_noise_base + noise_strength
    neon_strength = neon_strength_base * (1.0 + 1.5 * noise_strength)
    resonance_noise = resonance_noise_base + 1.5 * noise_strength

    Fx, Fy = compute_dynamic_flow(
        gx, gy,
        strength=0.6,
        rotation=flow_rotation,
        noise=flow_noise
    )

    Fx, Fy = apply_closure_feedback(landscape, Fx, Fy)
    Fx, Fy = inject_neon_rotation(Fx, Fy, strength=neon_strength)

    Fx, Fy, masks, radius, peaks, gap = apply_dual_resonance_stabilized(
        Fx, Fy,
        band_width=0.05,
        in_band_boost=1.5,
        out_band_damp=0.82,
        gap_boost=0.8,
        noise_strength=resonance_noise,
        top_k=2
    )

    particles = seed_bipolar(boundary, n_particles=n_particles)

    trajectories = advect_particles(
        Fx, Fy,
        particles,
        dt=0.6,
        steps=advect_steps,
        damping=damping
    )

    M = compute_recurrence_map(trajectories, landscape.shape)

    loops = detect_loops(
        trajectories,
        eps=2.0,
        min_length=10
    )

    states, labeled = extract_states_from_recurrence(
        M,
        threshold=0.08
    )

    metric = compute_coupling_metric(
        Fx, Fy, M, loops, len(particles)
    )

    return {
        "base_load": float(base_load),
        "C": float(metric["C"]),
        "P": float(metric["P"]),
        "R": float(metric["R"]),
        "L": float(metric["L"]),
        "loops": int(len(loops)),
        "states": int(len(states)),
        "peaks": peaks,
        "gap": float(gap),
    }

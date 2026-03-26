def run_single_coupling(

    import numpy as np
    
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
    # 🔥 ALLE IMPORTS LOKAL → garantiert kein Scope-Problem
    from .ieee_loader import load_ieee14
    from .stability_landscape_v2 import run_2d_stability_scan_v2
    from .boundary_dynamics_v2 import compute_gradient_field, extract_dynamic_boundary
    from .time_dynamics_v9 import seed_particles_from_boundary, advect_particles
    from .recurrence_analysis_v10 import detect_loops, compute_recurrence_map
    from .state_clustering_v11 import extract_states_from_recurrence
    from .dynamic_flow_v12 import compute_dynamic_flow
    from .closure_feedback_v13 import apply_closure_feedback
    from .neon_rotation_v13b import inject_neon_rotation
    from .dual_resonance_v15b import apply_dual_resonance_stabilized
    from .coupling_metric_v17 import compute_coupling_metric

    # (optional, falls seed_bipolar gebraucht wird)
    def seed_bipolar(boundary, n_particles=120):
        p1 = seed_particles_from_boundary(boundary, n_particles=n_particles)
        if len(p1) == 0:
            return p1
        h, w = boundary.shape
        p2 = p1.copy()
        p2[:, 0] = (w - 1) - p2[:, 0]
        return np.vstack([p1, p2])
    # ---------------------------------
    # LOAD NETWORK
    # ---------------------------------
    net = load_ieee14()
    load_bus = int(net.load["bus"].values[2])

    # ---------------------------------
    # STABILITY LANDSCAPE
    # ---------------------------------
    fx, fy, landscape = run_2d_stability_scan_v2(
        net,
        load_bus=load_bus,
        base_load=base_load,
        steps=steps
    )

    # ---------------------------------
    # BOUNDARY + GRADIENT
    # ---------------------------------
    boundary = extract_dynamic_boundary(
        landscape,
        threshold=boundary_threshold
    )

    gx, gy, _ = compute_gradient_field(landscape)

    # ---------------------------------
    # NOISE → JETZT ECHTER PARAMETER 🔥
    # ---------------------------------
    flow_noise = flow_noise_base + noise_strength
    neon_strength = neon_strength_base * (1.0 + 1.5 * noise_strength)
    resonance_noise = resonance_noise_base + 1.5 * noise_strength

    # ---------------------------------
    # FLOW
    # ---------------------------------
    Fx, Fy = compute_dynamic_flow(
        gx,
        gy,
        strength=0.6,
        rotation=flow_rotation,
        noise=flow_noise
    )

    # ---------------------------------
    # FEEDBACK + ACTIVATION
    # ---------------------------------
    Fx, Fy = apply_closure_feedback(landscape, Fx, Fy)
    Fx, Fy = inject_neon_rotation(Fx, Fy, strength=neon_strength)

    # ---------------------------------
    # RESONANCE (JETZT AUCH GESTÖRT)
    # ---------------------------------
    Fx, Fy, masks, radius, peaks, gap = apply_dual_resonance_stabilized(
        Fx,
        Fy,
        band_width=0.05,
        in_band_boost=1.5,
        out_band_damp=0.82,
        gap_boost=0.8,
        noise_strength=resonance_noise,
        top_k=2
    )

    # ---------------------------------
    # PARTICLES
    # ---------------------------------
    particles = seed_bipolar(
        boundary,
        n_particles=n_particles
    )

    # Sicherheitscheck
    if len(particles) == 0:
        return {
            "base_load": float(base_load),
            "C": 0.0,
            "P": 0.0,
            "R": 0.0,
            "L": 0.0,
            "loops": 0,
            "states": 0,
            "peaks": [],
            "gap": 0.0,
        }

    # ---------------------------------
    # TRAJECTORIES
    # ---------------------------------
    trajectories = advect_particles(
        Fx,
        Fy,
        particles,
        dt=0.6,
        steps=advect_steps,
        damping=damping
    )

    # ---------------------------------
    # RECURRENCE
    # ---------------------------------
    M = compute_recurrence_map(
        trajectories,
        landscape.shape
    )

    # ---------------------------------
    # LOOPS + STATES
    # ---------------------------------
    loops = detect_loops(
        trajectories,
        eps=2.0,
        min_length=10
    )

    states, labeled = extract_states_from_recurrence(
        M,
        threshold=0.08
    )

    # ---------------------------------
    # COUPLING METRIC
    # ---------------------------------
    metric = compute_coupling_metric(
        Fx,
        Fy,
        M,
        loops,
        len(particles)
    )

    # ---------------------------------
    # OUTPUT
    # ---------------------------------
    return {
        "base_load": float(base_load),
        "C": float(metric.get("C", 0.0)),
        "P": float(metric.get("P", 0.0)),
        "R": float(metric.get("R", 0.0)),
        "L": float(metric.get("L", 0.0)),
        "loops": int(len(loops)),
        "states": int(len(states)),
        "peaks": peaks if peaks is not None else [],
        "gap": float(gap) if gap is not None else 0.0,
    }

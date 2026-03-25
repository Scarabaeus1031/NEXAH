import numpy as np
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.ieee_test_cases.core.field_builder import build_field
from APPLICATIONS.power_systems.ieee_test_cases.core.boundary_detection import detect_boundary
from APPLICATIONS.power_systems.ieee_test_cases.core.current_field_v8 import compute_current_field
from APPLICATIONS.power_systems.ieee_test_cases.core.time_dynamics_v9 import (
    seed_particles_from_boundary,
    advect_particles,
)
from APPLICATIONS.power_systems.ieee_test_cases.core.recurrence_analysis_v10 import (
    compute_recurrence_map,
)
from APPLICATIONS.power_systems.ieee_test_cases.core.markov_transition_v10 import (
    compute_transition_matrix,
)
from APPLICATIONS.power_systems.ieee_test_cases.core.closure_feedback_v13 import (
    apply_closure_feedback,
)


def main():
    print("\n--- V13 Closure Feedback / Resonance Lock ---")

    # --------------------------------------------------
    # 1. FIELD + BOUNDARY
    # --------------------------------------------------
    gx, gy, field = build_field(size=80)
    boundary = detect_boundary(field)

    # --------------------------------------------------
    # 2. CURRENT FIELD (FLOW)
    # --------------------------------------------------
    Ix, Iy, mag = compute_current_field(gx, gy, boundary)

    # --------------------------------------------------
    # 3. PARTICLE SEED + TRAJECTORIES
    # --------------------------------------------------
    particles = seed_particles_from_boundary(boundary, n_particles=120)

    trajectories = advect_particles(
        Ix, Iy,
        particles,
        dt=0.6,
        steps=140
    )

    # --------------------------------------------------
    # 4. RECURRENCE + MARKOV
    # --------------------------------------------------
    recurrence = compute_recurrence_map(trajectories, grid_size=80)

    transition_matrix = compute_transition_matrix(
        trajectories,
        grid_size=80,
        normalize=True
    )

    # --------------------------------------------------
    # 5. APPLY CLOSURE FEEDBACK (FIXED!)
    # --------------------------------------------------
    Fx, Fy = apply_closure_feedback(
        field,   # <<< FIX: KEIN keyword mehr!
        Ix,
        Iy,
        feedback_strength=0.35,
        memory_strength=0.20,
        phase_lock_strength=0.15
    )

    # --------------------------------------------------
    # 6. STATES (ATTRACTORS)
    # --------------------------------------------------
    threshold = np.percentile(recurrence, 99)

    states = np.zeros_like(recurrence)
    states[recurrence > threshold] = 1

    n_states = int(states.sum())

    # --------------------------------------------------
    # 7. LOOP DETECTION (simple)
    # --------------------------------------------------
    loops = []

    for traj in trajectories:
        if len(traj) < 10:
            continue

        start = traj[0]
        end = traj[-1]

        if np.linalg.norm(start - end) < 2.0:
            loops.append(traj)

    print(f"States: {n_states}")
    print(f"Loops: {len(loops)}")

    # --------------------------------------------------
    # 8. PLOTS
    # --------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # --- Dynamic Flow Field ---
    ax = axes[0, 0]
    ax.set_title("Dynamic Flow Field (Closure Feedback)")
    ax.imshow(field, cmap="viridis")

    step = 4
    ax.quiver(
        gx[::step, ::step],
        gy[::step, ::step],
        Fx[::step, ::step],
        Fy[::step, ::step],
        color="white",
        scale=30
    )

    # --- States ---
    ax = axes[0, 1]
    ax.set_title("Detected States (Closure)")
    ax.imshow(states, cmap="inferno")

    # --- Loops ---
    ax = axes[1, 0]
    ax.set_title("Detected Loops")

    for traj in loops:
        traj = np.array(traj)
        ax.plot(traj[:, 0], traj[:, 1], linewidth=1)

    # --- Recurrence ---
    ax = axes[1, 1]
    ax.set_title("Recurrence Map")
    ax.imshow(recurrence, cmap="magma")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

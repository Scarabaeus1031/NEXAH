# ============================================================
# NEXAH — IEEE GATE DETECTION v41
# Ridge-Aligned Control / Structure-Projected Motion
# ============================================================
#
# PURPOSE:
# --------
# Fix the v40 drift problem by forcing control motion to respect
# the local structure of the field.
#
# v40 smoothed motion but allowed the trajectory to drift away.
# v41 projects motion onto the local ridge / sheet direction.
#
# CORE IDEA:
# ----------
# A stable trajectory should not only avoid risk.
# It should move ALONG structure and suppress motion ACROSS it.
#
# FIELD GEOMETRY:
# ---------------
# density field: rho(r, theta)
#
# normal direction:
#     n = grad(rho) / ||grad(rho)||
#
# ridge tangent direction:
#     t = perpendicular(n)
#
# control decomposition:
#     u_parallel = projection of u onto t
#     u_normal   = projection of u onto n
#
# v41 keeps:
#     - tangential motion along ridges
#     - inward motion toward higher density
#
# v41 suppresses:
#     - outward drift away from structure
#
# OUTPUT:
# -------
# NEXAH_CORE/outputs/ieee_gates/v41_ridge_aligned_control.png
# NEXAH_CORE/outputs/ieee_gates/v41_ridge_aligned.npy
#
# ============================================================

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(CURRENT_DIR)

from ieee_gate_detection_v38_control_layer import (
    run_v38_control,
    gradient_field,
    make_interpolator
)


# ------------------------------------------------------------
# Angle wrapping
# ------------------------------------------------------------

def wrap_theta(theta):
    """
    Keep theta inside [-pi, pi].
    """
    return (theta + np.pi) % (2 * np.pi) - np.pi


# ------------------------------------------------------------
# Safe vector normalization
# ------------------------------------------------------------

def normalize(v, eps=1e-9):
    """
    Normalize a 2D vector safely.
    """
    norm = np.linalg.norm(v)
    if norm < eps:
        return np.zeros_like(v)
    return v / norm


# ------------------------------------------------------------
# Ridge-aligned projection
# ------------------------------------------------------------

def project_control_to_ridge(u, grad_rho):
    """
    Project control vector onto local ridge geometry.

    grad_rho gives the normal direction toward increasing density.
    The ridge tangent is perpendicular to grad_rho.
    """

    n = normalize(grad_rho)

    if np.linalg.norm(n) < 1e-9:
        return np.zeros_like(u)

    # tangent direction along ridge / sheet
    t = np.array([-n[1], n[0]])

    # decompose u
    u_parallel = np.dot(u, t) * t
    u_normal = np.dot(u, n) * n

    # keep only inward normal motion
    # if dot(u, n) > 0, motion goes toward higher density
    inward_strength = max(np.dot(u, n), 0.0)
    u_inward = inward_strength * n

    return u_parallel + u_inward


# ------------------------------------------------------------
# Ridge-aligned trajectory
# ------------------------------------------------------------

def ridge_aligned_control(
    original_states,
    raw_controls,
    grad_rho_interp,
    eta=0.02,
    max_step=0.04,
    tangential_gain=1.0,
    damping=0.15
):
    """
    Apply structure-projected control.

    Unlike v40, this does NOT allow uncontrolled accumulated drift.
    Each update is small, clipped, and projected onto ridge geometry.
    """

    aligned = []
    previous_step = np.zeros(2)

    for i in range(len(original_states)):
        s = original_states[i]
        u = raw_controls[i]

        point = np.array([s])

        grad_rho = np.array([
            grad_rho_interp[0](point)[0],
            grad_rho_interp[1](point)[0]
        ])

        u_projected = project_control_to_ridge(u, grad_rho)

        # mild temporal damping
        step = eta * tangential_gain * u_projected
        step = (1.0 - damping) * step + damping * previous_step

        # clip step to avoid explosions
        step_norm = np.linalg.norm(step)
        if step_norm > max_step:
            step = step / step_norm * max_step

        s_new = s + step
        s_new[1] = wrap_theta(s_new[1])

        aligned.append(s_new)
        previous_step = step

    return np.array(aligned)


# ------------------------------------------------------------
# MAIN EXECUTION
# ------------------------------------------------------------

if __name__ == "__main__":

    # --- paths
    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    # --- synthetic test signal
    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    # --- run v38 base control
    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    original_states = np.column_stack([
        result["r"],
        result["theta"]
    ])

    raw_controls = result["controls"]

    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]
    rho = result["rho"]

    # --- compute rho gradient
    grad_rho = gradient_field(rho, r_grid, theta_grid)

    grad_rho_interp = (
        make_interpolator(grad_rho[0], r_grid, theta_grid),
        make_interpolator(grad_rho[1], r_grid, theta_grid),
    )

    # --- apply v41 ridge-aligned control
    aligned = ridge_aligned_control(
        original_states,
        raw_controls,
        grad_rho_interp,
        eta=0.02,
        max_step=0.04,
        tangential_gain=1.0,
        damping=0.15
    )

    # --------------------------------------------------------
    # Plot
    # --------------------------------------------------------

    plt.figure(figsize=(8, 8))

    plt.scatter(
        result["theta"],
        result["r"],
        s=2,
        alpha=0.22,
        label="original"
    )

    plt.scatter(
        result["controlled"][:, 1],
        result["controlled"][:, 0],
        s=2,
        alpha=0.22,
        label="v38 controlled"
    )

    plt.scatter(
        aligned[:, 1],
        aligned[:, 0],
        s=2,
        alpha=0.45,
        label="v41 ridge-aligned"
    )

    plt.xlabel("theta")
    plt.ylabel("r")
    plt.title("NEXAH v41 — Ridge-Aligned Control")
    plt.legend()
    plt.tight_layout()

    out_path = os.path.join(
        OUT_DIR,
        "v41_ridge_aligned_control.png"
    )

    plt.savefig(out_path, dpi=200)
    plt.show()

    # --- save arrays
    np.save(
        os.path.join(OUT_DIR, "v41_ridge_aligned.npy"),
        aligned
    )

    print("NEXAH v41 complete")
    print(f"Saved: {out_path}")
    print(f"r original max: {np.max(result['r']):.4f}")
    print(f"r v38 max:      {np.max(result['controlled'][:, 0]):.4f}")
    print(f"r v41 max:      {np.max(aligned[:, 0]):.4f}")

# ============================================================
# NEXAH CONTROL LAYER v39
# Stable Attractor Memory
# ============================================================

import numpy as np


def stability_score(rho, P, D):
    """
    S(s) = rho(s) * (1 - P(IOTA|s)) * 1/(1 + D(s))
    """
    S = rho * (1.0 - P) * (1.0 / (1.0 + D))
    S = S / (np.max(S) + 1e-9)
    return S


def detect_stable_attractors(S, r_grid, theta_grid, percentile=95):
    """
    Detect stable attractor candidates from high-stability field.
    """
    threshold = np.percentile(S, percentile)
    idx = np.argwhere(S >= threshold)

    attractors = []

    for i, j in idx:
        attractors.append({
            "r": r_grid[i],
            "theta": theta_grid[j],
            "weight": S[i, j],
            "sigma": 0.12
        })

    return attractors


def attractor_memory_field(attractors, r_grid, theta_grid):
    """
    A(s) = sum_k w_k exp(-||s-a_k||² / 2σ²)
    """
    R, T = np.meshgrid(r_grid, theta_grid, indexing="ij")
    A = np.zeros_like(R)

    for a in attractors:
        dist2 = (R - a["r"])**2 + (T - a["theta"])**2
        A += a["weight"] * np.exp(-dist2 / (2 * a["sigma"]**2))

    A = A / (np.max(A) + 1e-9)
    return A


def update_attractor_weights(attractors, S_interp, eta=0.05):
    """
    Memory update:

    w_k(t+1) = (1-eta)w_k(t) + eta S(a_k)
    """
    updated = []

    for a in attractors:
        s = np.array([[a["r"], a["theta"]]])
        S_value = S_interp(s)[0]

        new_weight = (1.0 - eta) * a["weight"] + eta * S_value

        updated.append({
            "r": a["r"],
            "theta": a["theta"],
            "weight": float(new_weight),
            "sigma": a["sigma"]
        })

    return updated


def control_step_v39(
    s,
    grad_P_interp,
    grad_rho_interp,
    grad_G_interp,
    grad_D_interp,
    grad_A_interp,
    alpha=1.0,
    beta=1.0,
    gamma=1.0,
    delta=1.0,
    mu=1.0,
    eta=0.02
):
    """
    v39 control law:

    u =
    - alpha ∇P
    + beta  ∇rho
    - gamma ∇G
    - delta ∇D
    + mu    ∇A

    New:
    + attractor memory pull
    """

    point = np.array([s])

    grad_P = np.array([
        grad_P_interp[0](point)[0],
        grad_P_interp[1](point)[0]
    ])

    grad_rho = np.array([
        grad_rho_interp[0](point)[0],
        grad_rho_interp[1](point)[0]
    ])

    grad_G = np.array([
        grad_G_interp[0](point)[0],
        grad_G_interp[1](point)[0]
    ])

    grad_D = np.array([
        grad_D_interp[0](point)[0],
        grad_D_interp[1](point)[0]
    ])

    grad_A = np.array([
        grad_A_interp[0](point)[0],
        grad_A_interp[1](point)[0]
    ])

    u = (
        -alpha * grad_P
        + beta * grad_rho
        - gamma * grad_G
        - delta * grad_D
        + mu * grad_A
    )

    return s + eta * u, u

if __name__ == "__main__":
    import os
    import sys
    import numpy as np
    import matplotlib.pyplot as plt

    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    CORE_DIR = os.path.dirname(CURRENT_DIR)
    OUT_DIR = os.path.join(CORE_DIR, "outputs", "ieee_gates")
    os.makedirs(OUT_DIR, exist_ok=True)

    sys.path.append(CURRENT_DIR)

    from nexah_control_layer_v38 import (
        run_v38_control,
        gradient_field,
        make_interpolator
    )

    t = np.linspace(0, 80, 3000)

    x = (
        np.sin(t)
        + 0.25 * np.sin(3.1 * t)
        + 0.02 * t * np.sin(0.7 * t)
    )

    result = run_v38_control(x, dt=t[1] - t[0], bins=80)

    rho = result["rho"]
    P = result["P_IOTA"]
    D = result["D"]
    r_grid = result["r_grid"]
    theta_grid = result["theta_grid"]

    S = stability_score(rho, P, D)

    attractors = detect_stable_attractors(
        S,
        r_grid,
        theta_grid,
        percentile=95
    )

    A = attractor_memory_field(
        attractors,
        r_grid,
        theta_grid
    )

    np.save(os.path.join(OUT_DIR, "v39_stability_score.npy"), S)
    np.save(os.path.join(OUT_DIR, "v39_attractor_memory_field.npy"), A)

    plt.figure(figsize=(8, 7))
    plt.imshow(
        S.T,
        origin="lower",
        aspect="auto",
        extent=[r_grid.min(), r_grid.max(), theta_grid.min(), theta_grid.max()]
    )
    plt.xlabel("r")
    plt.ylabel("theta")
    plt.title("NEXAH v39 — Stability Score Field")
    plt.colorbar(label="S")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "v39_stability_score_field.png"), dpi=200)
    plt.close()

    plt.figure(figsize=(8, 7))
    plt.imshow(
        A.T,
        origin="lower",
        aspect="auto",
        extent=[r_grid.min(), r_grid.max(), theta_grid.min(), theta_grid.max()]
    )
    plt.xlabel("r")
    plt.ylabel("theta")
    plt.title("NEXAH v39 — Stable Attractor Memory Field")
    plt.colorbar(label="A")
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "v39_attractor_memory_field.png"), dpi=200)
    plt.close()

    print("NEXAH v39 complete")
    print(f"Attractors detected: {len(attractors)}")
    print(f"Outputs written to: {OUT_DIR}")

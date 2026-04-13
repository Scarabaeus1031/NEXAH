# APPLICATIONS/power_systems/nexah_ieee9/controller/nexah_closed_loop_ieee9_v10_5.py

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# V10.5 — Adaptive Field / Target Navigator
# ============================================================
# Idea:
# - field force dominates in low-risk region
# - target force dominates as risk grows
# - 2D navigation in (lambda, psi)
# - synthetic surrogate dynamics for first navigator prototype
# ============================================================


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def clip(x, lo, hi):
    return max(lo, min(hi, x))


def synthetic_risk(lam, psi):
    """
    Smooth surrogate risk field.
    Risk rises for larger lambda and lower psi.
    """
    z = 7.0 * (lam - 1.72) + 5.0 * (0.74 - psi)
    return clip(sigmoid(z), 0.0, 1.0)


def synthetic_distance(lam, psi):
    """
    Surrogate 'distance to separatrix'.
    Lower values mean closer to the critical structural boundary.
    """
    d = (
        1.26
        - 0.36 * (lam - 1.25)
        + 0.22 * (psi - 0.55)
        + 0.10 * (lam - 1.25) ** 2
        + 0.08 * (psi - 0.55) ** 2
    )
    return max(0.35, d)


def field_vector(lam, psi):
    """
    Native field dynamics:
    - pushes lambda upward early
    - bends psi upward in mid-region
    - weak rotational structure
    """
    cx, cy = 1.18, 0.78

    radial_x = -(lam - cx)
    radial_y = -(psi - cy)

    rot_x = -(psi - cy)
    rot_y = +(lam - cx)

    drift_x = 0.085
    drift_y = 0.010

    fx = 0.18 * radial_x + 0.11 * rot_x + drift_x
    fy = 0.16 * radial_y + 0.09 * rot_y + drift_y
    return fx, fy


def target_vector(lam, psi, lam_target, psi_target):
    """
    Attractive target force.
    """
    return lam_target - lam, psi_target - psi


def potential(lam, psi, lam_target, psi_target):
    return 0.5 * ((lam - lam_target) ** 2 + (psi - psi_target) ** 2)


def main():
    steps = 180
    dt = 0.18

    # --------------------------------------------------------
    # Initial state
    # --------------------------------------------------------
    lam = 0.58
    psi = 0.46

    # --------------------------------------------------------
    # Navigation target
    # --------------------------------------------------------
    lam_target = 1.02
    psi_target = 0.86
    target_distance = 0.45

    # --------------------------------------------------------
    # Weighting parameters
    # --------------------------------------------------------
    alpha = 7.5           # how strongly risk suppresses pure field following
    distance_gain = 0.9   # extra urgency if still far away from target regime
    target_gain = 0.85
    field_gain = 1.00

    # damping / stability
    damping_lambda = 0.08
    damping_psi = 0.10

    # bounds
    lam_min, lam_max = 0.50, 2.30
    psi_min, psi_max = 0.20, 1.20

    # --------------------------------------------------------
    # Storage
    # --------------------------------------------------------
    rows = []
    prev_risk = None

    out_dir = "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v10_5"
    os.makedirs(out_dir, exist_ok=True)

    # --------------------------------------------------------
    # Simulation loop
    # --------------------------------------------------------
    for k in range(steps):
        risk = synthetic_risk(lam, psi)
        dist = synthetic_distance(lam, psi)

        grad = 0.0 if prev_risk is None else (risk - prev_risk)
        prev_risk = risk

        fx, fy = field_vector(lam, psi)
        tx, ty = target_vector(lam, psi, lam_target, psi_target)

        # adaptive weights:
        # low risk -> follow field
        # higher risk -> move more deliberately toward target
        w_field = np.exp(-alpha * risk)
        w_target = 1.0 - w_field

        # if still far from desired safe geometry, increase target pull slightly
        distance_factor = clip((dist - target_distance) / max(target_distance, 1e-6), 0.0, 3.0)
        w_target_eff = clip(w_target + distance_gain * 0.20 * distance_factor, 0.0, 1.5)

        dlambda = (
            field_gain * w_field * fx
            + target_gain * w_target_eff * tx
            - damping_lambda * (lam - lam_target)
        )
        dpsi = (
            field_gain * w_field * fy
            + target_gain * w_target_eff * ty
            - damping_psi * (psi - psi_target)
        )

        lam = clip(lam + dt * dlambda, lam_min, lam_max)
        psi = clip(psi + dt * dpsi, psi_min, psi_max)

        V = potential(lam, psi, lam_target, psi_target)

        rows.append(
            {
                "step": k,
                "lambda": lam,
                "psi": psi,
                "risk": risk,
                "distance": dist,
                "risk_grad": grad,
                "field_lambda": fx,
                "field_psi": fy,
                "target_lambda": tx,
                "target_psi": ty,
                "w_field": w_field,
                "w_target": w_target_eff,
                "dlambda": dlambda,
                "dpsi": dpsi,
                "potential": V,
            }
        )

        print(
            f"[STEP {k}] "
            f"lambda={lam:.4f} psi={psi:.4f} "
            f"risk={risk:.4f} dist={dist:.4f} grad={grad:.4f} "
            f"wF={w_field:.3f} wT={w_target_eff:.3f} "
            f"d=({dlambda:.4f},{dpsi:.4f})"
        )

    # --------------------------------------------------------
    # Export
    # --------------------------------------------------------
    df = pd.DataFrame(rows)
    csv_path = os.path.join(out_dir, "output_v10_5_data.csv")
    df.to_csv(csv_path, index=False)

    # --------------------------------------------------------
    # Plot 1: Timeseries
    # --------------------------------------------------------
    plt.figure(figsize=(12, 7))
    plt.plot(df["step"], df["lambda"], label="lambda")
    plt.plot(df["step"], df["psi"], label="psi")
    plt.plot(df["step"], df["risk"], label="risk")
    plt.plot(df["step"], df["distance"], label="distance")
    plt.plot(df["step"], df["w_field"], label="w_field", linestyle="--")
    plt.plot(df["step"], df["w_target"], label="w_target", linestyle="--")
    plt.axhline(target_distance, linestyle="--", label="target_distance")
    plt.title("NEXAH v10.5 Adaptive Navigation")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plot_path = os.path.join(out_dir, "output_v10_5_plot.png")
    plt.tight_layout()
    plt.savefig(plot_path, dpi=160)
    plt.close()

    # --------------------------------------------------------
    # Plot 2: Risk vs Distance
    # --------------------------------------------------------
    plt.figure(figsize=(8, 7))
    sc = plt.scatter(
        df["risk"],
        df["distance"],
        c=df["step"],
        cmap="viridis",
        s=55,
    )
    plt.plot(df["risk"], df["distance"], alpha=0.35)
    plt.axhline(target_distance, linestyle="--", label="target_distance")
    plt.xlabel("Risk")
    plt.ylabel("Distance")
    plt.title("NEXAH v10.5 Phase Plot (Risk vs Distance)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.colorbar(sc, label="Step")
    phase_rd_path = os.path.join(out_dir, "output_v10_5_phase_risk_distance.png")
    plt.tight_layout()
    plt.savefig(phase_rd_path, dpi=160)
    plt.close()

    # --------------------------------------------------------
    # Plot 3: lambda vs psi
    # --------------------------------------------------------
    plt.figure(figsize=(8, 7))
    sc = plt.scatter(
        df["lambda"],
        df["psi"],
        c=df["step"],
        cmap="viridis",
        s=55,
    )
    plt.plot(df["lambda"], df["psi"], alpha=0.35)
    plt.scatter([lam_target], [psi_target], marker="x", s=120, label="target")
    plt.xlabel("lambda")
    plt.ylabel("psi")
    plt.title("NEXAH v10.5 True Phase Portrait (lambda vs psi)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.colorbar(sc, label="Step")
    phase_lp_path = os.path.join(out_dir, "output_v10_5_phase_lambda_psi.png")
    plt.tight_layout()
    plt.savefig(phase_lp_path, dpi=160)
    plt.close()

    print("\nSaved:")
    print(csv_path)
    print(plot_path)
    print(phase_rd_path)
    print(phase_lp_path)


if __name__ == "__main__":
    main()

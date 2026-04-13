#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NEXAH Closed Loop IEEE9 v10.3
-----------------------------
First minimal 2D navigator with:

- lambda  : loading / progress coordinate
- psi     : internal phase / navigator coordinate
- risk    : derived from lambda and psi
- distance: derived from lambda and psi
- vector field with:
    * drift
    * restoring term
    * rotational coupling
    * soft damping
    * mild barrier near high-risk region

Goal:
- move beyond pure 1D saturation
- create visible 2D phase motion
- keep dynamics stable and interpretable
- export plots + CSV

Outputs:
APPLICATIONS/power_systems/nexah_ieee9/results/controller_v10_3/
    output_v10_3_data.csv
    output_v10_3_plot.png
    output_v10_3_phase_risk_distance.png
    output_v10_3_phase_lambda_psi.png
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

BASE_RESULTS = Path(
    "APPLICATIONS/power_systems/nexah_ieee9/results/controller_v10_3"
)
BASE_RESULTS.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def sigmoid(x: float) -> float:
    return 1.0 / (1.0 + np.exp(-x))


# ---------------------------------------------------------------------
# Field model
# ---------------------------------------------------------------------

def compute_risk(lam: float, psi: float) -> float:
    """
    Smooth synthetic risk surface.

    Risk increases with lambda and is modulated by psi.
    """
    core = sigmoid(7.0 * (lam - 1.72))
    phase_mod = 0.08 * (psi - 0.35) ** 2 + 0.02 * np.sin(4.0 * psi)
    risk = core + phase_mod - 0.02
    return clamp(risk, 0.0, 1.0)


def compute_distance(lam: float, psi: float) -> float:
    """
    Synthetic distance-to-collapse / separatrix proxy.

    Larger lambda reduces distance.
    Psi can either help or hurt depending on where the orbit sits.
    """
    base = 1.42 - 0.34 * (lam - 0.5)
    phase_term = 0.22 * (psi - 0.55) ** 2 - 0.03 * np.cos(3.0 * psi)
    dist = base + phase_term
    return max(dist, 0.0)


def potential(lam: float, psi: float) -> float:
    """
    Synthetic navigation potential.
    Lower is better.
    """
    risk = compute_risk(lam, psi)
    dist = compute_distance(lam, psi)

    # Prefer moderate lambda, decent phase location, larger distance, lower risk
    target_lambda = 1.25
    target_psi = 0.78

    v = (
        1.8 * risk
        + 0.35 * (lam - target_lambda) ** 2
        + 0.75 * (psi - target_psi) ** 2
        + 0.6 / (dist + 0.25)
    )
    return v


def field_vector(lam: float, psi: float, step: int) -> tuple[float, float, dict]:
    """
    2D vector field:
      dlam/dt = drift + restoring + rotational coupling - damping - barrier
      dpsi/dt = phase drift + restoring + rotational coupling - damping

    The rotation term is the key new ingredient in v10.3.
    """
    risk = compute_risk(lam, psi)
    dist = compute_distance(lam, psi)

    # --- desired region / soft attractor
    lam_star = 1.28
    psi_star = 0.82

    # --- base drift
    lam_drift = 0.010
    psi_drift = 0.004

    # --- restoring terms toward target region
    lam_restore = -0.090 * (lam - lam_star)
    psi_restore = -0.140 * (psi - psi_star)

    # --- rotational coupling
    # creates phase-plane circulation rather than pure 1D saturation
    rot_strength = 0.11
    lam_rot = -rot_strength * (psi - psi_star)
    psi_rot = +rot_strength * (lam - lam_star)

    # --- mild nonlinear shaping
    lam_nonlin = -0.015 * (lam - lam_star) ** 3
    psi_nonlin = -0.030 * (psi - psi_star) ** 3

    # --- damping grows with risk
    lam_damp = 0.030 * risk
    psi_damp = 0.020 * risk

    # --- barrier near critical loading
    barrier = 0.16 * sigmoid(16.0 * (lam - 1.88))
    lam_barrier = barrier

    # --- distance-based outward push if too close to collapse geometry
    dist_push = 0.0
    if dist < 0.72:
        dist_push = 0.10 * (0.72 - dist)

    # --- slight schedule: after early phase, let system breathe a bit more
    if step > 60:
        psi_drift += 0.0015
        rot_strength += 0.01
        lam_rot = -rot_strength * (psi - psi_star)
        psi_rot = +rot_strength * (lam - lam_star)

    dlam = (
        lam_drift
        + lam_restore
        + lam_rot
        + lam_nonlin
        + dist_push
        - lam_damp
        - lam_barrier
    )

    dpsi = (
        psi_drift
        + psi_restore
        + psi_rot
        + psi_nonlin
        - psi_damp
    )

    components = {
        "lam_drift": lam_drift,
        "psi_drift": psi_drift,
        "lam_restore": lam_restore,
        "psi_restore": psi_restore,
        "lam_rot": lam_rot,
        "psi_rot": psi_rot,
        "lam_nonlin": lam_nonlin,
        "psi_nonlin": psi_nonlin,
        "lam_damp": lam_damp,
        "psi_damp": psi_damp,
        "lam_barrier": lam_barrier,
        "dist_push": dist_push,
        "risk": risk,
        "distance": dist,
        "potential": potential(lam, psi),
    }
    return dlam, dpsi, components


def classify_state(risk: float, distance: float) -> str:
    if risk < 0.18 and distance > 0.90:
        return "NEXIT"
    if risk < 0.34 and distance > 0.75:
        return "ENGAGE"
    if risk < 0.60 and distance > 0.55:
        return "LOCK"
    return "CRITICAL"


# ---------------------------------------------------------------------
# Simulation
# ---------------------------------------------------------------------

def run_simulation(n_steps: int = 180, dt: float = 0.65) -> pd.DataFrame:
    lam = 0.50
    psi = 0.48

    rows: list[dict] = []
    prev_risk = None

    for step in range(n_steps):
        dlam, dpsi, c = field_vector(lam, psi, step)

        # Euler step
        lam = lam + dt * dlam
        psi = psi + dt * dpsi

        # keep within interpretable bounds
        lam = clamp(lam, 0.45, 2.10)
        psi = clamp(psi, 0.15, 1.25)

        risk = compute_risk(lam, psi)
        distance = compute_distance(lam, psi)
        grad = risk if prev_risk is None else risk - prev_risk
        prev_risk = risk
        state = classify_state(risk, distance)

        print(
            f"[STEP {step}] "
            f"lambda={lam:.4f} psi={psi:.4f} "
            f"risk={risk:.4f} dist={distance:.4f} grad={grad:.4f} "
            f"field=({dlam:.4f},{dpsi:.4f}) state={state}"
        )

        rows.append(
            {
                "step": step,
                "lambda": lam,
                "psi": psi,
                "risk": risk,
                "distance": distance,
                "grad": grad,
                "state": state,
                "dlam": dlam,
                "dpsi": dpsi,
                "lam_drift": c["lam_drift"],
                "psi_drift": c["psi_drift"],
                "lam_restore": c["lam_restore"],
                "psi_restore": c["psi_restore"],
                "lam_rot": c["lam_rot"],
                "psi_rot": c["psi_rot"],
                "lam_nonlin": c["lam_nonlin"],
                "psi_nonlin": c["psi_nonlin"],
                "lam_damp": c["lam_damp"],
                "psi_damp": c["psi_damp"],
                "lam_barrier": c["lam_barrier"],
                "dist_push": c["dist_push"],
                "potential": c["potential"],
            }
        )

    return pd.DataFrame(rows)


# ---------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------

def make_plots(df: pd.DataFrame) -> None:
    # Time series
    plt.figure(figsize=(12, 7))
    plt.plot(df["step"], df["lambda"], label="lambda")
    plt.plot(df["step"], df["psi"], label="psi")
    plt.plot(df["step"], df["risk"], label="risk")
    plt.plot(df["step"], df["distance"], label="distance")
    plt.plot(df["step"], df["potential"], label="potential")
    plt.plot(df["step"], df["dlam"], label="dlam")
    plt.plot(df["step"], df["dpsi"], label="dpsi")
    plt.title("NEXAH Closed Loop v10.3 (2D Navigator)")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(BASE_RESULTS / "output_v10_3_plot.png", dpi=160)
    plt.close()

    # Phase plot: risk vs distance
    plt.figure(figsize=(8, 8))
    plt.scatter(
        df["risk"],
        df["distance"],
        c=df["step"],
        s=55,
    )
    plt.plot(df["risk"], df["distance"], alpha=0.5)
    plt.axhline(0.45, linestyle="--", linewidth=1.5, label="target_distance")
    plt.title("NEXAH v10.3 Phase Plot (Risk vs Distance)")
    plt.xlabel("Risk")
    plt.ylabel("Distance")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.colorbar(label="Step")
    plt.tight_layout()
    plt.savefig(BASE_RESULTS / "output_v10_3_phase_risk_distance.png", dpi=160)
    plt.close()

    # True phase portrait: lambda vs psi
    plt.figure(figsize=(8, 8))
    plt.scatter(
        df["lambda"],
        df["psi"],
        c=df["step"],
        s=55,
    )
    plt.plot(df["lambda"], df["psi"], alpha=0.5)
    plt.title("NEXAH v10.3 True Phase Portrait (lambda vs psi)")
    plt.xlabel("lambda")
    plt.ylabel("psi")
    plt.grid(True, alpha=0.3)
    plt.colorbar(label="Step")
    plt.tight_layout()
    plt.savefig(BASE_RESULTS / "output_v10_3_phase_lambda_psi.png", dpi=160)
    plt.close()


# ---------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------

def main() -> None:
    df = run_simulation(n_steps=180, dt=0.65)
    csv_path = BASE_RESULTS / "output_v10_3_data.csv"
    df.to_csv(csv_path, index=False)
    make_plots(df)

    print("\nSaved:")
    print(csv_path)
    print(BASE_RESULTS / "output_v10_3_plot.png")
    print(BASE_RESULTS / "output_v10_3_phase_risk_distance.png")
    print(BASE_RESULTS / "output_v10_3_phase_lambda_psi.png")


if __name__ == "__main__":
    main()

import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "outputs" / "run_017_state_region_map"


# ============================================================
# Utils
# ============================================================

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)

    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return float(t[i])

    return None


def normalize_signal(x):
    x = np.asarray(x, dtype=float)
    return x / (np.max(np.abs(x)) + 1e-8)


# ============================================================
# Scenario
# ============================================================

def make_synthetic_scenario(kind="nonlinear", n=500):
    t = np.linspace(0, 100, n)
    V = 1.0 - 0.002 * t - 0.0005 * t**2

    if kind == "nonlinear":
        V += 0.015 * np.exp((t - 16) / 4.0) * (t < 25)
        V += 0.01 * np.sin(0.8 * t) * (t < 25)

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V += 0.01 * rng.normal(size=len(t))

    return t, V


# ============================================================
# Signals
# ============================================================

def compute_state_signals(t, V, sigma=2):
    V_smooth = gaussian_filter1d(V, sigma=sigma)
    dv_dt = gaussian_filter1d(np.gradient(V_smooth, t), sigma=sigma)
    d2v_dt2 = gaussian_filter1d(np.gradient(dv_dt, t), sigma=sigma)

    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    kappa = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma=sigma,
    )

    dx = np.diff(x, axis=0)
    drift = np.linalg.norm(dx, axis=1)
    drift = np.concatenate([[0.0], drift])
    drift = gaussian_filter1d(drift, sigma=sigma)

    return V_smooth, dv_dt, d2v_dt2, kappa, drift


def classify_regions(V_smooth, kappa, drift):
    stable_idx = int(0.30 * len(V_smooth))

    kappa_th = np.mean(kappa[:stable_idx]) + 2.0 * np.std(kappa[:stable_idx])
    drift_th = np.mean(drift[:stable_idx]) + 2.0 * np.std(drift[:stable_idx])

    regions = np.full(len(V_smooth), "stable", dtype=object)

    regions[(kappa > kappa_th) | (drift > drift_th)] = "transition"
    regions[V_smooth < 0.7] = "collapse"

    return regions, kappa_th, drift_th


# ============================================================
# Main
# ============================================================

def run(kind="nonlinear"):
    print("\n=== RUN 017 — STATE REGION MAP ===")

    t, V = make_synthetic_scenario(kind=kind)
    V_smooth, dv_dt, d2v_dt2, kappa, drift = compute_state_signals(t, V)

    regions, kappa_th, drift_th = classify_regions(V_smooth, kappa, drift)

    t_collapse = sustained_first_crossing(V_smooth < 0.7, t)
    t_transition = sustained_first_crossing(regions == "transition", t)

    print("\n=== RESULTS ===")
    print(f"scenario:      {kind}")
    print(f"t_transition:  {t_transition}")
    print(f"t_collapse:    {t_collapse}")
    print(f"kappa_th:      {kappa_th}")
    print(f"drift_th:      {drift_th}")

    # --------------------------------------------------------
    # Plot 1: state region map V vs dV/dt
    # --------------------------------------------------------
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    color_map = {
        "stable": "tab:blue",
        "transition": "tab:orange",
        "collapse": "tab:red",
    }

    colors = [color_map[r] for r in regions]

    plt.figure(figsize=(8, 6))
    plt.scatter(V_smooth, dv_dt, c=colors, s=22, alpha=0.85)

    # trajectory line
    plt.plot(V_smooth, dv_dt, color="black", alpha=0.25, linewidth=1)

    plt.title("State Region Map — V vs dV/dt")
    plt.xlabel("Voltage V(t)")
    plt.ylabel("dV/dt")
    plt.grid(alpha=0.3)

    # legend proxies
    for label, color in color_map.items():
        plt.scatter([], [], c=color, label=label)

    plt.legend()
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_01_state_region_map.png", dpi=150)

    # --------------------------------------------------------
    # Plot 2: state map colored by curvature
    # --------------------------------------------------------
    plt.figure(figsize=(8, 6))
    sc = plt.scatter(
        V_smooth,
        dv_dt,
        c=normalize_signal(kappa),
        cmap="viridis",
        s=24,
        alpha=0.9,
    )
    plt.plot(V_smooth, dv_dt, color="black", alpha=0.2, linewidth=1)

    plt.title("State Map Colored by Curvature κ(t)")
    plt.xlabel("Voltage V(t)")
    plt.ylabel("dV/dt")
    plt.colorbar(sc, label="normalized κ(t)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_02_curvature_map.png", dpi=150)

    # --------------------------------------------------------
    # Plot 3: time map with region bands
    # --------------------------------------------------------
    plt.figure(figsize=(12, 5))

    plt.plot(t, V_smooth, color="black", linewidth=2, label="Voltage V(t)")
    plt.plot(t, normalize_signal(kappa), color="orange", label="κ(t)")
    plt.plot(t, normalize_signal(drift), color="red", label="drift(t)")

    for i in range(len(t) - 1):
        if regions[i] == "transition":
            plt.axvspan(t[i], t[i + 1], color="orange", alpha=0.12)
        elif regions[i] == "collapse":
            plt.axvspan(t[i], t[i + 1], color="red", alpha=0.10)

    if t_transition is not None:
        plt.axvline(t_transition, color="orange", linestyle="--", label="transition start")

    if t_collapse is not None:
        plt.axvline(t_collapse, color="black", linestyle="-", linewidth=2, label="collapse")

    plt.title("Region Timeline — Stable / Transition / Collapse")
    plt.xlabel("Time (simulation steps)")
    plt.ylabel("Normalized signal")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_03_region_timeline.png", dpi=150)

    # --------------------------------------------------------
    # Save data
    # --------------------------------------------------------
    results = {
        "scenario": kind,
        "t_transition": t_transition,
        "t_collapse": t_collapse,
        "kappa_threshold": float(kappa_th),
        "drift_threshold": float(drift_th),
        "region_counts": {
            "stable": int(np.sum(regions == "stable")),
            "transition": int(np.sum(regions == "transition")),
            "collapse": int(np.sum(regions == "collapse")),
        },
        "interpretation": (
            "State region map separates stable, transition, and collapse regions "
            "using curvature and drift thresholds."
        ),
    }

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to: {OUT_DIR}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run(kind="nonlinear")

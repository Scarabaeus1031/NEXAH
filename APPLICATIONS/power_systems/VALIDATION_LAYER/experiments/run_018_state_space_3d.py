import json
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "outputs" / "run_018_state_space_3d"


# ============================================================
# Utils
# ============================================================

def sustained_first_crossing(mask, t, min_samples=3):
    mask = np.asarray(mask, dtype=bool)
    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return float(t[i])
    return None


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

    curvature = gaussian_filter1d(
        np.linalg.norm(np.gradient(np.gradient(x, axis=0), axis=0), axis=1),
        sigma=sigma
    )

    drift = np.linalg.norm(np.diff(x, axis=0), axis=1)
    drift = np.concatenate([[0.0], drift])
    drift = gaussian_filter1d(drift, sigma=sigma)

    return V_smooth, dv_dt, d2v_dt2, curvature, drift


def classify_regions(V_smooth, curvature, drift):
    stable_idx = int(0.30 * len(V_smooth))

    kappa_th = np.mean(curvature[:stable_idx]) + 2 * np.std(curvature[:stable_idx])
    drift_th = np.mean(drift[:stable_idx]) + 2 * np.std(drift[:stable_idx])

    regions = np.full(len(V_smooth), "stable", dtype=object)

    regions[(curvature > kappa_th) | (drift > drift_th)] = "transition"
    regions[V_smooth < 0.7] = "collapse"

    return regions, kappa_th, drift_th


# ============================================================
# MAIN
# ============================================================

def run(kind="nonlinear"):
    print("\n=== RUN 018 — 3D STATE SPACE ===")

    t, V = make_synthetic_scenario(kind=kind)

    V_smooth, dv_dt, d2v_dt2, curvature, drift = compute_state_signals(t, V)
    regions, kappa_th, drift_th = classify_regions(V_smooth, curvature, drift)

    t_transition = sustained_first_crossing(regions == "transition", t)
    t_collapse = sustained_first_crossing(V_smooth < 0.7, t)

    print("\n=== RESULTS ===")
    print(f"scenario:     {kind}")
    print(f"t_transition: {t_transition}")
    print(f"t_collapse:   {t_collapse}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------------
    # 3D Plot
    # --------------------------------------------------------
    from mpl_toolkits.mplot3d import Axes3D  # noqa

    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    color_map = {
        "stable": "tab:blue",
        "transition": "tab:orange",
        "collapse": "tab:red",
    }

    colors = [color_map[r] for r in regions]

    # scatter
    ax.scatter(
        V_smooth,
        dv_dt,
        d2v_dt2,
        c=colors,
        s=18,
        alpha=0.9
    )

    # trajectory line
    ax.plot(
        V_smooth,
        dv_dt,
        d2v_dt2,
        color="black",
        alpha=0.25,
        linewidth=1
    )

    ax.set_title("3D State Space — (V, dV/dt, d²V/dt²)")
    ax.set_xlabel("V(t)")
    ax.set_ylabel("dV/dt")
    ax.set_zlabel("d²V/dt²")

    # legend proxies
    for label, color in color_map.items():
        ax.scatter([], [], [], c=color, label=label)

    ax.legend()

    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_01_state_space_3d.png", dpi=150)

    # --------------------------------------------------------
    # Alternative: color by curvature (structure view)
    # --------------------------------------------------------
    fig = plt.figure(figsize=(9, 7))
    ax = fig.add_subplot(111, projection="3d")

    norm_kappa = curvature / (np.max(curvature) + 1e-8)

    sc = ax.scatter(
        V_smooth,
        dv_dt,
        d2v_dt2,
        c=norm_kappa,
        cmap="viridis",
        s=18,
        alpha=0.9
    )

    ax.plot(
        V_smooth,
        dv_dt,
        d2v_dt2,
        color="black",
        alpha=0.2,
        linewidth=1
    )

    ax.set_title("3D State Space — colored by κ(t)")
    ax.set_xlabel("V(t)")
    ax.set_ylabel("dV/dt")
    ax.set_zlabel("d²V/dt²")

    fig.colorbar(sc, ax=ax, label="normalized κ(t)")

    plt.tight_layout()
    plt.savefig(OUT_DIR / "figure_02_state_space_curvature.png", dpi=150)

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------
    results = {
        "scenario": kind,
        "t_transition": t_transition,
        "t_collapse": t_collapse,
        "kappa_threshold": float(kappa_th),
        "drift_threshold": float(drift_th),
        "interpretation": (
            "3D state space reveals separation between stable, transition, "
            "and collapse regimes as geometric structure."
        )
    }

    with open(OUT_DIR / "results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved to: {OUT_DIR}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    run(kind="nonlinear")

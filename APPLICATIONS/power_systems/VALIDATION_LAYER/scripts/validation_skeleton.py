import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


# ============================================================
# ⚡ NEXAH Validation Skeleton
# Golden Line Validation — Engineering Version
# ============================================================


def sustained_first_crossing(mask, t, min_samples=3):
    """
    Return first time where mask stays True for min_samples.
    Prevents single-sample noise spikes from defining detection.
    """
    mask = np.asarray(mask, dtype=bool)

    if min_samples <= 1:
        idx = np.where(mask)[0]
        return t[idx[0]] if len(idx) > 0 else None

    for i in range(0, len(mask) - min_samples + 1):
        if np.all(mask[i:i + min_samples]):
            return t[i]

    return None


def compute_lead_time(t_collapse, t_detection):
    if t_collapse is None or t_detection is None:
        return None
    return t_collapse - t_detection


def run_validation(
    data,
    output_dir="APPLICATIONS/power_systems/VALIDATION_LAYER/outputs",
    scenario_name="synthetic_validation",
):
    # --------------------------------------------------------
    # Input
    # --------------------------------------------------------
    t = np.asarray(data["time"])
    V = np.asarray(data["voltage"])

    os.makedirs(output_dir, exist_ok=True)

    # --------------------------------------------------------
    # Fixed parameters — do not tune after seeing results
    # --------------------------------------------------------
    V_threshold = 0.7
    dv_threshold = -0.02

    stable_fraction = 0.30
    smooth_sigma = 2
    sustained_samples = 3

    stable_idx = int(stable_fraction * len(t))

    if stable_idx < 5:
        raise ValueError("Stable window too small. Increase time series length.")

    # --------------------------------------------------------
    # Feature extraction
    # --------------------------------------------------------
    V_smooth = gaussian_filter1d(V, sigma=smooth_sigma)

    dv_dt = np.gradient(V_smooth, t)
    dv_dt = gaussian_filter1d(dv_dt, sigma=smooth_sigma)

    d2v_dt2 = np.gradient(dv_dt, t)
    d2v_dt2 = gaussian_filter1d(d2v_dt2, sigma=smooth_sigma)

    # --------------------------------------------------------
    # Reconstructed NEXAH state
    # x(t) = (V, dV/dt, d²V/dt²)
    # --------------------------------------------------------
    x = np.vstack([V_smooth, dv_dt, d2v_dt2]).T

    x_stable = x[:stable_idx]
    mu_stable = np.mean(x_stable, axis=0)

    distance = np.linalg.norm(x - mu_stable, axis=1)

    d_dist = np.gradient(distance, t)
    d_dist = gaussian_filter1d(d_dist, sigma=smooth_sigma)

    # --------------------------------------------------------
    # Thresholds
    # IMPORTANT:
    # Thresholds are computed ONLY from stable window.
    # No future leakage.
    # --------------------------------------------------------
    dv_stable = dv_dt[:stable_idx]
    d_dist_stable = d_dist[:stable_idx]

    nexah_threshold = np.mean(d_dist_stable) + 2.0 * np.std(d_dist_stable)

    # Classical threshold remains fixed.
    # dv_threshold is NOT estimated from full signal.
    # This keeps baseline honest and reproducible.

    # --------------------------------------------------------
    # Detection
    # --------------------------------------------------------
    collapse_mask = V_smooth < V_threshold
    classical_mask = dv_dt < dv_threshold
    nexah_mask = d_dist > nexah_threshold

    t_collapse = sustained_first_crossing(
        collapse_mask,
        t,
        min_samples=sustained_samples,
    )

    t_classical = sustained_first_crossing(
        classical_mask,
        t,
        min_samples=sustained_samples,
    )

    t_nexah = sustained_first_crossing(
        nexah_mask,
        t,
        min_samples=sustained_samples,
    )

    lead_classical = compute_lead_time(t_collapse, t_classical)
    lead_nexah = compute_lead_time(t_collapse, t_nexah)

    # --------------------------------------------------------
    # Console output
    # --------------------------------------------------------
    print("\n=== NEXAH GOLDEN LINE VALIDATION ===")
    print(f"Scenario:    {scenario_name}")
    print(f"Collapse:    {t_collapse}")
    print(f"Classical:   {t_classical} -> lead time = {lead_classical}")
    print(f"NEXAH:       {t_nexah} -> lead time = {lead_nexah}")
    print("")
    print("Thresholds:")
    print(f"V threshold:        {V_threshold}")
    print(f"dv/dt threshold:    {dv_threshold}")
    print(f"NEXAH threshold:    {nexah_threshold}")
    print("")
    print("Stable window:")
    print(f"fraction:           {stable_fraction}")
    print(f"samples:            {stable_idx}")

    # --------------------------------------------------------
    # Save lead-time table
    # --------------------------------------------------------
    csv_path = os.path.join(output_dir, f"{scenario_name}_lead_times.csv")

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["method", "detection_time", "collapse_time", "lead_time"])
        writer.writerow(["classical", t_classical, t_collapse, lead_classical])
        writer.writerow(["nexah", t_nexah, t_collapse, lead_nexah])

    # --------------------------------------------------------
    # Golden Figure
    # --------------------------------------------------------
    fig, axs = plt.subplots(4, 1, figsize=(11, 12), sharex=False)

    # Panel 1 — Voltage
    axs[0].plot(t, V_smooth, label="Voltage V(t)")
    axs[0].axhline(V_threshold, linestyle=":", label="Collapse threshold")

    if t_collapse is not None:
        axs[0].axvline(t_collapse, linestyle="--", label="Collapse")
    if t_classical is not None:
        axs[0].axvline(t_classical, linestyle="--", label="Classical")
    if t_nexah is not None:
        axs[0].axvline(t_nexah, linestyle="--", label="NEXAH")

    axs[0].set_title("Voltage V(t) with Detection Markers")
    axs[0].set_ylabel("Voltage")
    axs[0].legend(loc="best")

    # Panel 2 — Distance
    axs[1].plot(t, distance, label="Distance to stable region")
    axs[1].axvspan(t[0], t[stable_idx - 1], alpha=0.12, label="Stable window")
    axs[1].set_title("NEXAH Distance Signal")
    axs[1].set_ylabel("Distance")
    axs[1].legend(loc="best")

    # Panel 3 — d/dt distance
    axs[2].plot(t, d_dist, label="d/dt distance")
    axs[2].axhline(nexah_threshold, linestyle="--", label="NEXAH threshold")
    axs[2].axvspan(t[0], t[stable_idx - 1], alpha=0.12, label="Stable window")

    if t_nexah is not None:
        axs[2].axvline(t_nexah, linestyle="--", label="NEXAH detection")
    if t_classical is not None:
        axs[2].axvline(t_classical, linestyle=":", label="Classical detection")
    if t_collapse is not None:
        axs[2].axvline(t_collapse, linestyle="-.", label="Collapse")

    axs[2].set_title("NEXAH Early Signal: d/dt Distance")
    axs[2].set_ylabel("d/dt distance")
    axs[2].legend(loc="best")

    # Panel 4 — State space
    sc = axs[3].scatter(V_smooth, dv_dt, c=d_dist, s=8)
    axs[3].set_title("Reconstructed State Space")
    axs[3].set_xlabel("Voltage V(t)")
    axs[3].set_ylabel("dV/dt")

    cbar = plt.colorbar(sc, ax=axs[3])
    cbar.set_label("d/dt distance")

    plt.tight_layout()

    fig_path = os.path.join(output_dir, f"{scenario_name}_golden_figure.png")
    plt.savefig(fig_path, dpi=200)
    plt.show()

    # --------------------------------------------------------
    # Return structured results
    # --------------------------------------------------------
    return {
        "scenario": scenario_name,
        "t_collapse": t_collapse,
        "t_classical": t_classical,
        "t_nexah": t_nexah,
        "lead_classical": lead_classical,
        "lead_nexah": lead_nexah,
        "nexah_threshold": nexah_threshold,
        "V_threshold": V_threshold,
        "dv_threshold": dv_threshold,
        "stable_idx": stable_idx,
        "figure_path": fig_path,
        "csv_path": csv_path,
    }


# ============================================================
# Minimal synthetic scenarios
# Replace this block later with real IEEE14 loader.
# ============================================================

def make_synthetic_scenario(kind="smooth", n=500):
    t = np.linspace(0, 100, n)

    if kind == "smooth":
        V = 1.0 - 0.002 * t - 0.0005 * t**2

    elif kind == "fast":
        V = 1.0 - 0.0015 * t - 0.0008 * t**2

    elif kind == "noisy":
        rng = np.random.default_rng(7)
        V = 1.0 - 0.002 * t - 0.0005 * t**2
        V += 0.01 * rng.normal(size=len(t))

    elif kind == "precursor":
        V = 1.0 - 0.002 * t - 0.0005 * t**2
        precursor = 0.02 * np.exp((t - 18) / 5.0)
        precursor = precursor * (t < 25)
        V += precursor

    else:
        raise ValueError(f"Unknown scenario kind: {kind}")

    return {
        "time": t,
        "voltage": V,
    }


if __name__ == "__main__":

    # Choose one:
    # "smooth"     -> may show no NEXAH early signal
    # "fast"       -> sharper collapse
    # "noisy"      -> robustness check
    # "precursor"  -> contains pre-collapse dynamical deviation

    scenario = "precursor"

    data = make_synthetic_scenario(kind=scenario)

    run_validation(
        data,
        scenario_name=f"ieee14_placeholder_{scenario}",
    )

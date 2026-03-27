import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    compute_metrics,
    detect_gh_corridor,
)
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_adapter_v2 import (
    map_ieee_to_nexah,
)

# ============================================================
# CONFIG
# ============================================================

LOADS = np.linspace(1.0, 5.0, 10)
N_BUS = 14
SEED = 42

# If you later have a real loader, switch this to True and replace
# get_ieee_raw_data() with real IEEE power-flow output.
USE_REAL_IEEE = False


# ============================================================
# DATA SOURCES
# ============================================================

def get_mock_ieee_raw_data(load: float, n_bus: int = N_BUS, seed: int = SEED) -> dict:
    """
    Load-dependent mock IEEE-like raw data.
    This is still synthetic, but now the entire pipeline is driven
    by IEEE-style variables instead of generate_phase_data().
    """
    rng = np.random.default_rng(seed + int(load * 1000))

    # Voltage magnitude: mean drops with load, spread increases with load
    voltage_magnitude = (
        1.03
        - 0.035 * (load - 1.0)
        + rng.normal(0.0, 0.004 + 0.0035 * (load - 1.0), n_bus)
    )

    # Voltage angle: spread increases with load
    angle_base = np.linspace(-1.0, 1.0, n_bus)
    voltage_angle = (
        0.02 * angle_base
        + 0.04 * (load - 1.0) * angle_base
        + rng.normal(0.0, 0.004 + 0.003 * (load - 1.0), n_bus)
    )

    # Active/reactive mismatch: both increase with load
    p_mismatch = rng.normal(0.0, 0.06 * load, n_bus)
    q_mismatch = rng.normal(0.0, 0.08 * load, n_bus)

    return {
        "voltage_magnitude": voltage_magnitude,
        "voltage_angle": voltage_angle,
        "p_mismatch": p_mismatch,
        "q_mismatch": q_mismatch,
    }


def get_ieee_raw_data(load: float) -> dict:
    """
    Replace this function later with your real IEEE loader / power-flow output.
    For now it returns mock IEEE-style data.
    """
    if USE_REAL_IEEE:
        raise NotImplementedError(
            "Connect this function to your real IEEE loader / power-flow results."
        )
    return get_mock_ieee_raw_data(load)


# ============================================================
# FULLY COUPLED PIPELINE
# ============================================================

def build_phase_space_from_raw(raw: dict) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Fully coupled mapping:
    raw IEEE variables -> theta, c, loops arrays
    """
    theta = np.mod(np.asarray(raw["voltage_angle"]), 2 * np.pi)
    c = np.asarray(raw["voltage_magnitude"])
    loops = np.abs(np.asarray(raw["p_mismatch"])) + np.abs(np.asarray(raw["q_mismatch"]))
    return theta, c, loops


# ============================================================
# MAIN
# ============================================================

def main() -> None:
    print("RUNNING IEEE SENSITIVITY TEST V3 (FULLY COUPLED)")

    results = []

    for load in LOADS:
        raw = get_ieee_raw_data(load)
        mapped = map_ieee_to_nexah(raw)

        # Fully coupled pipeline inputs
        theta, c, loops = build_phase_space_from_raw(raw)

        # Pipeline metrics now operate on adapter-driven data
        metrics = compute_metrics(theta, c, loops)
        gh = detect_gh_corridor(theta, c, loops)

        gh_theta = gh["theta_corridor"]
        gh_c = gh["c_corridor"]

        gh_points = len(gh_theta)
        gh_width_theta = float(np.ptp(gh_theta)) if gh_points > 0 else 0.0
        gh_width_c = float(np.ptp(gh_c)) if gh_points > 0 else 0.0
        gh_theta_center = float(np.mean(gh_theta)) if gh_points > 0 else np.nan
        gh_c_center = float(np.mean(gh_c)) if gh_points > 0 else np.nan

        results.append({
            "load": float(load),
            "pipeline_C": float(metrics["C"]),
            "pipeline_P": float(metrics["P"]),
            "pipeline_R": float(metrics["R"]),
            "pipeline_L": float(metrics["L"]),
            "gh_points": int(gh_points),
            "gh_width_theta": gh_width_theta,
            "gh_width_c": gh_width_c,
            "gh_theta_center": gh_theta_center,
            "gh_c_center": gh_c_center,
            "adapter_C": float(mapped["C"]),
            "adapter_theta": float(mapped["theta"]),
            "adapter_theta_spread": float(mapped["theta_spread"]),
            "adapter_loops": float(mapped["loops"]),
            "adapter_stress": float(mapped["stress"]),
            "v_mean": float(np.mean(raw["voltage_magnitude"])),
            "v_std": float(np.std(raw["voltage_magnitude"])),
            "theta_std_raw": float(np.std(raw["voltage_angle"])),
            "p_abs_sum": float(np.sum(np.abs(raw["p_mismatch"]))),
            "q_abs_sum": float(np.sum(np.abs(raw["q_mismatch"]))),
        })

    df = pd.DataFrame(results)
    out_csv = "ieee_sensitivity_test_v3.csv"
    df.to_csv(out_csv, index=False)

    print("\n--- RESULTS ---")
    print(df.round(6))
    print(f"\nSaved: {out_csv}")

    # ============================================================
    # PLOTS
    # ============================================================

    plt.figure(figsize=(14, 8))

    plt.subplot(2, 3, 1)
    plt.plot(df["load"], df["pipeline_C"], marker="o")
    plt.title("Pipeline C vs Load")
    plt.xlabel("load")

    plt.subplot(2, 3, 2)
    plt.plot(df["load"], df["gh_points"], marker="o")
    plt.title("GH Points vs Load")
    plt.xlabel("load")

    plt.subplot(2, 3, 3)
    plt.plot(df["load"], df["gh_width_theta"], marker="o")
    plt.title("GH Width θ")
    plt.xlabel("load")

    plt.subplot(2, 3, 4)
    plt.plot(df["load"], df["gh_width_c"], marker="o")
    plt.title("GH Width C")
    plt.xlabel("load")

    plt.subplot(2, 3, 5)
    plt.plot(df["load"], df["adapter_C"], marker="o")
    plt.title("Adapter C vs Load")
    plt.xlabel("load")

    plt.subplot(2, 3, 6)
    plt.plot(df["load"], df["adapter_loops"], marker="o")
    plt.title("Adapter Loops vs Load")
    plt.xlabel("load")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

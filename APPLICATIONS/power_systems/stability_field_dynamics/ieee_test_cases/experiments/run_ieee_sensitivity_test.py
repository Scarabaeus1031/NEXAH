import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.pipeline.phase_data_pipeline import (
    compute_metrics,
    detect_gh_corridor
)
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core.ieee_adapter_v2 import (
    map_ieee_to_nexah
)

# ----------------------------
# TEST CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)
N = 200
results = []

# ----------------------------
# SYNTHETIC IEEE-LIKE RAW DATA
# Replace later with real loader output
# ----------------------------

def make_ieee_like_raw_data(load: float, n: int = N) -> dict:
    """
    Minimal synthetic IEEE-like state that actually changes with load.
    This is still a proxy, but now the adapter is truly used.
    """
    rng = np.random.default_rng(42)

    # Voltage magnitude degrades and spreads with load
    voltage_magnitude = (
        1.02
        - 0.03 * (load - 1.0)
        + rng.normal(0.0, 0.005 + 0.004 * (load - 1.0), n)
    )

    # Voltage angles spread more with load
    voltage_angle = (
        rng.normal(0.0, 0.03 + 0.02 * (load - 1.0), n)
    )

    # Active/reactive mismatch increase with load
    p_mismatch = rng.normal(0.0, 0.01 * load, n)
    q_mismatch = rng.normal(0.0, 0.012 * load, n)

    return {
        "voltage_magnitude": voltage_magnitude,
        "voltage_angle": voltage_angle,
        "p_mismatch": p_mismatch,
        "q_mismatch": q_mismatch,
    }

# ----------------------------
# MAIN LOOP
# ----------------------------

for load in loads:
    raw = make_ieee_like_raw_data(load)

    mapped = map_ieee_to_nexah(raw)

    # Build phase-space arrays from raw IEEE-like data
    theta = np.mod(raw["voltage_angle"], 2 * np.pi)
    c = raw["voltage_magnitude"]
    loops = np.abs(raw["p_mismatch"]) + np.abs(raw["q_mismatch"])

    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    gh_width_theta = np.ptp(gh["theta_corridor"]) if len(gh["theta_corridor"]) > 0 else 0.0
    gh_width_c = np.ptp(gh["c_corridor"]) if len(gh["c_corridor"]) > 0 else 0.0

    results.append({
        "load": load,
        "C": metrics["C"],
        "P": metrics["P"],
        "R": metrics["R"],
        "L": metrics["L"],
        "gh_points": len(gh["theta_corridor"]),
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,
        "adapter_C": mapped["C"],
        "adapter_theta": mapped["theta"],
        "adapter_theta_spread": mapped["theta_spread"],
        "adapter_loops": mapped["loops"],
        "adapter_stress": mapped["stress"],
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(12, 8))

plt.subplot(2, 3, 1)
plt.plot(df["load"], df["C"], marker="o")
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

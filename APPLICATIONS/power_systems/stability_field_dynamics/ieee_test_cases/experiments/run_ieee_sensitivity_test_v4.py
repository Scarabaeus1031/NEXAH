```python
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

print("RUNNING IEEE SENSITIVITY TEST V3 (FULLY COUPLED)")

# ----------------------------
# CONFIG
# ----------------------------

loads = np.linspace(1.0, 5.0, 10)
N = 200
results = []

# ----------------------------
# SYNTHETIC IEEE-LIKE DATA
# ----------------------------

def make_ieee_like_raw_data(load: float, n: int = N):

    rng = np.random.default_rng(42)

    voltage_magnitude = (
        1.02
        - 0.03 * (load - 1.0)
        + rng.normal(0.0, 0.005 + 0.004 * (load - 1.0), n)
    )

    voltage_angle = rng.normal(
        0.0,
        0.03 + 0.02 * (load - 1.0),
        n
    )

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

    theta = np.mod(raw["voltage_angle"], 2 * np.pi)
    c = raw["voltage_magnitude"]
    loops = np.abs(raw["p_mismatch"]) + np.abs(raw["q_mismatch"])

    metrics = compute_metrics(theta, c, loops)
    gh = detect_gh_corridor(theta, c, loops)

    gh_width_theta = np.ptp(gh["theta_corridor"]) if len(gh["theta_corridor"]) > 0 else 0.0
    gh_width_c = np.ptp(gh["c_corridor"]) if len(gh["c_corridor"]) > 0 else 0.0

    results.append({
        "load": load,

        # pipeline
        "pipeline_C": metrics["C"],
        "pipeline_P": metrics["P"],
        "pipeline_R": metrics["R"],
        "pipeline_L": metrics["L"],

        # GH
        "gh_points": len(gh["theta_corridor"]),
        "gh_width_theta": gh_width_theta,
        "gh_width_c": gh_width_c,

        # adapter
        "adapter_C": mapped["C"],
        "adapter_loops": mapped["loops"],
        "adapter_theta": mapped["theta"],
        "adapter_theta_spread": mapped["theta_spread"],
        "adapter_stress": mapped["stress"],

        # raw diagnostics
        "voltage_mean": np.mean(raw["voltage_magnitude"]),
        "voltage_std": np.std(raw["voltage_magnitude"]),
        "theta_std_raw": np.std(raw["voltage_angle"]),
        "p_abs_sum": np.sum(np.abs(raw["p_mismatch"])),
        "q_abs_sum": np.sum(np.abs(raw["q_mismatch"]))
    })

# ----------------------------
# SAVE
# ----------------------------

df = pd.DataFrame(results)
df.to_csv("ieee_sensitivity_test_v3.csv", index=False)

print("\n--- RESULTS ---")
print(df)

# ----------------------------
# PLOTS
# ----------------------------

plt.figure(figsize=(14, 8))

plt.subplot(2, 3, 1)
plt.plot(df["load"], df["pipeline_C"], marker="o")
plt.title("Pipeline C vs Load")

plt.subplot(2, 3, 2)
plt.plot(df["load"], df["gh_points"], marker="o")
plt.title("GH Points vs Load")

plt.subplot(2, 3, 3)
plt.plot(df["load"], df["gh_width_theta"], marker="o")
plt.title("GH Width θ")

plt.subplot(2, 3, 4)
plt.plot(df["load"], df["gh_width_c"], marker="o")
plt.title("GH Width C")

plt.subplot(2, 3, 5)
plt.plot(df["load"], df["adapter_C"], marker="o")
plt.title("Adapter C vs Load")

plt.subplot(2, 3, 6)
plt.plot(df["load"], df["adapter_loops"], marker="o")
plt.title("Adapter Loops vs Load")

plt.tight_layout()
plt.show()
```

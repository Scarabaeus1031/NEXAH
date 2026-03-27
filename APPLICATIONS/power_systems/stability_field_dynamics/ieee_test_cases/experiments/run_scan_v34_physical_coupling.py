# APPLICATIONS/.../run_scan_v34_physical_coupling.py

import numpy as np
import pandas as pd
import time

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling
from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.ieee_loader import load_ieee14


# =========================
# PHASE CLASSIFIER (reuse logic)
# =========================
def classify_phase(loops, C, loops_low, loops_high, c_low, c_high):
    if loops <= loops_low and C <= c_low:
        return "KKK"
    elif loops >= loops_high and C >= c_high:
        return "CCC"
    else:
        return "GH"


# =========================
# EXTRACT MIN VOLTAGE
# =========================
def compute_min_voltage(base_load):
    net = load_ieee14()

    # einfache Skalierung der Last
    net.load["p_mw"] *= base_load

    try:
        import pandapower as pp
        pp.runpp(net, init="auto", max_iteration=20)
        return float(net.res_bus.vm_pu.min())
    except:
        return np.nan


# =========================
# MAIN SCAN
# =========================
def main():
    print("\n--- V34 Physical Coupling Scan ---\n")

    k_values = [1.0, 1.5, 2.0]
    load_values = [1.0, 2.0, 3.0, 4.0]

    records = []

    for base_load in load_values:
        print(f"\n=== LOAD {base_load} ===")

        min_v = compute_min_voltage(base_load)
        print(f"min_voltage = {min_v:.4f}")

        for k in k_values:

            for t in range(24):
                t0 = time.time()

                # gleiche Phase-Parameter wie V32/V33
                angle = 2 * np.pi * t / 24

                noise = 0.15 + 0.15 * np.sin(angle)
                rotation = 0.5 + 0.3 * np.cos(k * angle)
                damping = 0.95 - 0.05 * np.sin(angle)

                try:
                    result = run_single_coupling(
                        base_load=base_load,
                        noise_strength=noise,
                        flow_rotation=rotation,
                        damping=damping,
                    )

                    loops = result["loops"]
                    C = result["C"]

                except Exception as e:
                    print("FAILED:", e)
                    loops = np.nan
                    C = np.nan

                records.append({
                    "load": base_load,
                    "k": k,
                    "t": t,
                    "noise": noise,
                    "rotation": rotation,
                    "damping": damping,
                    "loops": loops,
                    "C": C,
                    "min_voltage": min_v
                })

                dt = time.time() - t0
                print(f"t={t:02d} | C={C:.4f} | loops={loops} | dt={dt:.2f}s")

    df = pd.DataFrame(records)

    # -------------------------
    # GLOBAL THRESHOLDS
    # -------------------------
    loops_low = df["loops"].quantile(0.25)
    loops_high = df["loops"].quantile(0.75)
    c_low = df["C"].quantile(0.25)
    c_high = df["C"].quantile(0.75)

    print("\n--- GLOBAL THRESHOLDS ---")
    print(f"loops_low  = {loops_low:.3f}")
    print(f"loops_high = {loops_high:.3f}")
    print(f"c_low      = {c_low:.6f}")
    print(f"c_high     = {c_high:.6f}")

    # -------------------------
    # CLASSIFY
    # -------------------------
    df["phase"] = df.apply(
        lambda r: classify_phase(
            r["loops"], r["C"],
            loops_low, loops_high,
            c_low, c_high
        ),
        axis=1
    )

    # -------------------------
    # GH ANALYSIS
    # -------------------------
    gh = df[df["phase"] == "GH"]

    print("\n--- GH vs VOLTAGE ---")
    print(gh.groupby("load")["min_voltage"].mean())

    print("\n--- PHASE DISTRIBUTION ---")
    print(df.groupby(["load", "phase"]).size())

    # -------------------------
    # SAVE
    # -------------------------
    df.to_csv("v34_physical_coupling.csv", index=False)
    gh.to_csv("v34_gh_only.csv", index=False)

    print("\nSaved: v34_physical_coupling.csv")
    print("Saved: v34_gh_only.csv")


if __name__ == "__main__":
    main()

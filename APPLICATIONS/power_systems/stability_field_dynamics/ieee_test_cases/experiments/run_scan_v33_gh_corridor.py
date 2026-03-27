import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


def classify_phase(loops, C, loops_low, loops_high, c_low, c_high):
    if (loops <= loops_low) and (C <= c_low):
        return "KKK"
    if (loops >= loops_high) and (C >= c_high):
        return "CCC"
    return "GH"


def run_cycle(base_load, k, steps=24):
    rows = []

    print(f"\n=== Testing k = {k} ===")

    for t in range(steps):
        phase = 2 * np.pi * t / steps

        noise = 0.15 * np.sin(phase) + 0.15
        rotation = 0.5 + 0.3 * np.cos(k * phase)
        damping = 0.95 - 0.05 * np.sin(phase)

        print(f"t={t:02d} | noise={noise:.3f} | rot={rotation:.3f} | damp={damping:.3f}")

        r = run_single_coupling(
            base_load=base_load,
            noise_strength=noise,
            flow_rotation=rotation,
            damping=damping,
        )

        rows.append({
            "t": t,
            "k": k,
            "phase": phase,
            "noise": noise,
            "rotation": rotation,
            "damping": damping,
            "C": r["C"],
            "loops": r["loops"],
            "states": r["states"],
            "gap": r["gap"],
        })

    return pd.DataFrame(rows)


def main():
    print("\n--- V33 GH Corridor Detector ---\n")

    k_values = [1.0, 1.5, 2.0]
    all_results = []

    # -------------------------
    # 1) run cycles
    # -------------------------
    for k in k_values:
        df = run_cycle(base_load=1.0, k=k, steps=24)
        all_results.append(df)

    full_df = pd.concat(all_results, ignore_index=True)

    # -------------------------
    # 2) thresholds from global data
    # -------------------------
    loops_low = full_df["loops"].quantile(0.25)
    loops_high = full_df["loops"].quantile(0.75)
    c_low = full_df["C"].quantile(0.25)
    c_high = full_df["C"].quantile(0.75)

    print("\n--- GLOBAL THRESHOLDS ---")
    print(f"loops_low  = {loops_low:.3f}")
    print(f"loops_high = {loops_high:.3f}")
    print(f"c_low      = {c_low:.6f}")
    print(f"c_high     = {c_high:.6f}")

    # -------------------------
    # 3) phase classification
    # -------------------------
    full_df["phase_class"] = full_df.apply(
        lambda row: classify_phase(
            row["loops"],
            row["C"],
            loops_low,
            loops_high,
            c_low,
            c_high,
        ),
        axis=1,
    )

    gh_df = full_df[full_df["phase_class"] == "GH"].copy()
    gh_df.to_csv("v33_gh_corridor_points.csv", index=False)
    full_df.to_csv("v33_phase_full.csv", index=False)

    print("\nSaved: v33_gh_corridor_points.csv")
    print("Saved: v33_phase_full.csv")

    # -------------------------
    # 4) GH summary per k
    # -------------------------
    print("\n--- GH SUMMARY ---")
    summary_rows = []

    for k in k_values:
        sub = gh_df[gh_df["k"] == k]

        if len(sub) == 0:
            print(f"k={k}: no GH points")
            continue

        row = {
            "k": k,
            "gh_count": len(sub),
            "noise_mean": sub["noise"].mean(),
            "noise_min": sub["noise"].min(),
            "noise_max": sub["noise"].max(),
            "rotation_mean": sub["rotation"].mean(),
            "rotation_min": sub["rotation"].min(),
            "rotation_max": sub["rotation"].max(),
            "loops_mean": sub["loops"].mean(),
            "C_mean": sub["C"].mean(),
        }
        summary_rows.append(row)

        print(
            f"k={k} | count={row['gh_count']} | "
            f"noise=[{row['noise_min']:.3f}, {row['noise_max']:.3f}] | "
            f"rot=[{row['rotation_min']:.3f}, {row['rotation_max']:.3f}] | "
            f"loops_mean={row['loops_mean']:.3f} | C_mean={row['C_mean']:.6f}"
        )

    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv("v33_gh_summary.csv", index=False)
    print("Saved: v33_gh_summary.csv")

    # -------------------------
    # 5) scatter plot: noise vs rotation
    # -------------------------
    color_map = {"KKK": "#4C78A8", "GH": "#72B7B2", "CCC": "#F58518"}

    plt.figure(figsize=(10, 8))
    for phase_class, sub in full_df.groupby("phase_class"):
        plt.scatter(
            sub["noise"],
            sub["rotation"],
            s=90,
            alpha=0.75,
            label=phase_class,
            color=color_map[phase_class],
        )

    plt.xlabel("noise")
    plt.ylabel("rotation")
    plt.title("V33 Phase Regions in (noise, rotation)")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # -------------------------
    # 6) GH corridor per k
    # -------------------------
    plt.figure(figsize=(10, 8))
    for k, sub in gh_df.groupby("k"):
        plt.plot(
            sub["noise"],
            sub["rotation"],
            marker="o",
            linewidth=2,
            label=f"k={k}"
        )

    plt.xlabel("noise")
    plt.ylabel("rotation")
    plt.title("V33 GH Corridor")
    plt.legend()
    plt.tight_layout()
    plt.show()

    # -------------------------
    # 7) t vs k GH occupancy map
    # -------------------------
    occ = full_df.copy()
    occ["gh_flag"] = (occ["phase_class"] == "GH").astype(int)
    pivot = occ.pivot(index="k", columns="t", values="gh_flag")

    plt.figure(figsize=(12, 4))
    plt.imshow(pivot.values, aspect="auto", origin="lower")
    plt.yticks(range(len(pivot.index)), [str(v) for v in pivot.index])
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.xlabel("t")
    plt.ylabel("k")
    plt.title("GH Occupancy Map (1 = GH)")
    plt.colorbar()
    plt.tight_layout()
    plt.show()

    # -------------------------
    # 8) GH center estimate
    # -------------------------
    if len(gh_df) > 0:
        gh_center_noise = gh_df["noise"].mean()
        gh_center_rotation = gh_df["rotation"].mean()

        print("\n--- GH CENTER ---")
        print(f"noise_center    = {gh_center_noise:.6f}")
        print(f"rotation_center = {gh_center_rotation:.6f}")

        print("\nInterpretation:")
        print("GH is the corridor between CCC expansion and KKK collapse.")
        print("The center above is the average hinge location in parameter space.")

    else:
        print("\nNo GH points found.")


if __name__ == "__main__":
    main()

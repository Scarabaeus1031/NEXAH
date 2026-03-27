import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from APPLICATIONS.power_systems.stability_field_dynamics.ieee_test_cases.core_coupling import run_single_coupling


def classify_phase(loops, C, loops_low, loops_high, c_low, c_high):
    """
    Simple 3-phase classifier:
    KKK = compact / low activity
    GH  = transition / hinge / lock corridor
    CCC = expanded / high activity
    """
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

    df = pd.DataFrame(rows)
    return df


def detect_lock_points(df):
    """
    Lock points = locally minimal loops and low C.
    """
    lock_points = []

    loops = df["loops"].values
    C = df["C"].values
    ts = df["t"].values

    for i in range(1, len(df) - 1):
        local_min_loops = (loops[i] <= loops[i - 1]) and (loops[i] <= loops[i + 1])
        local_low_C = (C[i] <= C[i - 1]) and (C[i] <= C[i + 1])

        if local_min_loops and local_low_C:
            lock_points.append(int(ts[i]))

    return lock_points


def build_phase_map(full_df):
    """
    Convert phase labels to integers for plotting.
    """
    label_to_int = {"KKK": 0, "GH": 1, "CCC": 2}

    phase_df = full_df.copy()
    phase_df["phase_class_int"] = phase_df["phase_class"].map(label_to_int)

    pivot = phase_df.pivot(index="k", columns="t", values="phase_class_int")
    return pivot, label_to_int


def main():
    print("\n--- V32 Phase Classifier / GH Detector ---\n")

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
    # 2) global thresholds
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
    # 3) classify phases
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

    # -------------------------
    # 4) detect lock points
    # -------------------------
    lock_rows = []

    print("\n--- LOCK POINTS ---")
    for k in k_values:
        sub = full_df[full_df["k"] == k].reset_index(drop=True)
        locks = detect_lock_points(sub)

        print(f"k={k}: lock points = {locks}")

        for t_lock in locks:
            row = sub[sub["t"] == t_lock].iloc[0]
            lock_rows.append({
                "k": k,
                "t_lock": t_lock,
                "loops": row["loops"],
                "C": row["C"],
                "phase_class": row["phase_class"],
                "rotation": row["rotation"],
                "noise": row["noise"],
            })

    lock_df = pd.DataFrame(lock_rows)

    # -------------------------
    # 5) save tables
    # -------------------------
    full_df.to_csv("v32_phase_classifier.csv", index=False)
    lock_df.to_csv("v32_lock_points.csv", index=False)

    print("\nSaved: v32_phase_classifier.csv")
    print("Saved: v32_lock_points.csv")

    # -------------------------
    # 6) plot per k
    # -------------------------
    color_map = {"KKK": "#4C78A8", "GH": "#BAB0AC", "CCC": "#F58518"}

    for k in k_values:
        sub = full_df[full_df["k"] == k].copy()

        plt.figure(figsize=(11, 6))
        plt.plot(sub["t"], sub["loops"], marker="o", label="loops")
        plt.plot(sub["t"], sub["C"], marker="o", label="C")

        for _, row in sub.iterrows():
            plt.axvspan(
                row["t"] - 0.5,
                row["t"] + 0.5,
                color=color_map[row["phase_class"]],
                alpha=0.12
            )

        # lock markers
        locks = lock_df[lock_df["k"] == k]["t_lock"].tolist()
        for t_lock in locks:
            plt.axvline(t_lock, linestyle="--", linewidth=1.5)

        plt.title(f"V32 Phase Classification (k={k})")
        plt.xlabel("t")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # -------------------------
    # 7) phase map
    # -------------------------
    pivot, label_to_int = build_phase_map(full_df)

    plt.figure(figsize=(12, 4))
    plt.imshow(pivot.values, aspect="auto", origin="lower")
    plt.yticks(range(len(pivot.index)), [str(v) for v in pivot.index])
    plt.xticks(range(len(pivot.columns)), pivot.columns)
    plt.xlabel("t")
    plt.ylabel("k")
    plt.title("Phase Map (0=KKK, 1=GH, 2=CCC)")
    plt.colorbar()
    plt.tight_layout()
    plt.show()

    # -------------------------
    # 8) summary
    # -------------------------
    print("\n--- PHASE COUNTS ---")
    print(full_df.groupby(["k", "phase_class"]).size())

    if not lock_df.empty:
        print("\n--- LOCK TABLE ---")
        print(lock_df.to_string(index=False))
    else:
        print("\nNo lock points detected.")

    # -------------------------
    # 9) simple interpretation
    # -------------------------
    print("\n--- INTERPRETATION ---")
    for k in k_values:
        sub = full_df[full_df["k"] == k]
        counts = sub["phase_class"].value_counts().to_dict()
        print(f"k={k} -> {counts}")


if __name__ == "__main__":
    main()

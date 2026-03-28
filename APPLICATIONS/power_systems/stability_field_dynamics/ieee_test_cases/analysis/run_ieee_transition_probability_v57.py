# run_ieee_transition_probability_v57.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

STATE_ORDER = [-1, 0, 1]   # noise / transition, core, secondary


# --------------------------------------------------
# HELPERS
# --------------------------------------------------

def load_transitions(case: str):
    file_path = BASE_PATH / f"{case}_v56_transitions.csv"
    if not file_path.exists():
        print(f"Missing file: {file_path}")
        return None

    df = pd.read_csv(file_path).dropna()

    required = {"from_cluster", "to_cluster"}
    if not required.issubset(df.columns):
        print(f"[{case}] Missing required columns: {required - set(df.columns)}")
        return None

    return df


def build_transition_matrix(df: pd.DataFrame):
    counts = pd.DataFrame(
        0,
        index=STATE_ORDER,
        columns=STATE_ORDER,
        dtype=int
    )

    for _, row in df.iterrows():
        f = int(row["from_cluster"])
        t = int(row["to_cluster"])
        if f in STATE_ORDER and t in STATE_ORDER:
            counts.loc[f, t] += 1

    probs = counts.div(counts.sum(axis=1).replace(0, np.nan), axis=0).fillna(0.0)

    return counts, probs


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V57 — TRANSITION PROBABILITY MODEL")

    summary_rows = []

    for case in CASES:
        print(f"\n--- {case.upper()} ---")

        df = load_transitions(case)
        if df is None:
            continue

        counts, probs = build_transition_matrix(df)

        # save matrices
        counts_path = BASE_PATH / f"{case}_v57_transition_counts.csv"
        probs_path = BASE_PATH / f"{case}_v57_transition_probs.csv"

        counts.to_csv(counts_path)
        probs.to_csv(probs_path)

        print(f"Saved: {counts_path}")
        print(f"Saved: {probs_path}")

        print("\nTransition counts:")
        print(counts)

        print("\nTransition probabilities:")
        print(probs.round(4))

        # heatmap
        plt.figure(figsize=(6, 5))
        plt.imshow(probs.values, aspect="auto")
        plt.xticks(range(len(STATE_ORDER)), STATE_ORDER)
        plt.yticks(range(len(STATE_ORDER)), STATE_ORDER)
        plt.xlabel("To state")
        plt.ylabel("From state")
        plt.title(f"{case.upper()} — Transition Probabilities (V57)")
        plt.colorbar(label="Probability")

        for i in range(len(STATE_ORDER)):
            for j in range(len(STATE_ORDER)):
                plt.text(j, i, f"{probs.values[i, j]:.2f}", ha="center", va="center")

        plt.tight_layout()
        plt.savefig(BASE_PATH / f"{case}_v57_transition_heatmap.png", dpi=150)
        plt.close()

        summary_rows.append({
            "case": case,
            "p_stay_core": float(probs.loc[0, 0]) if 0 in probs.index and 0 in probs.columns else np.nan,
            "p_core_to_noise": float(probs.loc[0, -1]) if 0 in probs.index and -1 in probs.columns else np.nan,
            "p_noise_to_secondary": float(probs.loc[-1, 1]) if -1 in probs.index and 1 in probs.columns else np.nan,
            "p_secondary_to_noise": float(probs.loc[1, -1]) if 1

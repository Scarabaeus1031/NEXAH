import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

# cluster mapping
STATE_MAP = {
    -1: 0,  # noise
    0: 1,   # core
    1: 2    # secondary
}

STATE_NAMES = ["noise", "core", "secondary"]

# --------------------------------------------------
# LOAD TRANSITION MATRIX
# --------------------------------------------------

def load_transition_matrix(case):
    file_path = BASE_PATH / f"{case}_v57_probs.csv"
    if not file_path.exists():
        print(f"Missing: {file_path}")
        return None
    return pd.read_csv(file_path, index_col=0).values


# --------------------------------------------------
# LOAD STATE TRAJECTORY
# --------------------------------------------------

def load_states(case):
    file_path = BASE_PATH / f"{case}_v56_clustered_states.csv"
    if not file_path.exists():
        print(f"Missing: {file_path}")
        return None
    return pd.read_csv(file_path)


# --------------------------------------------------
# BUILD INITIAL STATE VECTOR
# --------------------------------------------------

def build_state_vector(cluster):
    vec = np.zeros(3)
    idx = STATE_MAP.get(cluster, 0)
    vec[idx] = 1.0
    return vec


# --------------------------------------------------
# SIMULATE FUTURE
# --------------------------------------------------

def simulate_markov(P, initial_state, steps=10):
    probs = [initial_state]

    current = initial_state.copy()

    for _ in range(steps):
        current = P @ current
        probs.append(current)

    return np.array(probs)


# --------------------------------------------------
# MAIN PROCESS
# --------------------------------------------------

def process_case(case):
    print(f"\n--- {case.upper()} ---")

    P = load_transition_matrix(case)
    df = load_states(case)

    if P is None or df is None:
        return

    # last observed state
    last_cluster = df["cluster"].iloc[-1]

    initial_state = build_state_vector(last_cluster)

    probs = simulate_markov(P, initial_state, steps=20)

    # collapse probability = noise state
    collapse_prob = probs[:, 0]

    # --------------------------------------------------
    # PLOT
    # --------------------------------------------------

    plt.figure(figsize=(10, 5))

    for i, name in enumerate(STATE_NAMES):
        plt.plot(probs[:, i], label=name)

    plt.xlabel("Time step")
    plt.ylabel("Probability")
    plt.title(f"{case.upper()} — State Evolution (V58)")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v58_state_evolution.png", dpi=150)
    plt.close()

    # collapse curve
    plt.figure(figsize=(10, 5))
    plt.plot(collapse_prob, color="red")
    plt.xlabel("Time step")
    plt.ylabel("Collapse probability")
    plt.title(f"{case.upper()} — Collapse Probability (V58)")
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v58_collapse_probability.png", dpi=150)
    plt.close()

    print(f"Saved V58 outputs for {case}")


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V58 — COLLAPSE PREDICTION")

    for case in CASES:
        process_case(case)


if __name__ == "__main__":
    main()

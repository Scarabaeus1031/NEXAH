import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_PATH = Path("APPLICATIONS/power_systems/stability_field_dynamics/ieee_test_cases/outputs")
CASES = ["ieee30", "ieee57", "ieee118"]

STATE_MAP = {-1: 0, 0: 1, 1: 2}
STATE_NAMES = ["noise", "core", "secondary"]

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_states(case):
    path = BASE_PATH / f"{case}_v56_clustered_states.csv"
    if not path.exists():
        print(f"[ERROR] Missing: {path}")
        return None
    return pd.read_csv(path)

# --------------------------------------------------
# DYNAMIC TRANSITION MATRIX
# --------------------------------------------------

def dynamic_transition_matrix(tau):
    """
    Drift-Modell:
    mit wachsendem tau steigt Collapse-Tendenz
    """

    P = np.array([
        [0.5, 0.0, 0.5],   # noise
        [0.06, 0.94, 0.0], # core
        [0.5, 0.5, 0.0]    # secondary
    ], dtype=float)

    # Drift Richtung Collapse
    P[1, 0] += 0.35 * tau   # core → noise
    P[2, 0] += 0.35 * tau   # secondary → noise

    # Normieren
    P = P / P.sum(axis=1, keepdims=True)

    return P

# --------------------------------------------------
# STATE VECTOR
# --------------------------------------------------

def build_state_vector(cluster):
    vec = np.zeros(3)
    vec[STATE_MAP.get(cluster, 0)] = 1.0
    return vec

# --------------------------------------------------
# SIMULATION
# --------------------------------------------------

def simulate(case):
    print(f"\n--- {case.upper()} ---")

    df = load_states(case)
    if df is None:
        return

    clusters = df["cluster"].values

    # tau verwenden oder fallback
    if "tau" in df.columns:
        tau_series = df["tau"].values
    else:
        tau_series = np.linspace(0, 1, len(df))

    state = build_state_vector(clusters[0])

    probs = []

    for t in range(len(tau_series)):
        tau = tau_series[t]

        P = dynamic_transition_matrix(tau)
        state = P @ state

        probs.append(state.copy())

    probs = np.array(probs)
    collapse = probs[:, 0]

    # --------------------------------------------------
    # STATE EVOLUTION
    # --------------------------------------------------

    plt.figure(figsize=(10, 5))

    for i, name in enumerate(STATE_NAMES):
        plt.plot(probs[:, i], label=name)

    plt.title(f"{case.upper()} — State Evolution (V59)")
    plt.xlabel("time step")
    plt.ylabel("probability")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v59_state_evolution.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # COLLAPSE PROBABILITY
    # --------------------------------------------------

    plt.figure(figsize=(10, 5))
    plt.plot(collapse, color="red")

    plt.title(f"{case.upper()} — Collapse Drift (V59)")
    plt.xlabel("time step")
    plt.ylabel("collapse probability")
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v59_collapse_drift.png", dpi=150)
    plt.close()

    print(f"[DONE] {case}")

# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():
    print("RUNNING V59 — COLLAPSE DRIFT MODEL")

    for case in CASES:
        simulate(case)

if __name__ == "__main__":
    main()

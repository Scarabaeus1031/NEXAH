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
# LOAD
# --------------------------------------------------

def load_states(case):
    path = BASE_PATH / f"{case}_v56_clustered_states.csv"
    if not path.exists():
        print(f"Missing: {path}")
        return None
    return pd.read_csv(path)

# --------------------------------------------------
# WARNING FUNCTION
# --------------------------------------------------

def compute_warning_score(probs):
    """
    probs = [noise, core, secondary]
    """

    noise = probs[:, 0]
    core = probs[:, 1]
    secondary = probs[:, 2]

    # zentrale Idee:
    warning = (
        0.6 * secondary +      # Übergang wächst
        0.3 * noise +          # Zerfall beginnt
        0.3 * (1 - core)       # Stabilität sinkt
    )

    return warning

# --------------------------------------------------
# SIMULATION (reuse V59 logic)
# --------------------------------------------------

def dynamic_transition_matrix(tau):

    P = np.array([
        [0.5, 0.0, 0.5],
        [0.06, 0.94, 0.0],
        [0.5, 0.5, 0.0]
    ], dtype=float)

    # Drift
    P[1, 0] += 0.35 * tau
    P[2, 0] += 0.35 * tau

    P = P / P.sum(axis=1, keepdims=True)

    return P

def build_state(cluster):
    v = np.zeros(3)
    v[STATE_MAP.get(cluster, 0)] = 1.0
    return v

# --------------------------------------------------
# RUN
# --------------------------------------------------

def simulate(case):
    print(f"\n--- {case} ---")

    df = load_states(case)
    if df is None:
        return

    clusters = df["cluster"].values
    tau = df["tau"].values if "tau" in df else np.linspace(0, 1, len(df))

    state = build_state(clusters[0])

    probs = []

    for i in range(len(tau)):
        P = dynamic_transition_matrix(tau[i])
        state = P @ state
        probs.append(state.copy())

    probs = np.array(probs)

    # --------------------------------------------------
    # EARLY WARNING
    # --------------------------------------------------

    warning = compute_warning_score(probs)

    # normalize
    warning = warning / np.max(warning)

    # threshold detection
    threshold = 0.6
    alerts = warning > threshold

    # --------------------------------------------------
    # PLOT
    # --------------------------------------------------

    plt.figure(figsize=(10,5))

    plt.plot(warning, label="warning score", color="orange")
    plt.axhline(threshold, linestyle="--", color="red", label="threshold")

    # mark alert region
    for i in range(len(alerts)):
        if alerts[i]:
            plt.scatter(i, warning[i], color="red", s=20)

    plt.title(f"{case} — Early Warning (V60)")
    plt.xlabel("time step")
    plt.ylabel("normalized warning")
    plt.legend()
    plt.grid()

    plt.savefig(BASE_PATH / f"{case}_v60_warning.png", dpi=150)
    plt.close()

    print("alert triggered at steps:", np.where(alerts)[0])

# --------------------------------------------------
# MAIN
# --------------------------------------------------

if __name__ == "__main__":
    print("RUNNING V60 — EARLY WARNING SYSTEM")

    for case in CASES:
        simulate(case)

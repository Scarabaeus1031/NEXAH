import numpy as np
import csv
import os
import matplotlib.pyplot as plt

# ----------------------------------------
# 1. CSV LOAD
# ----------------------------------------

def load_csv(filepath):
    time = []
    voltage = []

    with open(filepath, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            time.append(float(row["time"]))
            voltage.append(float(row["voltage"]))

    return np.array(time), np.array(voltage)


# ----------------------------------------
# 2. SIGNALS
# ----------------------------------------

def compute_drift(v):
    dv = np.diff(v)
    dv = np.concatenate([[0], dv])
    return dv


def compute_acceleration(v):
    dv = np.diff(v)
    ddv = np.diff(dv)
    ddv = np.concatenate([[0, 0], ddv])
    return ddv


def compute_score(drift, acc):
    return np.abs(drift) + 0.5 * np.abs(acc)


# ----------------------------------------
# 3. ANALYSIS (KEY PART)
# ----------------------------------------

def analyze(time, voltage, collapse_threshold=0.7, window=10):

    drift = compute_drift(voltage)
    acc = compute_acceleration(voltage)
    score = compute_score(drift, acc)

    # ----------------------------------------
    # Collapse detection
    # ----------------------------------------

    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]

    # ----------------------------------------
    # Adaptive threshold (rolling)
    # ----------------------------------------

    threshold_series = np.zeros_like(score)
    regime_idx = None

    for i in range(window, len(score)):

        past = score[i-window:i]
        threshold = np.mean(past) + 2 * np.std(past)

        threshold_series[i] = threshold

        if regime_idx is None and score[i] > threshold:
            regime_idx = i

    # ----------------------------------------
    # OUTPUT
    # ----------------------------------------

    print("\n--- RESULTS ---")

    if regime_idx is not None:
        print(f"Regime change at t = {time[regime_idx]}")
    else:
        print("No regime change detected")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]}")
    else:
        print("No collapse detected")

    if regime_idx is not None and collapse_idx is not None:
        lead_time = time[collapse_idx] - time[regime_idx]
        print(f"Lead time = {lead_time}")
    else:
        print("Lead time not computable")

    # ----------------------------------------
    # PLOT
    # ----------------------------------------

    plt.figure(figsize=(10, 8))

    # Voltage
    plt.subplot(4, 1, 1)
    plt.plot(time, voltage, label="Voltage")

    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":", label="Regime")

    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="--", label="Collapse")

    plt.legend()
    plt.title("Voltage")

    # Drift
    plt.subplot(4, 1, 2)
    plt.plot(time, drift, label="Drift dv/dt")
    plt.legend()
    plt.title("Drift")

    # Acceleration
    plt.subplot(4, 1, 3)
    plt.plot(time, acc, label="Acceleration d²v/dt²")
    plt.legend()
    plt.title("Acceleration")

    # Score + Threshold
    plt.subplot(4, 1, 4)
    plt.plot(time, score, label="Score")
    plt.plot(time, threshold_series, linestyle="--", label="Adaptive Threshold")

    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":", label="Regime")

    plt.legend()
    plt.title("Hybrid Detection (Score vs Threshold)")

    plt.tight_layout()

    return regime_idx, collapse_idx


# ----------------------------------------
# 4. RUN (IEEE READY)
# ----------------------------------------

if __name__ == "__main__":

    base_path = "APPLICATIONS/power_systems/stability_field_dynamics/data/"

    test_files = [
        "ieee_linear.csv",
        "ieee_accelerated.csv",
        "ieee_noisy.csv",
        "ieee_delayed.csv",
        "ieee_realistic.csv"   # ← dein echtes / generator file
    ]

    for file in test_files:

        filepath = os.path.join(base_path, file)

        print("\n==============================")
        print(f"Testing: {file}")
        print("==============================")

        if not os.path.exists(filepath):
            print("File not found:", filepath)
            continue

        time, voltage = load_csv(filepath)

        analyze(time, voltage)

    plt.show()

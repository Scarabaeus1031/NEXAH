import numpy as np
import csv
import os
import matplotlib.pyplot as plt


# ----------------------------------------
# 1. CSV laden
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
# 2. Drift
# ----------------------------------------

def compute_drift(time, voltage):
    return np.gradient(voltage, time)


# ----------------------------------------
# 3. Change Score (KEY STEP)
# ----------------------------------------

def compute_change_score(time, voltage, window=5):

    drift = compute_drift(time, voltage)

    scores = []

    for i in range(window, len(drift) - window):

        left = drift[i-window:i]
        right = drift[i:i+window]

        mean_diff = abs(np.mean(right) - np.mean(left))
        var_diff = abs(np.var(right) - np.var(left))

        score = mean_diff + var_diff
        scores.append(score)

    scores = np.array(scores)
    offset = window

    return scores, offset


# ----------------------------------------
# 4. Detection
# ----------------------------------------

def detect_regime(time, voltage, collapse_threshold=0.7):

    scores, offset = compute_change_score(time, voltage)

    if len(scores) == 0:
        return None

    regime_idx = np.argmax(scores) + offset

    # Collapse
    collapse_idx = None
    collapse_candidates = np.where(voltage < collapse_threshold)[0]
    if len(collapse_candidates) > 0:
        collapse_idx = collapse_candidates[0]

    return regime_idx, collapse_idx, scores, offset


# ----------------------------------------
# 5. Plot
# ----------------------------------------

def plot_result(time, voltage, regime_idx, collapse_idx, scores, offset, filename):

    drift = compute_drift(time, voltage)

    # Align scores with time axis
    score_time = time[offset:len(time)-offset]

    plt.figure(figsize=(10, 8))

    # Voltage
    plt.subplot(3, 1, 1)
    plt.plot(time, voltage, label="Voltage")
    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":", label="Regime Change")
    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="--", label="Collapse")
    plt.title("Voltage")
    plt.legend()
    plt.grid()

    # Drift
    plt.subplot(3, 1, 2)
    plt.plot(time, drift, label="Drift dv/dt")
    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":")
    plt.title("Drift")
    plt.legend()
    plt.grid()

    # Change Score
    plt.subplot(3, 1, 3)
    plt.plot(score_time, scores, label="Change Score")
    if regime_idx is not None:
        plt.axvline(time[regime_idx], linestyle=":", label="Regime Change")
    plt.title("Change Score (KEY SIGNAL)")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# ----------------------------------------
# 6. Report
# ----------------------------------------

def print_report(name, time, regime_idx, collapse_idx):

    print("\n==============================")
    print(f"Testing: {name}")
    print("==============================\n")

    if regime_idx is not None:
        print(f"Regime change at t = {time[regime_idx]:.2f}")
    else:
        print("No regime change detected")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]:.2f}")

        if regime_idx is not None:
            print(f"Lead time = {time[collapse_idx] - time[regime_idx]:.2f}")
    else:
        print("No collapse detected")


# ----------------------------------------
# 7. RUN
# ----------------------------------------

if __name__ == "__main__":

    base_path = "APPLICATIONS/power_systems/stability_field_dynamics/data/"
    output_path = "APPLICATIONS/power_systems/stability_field_dynamics/iee_core_geometry/phi_geometry/plots/"

    os.makedirs(output_path, exist_ok=True)

    test_files = [
        "ieee_linear.csv",
        "ieee_accelerated.csv",
        "ieee_noisy.csv",
        "ieee_delayed.csv"
    ]

    for file in test_files:

        filepath = os.path.join(base_path, file)

        if not os.path.exists(filepath):
            print("File not found:", filepath)
            continue

        time, voltage = load_csv(filepath)

        result = detect_regime(time, voltage)

        if result is None:
            print("No result")
            continue

        regime_idx, collapse_idx, scores, offset = result

        print_report(file, time, regime_idx, collapse_idx)

        out_file = os.path.join(output_path, file.replace(".csv", "_change_score.png"))

        plot_result(time, voltage, regime_idx, collapse_idx, scores, offset, out_file)

        print(f"Saved plot to: {out_file}")

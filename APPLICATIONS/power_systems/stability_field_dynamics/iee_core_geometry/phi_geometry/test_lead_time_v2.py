import numpy as np
import csv
import os
import matplotlib.pyplot as plt

# ----------------------------------------
# 1. CSV Laden
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
# 2. Acceleration + Smoothing
# ----------------------------------------

def compute_acceleration(v, window=5):
    dv = np.diff(v)
    ddv = np.diff(dv)

    ddv = np.concatenate([[0, 0], ddv])

    kernel = np.ones(window) / window
    ddv_smooth = np.convolve(ddv, kernel, mode='same')

    return np.abs(ddv_smooth)


# ----------------------------------------
# 3. Hybrid Analyse
# ----------------------------------------

def analyze(time, voltage, collapse_threshold=0.7):

    # Collapse Detection
    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]

    # Features
    dv = np.diff(voltage, prepend=voltage[0])
    acc = compute_acceleration(voltage)

    slope = np.abs(dv)
    distance = np.maximum(voltage - collapse_threshold, 0)

    # ----------------------------------------
    # Hybrid Score
    # ----------------------------------------

    score = (
        1.0 * acc +
        0.5 * slope +
        0.5 * (1.0 / (distance + 1e-3))
    )

    # Glättung
    kernel = np.ones(5) / 5
    score = np.convolve(score, kernel, mode='same')

    # ----------------------------------------
    # Detection Zone
    # ----------------------------------------

    min_idx = int(0.1 * len(time))
    max_idx = int(0.9 * len(time))

    valid = np.arange(len(time))
    valid = valid[(valid >= min_idx) & (valid <= max_idx)]

    phi_idx = valid[np.argmax(score[valid])]

    # ----------------------------------------
    # Output
    # ----------------------------------------

    print("\n--- RESULTS ---")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]}")
    else:
        print("No collapse detected")

    print(f"Phi-Split (hybrid) at t = {time[phi_idx]}")

    if collapse_idx is not None:
        lead_time = time[collapse_idx] - time[phi_idx]
        print(f"Lead Time = {lead_time}")
    else:
        print("Lead Time not computable")

    print(f"Max score = {np.max(score):.6f}")

    return phi_idx, collapse_idx, acc, score


# ----------------------------------------
# 4. Plot
# ----------------------------------------

def plot_result(time, voltage, acc, score, collapse_idx, phi_idx, filename):

    plt.figure(figsize=(10, 7))

    # Voltage
    plt.subplot(3, 1, 1)
    plt.plot(time, voltage, label="Voltage")

    if collapse_idx is not None:
        plt.axvline(time[collapse_idx], linestyle="--", label="Collapse")

    plt.axvline(time[phi_idx], linestyle=":", label="Phi-Split")

    plt.title("Voltage")
    plt.legend()
    plt.grid()

    # Acceleration
    plt.subplot(3, 1, 2)
    plt.plot(time, acc, label="Acceleration")
    plt.axvline(time[phi_idx], linestyle=":", label="Phi-Split")

    plt.title("Acceleration")
    plt.legend()
    plt.grid()

    # Hybrid Score
    plt.subplot(3, 1, 3)
    plt.plot(time, score, label="Hybrid Score")
    plt.axvline(time[phi_idx], linestyle=":", label="Phi-Split")

    plt.title("Hybrid Detection Score")
    plt.legend()
    plt.grid()

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()


# ----------------------------------------
# 5. RUN
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

        print("\n==============================")
        print(f"Testing: {file}")
        print("==============================")

        if not os.path.exists(filepath):
            print("File not found:", filepath)
            continue

        time, voltage = load_csv(filepath)

        phi_idx, collapse_idx, acc, score = analyze(time, voltage)

        out_file = os.path.join(output_path, file.replace(".csv", "_hybrid.png"))

        plot_result(time, voltage, acc, score, collapse_idx, phi_idx, out_file)

        print("Saved plot to:", out_file)

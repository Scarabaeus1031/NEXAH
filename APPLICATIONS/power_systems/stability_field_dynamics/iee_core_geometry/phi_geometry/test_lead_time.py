import numpy as np
import csv
import os

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

    # Padding für gleiche Länge
    ddv = np.concatenate([[0, 0], ddv])

    # Moving average smoothing
    kernel = np.ones(window) / window
    ddv_smooth = np.convolve(ddv, kernel, mode='same')

    return np.abs(ddv_smooth)


# ----------------------------------------
# 3. Analyse
# ----------------------------------------

def analyze(time, voltage, collapse_threshold=0.7):

    # Collapse Detection
    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]

    # Acceleration
    acc = compute_acceleration(voltage)

    # Adaptive Threshold
    threshold = np.mean(acc) + 2 * np.std(acc)

    # Phi-Split Detection
    phi_idx = None
    phi_indices = np.where(acc > threshold)[0]
    if len(phi_indices) > 0:
        phi_idx = phi_indices[0]

    # Output
    print("\n--- RESULTS ---")

    if collapse_idx is not None:
        print(f"Collapse at t = {time[collapse_idx]}")
    else:
        print("No collapse detected")

    if phi_idx is not None:
        print(f"Phi-Split at t = {time[phi_idx]}")
    else:
        print("No Phi-Split detected")

    if collapse_idx is not None and phi_idx is not None:
        lead_time = time[collapse_idx] - time[phi_idx]
        print(f"Lead Time = {lead_time}")
    else:
        print("Lead Time not computable")

    print(f"Adaptive threshold = {threshold:.6f}")
    print(f"Max acceleration = {np.max(acc):.6f}")


# ----------------------------------------
# 4. RUN ALL FILES
# ----------------------------------------

if __name__ == "__main__":

    base_path = "APPLICATIONS/power_systems/stability_field_dynamics/data/"

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
        analyze(time, voltage)

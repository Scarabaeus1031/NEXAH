import numpy as np
import csv
import os

# ----------------------------------------
# 1. CSV Loader
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
# 2. Drift (relative)
# ----------------------------------------

def compute_drift(v):
    dv = np.diff(v)
    return np.abs(dv / v[:-1])


# ----------------------------------------
# 3. Analyse
# ----------------------------------------

def analyze(time, voltage, phi_threshold=0.04, collapse_threshold=0.7):

    # Collapse detection
    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]

    # Drift
    drift = compute_drift(voltage)

    # Phi-Split detection
    phi_idx = None
    phi_indices = np.where(drift > phi_threshold)[0]
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


# ----------------------------------------
# 4. RUN (multi-file batch)
# ----------------------------------------

if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    DATA_DIR = os.path.normpath(
        os.path.join(BASE_DIR, "../../data")
    )

    files = [
        "ieee_linear.csv",
        "ieee_accelerated.csv",
        "ieee_noisy.csv",
        "ieee_delayed.csv"
    ]

    for f in files:
        print(f"\n==============================")
        print(f"Testing: {f}")
        print(f"==============================")

        filepath = os.path.join(DATA_DIR, f)

        if not os.path.exists(filepath):
            print(f"❌ File not found: {filepath}")
            continue

        time, voltage = load_csv(filepath)
        analyze(time, voltage)

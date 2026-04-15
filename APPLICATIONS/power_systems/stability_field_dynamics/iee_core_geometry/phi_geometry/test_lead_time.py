import numpy as np
import csv

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
# 2. Drift (besser: relativ)
# ----------------------------------------

def compute_drift(v):
    dv = np.diff(v)
    return np.abs(dv / v[:-1])


# ----------------------------------------
# 3. Analyse
# ----------------------------------------

def analyze(time, voltage, phi_threshold=0.04, collapse_threshold=0.7):

    # Collapse
    collapse_idx = None
    collapse_indices = np.where(voltage < collapse_threshold)[0]
    if len(collapse_indices) > 0:
        collapse_idx = collapse_indices[0]

    # Drift
    drift = compute_drift(voltage)

    # Phi-Split
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
# 4. RUN
# ----------------------------------------

if __name__ == "__main__":

    filepath = "APPLICATIONS/power_systems/stability_field_dynamics/data/ieee9_voltage.csv"

    time, voltage = load_csv(filepath)

    analyze(time, voltage)    print("Lead Time not computable")

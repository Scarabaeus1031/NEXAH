import numpy as np
import csv
import os

# ----------------------------------------
# Output folder
# ----------------------------------------

OUTPUT_DIR = "APPLICATIONS/power_systems/stability_field_dynamics/data"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ----------------------------------------
# Helper: CSV writer
# ----------------------------------------

def save_csv(filename, time, voltage):
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "voltage"])

        for t, v in zip(time, voltage):
            writer.writerow([t, v])

    print(f"Saved: {filepath}")


# ----------------------------------------
# 1. Simple linear collapse (baseline)
# ----------------------------------------

def generate_linear():
    time = np.arange(0, 50)
    voltage = np.linspace(0.98, 0.65, len(time))
    return time, voltage


# ----------------------------------------
# 2. Accelerated collapse (more realistic)
# ----------------------------------------

def generate_accelerated():
    time = np.arange(0, 50)
    voltage = 0.98 - 0.33 * (time / time.max())**2
    return time, voltage


# ----------------------------------------
# 3. Noisy collapse (realistic grid noise)
# ----------------------------------------

def generate_noisy():
    time = np.arange(0, 50)
    base = 0.98 - 0.33 * (time / time.max())**1.5
    noise = np.random.normal(0, 0.003, size=len(time))
    voltage = base + noise
    return time, voltage


# ----------------------------------------
# 4. Delayed collapse (late instability)
# ----------------------------------------

def generate_delayed():
    time = np.arange(0, 50)

    voltage = np.ones_like(time) * 0.98
    drop_start = 30

    for i in range(len(time)):
        if i > drop_start:
            voltage[i] = 0.98 - 0.33 * ((i - drop_start) / (50 - drop_start))**2

    return time, voltage


# ----------------------------------------
# Generate all
# ----------------------------------------

if __name__ == "__main__":

    generators = {
        "ieee_linear.csv": generate_linear,
        "ieee_accelerated.csv": generate_accelerated,
        "ieee_noisy.csv": generate_noisy,
        "ieee_delayed.csv": generate_delayed,
    }

    for name, func in generators.items():
        t, v = func()
        save_csv(name, t, v)

    print("\n✅ All CSVs generated.")

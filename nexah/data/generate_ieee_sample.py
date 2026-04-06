# generate_ieee_sample.py

import numpy as np
import csv

# time axis
t = np.linspace(0, 120, 1200)

# synthetic "IEEE-like" voltage collapse
def voltage_curve(t):
    base = 1.0
    drop = 0.88 / (1 + np.exp(-(t - 76) / 4))
    noise = 0.002 * np.random.randn(len(t))
    return base - drop + noise

voltage = voltage_curve(t)

# save CSV
with open("data/ieee_sample.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["time", "voltage"])

    for i in range(len(t)):
        writer.writerow([round(t[i], 4), round(voltage[i], 6)])

print("✅ ieee_sample.csv created in /data/")

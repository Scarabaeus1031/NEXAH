import numpy as np
import matplotlib.pyplot as plt
import json

# --- Load data ---
price = np.loadtxt("btc.csv", delimiter=",")

# --- Load NEXAH result ---
with open("btc_result.json") as f:
    res = json.load(f)

zones = res["regime_zones"]

# --- Plot ---
plt.figure(figsize=(14,6))

plt.plot(price, label="Price", linewidth=1.5)

# --- Overlay regime zones ---
for start, end in zones:
    plt.axvspan(start, end, alpha=0.3)

plt.title("NEXAH Regime Detection")
plt.xlabel("Time")
plt.ylabel("Price")

plt.legend()
plt.tight_layout()
plt.show()

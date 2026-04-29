import numpy as np
import matplotlib.pyplot as plt
import os
import json

print("\n=== RUN 034 — FLOW-ALIGNED CONTROL ===\n")

# =========================
# Output path (FIX: ganz nach oben!)
# =========================

output_path = "../outputs/run_034_flow_control"
os.makedirs(output_path, exist_ok=True)

# =========================
# Load / reuse trajectory
# =========================

t = np.linspace(0, 100, 100)

# TODO: hier echte trajectory einsetzen
V = np.linspace(1, -4.2, 100)

V_base = V.copy()

# =========================
# Approx flow (dx/dt)
# =========================

dV = np.gradient(V)

# =========================
# Gate window
# =========================

gate_start = 22
gate_end   = 27

# =========================
# Flow-aligned control
# =========================

V_control = V.copy()
strength = 0.015

for i in range(1, len(V)-1):

    if gate_start <= i <= gate_end:

        flow = dV[i]

        # robust gegen 0
        if flow == 0:
            continue

        direction = np.sign(flow)

        # kleine Gegenrichtung → minimale Umlenkung
        perturb = -direction * strength

        V_control[i] += perturb

# =========================
# Metrics
# =========================

deviation = np.abs(V_control - V_base)

results = {
    "max_deviation": float(np.max(deviation)),
    "mean_deviation": float(np.mean(deviation)),
    "interpretation": "Flow-aligned control perturbs trajectory only within gate window."
}

print(results)

# =========================
# Plot 1 — State space
# =========================

plt.figure(figsize=(6,5))

# FIX: baseline sichtbar machen
plt.plot(V_base, dV, color="black", linewidth=2, label="baseline")
plt.plot(V_control, np.gradient(V_control), color="red", linewidth=1.5, label="controlled")

plt.title("State Space: Flow-Aligned Control")
plt.xlabel("V")
plt.ylabel("dV")
plt.legend()
plt.grid()

plt.savefig(f"{output_path}/figure_01_state.png")
plt.close()

# =========================
# Plot 2 — Time series
# =========================

plt.figure(figsize=(6,4))

plt.plot(V_base, color="black", linewidth=2, label="baseline")
plt.plot(V_control, color="red", linewidth=1.5, label="controlled")

plt.title("Time Series")
plt.xlabel("time")
plt.ylabel("V")
plt.legend()
plt.grid()

plt.savefig(f"{output_path}/figure_02_time.png")
plt.close()

# =========================
# Plot 3 — Deviation
# =========================

plt.figure(figsize=(6,4))

plt.plot(deviation, color="orange", linewidth=2)

plt.title("Control Impact (|ΔV|)")
plt.xlabel("time")
plt.ylabel("difference")
plt.grid()

plt.savefig(f"{output_path}/figure_03_deviation.png")
plt.close()

# =========================
# Save results
# =========================

with open(f"{output_path}/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to:", output_path)

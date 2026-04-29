import numpy as np
import matplotlib.pyplot as plt

print("\n=== RUN 034 — FLOW-ALIGNED CONTROL ===\n")

# =========================
# Load / reuse trajectory
# =========================

# hier ggf. deinen echten trajectory loader einsetzen
# aktuell placeholder → ersetze mit deinem x(t)
t = np.linspace(0, 100, 100)
V = np.linspace(1, -4.2, 100)  # dummy → ersetzen mit echter trajectory

# baseline
V_base = V.copy()

# =========================
# Approx flow (dx/dt)
# =========================

dV = np.gradient(V)

# =========================
# Gate window (aus Run 31/32)
# =========================

gate_start = 22
gate_end   = 27

# =========================
# Flow-aligned control
# =========================

V_control = V.copy()

strength = 0.015   # bewusst klein!

for i in range(1, len(V)-1):

    if gate_start <= i <= gate_end:

        # lokaler Flow
        flow = dV[i]

        # Richtung normalisieren
        direction = np.sign(flow)

        # kleine orthogonale Störung simulieren
        # (Rotation im 1D reduziert → Richtungsflip-Anteil)
        perturb = -direction * strength

        # sanfte Mischung
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
plt.plot(V_base, dV, color="white", label="baseline")
plt.plot(V_control, np.gradient(V_control), color="red", label="controlled")
plt.title("State Space: Flow-Aligned Control")
plt.xlabel("V")
plt.ylabel("dV")
plt.legend()
plt.grid()

plt.savefig("../outputs/run_034_flow_control/figure_01_state.png")

# =========================
# Plot 2 — Time series
# =========================

plt.figure(figsize=(6,4))
plt.plot(V_base, label="baseline")
plt.plot(V_control, label="controlled", color="red")
plt.title("Time Series")
plt.xlabel("time")
plt.ylabel("V")
plt.legend()
plt.grid()

plt.savefig("../outputs/run_034_flow_control/figure_02_time.png")

# =========================
# Plot 3 — Deviation
# =========================

plt.figure(figsize=(6,4))
plt.plot(deviation, color="orange")
plt.title("Control Impact (|ΔV|)")
plt.xlabel("time")
plt.ylabel("difference")
plt.grid()

plt.savefig("../outputs/run_034_flow_control/figure_03_deviation.png")

# =========================
# Save results
# =========================

import json, os

output_path = "../outputs/run_034_flow_control"
os.makedirs(output_path, exist_ok=True)

with open(f"{output_path}/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to:", output_path)

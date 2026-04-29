import numpy as np
import matplotlib.pyplot as plt
import os, json

print("\n=== RUN 040 — PHASE SPACE CONTROL ===\n")

# =========================
# Trajectory
# =========================

t = np.linspace(0, 100, 100)
V = np.linspace(1, -4.2, 100)  # TODO: echte trajectory einsetzen

V_base = V.copy()
dV_base = np.gradient(V)

# =========================
# Gate
# =========================

gate_start = 20
gate_end   = 30

# =========================
# Phase space control
# =========================

V_control  = V.copy()
dV_control = np.gradient(V_control)

strength_v  = 0.05
strength_dv = 0.1

for i in range(2, len(V)-2):

    if gate_start <= i <= gate_end:

        # aktuelle Richtung
        flow = dV_control[i]

        # orthogonale Komponente simulieren
        orth = np.sign(np.gradient(dV_control)[i])

        # update im Phasenraum
        dV_control[i] += orth * strength_dv
        V_control[i]  += flow * strength_v

# recompute dV sauber
dV_control = np.gradient(V_control)

# =========================
# Metrics
# =========================

deviation = np.abs(V_control - V_base)

results = {
    "max_deviation": float(np.max(deviation)),
    "mean_deviation": float(np.mean(deviation)),
    "interpretation": "2D phase-space control attempts manifold escape."
}

print(results)

# =========================
# Output path
# =========================

output_path = "outputs/run_040_phase_space_control"
os.makedirs(output_path, exist_ok=True)

# =========================
# Plot 1 — State space
# =========================

plt.figure(figsize=(6,5))
plt.plot(V_base, dV_base, color="black", label="baseline")
plt.plot(V_control, dV_control, color="red", label="controlled")
plt.title("State Space (V, dV)")
plt.xlabel("V")
plt.ylabel("dV")
plt.legend()
plt.grid()

plt.savefig(f"{output_path}/figure_01_state.png")

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

plt.savefig(f"{output_path}/figure_02_time.png")

# =========================
# Plot 3 — dV evolution
# =========================

plt.figure(figsize=(6,4))
plt.plot(dV_base, label="baseline")
plt.plot(dV_control, label="controlled", color="red")
plt.title("Velocity Field (dV)")
plt.xlabel("time")
plt.ylabel("dV")
plt.legend()
plt.grid()

plt.savefig(f"{output_path}/figure_03_velocity.png")

# =========================
# Plot 4 — Deviation
# =========================

plt.figure(figsize=(6,4))
plt.plot(deviation, color="orange")
plt.title("Control Impact (|ΔV|)")
plt.xlabel("time")
plt.ylabel("difference")
plt.grid()

plt.savefig(f"{output_path}/figure_04_deviation.png")

# =========================
# Plot 5 — Phase portrait density
# =========================

plt.figure(figsize=(6,5))
plt.scatter(V_control, dV_control, c=t, cmap="viridis", s=10)
plt.title("Phase Trajectory (Colored by Time)")
plt.xlabel("V")
plt.ylabel("dV")
plt.colorbar(label="time")
plt.grid()

plt.savefig(f"{output_path}/figure_05_phase_density.png")

# =========================
# Save results
# =========================

with open(f"{output_path}/results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nSaved to:", output_path)

import imageio

frames = []

for i in range(len(V_control)):
    plt.figure(figsize=(5,4))
    plt.plot(V_control[:i], dV_control[:i], color="red")
    plt.xlim(min(V_control), max(V_control))
    plt.ylim(min(dV_control), max(dV_control))
    plt.title(f"t = {i}")
    
    fname = f"{output_path}/frame_{i}.png"
    plt.savefig(fname)
    plt.close()
    
    frames.append(imageio.imread(fname))

imageio.mimsave(f"{output_path}/phase_evolution.gif", frames, fps=10)

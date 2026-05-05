import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Kuramoto Simulation
# -----------------------------
def simulate_kuramoto(N=100, K=2.5, T=2000, dt=0.01):
    theta = np.random.uniform(0, 2*np.pi, N)
    omega = np.random.normal(0, 1, N)

    phases = []
    drift = []

    for _ in range(T):
        order = np.mean(np.exp(1j * theta))
        r = np.abs(order)
        psi = np.angle(order)

        dtheta = omega + K * r * np.sin(psi - theta)
        theta += dtheta * dt

        # global phase
        phi = np.angle(order)

        # drift measure
        drift_val = np.std(dtheta)

        phases.append(phi)
        drift.append(drift_val)

    return np.array(phases), np.array(drift)


# -----------------------------
# 2. Example Control Law s*(φ)
# (replace later with your real one)
# -----------------------------
def control_law(phi):
    # placeholder shape similar to your plot
    return 0.3 + 0.4 * (1 + np.cos(phi))


# -----------------------------
# 3. Run Simulation
# -----------------------------
phi, drift = simulate_kuramoto()

# normalize phi to [0, 2π]
phi = (phi + 2*np.pi) % (2*np.pi)

# sort by phase
idx = np.argsort(phi)
phi_sorted = phi[idx]
drift_sorted = drift[idx]

# evaluate control law
s_phi = control_law(phi_sorted)

# normalize for comparison
drift_norm = drift_sorted / np.max(drift_sorted)
s_norm = s_phi / np.max(s_phi)


# -----------------------------
# 4. Plot
# -----------------------------
plt.figure(figsize=(10, 5))

plt.plot(phi_sorted, drift_norm, label="Drift(φ)", linewidth=2)
plt.plot(phi_sorted, s_norm, label="Control s*(φ)", linewidth=2)

plt.xlabel("Phase φ")
plt.ylabel("Normalized value")
plt.title("Control vs Phase Geometry")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("RESEARCH/VALIDATION/causality/results/control_vs_phase_geometry.png")
plt.show()

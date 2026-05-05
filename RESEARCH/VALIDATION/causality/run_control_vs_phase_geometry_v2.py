import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Kuramoto Simulation
# -----------------------------
def simulate_kuramoto(N=100, K=2.5, T=3000, dt=0.01):
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

        phi = np.angle(order)
        drift_val = np.std(dtheta)

        phases.append(phi)
        drift.append(drift_val)

    phi = np.array(phases)
    drift = np.array(drift)

    # normalize phase to [0, 2π]
    phi = (phi + 2*np.pi) % (2*np.pi)

    return phi, drift


# -----------------------------
# 2. Control Law (replace later)
# -----------------------------
def control_law(phi):
    return 0.3 + 0.4 * (1 + np.cos(phi))


# -----------------------------
# 3. Run Simulation
# -----------------------------
phi, drift = simulate_kuramoto()

# -----------------------------
# 4. Phase Binning (KEY STEP)
# -----------------------------
num_bins = 80
bins = np.linspace(0, 2*np.pi, num_bins)
digitized = np.digitize(phi, bins)

phi_centers = []
drift_mean = []

for i in range(1, len(bins)):
    mask = digitized == i
    if np.sum(mask) > 10:  # avoid empty bins
        phi_centers.append(np.mean(phi[mask]))
        drift_mean.append(np.mean(drift[mask]))

phi_centers = np.array(phi_centers)
drift_mean = np.array(drift_mean)

# -----------------------------
# 5. Evaluate Control Law
# -----------------------------
s_vals = control_law(phi_centers)

# normalize both
drift_norm = drift_mean / np.max(drift_mean)
s_norm = s_vals / np.max(s_vals)


# -----------------------------
# 6. Correlation (optional but important)
# -----------------------------
corr = np.corrcoef(drift_norm, s_norm)[0, 1]
print(f"Correlation Drift vs Control: {corr:.4f}")


# -----------------------------
# 7. Plot
# -----------------------------
plt.figure(figsize=(10, 5))

plt.plot(phi_centers, drift_norm, label="Mean Drift(φ)", linewidth=3)
plt.plot(phi_centers, s_norm, label="Control s*(φ)", linewidth=3)

plt.xlabel("Phase φ")
plt.ylabel("Normalized value")
plt.title("Control vs Phase Geometry (Binned)")
plt.legend()
plt.grid()

plt.tight_layout()
plt.savefig("RESEARCH/VALIDATION/causality/results/control_vs_phase_geometry_v2.png")
plt.show()

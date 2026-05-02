import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Phase Dynamics Analysis")

# =========================
# PARAMETERS
# =========================

n_steps = 3000
dt = 0.01

# =========================
# LORENZ SYSTEM
# =========================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# =========================
# SIMULATION
# =========================

x = np.array([10.0, 10.0, 20.0])

trajectory = []
theta = []
instability = []

for i in range(n_steps):
    dx = lorenz(x)

    trajectory.append(x.copy())
    theta.append(np.arctan2(x[1], x[0]))
    instability.append(np.linalg.norm(dx[:2]))

    x = x + dt * dx

trajectory = np.array(trajectory)
theta = np.unwrap(np.array(theta))
instability = np.array(instability)

# =========================
# PHASE DYNAMICS
# =========================

omega = np.gradient(theta, dt)          # dφ/dt
alpha_phase = np.gradient(omega, dt)    # d²φ/dt²

omega_smooth = np.convolve(
    omega,
    np.ones(25) / 25,
    mode="same"
)

phase_mismatch = np.abs(omega - omega_smooth)

# =========================
# IOTA EVENTS
# =========================

iota_threshold = np.percentile(instability, 95)
iota_mask = instability > iota_threshold
iota_idx = np.where(iota_mask)[0]

# =========================
# STATISTICS
# =========================

mean_phase_mismatch_iota = np.mean(phase_mismatch[iota_mask])
mean_phase_mismatch_all = np.mean(phase_mismatch)

mean_omega_iota = np.mean(np.abs(omega[iota_mask]))
mean_omega_all = np.mean(np.abs(omega))

print("\n📊 Phase Dynamics Statistics:")
print(f"IOTA count: {len(iota_idx)}")
print(f"Mean |ω| at IOTA:        {mean_omega_iota:.6f}")
print(f"Mean |ω| overall:        {mean_omega_all:.6f}")
print(f"Mean phase mismatch IOTA:{mean_phase_mismatch_iota:.6f}")
print(f"Mean phase mismatch all: {mean_phase_mismatch_all:.6f}")
print(f"Δ mismatch:              {mean_phase_mismatch_iota - mean_phase_mismatch_all:.6f}")

# =========================
# PLOT 1 — PHASE VELOCITY
# =========================

plt.figure(figsize=(14, 6))
plt.plot(omega, label="ω = dφ/dt", alpha=0.7)
plt.plot(omega_smooth, label="expected / smoothed ω", linewidth=2)

plt.scatter(
    iota_idx,
    omega[iota_idx],
    color="red",
    s=25,
    label="IOTA"
)

plt.title("Phase Velocity and IOTA Events")
plt.xlabel("time")
plt.ylabel("phase velocity ω")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "RESEARCH/validation/causality/results/phase_velocity_iota.png",
    dpi=200
)
plt.close()

# =========================
# PLOT 2 — PHASE MISMATCH
# =========================

plt.figure(figsize=(14, 6))
plt.plot(phase_mismatch, label="phase mismatch |ω - smooth(ω)|", linewidth=2)

plt.scatter(
    iota_idx,
    phase_mismatch[iota_idx],
    color="red",
    s=25,
    label="IOTA"
)

plt.title("Phase Mismatch and IOTA Events")
plt.xlabel("time")
plt.ylabel("phase mismatch")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "RESEARCH/validation/causality/results/phase_mismatch_iota.png",
    dpi=200
)
plt.close()

# =========================
# PLOT 3 — PROBABILITY LAW
# =========================

bins = np.linspace(np.min(phase_mismatch), np.max(phase_mismatch), 25)
centers = 0.5 * (bins[:-1] + bins[1:])

p_iota = []

for lo, hi in zip(bins[:-1], bins[1:]):
    mask = (phase_mismatch >= lo) & (phase_mismatch < hi)

    if np.sum(mask) == 0:
        p_iota.append(np.nan)
    else:
        p_iota.append(np.mean(iota_mask[mask]))

p_iota = np.array(p_iota)

plt.figure(figsize=(9, 5))
plt.plot(centers, p_iota, "o-", linewidth=2)

plt.title("P(IOTA | Phase Mismatch)")
plt.xlabel("phase mismatch")
plt.ylabel("P(IOTA)")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "RESEARCH/validation/causality/results/phase_mismatch_probability.png",
    dpi=200
)
plt.close()

# =========================
# PLOT 4 — PHASE PORTRAIT
# =========================

plt.figure(figsize=(8, 6))
plt.scatter(
    omega,
    phase_mismatch,
    s=8,
    alpha=0.3,
    label="all"
)
plt.scatter(
    omega[iota_mask],
    phase_mismatch[iota_mask],
    color="red",
    s=25,
    label="IOTA"
)

plt.title("IOTA in Phase-Dynamics Space")
plt.xlabel("ω = dφ/dt")
plt.ylabel("|ω - smooth(ω)|")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig(
    "RESEARCH/validation/causality/results/phase_dynamics_space.png",
    dpi=200
)
plt.close()

# =========================
# SAVE SUMMARY
# =========================

summary_path = "RESEARCH/validation/causality/results/phase_dynamics_summary.txt"

with open(summary_path, "w") as f:
    f.write("NEXAH — Phase Dynamics Analysis\n\n")
    f.write(f"IOTA count: {len(iota_idx)}\n")
    f.write(f"Mean |omega| at IOTA: {mean_omega_iota:.6f}\n")
    f.write(f"Mean |omega| overall: {mean_omega_all:.6f}\n")
    f.write(f"Mean phase mismatch at IOTA: {mean_phase_mismatch_iota:.6f}\n")
    f.write(f"Mean phase mismatch overall: {mean_phase_mismatch_all:.6f}\n")
    f.write(f"Delta mismatch: {mean_phase_mismatch_iota - mean_phase_mismatch_all:.6f}\n\n")
    f.write("Interpretation:\n")
    f.write("IOTA events are tested against deviations in phase velocity.\n")
    f.write("This checks whether transitions are associated with broken rotational consistency.\n")

print("✅ Saved: phase_velocity_iota.png")
print("✅ Saved: phase_mismatch_iota.png")
print("✅ Saved: phase_mismatch_probability.png")
print("✅ Saved: phase_dynamics_space.png")
print("✅ Saved: phase_dynamics_summary.txt")

# ================================
# IOTA ANGULAR SYMMETRY TEST
# ================================

print("\n🔬 Running angular symmetry test...")

theta_iota = theta[iota_indices]  # oder iota_mask

# normalize
theta_iota = (theta_iota + 2*np.pi) % (2*np.pi)

# histogram
bins = 36
hist, edges = np.histogram(theta_iota, bins=bins, density=True)
centers = (edges[:-1] + edges[1:]) / 2

plt.figure(figsize=(8,4))
plt.plot(centers, hist)
plt.title("IOTA Angular Distribution")
plt.xlabel("theta")
plt.ylabel("density")
plt.grid()
plt.show()

# Fourier
fft_vals = np.abs(np.fft.fft(hist))

plt.figure(figsize=(8,4))
plt.plot(fft_vals[:len(fft_vals)//2])
plt.title("Angular Frequency Spectrum")
plt.xlabel("mode k")
plt.ylabel("amplitude")
plt.grid()
plt.show()

# dominant modes
dominant = np.argsort(fft_vals)[-5:]
print("Top angular modes:", dominant)

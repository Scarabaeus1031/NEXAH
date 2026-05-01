import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — Control Mismatch Analysis")

# =========================
# LOAD CONTROL LAW
# =========================

data = np.load("RESEARCH/validation/causality/control_law_data.npz")
phi_grid = data["phi"]
s_star = data["s_star"]

# =========================
# SIMULATE SYSTEM (Lorenz)
# =========================

dt = 0.01
n_steps = 2000

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# initial state
x = np.array([1.0, 1.0, 20.0])

trajectory = []
theta_series = []
instability_series = []

for i in range(n_steps):
    dx = lorenz(x)
    x = x + dt * dx

    trajectory.append(x.copy())

    # phase angle in xy-plane
    theta = np.arctan2(x[1], x[0])
    theta_series.append(theta)

    # instability proxy
    instability = np.linalg.norm(dx[:2])
    instability_series.append(instability)

trajectory = np.array(trajectory)
theta_series = np.unwrap(np.array(theta_series))
instability_series = np.array(instability_series)

# =========================
# MAP s*(φ) TO TIME SERIES
# =========================

theta_mod = theta_series % (2 * np.pi)
s_t = np.interp(theta_mod, phi_grid, s_star)

# =========================
# DETECT IOTA EVENTS
# =========================

threshold = np.percentile(instability_series, 95)

iota_mask = instability_series > threshold
iota_indices = np.where(iota_mask)[0]

print(f"Detected IOTA events: {len(iota_indices)}")

# =========================
# MISMATCH COMPUTATION
# =========================

# normalize both signals
inst_norm = (instability_series - np.mean(instability_series)) / np.std(instability_series)
s_norm = (s_t - np.mean(s_t)) / np.std(s_t)

mismatch = inst_norm - s_norm

# =========================
# STATISTICS
# =========================

mean_mismatch_iota = np.mean(mismatch[iota_indices])
mean_mismatch_all = np.mean(mismatch)

print("\n📊 Mismatch Statistics:")
print(f"Mean mismatch at IOTA: {mean_mismatch_iota:.4f}")
print(f"Mean mismatch overall: {mean_mismatch_all:.4f}")
print(f"Δ: {mean_mismatch_iota - mean_mismatch_all:.4f}")

# =========================
# PLOT 1: Time Series
# =========================

plt.figure(figsize=(14, 6))

plt.plot(inst_norm, label="instability (normalized)", alpha=0.7)
plt.plot(s_norm, label="s*(θ(t)) (normalized)", alpha=0.7)
plt.plot(mismatch, label="mismatch", linewidth=2)

plt.scatter(iota_indices, mismatch[iota_indices], color="red", label="IOTA", zorder=5)

plt.legend()
plt.title("Control vs Instability vs Mismatch")
plt.xlabel("time")
plt.ylabel("value")
plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/mismatch_timeseries.png", dpi=200)
plt.close()

# =========================
# PLOT 2: Distribution
# =========================

plt.figure(figsize=(8, 5))

plt.hist(mismatch, bins=50, alpha=0.6, label="all")
plt.hist(mismatch[iota_indices], bins=50, alpha=0.6, label="IOTA")

plt.legend()
plt.title("Mismatch Distribution")
plt.xlabel("mismatch")
plt.ylabel("frequency")
plt.grid(True)
plt.tight_layout()

plt.savefig("RESEARCH/validation/causality/results/mismatch_distribution.png", dpi=200)
plt.close()

print("✅ Saved: mismatch_timeseries.png")
print("✅ Saved: mismatch_distribution.png")

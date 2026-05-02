import numpy as np
import matplotlib.pyplot as plt

print("⚡ NEXAH — YUGO Control Overlay (LOCAL)")

# ======================================
# PARAMETERS
# ======================================

n_steps = 2000
dt = 0.01

# target (wie im Gate-System)
target = np.array([15.0, 15.0])
target_radius = 3.0

# ======================================
# LORENZ SYSTEM
# ======================================

def lorenz(x, sigma=10.0, rho=28.0, beta=8/3):
    dx = sigma * (x[1] - x[0])
    dy = x[0] * (rho - x[2]) - x[1]
    dz = x[0] * x[1] - beta * x[2]
    return np.array([dx, dy, dz])

# ======================================
# SIMULATION
# ======================================

x = np.array([1.0, 1.0, 20.0])

trajectory = []

for i in range(n_steps):
    x = x + dt * lorenz(x)
    trajectory.append(x.copy())

trajectory = np.array(trajectory)

# ======================================
# PHASE (θ) + YUGO APPROX
# ======================================

dx = np.gradient(trajectory[:, 0])
dy = np.gradient(trajectory[:, 1])

theta = np.arctan2(dy, dx)
theta_unwrapped = np.unwrap(theta)

phi = np.mod(theta_unwrapped, 2*np.pi)

# ======================================
# IOTA DETECTION (simple proxy)
# ======================================

dtheta = np.gradient(theta_unwrapped)
threshold = np.percentile(np.abs(dtheta), 98)

iota_indices = np.where(np.abs(dtheta) > threshold)[0]

print(f"Detected IOTA events: {len(iota_indices)}")

# ======================================
# LOAD CONTROL LAW
# ======================================

control_data = np.load("RESEARCH/validation/causality/control_law_data.npz")

phi_grid = control_data["phi"]
s_star = control_data["s_star"]

def s_star_function(phi):
    return np.interp(phi, phi_grid, s_star, period=2*np.pi)

s_values = s_star_function(phi)

# ======================================
# PLOT 1 — Phase vs Control
# ======================================

plt.figure(figsize=(12, 5))

plt.plot(phi, s_values, label="s*(φ)", linewidth=2)

plt.scatter(
    phi[iota_indices],
    s_values[iota_indices],
    color="red",
    label="IOTA events",
    zorder=3
)

plt.xlabel("phase φ")
plt.ylabel("control strength")
plt.title("NEXAH — Control Law vs Phase")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/yugo_control_overlay.png")
print("✅ Saved: yugo_control_overlay.png")

plt.show()

# ======================================
# PLOT 2 — Time vs Control + Instability
# ======================================

plt.figure(figsize=(12, 5))

plt.plot(s_values, label="s*(θ(t))")
plt.plot(np.abs(dtheta), label="|dθ/dt| (instability)", alpha=0.7)

plt.scatter(
    iota_indices,
    s_values[iota_indices],
    color="red",
    label="IOTA events",
    zorder=3
)

plt.xlabel("time")
plt.ylabel("value")
plt.title("Control vs Instability")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig("RESEARCH/validation/causality/yugo_control_timeseries.png")
print("✅ Saved: yugo_control_timeseries.png")

plt.show()

# ======================================
# STATISTICS
# ======================================

mean_s_iota = np.mean(s_values[iota_indices])
mean_s_all = np.mean(s_values)

print("\n📊 Statistics:")
print(f"Mean s*(φ) at IOTA: {mean_s_iota:.4f}")
print(f"Mean s*(φ) overall: {mean_s_all:.4f}")
print(f"Δ: {mean_s_iota - mean_s_all:.4f}")

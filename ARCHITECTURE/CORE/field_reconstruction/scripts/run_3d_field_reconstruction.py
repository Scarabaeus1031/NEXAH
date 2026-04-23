import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from mpl_toolkits.mplot3d import Axes3D

# =========================
# 1. Generate signal (IEEE-like synthetic proxy)
# =========================
t = np.linspace(0, 50, 5000)

# mixture of oscillations → like power system signal
signal = (
    np.sin(t)
    + 0.5 * np.sin(2.3 * t + 0.5)
    + 0.3 * np.sin(0.5 * t)
)

# slight instability injection
signal += 0.05 * np.random.randn(len(t))

# smooth (important!)
signal = savgol_filter(signal, 51, 3)

# =========================
# 2. Delay embedding (3D)
# =========================
tau = 10

x = signal[:-2*tau]
y = signal[tau:-tau]
z = signal[2*tau:]

# =========================
# 3. Derivatives (flow)
# =========================
dx = np.gradient(x)
dy = np.gradient(y)
dz = np.gradient(z)

# =========================
# 4. Plot
# =========================
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# subsample for clarity
step = 10

ax.quiver(
    x[::step], y[::step], z[::step],
    dx[::step], dy[::step], dz[::step],
    length=0.1,
    normalize=True
)

# trajectory overlay
ax.plot(x, y, z, alpha=0.3)

ax.set_title("⚡ NEXAH 3D Field Reconstruction")
ax.set_xlabel("X(t)")
ax.set_ylabel("X(t+τ)")
ax.set_zlabel("X(t+2τ)")

plt.tight_layout()
plt.savefig("ARCHITECTURE/CORE/field_reconstruction/dynamics/nexah_3d_field.png", dpi=200)
plt.show()

print("✔ Saved → nexah_3d_field.png")

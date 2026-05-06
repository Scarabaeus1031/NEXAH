# ============================================================
# VISUAL 08 — ZETA × NEXAH BRIDGE (SCRIPT VERSION)
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ------------------------------------------------------------
# 1. ZETA-LIKE PATH
# ------------------------------------------------------------
def zeta_like_path(n_terms=200, sigma=0.5, t=14):
    z = 0+0j
    path = []

    for n in range(1, n_terms+1):
        term = n**(-sigma) * np.exp(-1j * t * np.log(n))
        z += term
        path.append(z)

    return np.array(path)


# ------------------------------------------------------------
# 2. FIELD STRUCTURE
# ------------------------------------------------------------
def generate_field(n=1200):
    clusters = [
        (-15,  8), (15,  8),
        (-12, -12), (10, -10)
    ]

    pts = []
    for cx, cy in clusters:
        x = np.random.normal(cx, 4, n//len(clusters))
        y = np.random.normal(cy, 3, n//len(clusters))
        pts.append(np.vstack([x, y]).T)

    return np.vstack(pts)


# ------------------------------------------------------------
# 3. APERTURE RING
# ------------------------------------------------------------
def aperture_ring():
    theta = np.linspace(0, 2*np.pi, 400)
    r = 10 + 3*np.cos(2*theta)
    return r*np.cos(theta), r*np.sin(theta)


# ------------------------------------------------------------
# 4. COHERENCE
# ------------------------------------------------------------
def coherence(signal, window=20):
    C = []
    for i in range(len(signal)):
        if i < window:
            C.append(1.0)
        else:
            seg = signal[i-window:i]
            c = np.corrcoef(seg[:-1], seg[1:])[0,1]
            if np.isnan(c):
                c = 0
            C.append(c)
    return np.array(C)


# ------------------------------------------------------------
# DATA
# ------------------------------------------------------------
z_path = zeta_like_path()
field = generate_field()
ring_x, ring_y = aperture_ring()

signal = np.abs(z_path)
C = coherence(signal)

threshold = 0.1
gates = np.where(C < threshold)[0]

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
fig, axs = plt.subplots(2, 3, figsize=(16, 10))

# ------------------------------------------------------------
# 1 — ROTATION
# ------------------------------------------------------------
axs[0,0].plot(z_path.real, z_path.imag)
axs[0,0].scatter(0,0)
axs[0,0].set_title("Rotating Contributions")
axs[0,0].grid(alpha=0.3)

# ------------------------------------------------------------
# 2 — INTERFERENCE
# ------------------------------------------------------------
axs[0,1].plot(z_path.real, z_path.imag)
axs[0,1].set_title("Interference Path")
axs[0,1].grid(alpha=0.3)

# ------------------------------------------------------------
# 3 — FIELD
# ------------------------------------------------------------
axs[0,2].scatter(field[:,0], field[:,1], s=5, alpha=0.3)
axs[0,2].set_title("Field Projection")
axs[0,2].grid(alpha=0.3)

# ------------------------------------------------------------
# 4 — APERTURE
# ------------------------------------------------------------
axs[1,0].plot(ring_x, ring_y)
axs[1,0].set_title("Aperture Structure")
axs[1,0].grid(alpha=0.3)

# ------------------------------------------------------------
# 5 — COHERENCE
# ------------------------------------------------------------
axs[1,1].plot(C)
axs[1,1].axhline(threshold, linestyle="--")

for g in gates:
    axs[1,1].axvline(g, alpha=0.2)

axs[1,1].set_title("Coherence + Gates")
axs[1,1].grid(alpha=0.3)

# ------------------------------------------------------------
# 6 — SUMMARY
# ------------------------------------------------------------
axs[1,2].axis("off")

axs[1,2].text(
    0.1, 0.5,
    "Rotation → Interference → Structure → Coherence → Transition",
    fontsize=12
)

plt.suptitle("VISUAL 08 — ZETA × NEXAH BRIDGE")
plt.tight_layout()
plt.savefig("08_zeta_nexah_bridge_clean.png", dpi=300)
plt.show()

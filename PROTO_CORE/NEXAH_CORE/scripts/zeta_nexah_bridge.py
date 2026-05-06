# ============================================================
# VISUAL 08 — ZETA × NEXAH BRIDGE
# "From rotating contributions to field transitions"
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

# ------------------------------------------------------------
# 1. ZETA-LIKE ROTATING SUM
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
# 2. SYNTHETIC FIELD (NEXAH-style cloud)
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
# 3. APERTURE RING (pink structure)
# ------------------------------------------------------------
def aperture_ring():
    theta = np.linspace(0, 2*np.pi, 400)
    r = 10 + 3*np.cos(2*theta)
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y


# ------------------------------------------------------------
# 4. COHERENCE (simple proxy)
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

# fake signal from magnitude evolution
signal = np.abs(z_path)
C = coherence(signal)

# gate candidates
threshold = 0.1
gates = np.where(C < threshold)[0]

# ------------------------------------------------------------
# PLOT
# ------------------------------------------------------------
fig = plt.figure(figsize=(18, 10))

# ------------------------------------------------------------
# Q1 — ZETA PATH
# ------------------------------------------------------------
ax1 = plt.subplot(2, 3, 1)
ax1.plot(z_path.real, z_path.imag, lw=1.2)
ax1.scatter(0, 0, s=40)  # origin
ax1.set_title("Zeta-like Path (Interference)")
ax1.set_xlabel("Re")
ax1.set_ylabel("Im")
ax1.grid(True, alpha=0.3)


# ------------------------------------------------------------
# Q2 — FIELD + RING
# ------------------------------------------------------------
ax2 = plt.subplot(2, 3, 2)
ax2.scatter(field[:,0], field[:,1], s=4, alpha=0.3)
ax2.plot(ring_x, ring_y, lw=2)

ax2.set_title("Field Structure + Aperture Ring")
ax2.set_xlabel("α")
ax2.set_ylabel("β")
ax2.grid(True, alpha=0.3)


# ------------------------------------------------------------
# Q3 — OVERLAY (KEY BRIDGE)
# ------------------------------------------------------------
ax3 = plt.subplot(2, 3, 3)
ax3.scatter(field[:,0], field[:,1], s=3, alpha=0.2)
ax3.plot(ring_x, ring_y, lw=2)
ax3.plot(
    z_path.real * 3,  # scaled into field space
    z_path.imag * 3,
    lw=1.2
)

ax3.set_title("Overlay: Zeta ↔ Field Mapping")
ax3.set_xlabel("α")
ax3.set_ylabel("β")
ax3.grid(True, alpha=0.3)


# ------------------------------------------------------------
# Q4 — SIGNAL
# ------------------------------------------------------------
ax4 = plt.subplot(2, 3, 4)
ax4.plot(signal)
ax4.set_title("Signal |Z(t)|")
ax4.set_xlabel("t")
ax4.grid(True, alpha=0.3)


# ------------------------------------------------------------
# Q5 — COHERENCE + GATES
# ------------------------------------------------------------
ax5 = plt.subplot(2, 3, 5)
ax5.plot(C, lw=1.5)
ax5.axhline(threshold, linestyle="--", linewidth=1)

for g in gates:
    ax5.axvline(g, alpha=0.2)

ax5.set_title("Coherence + Gate Candidates")
ax5.set_xlabel("t")
ax5.set_ylabel("C(t)")
ax5.grid(True, alpha=0.3)


# ------------------------------------------------------------
# Q6 — ABSTRACT SUMMARY PANEL
# ------------------------------------------------------------
ax6 = plt.subplot(2, 3, 6)
ax6.axis("off")

text = """
ROTATION → INTERFERENCE → STRUCTURE → TRANSITION

Zeta:
    rotating contributions
    ↓
    interference path

NEXAH:
    field structure
    ↓
    coherence collapse
    ↓
    gates

Insight:
    transitions occur where
    structured contributions cancel
"""

ax6.text(0.05, 0.5, text, fontsize=11, va='center')


# ------------------------------------------------------------
# TITLE + SAVE
# ------------------------------------------------------------
plt.suptitle(
    "VISUAL 08 — ZETA × NEXAH BRIDGE\nMulti-Layer Mapping: Interference → Field → Coherence → Gates",
    fontsize=16
)

plt.tight_layout(rect=[0, 0, 1, 0.93])

plt.savefig("08_zeta_nexah_bridge.png", dpi=300)
plt.show()

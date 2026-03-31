import numpy as np
import matplotlib.pyplot as plt

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
states = np.load("states.npy")
rift = np.load("rift.npy")

phi = states[:, 0]
instability = states[:, 1]

t = np.arange(len(phi))

# -------------------------------------------------
# BASE PARAMETERS (from V20)
# -------------------------------------------------
base = np.mean(phi)
std = np.std(phi)

upper = base + std
lower = base - std

base_freq = 0.0083

print(f"Base Layer:  {base:.4f} ± {std:.4f}")
print(f"Upper Layer: {upper:.4f}")
print(f"Lower Layer: {lower:.4f}")
print(f"Base frequency: {base_freq:.4f}")

# -------------------------------------------------
# PHASE → ANGLE (TORUS PROJECTION)
# -------------------------------------------------
theta = phi % (2*np.pi)

# -------------------------------------------------
# PETAL SEGMENTATION (13 petals)
# -------------------------------------------------
NUM_PETALS = 13

petal_ids = np.floor((theta / (2*np.pi)) * NUM_PETALS).astype(int)

# -------------------------------------------------
# RING CLASSIFICATION (like V20)
# -------------------------------------------------
ring_ids = np.zeros(len(phi))

for i in range(len(phi)):
    if phi[i] > upper:
        ring_ids[i] = 2  # upper ring
    elif phi[i] < lower:
        ring_ids[i] = 0  # lower ring
    else:
        ring_ids[i] = 1  # base ring

# -------------------------------------------------
# PORTAL DETECTION (center stability)
# -------------------------------------------------
phase_error = phi - (base_freq * t)
portal_mask = np.abs(phase_error) < 0.02

# -------------------------------------------------
# TRANSITION MATRIX (PETAL FLOW)
# -------------------------------------------------
transitions = np.zeros((NUM_PETALS, NUM_PETALS))

for i in range(len(petal_ids)-1):
    a = petal_ids[i]
    b = petal_ids[i+1]
    transitions[a, b] += 1

# normalize
row_sums = transitions.sum(axis=1, keepdims=True)
transitions_norm = np.divide(transitions, row_sums, where=row_sums!=0)

# -------------------------------------------------
# TORUS PROJECTION (2D rings)
# -------------------------------------------------
r_map = {0: 0.85, 1: 1.0, 2: 1.15}

x = np.array([r_map[r] * np.cos(theta[i]) for i, r in enumerate(ring_ids)])
y = np.array([r_map[r] * np.sin(theta[i]) for i, r in enumerate(ring_ids)])

# -------------------------------------------------
# SAVE OUTPUT
# -------------------------------------------------
np.save("field_navigation_v21.npy", np.vstack([x, y]).T)
np.save("v21_petal_ids.npy", petal_ids)
np.save("v21_transitions.npy", transitions_norm)

print("Saved → field_navigation_v21.npy")
print("Saved → v21_petal_ids.npy")
print("Saved → v21_transitions.npy")

# -------------------------------------------------
# PLOT — TORUS + PETALS
# -------------------------------------------------
plt.figure(figsize=(6,6))

colors = ["purple", "gold", "green"]

for r in [0,1,2]:
    mask = ring_ids == r
    plt.scatter(x[mask], y[mask], s=20, color=colors[r], label=f"ring {r}")

# portal points
plt.scatter(x[portal_mask], y[portal_mask], color="red", s=40, label="portal")

plt.gca().set_aspect("equal")
plt.title("V21 — Torus Petal Mapping")
plt.legend()
plt.grid()

plt.savefig("v21_torus_petals.png", dpi=150)
plt.show()

# -------------------------------------------------
# PLOT — TRANSITION MATRIX
# -------------------------------------------------
plt.figure(figsize=(6,5))
plt.imshow(transitions_norm, cmap="viridis")
plt.colorbar(label="transition prob")
plt.title("V21 — Petal Transition Matrix")
plt.xlabel("to")
plt.ylabel("from")

plt.savefig("v21_transition_matrix.png", dpi=150)
plt.show()

print("V21 DONE")

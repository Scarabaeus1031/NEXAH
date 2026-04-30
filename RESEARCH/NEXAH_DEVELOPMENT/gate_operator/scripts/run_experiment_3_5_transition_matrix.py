import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# SYSTEM
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(steps=8000, dt=0.01):
    xs, ys, zs = np.zeros(steps), np.zeros(steps), np.zeros(steps)
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys

def compute_sheets(xs, ys, num_sheets=6):
    r = np.sqrt(xs**2 + ys**2)
    bins = np.linspace(r.min(), r.max(), num_sheets + 1)
    return np.digitize(r, bins) - 1

# ============================================================
# RUN
# ============================================================

print("Running Experiment 3.5 — Transition Matrix")

xs, ys = simulate()
sheets = compute_sheets(xs, ys)

num_states = len(np.unique(sheets))

T = np.zeros((num_states, num_states))

for i in range(1, len(sheets)):
    a = int(sheets[i-1])
    b = int(sheets[i])
    T[a, b] += 1

# normalize rows
P = T / (T.sum(axis=1, keepdims=True) + 1e-9)

print("\nTransition Matrix (counts):")
print(T)

print("\nTransition Matrix (probabilities):")
print(P)

# ============================================================
# OUTPUT DIR
# ============================================================

output_dir = "../output_results"
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# SAVE DATA (WICHTIG FÜR 3.6)
# ============================================================

np.save(os.path.join(output_dir, "experiment_3_5_transition_matrix.npy"), T)
np.save(os.path.join(output_dir, "experiment_3_5_transition_prob_matrix.npy"), P)
np.save(os.path.join(output_dir, "experiment_3_5_sheet_sequence.npy"), sheets)

print("Saved transition matrix + probabilities + sheet sequence")

# ============================================================
# PLOT
# ============================================================

plt.figure(figsize=(6,5))

plt.imshow(P, cmap="viridis")
plt.colorbar(label="P(i → j)")

plt.xlabel("to state")
plt.ylabel("from state")
plt.title("Experiment 3.5 — Sheet Transition Matrix")

plt.tight_layout()

# SAVE FIGURE
plt.savefig(
    os.path.join(output_dir, "experiment_3_5_transition_matrix.png"),
    dpi=200
)

plt.close()

print("Saved visualization: experiment_3_5_transition_matrix.png")

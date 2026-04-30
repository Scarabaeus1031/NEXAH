import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# SAFE OUTPUT PATH (FIX!)
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(BASE_DIR, "../output_results")
os.makedirs(output_dir, exist_ok=True)

print(f"📁 Output directory: {output_dir}")

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
# SAVE DATA (CRITICAL FOR 3.6)
# ============================================================

path_T = os.path.join(output_dir, "experiment_3_5_transition_matrix.npy")
path_P = os.path.join(output_dir, "experiment_3_5_transition_prob_matrix.npy")
path_sheets = os.path.join(output_dir, "experiment_3_5_sheet_sequence.npy")

np.save(path_T, T)
np.save(path_P, P)
np.save(path_sheets, sheets)

# VERIFY SAVE
for path in [path_T, path_P, path_sheets]:
    if os.path.exists(path):
        print(f"✅ Saved: {path}")
    else:
        print(f"❌ ERROR saving: {path}")

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

file_plot = os.path.join(output_dir, "experiment_3_5_transition_matrix.png")
plt.savefig(file_plot, dpi=200)

if os.path.exists(file_plot):
    print(f"✅ Saved visualization: {file_plot}")
else:
    print("❌ ERROR saving visualization")

plt.close()

print("✅ Experiment 3.5 complete")

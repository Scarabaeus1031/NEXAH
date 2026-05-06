import numpy as np
import matplotlib.pyplot as plt
import os

# ============================================================
# OUTPUT SETUP
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "..", "visuals", "structure")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"📁 Output directory: {OUTPUT_DIR}")

# ============================================================
# SYSTEM (Lorenz)
# ============================================================

def lorenz(x, y, z, s=10, r=28, b=2.667):
    return s*(y-x), x*(r-z)-y, x*y - b*z

def simulate(steps=8000, dt=0.01):
    xs = np.zeros(steps)
    ys = np.zeros(steps)
    zs = np.zeros(steps)

    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)

    for i in range(steps - 1):
        dx, dy, dz = lorenz(xs[i], ys[i], zs[i])
        xs[i+1] = xs[i] + dx*dt
        ys[i+1] = ys[i] + dy*dt
        zs[i+1] = zs[i] + dz*dt

    return xs, ys, zs

# ============================================================
# SHEET STRUCTURE
# ============================================================

def compute_sheets(xs, ys, num_sheets=6):
    r = np.sqrt(xs**2 + ys**2)

    bins = np.linspace(r.min(), r.max(), num_sheets + 1)
    sheet_idx = np.digitize(r, bins) - 1

    return sheet_idx

def compute_transition_matrix(sheets):
    n_states = len(np.unique(sheets))
    T = np.zeros((n_states, n_states))

    for t in range(1, len(sheets)):
        i = int(sheets[t-1])
        j = int(sheets[t])

        T[i, j] += 1

    P = T / (T.sum(axis=1, keepdims=True) + 1e-9)

    return T, P

# ============================================================
# MAIN
# ============================================================

print("Running Transition Structure Analysis")

# simulate system
xs, ys, zs = simulate()

# compute sheets
sheets = compute_sheets(xs, ys, num_sheets=6)

# transitions
transitions = np.zeros(len(sheets), dtype=bool)
transitions[1:] = sheets[1:] != sheets[:-1]

# transition matrix
T, P = compute_transition_matrix(sheets)

# ============================================================
# PRINT RESULTS
# ============================================================

print("\n--- Transition Structure ---")
print(f"Total transitions: {np.sum(transitions)}")
print(f"Number of states: {len(np.unique(sheets))}")

print("\nTransition Matrix (probabilities):")
print(P)

# ============================================================
# VISUAL 1 — SHEET TRAJECTORY
# ============================================================

plt.figure(figsize=(16, 4))

plt.plot(sheets, label="sheet index", alpha=0.7)

plt.scatter(
    np.where(transitions)[0],
    sheets[transitions],
    color="red",
    s=10,
    label="transitions"
)

plt.title("Transition Structure — Sheet Dynamics")
plt.xlabel("time")
plt.ylabel("sheet")
plt.legend()

plt.tight_layout()

path1 = os.path.join(OUTPUT_DIR, "transition_structure_timeseries.png")
plt.savefig(path1, dpi=200)
plt.close()

print(f"✅ Saved: {path1}")

# ============================================================
# VISUAL 2 — TRANSITION MATRIX
# ============================================================

plt.figure(figsize=(6, 5))

plt.imshow(P, cmap="viridis")
plt.colorbar(label="P(i → j)")

plt.title("Transition Matrix (Sheet Structure)")
plt.xlabel("to state")
plt.ylabel("from state")

plt.tight_layout()

path2 = os.path.join(OUTPUT_DIR, "transition_structure_matrix.png")
plt.savefig(path2, dpi=200)
plt.close()

print(f"✅ Saved: {path2}")

# ============================================================
# VISUAL 3 — STATE SPACE COLORED BY SHEETS
# ============================================================

plt.figure(figsize=(6, 6))

scatter = plt.scatter(
    xs, ys,
    c=sheets,
    cmap="tab10",
    s=2
)

plt.colorbar(scatter, label="sheet index")

plt.title("Phase Space Partition (Sheets)")
plt.xlabel("x")
plt.ylabel("y")

plt.tight_layout()

path3 = os.path.join(OUTPUT_DIR, "transition_structure_phase.png")
plt.savefig(path3, dpi=200)
plt.close()

print(f"✅ Saved: {path3}")

# ============================================================
# SAVE DATA
# ============================================================

np.save(os.path.join(OUTPUT_DIR, "transition_sheets.npy"), sheets)
np.save(os.path.join(OUTPUT_DIR, "transition_matrix.npy"), T)
np.save(os.path.join(OUTPUT_DIR, "transition_matrix_prob.npy"), P)

print("💾 Saved data")

# ============================================================
# DONE
# ============================================================

print("\n✅ Transition Structure complete")

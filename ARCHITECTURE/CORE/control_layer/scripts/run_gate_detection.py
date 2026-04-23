import numpy as np
import matplotlib.pyplot as plt
import os

print("⚡ NEXAH Gate Detection")

# --------------------------------------------------
# Output Path
# --------------------------------------------------
BASE_DIR = os.path.dirname(__file__)
OUT_DIR = os.path.abspath(os.path.join(BASE_DIR, "../outputs/demo"))
os.makedirs(OUT_DIR, exist_ok=True)

# --------------------------------------------------
# Field Definition (same as before)
# --------------------------------------------------

def flow_field(x, y):
    dx = y - x * (x**2 + y**2)
    dy = -x - y * (x**2 + y**2)
    return np.array([dx, dy])

def boundary_field(x, y):
    return np.exp((x**2 + y**2))

def target_field(x, y, tx, ty):
    return np.array([tx - x, ty - y])


# --------------------------------------------------
# Gate Score Function
# --------------------------------------------------

def gate_score(x, y, target):

    flow = flow_field(x, y)
    target_vec = target_field(x, y, target[0], target[1])

    # normalize
    flow_n = flow / (np.linalg.norm(flow) + 1e-8)
    target_n = target_vec / (np.linalg.norm(target_vec) + 1e-8)

    # alignment: how well flow points toward target
    alignment = np.dot(flow_n, target_n)

    # boundary penalty
    b = boundary_field(x, y)

    # final score
    score = alignment * np.exp(-0.3 * b)

    return score


# --------------------------------------------------
# Grid Scan
# --------------------------------------------------

target = np.array([1.5, 0.5])

x = np.linspace(-2, 2, 120)
y = np.linspace(-2, 2, 120)

X, Y = np.meshgrid(x, y)

S = np.zeros_like(X)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        S[i, j] = gate_score(X[i, j], Y[i, j], target)


# --------------------------------------------------
# Extract Gates
# --------------------------------------------------

threshold = np.percentile(S, 97)  # top 3%

gate_mask = S > threshold

# --------------------------------------------------
# Plot
# --------------------------------------------------

plt.figure(figsize=(8, 8))

# heatmap
plt.contourf(X, Y, S, levels=30, alpha=0.6)

# gates
plt.scatter(X[gate_mask], Y[gate_mask], color="red", s=10, label="gates")

# flow field
U = np.zeros_like(X)
V = np.zeros_like(Y)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        vec = flow_field(X[i, j], Y[i, j])
        U[i, j] = vec[0]
        V[i, j] = vec[1]

plt.streamplot(X, Y, U, V, color="black", density=1)

# target
plt.scatter(target[0], target[1], color="blue", s=100, label="target")

plt.legend()
plt.title("NEXAH Gate Detection")

out_path = os.path.join(OUT_DIR, "nexah_gate_detection.png")
plt.savefig(out_path, dpi=200)

print(f"✔ Saved → {out_path}")

# --------------------------------------------------
# Interpretation
# --------------------------------------------------

print("\n🧠 Interpretation:\n")
print("Red regions = optimal entry gates")
print("→ flow aligns with target")
print("→ boundary penalty is low")
print("→ these are the only stable entry paths\n")

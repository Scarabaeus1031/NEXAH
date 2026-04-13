import numpy as np
import matplotlib.pyplot as plt
import os

# =========================================
# LOAD DATA (adjust path!)
# =========================================

run_dir = "APPLICATIONS/power_systems/nexah_ieeeX/results/run_ieee300_20260413_015843"

risk = np.load(os.path.join(run_dir, "risk.npy"))
c = np.load(os.path.join(run_dir, "c.npy"))
d2c = np.load(os.path.join(run_dir, "d2c.npy"))
frag = np.load(os.path.join(run_dir, "frag.npy"))
Vmin = np.load(os.path.join(run_dir, "Vmin.npy"))

# reconstruct lambda axis
lambdas = np.linspace(0.9, 1.15, len(Vmin))

# =========================================
# ACTIONS (optional)
# =========================================

actions_path = os.path.join(run_dir, "actions.txt")
actions = []

if os.path.exists(actions_path):
    with open(actions_path) as f:
        actions = [line.strip() for line in f.readlines()]
else:
    actions = ["STABILIZE"] * len(Vmin)

y_map = {
    "STABILIZE": 0,
    "PREEMPTIVE_STABILIZE": 1,
    "REDUCE_LOAD": 2,
    "EMERGENCY_SHED": 3,
}

y = [y_map.get(a, 0) for a in actions]

# =========================================
# BUILD FIGURE
# =========================================

fig, axes = plt.subplots(4, 1, figsize=(10, 14))

# -----------------------------------------
# (A) Voltage Collapse
# -----------------------------------------
axes[0].plot(lambdas, Vmin, linewidth=2)
axes[0].set_title("(A) Voltage Collapse (Vmin)")
axes[0].set_ylabel("Voltage (p.u.)")
axes[0].grid(True)

# -----------------------------------------
# (B) Structural Features
# -----------------------------------------
axes[1].plot(lambdas, c, label="c", linewidth=2)
axes[1].plot(lambdas, d2c, label="d2c", alpha=0.7)
axes[1].plot(lambdas, frag, label="frag", alpha=0.7)
axes[1].legend()
axes[1].set_title("(B) Structural Features")
axes[1].grid(True)

# -----------------------------------------
# (C) Risk Field
# -----------------------------------------
axes[2].plot(lambdas, risk, linewidth=2)
axes[2].set_title("(C) Risk Field")
axes[2].set_ylabel("Risk ∈ [0,1]")
axes[2].grid(True)

# -----------------------------------------
# (D) Actions
# -----------------------------------------
axes[3].scatter(lambdas, y)
axes[3].set_yticks([0, 1, 2, 3])
axes[3].set_yticklabels(["STAB", "PRE", "REDUCE", "SHED"])
axes[3].set_title("(D) Control Actions")
axes[3].set_xlabel("Load Scaling λ")
axes[3].grid(True)

fig.tight_layout()

# =========================================
# SAVE
# =========================================

out_path = os.path.join(run_dir, "paper_figure.png")
fig.savefig(out_path, dpi=300)

print("Saved figure to:", out_path)

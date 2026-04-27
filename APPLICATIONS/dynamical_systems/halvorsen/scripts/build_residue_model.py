# ============================================================
# NEXAH — Build Residue Model (mod 17)
# ============================================================

import numpy as np
import os
import glob

# ------------------------------------------------------------
# Find latest matrix automatically
# ------------------------------------------------------------
base_path = os.path.dirname(__file__)
outputs_path = os.path.join(base_path, "..", "outputs")

files = sorted(glob.glob(os.path.join(outputs_path, "gate_aware_policy_matrix_*.npy")))

if not files:
    raise RuntimeError("❌ No gate_aware_policy_matrix found.")

matrix_path = files[-1]
print(f"→ using matrix: {matrix_path}")

P = np.load(matrix_path)

# ------------------------------------------------------------
# Build residue model
# ------------------------------------------------------------
mod = 17
n = P.shape[0]

model = np.zeros((mod, mod))

for i in range(n):
    for j in range(n):
        p = P[i, j]
        if p > 0:
            r_i = i % mod
            r_j = j % mod
            model[r_i, r_j] += p

# normalize
for i in range(mod):
    if model[i].sum() > 0:
        model[i] /= model[i].sum()

# ------------------------------------------------------------
# Save
# ------------------------------------------------------------
save_path = os.path.join(outputs_path, "residue_model_mod17.npy")
np.save(save_path, model)

print(f"[✓] residue model saved: {save_path}")

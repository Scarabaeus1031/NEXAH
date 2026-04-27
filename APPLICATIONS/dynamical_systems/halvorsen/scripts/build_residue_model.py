import numpy as np

P = np.load("APPLICATIONS/dynamical_systems/halvorsen/outputs/gate_aware_policy_matrix_20260427_025844.npy")

n = P.shape[0]
mod = 17

model = np.zeros((mod, n))

for i in range(n):
    r = i % mod
    model[r] += P[i]

# normalize
for r in range(mod):
    if model[r].sum() > 0:
        model[r] /= model[r].sum()

np.save("APPLICATIONS/dynamical_systems/halvorsen/outputs/residue_model_mod17.npy", model)

print("✓ residue model saved")

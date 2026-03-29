import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d
from sklearn.decomposition import PCA

# --- ensure repo root is in path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../")))

from nexah.field_layer import Field


# =========================================================
# ⚠️ REPLACE WITH YOUR REAL IEEE PIPELINE
# =========================================================
def run_powerflow(lam):
    n = 10
    V = 1.0 - 0.3 * lam + 0.01 * np.random.randn(n)
    theta = 0.1 * lam + 0.01 * np.random.randn(n)
    return V, theta


# =========================================================
# GENERATE STATES
# =========================================================

lambda_values = np.linspace(0.5, 1.5, 120)

states = []
lambdas = []

for lam in lambda_values:
    V, theta = run_powerflow(lam)
    state = np.concatenate([V, theta])

    states.append(state)
    lambdas.append(lam)

states = np.array(states)
lambdas = np.array(lambdas)


# =========================================================
# FIELD
# =========================================================

field = Field(states)
vectors = field.get_vector_field()


# =========================================================
# DIMENSION REDUCTION (PCA)
# =========================================================

pca = PCA(n_components=2)
states_2d = pca.fit_transform(states)

vectors_2d = pca.transform(states + vectors) - states_2d


# =========================================================
# PLOT FIELD FLOW
# =========================================================

plt.figure(figsize=(10, 8))

# trajectory
plt.plot(states_2d[:, 0], states_2d[:, 1], alpha=0.3, label="trajectory")

# flow vectors
plt.quiver(
    states_2d[:, 0],
    states_2d[:, 1],
    vectors_2d[:, 0],
    vectors_2d[:, 1],
    lambdas,
    angles='xy',
    scale_units='xy',
    scale=1,
    cmap='viridis',
    width=0.003
)

# highlight collapse region (end of trajectory)
plt.scatter(states_2d[-1, 0], states_2d[-1, 1], color='red', label='collapse')

plt.title("NEXAH FIELD — Flow Geometry (IEEE Projection)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(label="Load λ")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()
```
plt.scatter(states_2d[-1, 0], states_2d[-1, 1], color='red', label='collapse')

plt.title("NEXAH FIELD — Flow Geometry (IEEE Projection)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.colorbar(label="Load λ")
plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()
plt.show()

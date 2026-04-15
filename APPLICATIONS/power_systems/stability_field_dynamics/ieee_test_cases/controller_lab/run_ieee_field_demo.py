import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d

# --- ensure repo root is in path ---
sys.path.append(os.path.abspath("."))

# --- import FIELD layer ---
from nexah.field_layer import Field, FieldMetrics


# =========================================================
# ⚠️ REPLACE THIS WITH YOUR REAL IEEE PIPELINE
# =========================================================
def run_powerflow(lam):
    """
    Dummy placeholder.

    Replace this with your real IEEE solver:
    V, theta = your_existing_function(lam)
    """
    n = 10
    V = 1.0 - 0.3 * lam + 0.01 * np.random.randn(n)
    theta = 0.1 * lam + 0.01 * np.random.randn(n)
    return V, theta


# =========================================================
# MAIN EXPERIMENT
# =========================================================

lambda_values = np.linspace(0.5, 1.5, 100)

states = []
lambdas = []
min_voltage = []

for lam in lambda_values:
    V, theta = run_powerflow(lam)

    state = np.concatenate([V, theta])

    states.append(state)
    lambdas.append(lam)
    min_voltage.append(np.min(V))

states = np.array(states)
lambdas = np.array(lambdas)
min_voltage = np.array(min_voltage)


# =========================================================
# FIELD LAYER
# =========================================================

field = Field(states)
metrics = FieldMetrics(field)

kappa = metrics.curvature()
frag = metrics.fragmentation()


# =========================================================
# DETECT EARLY WARNING
# =========================================================

threshold = np.mean(kappa) + 2 * np.std(kappa)

warning_idx = np.argmax(kappa > threshold)
lambda_warning = lambdas[warning_idx]

lambda_collapse = lambdas[-1]  # replace with real detection


# =========================================================
# PLOT (OPTIMIZED)
# =========================================================

def normalize(x):
    return (x - np.min(x)) / (np.max(x) - np.min(x) + 1e-8)

kappa_s = gaussian_filter1d(kappa, sigma=2)
frag_s = gaussian_filter1d(frag, sigma=2)

plt.figure(figsize=(12, 7))

# classical
plt.plot(lambdas, normalize(min_voltage), label="min(V) (classical)", linewidth=2)

# FIELD signals
plt.plot(lambdas, normalize(kappa_s), label="curvature κ (FIELD)", linewidth=2)
plt.plot(lambdas, normalize(frag_s), label="fragmentation (FIELD)", linestyle="--", linewidth=2)

# markers
plt.axvline(lambda_collapse, color="red", linestyle="--", linewidth=2, label="collapse")
plt.axvline(lambda_warning, color="orange", linestyle="--", linewidth=2, label="NEXAH early warning")

# annotations
plt.text(lambda_warning, 0.8, "Early Warning", rotation=90, color="orange")
plt.text(lambda_collapse, 0.8, "Collapse", rotation=90, color="red")

# styling
plt.xlabel("Load Scaling λ", fontsize=12)
plt.ylabel("Normalized Metrics", fontsize=12)

delta_lambda = lambda_collapse - lambda_warning
plt.title(f"NEXAH FIELD Early Collapse Detection (Δλ = {delta_lambda:.3f})", fontsize=14)

plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()

plt.show()

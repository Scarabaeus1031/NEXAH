from simulation.load_sweep import run_load_sweep
from features.coherence import compute_coherence
from features.structural_state import compute_structural_state
from features.derivatives import compute_derivatives

from overlay.manifold_fit import fit_manifold
from overlay.residual_distance import compute_residual, compute_distance
from overlay.clustering import cluster_overlay

from context.gh_filter import gh_filter
from decision.state_classifier import classify_states

from visualization.plots import plot_all

import numpy as np

# --- 1. simulate ---
lambdas = np.linspace(0.5, 2.5, 100)
results = run_load_sweep(powerflow_solver, lambdas)

# --- 2. extract ---
Vmin = []
c_list = []
frag_list = []

for r in results:
    V = r["V"]
    theta = r["theta"]
    
    Vmin.append(np.min(V))
    
    c, R, spread = compute_structural_state(V, theta, r["lambda"])
    
    c_list.append(c)
    frag_list.append((1 - R) * spread)

c = np.array(c_list)
frag = np.array(frag_list)

# --- 3. derivatives ---
dc, d2c = compute_derivatives(lambdas, c)

# --- 4. manifold ---
params = fit_manifold(c[:-5], dc[:-5], d2c[:-5])  # exclude collapse tail

# --- 5. overlay ---
residual = compute_residual(c, dc, d2c, params)

# define rift as last few stable points
rift_points = np.column_stack([c[-10:-5], dc[-10:-5]])
distance = compute_distance(c, dc, rift_points)

# --- 6. clustering ---
labels, centers = cluster_overlay(distance, residual)

# --- 7. context ---
gh_clusters = gh_filter(labels, centers)

# --- 8. decision ---
states = classify_states(c, dc, d2c, frag, labels, gh_clusters)

# --- 9. plot ---
plot_all(lambdas, Vmin, c, dc, d2c, frag,
         distance, residual, states)

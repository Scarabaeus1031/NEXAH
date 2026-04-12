import numpy as np
from sklearn.cluster import KMeans

def cluster_overlay(distance, residual, k=3):

    # Combine features
    X = np.column_stack([distance, residual])

    # --- FILTER INVALID VALUES (NaN / inf) ---
    valid = np.isfinite(X).all(axis=1)

    if np.sum(valid) < k:
        raise ValueError("Not enough valid points for clustering")

    X_valid = X[valid]

    # --- RUN KMEANS ONLY ON VALID DATA ---
    kmeans = KMeans(n_clusters=k, random_state=0).fit(X_valid)

    # --- REBUILD FULL LABEL ARRAY ---
    labels = np.full(len(X), -1)  # -1 = invalid / outside field
    labels[valid] = kmeans.labels_

    return labels, kmeans.cluster_centers_


# =========================================
# 1. SIMULATION
# =========================================

lambdas = np.linspace(0.5, 2.5, 120)

results = run_load_sweep(powerflow_solver, lambdas)


# =========================================
# 2. FEATURE EXTRACTION
# =========================================

Vmin = []
c_list = []
frag_list = []

for r in results:
    V = r["V"]
    theta = r["theta"]

    # handle non-converged safely
    if not r["converged"] or np.any(np.isnan(V)):
        Vmin.append(np.nan)
        c_list.append(np.nan)
        frag_list.append(np.nan)
        continue

    Vmin.append(np.min(V))

    c, R, spread = compute_structural_state(V, theta, r["lambda"])
    c_list.append(c)

    fragmentation = (1 - R) * spread
    frag_list.append(fragmentation)


c = np.array(c_list)
frag = np.array(frag_list)
Vmin = np.array(Vmin)


# =========================================
# 3. DERIVATIVES (SMOOTHED)
# =========================================

def compute_derivatives_smooth(x, y):
    y_smooth = gaussian_filter1d(y, sigma=1.0)
    dy = np.gradient(y_smooth, x)
    d2y = np.gradient(dy, x)
    return dy, d2y


dc, d2c = compute_derivatives_smooth(lambdas, c)


# =========================================
# 4. CLEAN DATA FOR MANIFOLD FIT
# =========================================

valid = (
    np.isfinite(c) &
    np.isfinite(dc) &
    np.isfinite(d2c)
)

if np.sum(valid) < 10:
    raise ValueError("Not enough valid points for manifold fit")

# remove extreme spikes
threshold = np.percentile(np.abs(d2c[valid]), 95)

stable = valid & (np.abs(d2c) < threshold)

c_clean = c[stable]
dc_clean = dc[stable]
d2c_clean = d2c[stable]

# cut last unstable region
cut = int(len(c_clean) * 0.85)

print("Clean points:", len(c_clean))
print("Using for fit:", cut)

params = fit_manifold(
    c_clean[:cut],
    dc_clean[:cut],
    d2c_clean[:cut]
)

print("Manifold params:", params)


# =========================================
# 5. OVERLAY
# =========================================

residual = compute_residual(c, dc, d2c, params)

# define rift region from late but still stable points
rift_indices = np.where(valid)[0][-15:-5]

rift_points = np.column_stack([
    c[rift_indices],
    dc[rift_indices]
])

distance = compute_distance(c, dc, rift_points)


# =========================================
# 6. CLUSTERING
# =========================================

labels, centers = cluster_overlay(distance, residual)

print("Cluster centers:", centers)


# =========================================
# 7. CONTEXT (GH FILTER)
# =========================================

gh_clusters = gh_filter(labels, centers)

print("GH clusters:", gh_clusters)


# =========================================
# 8. DECISION
# =========================================

states = classify_states(
    c, dc, d2c,
    frag,
    labels,
    gh_clusters
)

print("First 30 states:")
print(states[:30])


# =========================================
# 9. VISUALIZATION
# =========================================

plot_all(
    lambdas,
    Vmin,
    c,
    dc,
    d2c,
    frag,
    distance,
    residual,
    states
)

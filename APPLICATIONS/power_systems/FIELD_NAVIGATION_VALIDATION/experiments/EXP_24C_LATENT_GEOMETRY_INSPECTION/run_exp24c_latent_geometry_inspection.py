# ============================================================
# EXP_24C — LATENT GEOMETRY INSPECTION
#
# Question:
# Is the observed NEXAH field geometry truly a horn /
# transport manifold, or is PCA hiding additional structure?
#
# Visualizations:
#   exp24c_pca2d.png
#   exp24c_pca3d.png
#   exp24c_tsne2d.png
#   exp24c_umap2d.png   (optional)
#   exp24c_summary.txt
#
# ============================================================

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

# ------------------------------------------------------------
# Optional UMAP
# ------------------------------------------------------------

HAS_UMAP = True

try:
    import umap
except:
    HAS_UMAP = False

# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------

INPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/outputs/"
    "EXP_08_REAL_FIELD_GEOMETRY"
)

OUTPUT_DIR = (
    "APPLICATIONS/power_systems/"
    "FIELD_NAVIGATION_VALIDATION/outputs/"
    "EXP_24C_LATENT_GEOMETRY_INSPECTION"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("\nInput  ->", os.path.abspath(INPUT_DIR))
print("Output ->", os.path.abspath(OUTPUT_DIR))

# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------

df = pd.read_csv(
    os.path.join(INPUT_DIR, "exp08_field_states.csv")
)

print("\nLoaded states:", len(df))

# ------------------------------------------------------------
# Feature set
# ------------------------------------------------------------

features = [
    "global_scale",
    "min_vm",
    "mean_vm",
    "std_vm",
    "angle_span",
    "max_loading",
    "mean_loading",
    "density",
    "betweenness"
]

X = df[features].values

X = StandardScaler().fit_transform(X)

print("Feature dimension:", X.shape[1])

# ------------------------------------------------------------
# PCA 2D
# ------------------------------------------------------------

pca2 = PCA(n_components=2)

pca2_coords = pca2.fit_transform(X)

print(
    "\nPCA 2D explained variance:",
    round(
        np.sum(
            pca2.explained_variance_ratio_
        ),
        4
    )
)

plt.figure(figsize=(8,6))

plt.scatter(
    pca2_coords[:,0],
    pca2_coords[:,1],
    s=25,
    alpha=0.7
)

plt.title(
    "EXP_24C — PCA 2D"
)

plt.xlabel("PC1")
plt.ylabel("PC2")

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24c_pca2d.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# PCA 3D
# ------------------------------------------------------------

pca3 = PCA(n_components=3)

pca3_coords = pca3.fit_transform(X)

fig = plt.figure(figsize=(9,7))

ax = fig.add_subplot(
    111,
    projection="3d"
)

ax.scatter(
    pca3_coords[:,0],
    pca3_coords[:,1],
    pca3_coords[:,2],
    s=15
)

ax.set_title(
    "EXP_24C — PCA 3D"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24c_pca3d.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# t-SNE
# ------------------------------------------------------------

print("\nRunning t-SNE...")

tsne = TSNE(
    n_components=2,
    perplexity=30,
    random_state=42
)

tsne_coords = tsne.fit_transform(X)

plt.figure(figsize=(8,6))

plt.scatter(
    tsne_coords[:,0],
    tsne_coords[:,1],
    s=25,
    alpha=0.7
)

plt.title(
    "EXP_24C — t-SNE"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        OUTPUT_DIR,
        "exp24c_tsne2d.png"
    ),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# UMAP (optional)
# ------------------------------------------------------------

if HAS_UMAP:

    print("Running UMAP...")

    reducer = umap.UMAP(
        n_neighbors=15,
        min_dist=0.1,
        random_state=42
    )

    umap_coords = reducer.fit_transform(X)

    plt.figure(figsize=(8,6))

    plt.scatter(
        umap_coords[:,0],
        umap_coords[:,1],
        s=25,
        alpha=0.7
    )

    plt.title(
        "EXP_24C — UMAP"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "exp24c_umap2d.png"
        ),
        dpi=300
    )

    plt.close()

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

with open(
    os.path.join(
        OUTPUT_DIR,
        "exp24c_summary.txt"
    ),
    "w"
) as f:

    f.write(
        "EXP_24C LATENT GEOMETRY INSPECTION\n"
    )

    f.write(
        "========================================\n\n"
    )

    f.write(
        f"States: {len(df)}\n"
    )

    f.write(
        f"Features: {len(features)}\n"
    )

    f.write(
        f"PCA 2D variance: "
        f"{np.sum(pca2.explained_variance_ratio_):.4f}\n"
    )

    f.write(
        f"UMAP available: {HAS_UMAP}\n"
    )

print("\nEXP_24C completed.")

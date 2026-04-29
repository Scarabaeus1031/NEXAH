import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# ============================================================
# Paths
# ============================================================

BASE = "APPLICATIONS/power_systems/VALIDATION_LAYER/outputs"

IMG_A = os.path.join(BASE, "run_017_state_region_map/figure_01_state_region_map.png")
IMG_B = os.path.join(BASE, "run_018_state_space_3d/figure_01_state_space_3d.png")
IMG_C = os.path.join(BASE, "run_019_multi_trajectory_map/figure_01_multi_trajectory.png")

OUT_DIR = os.path.join(BASE, "run_020_final_composite")
os.makedirs(OUT_DIR, exist_ok=True)

OUT_FILE = os.path.join(OUT_DIR, "figure_01_nexah_core_result.png")


# ============================================================
# Load images
# ============================================================

img_a = mpimg.imread(IMG_A)
img_b = mpimg.imread(IMG_B)
img_c = mpimg.imread(IMG_C)


# ============================================================
# Plot
# ============================================================

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# --- Panel A ---
axes[0].imshow(img_a)
axes[0].set_title("(A) State Region Map")
axes[0].axis("off")

# --- Panel B ---
axes[1].imshow(img_b)
axes[1].set_title("(B) 3D State Trajectory")
axes[1].axis("off")

# --- Panel C ---
axes[2].imshow(img_c)
axes[2].set_title("(C) Multi-Trajectory Transition")
axes[2].axis("off")

plt.tight_layout()
plt.savefig(OUT_FILE, dpi=300)
plt.close()

print("\n=== RUN 020 — FINAL COMPOSITE FIGURE ===")
print(f"Saved to: {OUT_FILE}")

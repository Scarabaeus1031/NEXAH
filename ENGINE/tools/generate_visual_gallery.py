import os
from glob import glob

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

VISUALS_ROOT = "ENGINE/visuals"
OUTPUT_FILE = "dynamics_engine/visual_gallery.md"

LEVELS = {
    20: "Phase Synchronization",
    21: "Controlled Desync",
    22: "Crown / Shell",
    23: "Orbit Stabilization",
    24: "Multi-Shell Resonance",
    25: "Shell Coupling",
    26: "Geometry Collapse",
    27: "Autonomous Field"
}

DESCRIPTIONS = {
    20: "dense overlapping trajectories • high coherence • uniform motion",
    21: "phase fragmentation • increased diversity • structured instability",
    22: "radial density formation • central clustering • early shell geometry",
    23: "stable cyclic trajectories • ring formation • orbit dynamics",
    24: "multiple shells • resonance patterns • layered structures",
    25: "cross-shell interaction • asymmetric density • coupling zones",
    26: "smooth circular geometry • strong alignment • minimal noise",
    27: "self-sustained structures • internal coordinates • emerging grids"
}

# --------------------------------------------------
# HELPER
# --------------------------------------------------

def get_latest_image(folder):
    images = glob(os.path.join(folder, "*.png"))
    if not images:
        return None
    return max(images, key=os.path.getctime)

# --------------------------------------------------
# BUILD GALLERY
# --------------------------------------------------

lines = []

lines.append("# NEXAH Dynamics Engine — Visual Gallery\n")
lines.append("Auto-generated from simulation outputs.\n\n---\n")

for level, title in LEVELS.items():

    folder = os.path.join(VISUALS_ROOT, f"navigation_level{level}")
    img = get_latest_image(folder)

    lines.append(f"\n# LEVEL {level} — {title}\n")

    if img:
        # make path relative for GitHub
        rel_path = os.path.relpath(img, start=".")
        lines.append(f"\n![Level {level}]({rel_path})\n")
    else:
        lines.append("\n*(no image found)*\n")

    desc = DESCRIPTIONS.get(level, "")
    lines.append(f"\n• {desc}\n")

    lines.append("\n---\n")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

lines.append("""
# KEY OBSERVATION

> Geometry is not imposed — it is **accumulated memory**.

---

# SUMMARY

noise → structure → pattern → geometry → autonomy

---
""")

# --------------------------------------------------
# WRITE FILE
# --------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    f.writelines("\n".join(lines))

print("Visual gallery generated:", OUTPUT_FILE)

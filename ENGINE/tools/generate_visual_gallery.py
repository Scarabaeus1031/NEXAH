import os
import shutil
from glob import glob

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

VISUALS_ROOT = "ENGINE/visuals"
OUTPUT_FILE = "DISCOVERY_ENGINE/nexah_dynamics_engine/visual_gallery.md"
CURATED_DIR = "DISCOVERY_ENGINE/visuals/dynamics"

os.makedirs(CURATED_DIR, exist_ok=True)

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
        # copy to curated folder
        target_path = os.path.join(CURATED_DIR, f"level{level}.png")
        shutil.copy(img, target_path)

        rel_path = os.path.relpath(target_path, start=".")
        lines.append(f"\n![Level {level}]({rel_path})\n")

    else:
        lines.append("\n*(no image found)*\n")

    lines.append("\n---\n")

# --------------------------------------------------
# WRITE FILE
# --------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))

print("Gallery + curated visuals updated")

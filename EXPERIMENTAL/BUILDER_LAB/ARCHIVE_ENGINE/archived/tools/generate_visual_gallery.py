import os
from glob import glob

# --------------------------------------------------
# CONFIG
# --------------------------------------------------

BASE_DIR = os.path.dirname(__file__)

VISUALS_ROOT = os.path.abspath(os.path.join(BASE_DIR, "../visuals"))
OUTPUT_FILE = os.path.abspath(os.path.join(BASE_DIR, "../../DISCOVERY_ENGINE/nexah_dynamics_engine/visual_gallery.md"))

LEVELS = {
    20: "Phase Synchronization",
    21: "Controlled Desync",
    22: "Crown / Shell",
    23: "Orbit Stabilization",
    24: "Multi-Shell Resonance",
    25: "Shell Coupling",
    26: "Geometry Collapse",
    27: "Autonomous Field",
    35: "Resonance Alignment",
    36: "Resonance Dynamics",
    37: "Phi Attractor Mapping",
    38: "Phi Basin Locking",
    38.5: "Phi Soft Lock",
    39: "Phi Orbit Spiral Lock",
    40: "Phase Transition Detection"
}

DESCRIPTIONS = {
    35: "local alignment structures • directional coherence",
    36: "temporal resonance patterns • oscillatory motion",
    37: "phi attractor regions • clustered resonance zones",
    38: "hard basin locking • strong stability regions",
    38.5: "soft locking • sparse stable regions",
    39: "orbit + spiral structures • dynamic locking",
    40: "rare transition points • regime switching events"
}

# --------------------------------------------------
# FIND LATEST RUN PER LEVEL
# --------------------------------------------------

def extract_level(folder_name):
    try:
        if "level" in folder_name:
            part = folder_name.split("level")[1]
            num = part.split("_")[0]
            return float(num.replace("b", ".5"))
    except:
        return None
    return None


def get_latest_run_folders():
    folders = glob(os.path.join(VISUALS_ROOT, "level*"))
    level_map = {}

    for f in folders:
        name = os.path.basename(f)
        lvl = extract_level(name)

        if lvl is None:
            continue

        if lvl not in level_map:
            level_map[lvl] = []

        level_map[lvl].append(f)

    # pick latest per level
    latest = {}
    for lvl, flist in level_map.items():
        latest[lvl] = max(flist, key=os.path.getctime)

    return latest


def get_image(folder):
    imgs = glob(os.path.join(folder, "*.png"))
    if not imgs:
        return None
    return max(imgs, key=os.path.getctime)

# --------------------------------------------------
# BUILD GALLERY
# --------------------------------------------------

latest_runs = get_latest_run_folders()

lines = []
lines.append("# NEXAH Dynamics Engine — Visual Gallery\n")
lines.append("Auto-generated from simulation outputs.\n\n---\n")

for lvl in sorted(LEVELS.keys()):

    title = LEVELS[lvl]
    lines.append(f"\n# LEVEL {lvl} — {title}\n")

    folder = latest_runs.get(lvl)

    if folder:
        img = get_image(folder)

        if img:
            rel_path = os.path.relpath(img, start=os.path.dirname(OUTPUT_FILE))
            rel_path = rel_path.replace("\\", "/")
            lines.append(f"\n![Level {lvl}]({rel_path})\n")
        else:
            lines.append("\n*(no image found in latest run)*\n")
    else:
        lines.append("\n*(no run found)*\n")

    desc = DESCRIPTIONS.get(lvl, "")
    if desc:
        lines.append(f"\n• {desc}\n")

    lines.append("\n---\n")

# --------------------------------------------------
# WRITE FILE
# --------------------------------------------------

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

with open(OUTPUT_FILE, "w") as f:
    f.write("\n".join(lines))

print("Visual gallery updated:", OUTPUT_FILE)
